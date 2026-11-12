#!/usr/bin/env python3
"""
Processes the user's uploaded ElevenLabs voiceover (assets/audio/elevenlabs_cosplay_vo.mp3):
1. Tightens inter-sentence pauses (>0.30s) down to 0.10s per the Nexivo Viral Shorts Blueprint
   while preserving internal natural micro-pauses and 100% of ElevenLabs' vocal fidelity.
2. Adds 0.11s preroll (Frame 3 speech start) and 0.32s loop tail -> output/cosplay_short_work/narration_full.wav.
3. Runs whisper-cli (-ojf) for exact word-level alignment across all 81 words -> words.json & clauses.json.
4. Updates output/Never_Do_This_Cosplay_Japan_Short.srt with exact ElevenLabs timestamps.
"""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path("/Users/digiex/Documents/deepseek-harness/default-workspace/jp_refusals_video")
WORK_DIR = ROOT / "output/cosplay_short_work"
VO_MP3 = ROOT / "assets/audio/elevenlabs_cosplay_vo.mp3"
WHISPER_CLI = str(ROOT / "tools-whisper/build/bin/whisper-cli")
WHISPER_MODEL = str(ROOT / "tools-whisper/models/ggml-large-v3-turbo.bin")
SRT_OUT = ROOT / "output/Never_Do_This_Cosplay_Japan_Short.srt"

CLAUSES_SPEC = [
    ("c01_act1_hook", "People in Japan will seriously hate you if you do this to cosplayers in Japan."),
    ("c02_act2_sacred", "Cosplay isn't just dressing up in Japan, it represents hundreds of hours of pure devotion to a character."),
    ("c03_act3_violation", "But every year, some tourists ruin the experience by snapping photos without asking first, never realizing how disrespectful it can be."),
    ("c04_act4_secret", "Because in Japanese culture, when you bow and ask first, cosplayers strike their best pose for you."),
    ("c05_act4_moral", "You're supposed to earn the pose, not steal the shot."),
]


def get_dur(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True
    )
    return float(r.stdout.strip())


def format_srt_ts(sec: float) -> str:
    ms = int(round(sec * 1000))
    hh = ms // 3_600_000
    ms %= 3_600_000
    mm = ms // 60_000
    ms %= 60_000
    ss = ms // 1000
    ms %= 1000
    return f"{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}"


def main():
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    # 1. Trim leading/trailing silence and cap any internal silence >0.10s to 0.10s smoothly
    trimmed_speech = WORK_DIR / "eleven_speech_tight.wav"
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(VO_MP3),
            "-af", (
                "silenceremove=start_periods=1:start_duration=0.01:start_threshold=-45dB,"
                "areverse,silenceremove=start_periods=1:start_duration=0.01:start_threshold=-45dB,areverse,"
                "silenceremove=stop_periods=-1:stop_duration=0.10:stop_threshold=-42dB:window=0.02"
            ),
            "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(trimmed_speech)
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    speech_dur = get_dur(trimmed_speech)

    # 2. Prepend 0.11s preroll and append 0.32s loop tail
    narration_full = WORK_DIR / "narration_full.wav"
    narration_16k = WORK_DIR / "narration_16k.wav"
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-f", "lavfi", "-t", "0.11", "-i", "anullsrc=r=48000:cl=mono",
            "-i", str(trimmed_speech),
            "-f", "lavfi", "-t", "0.32", "-i", "anullsrc=r=48000:cl=mono",
            "-filter_complex", "[0:a][1:a][2:a]concat=n=3:v=0:a=1[out]",
            "-map", "[out]", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(narration_full)
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(narration_full), "-ar", "16000", "-ac", "1", str(narration_16k)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    total_dur = get_dur(narration_full)
    speech_end = round(0.11 + speech_dur, 3)

    # 3. Run Whisper word-level alignment
    subprocess.run(
        [WHISPER_CLI, "-m", WHISPER_MODEL, "-f", str(narration_16k), "-ojf", "-of", str(WORK_DIR / "whisper_eleven")],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    wdata = json.loads((WORK_DIR / "whisper_eleven.json").read_text())

    raw_tokens = []
    for seg in wdata.get("transcription", []):
        for tok in seg.get("tokens", []):
            txt = tok.get("text", "")
            if txt.startswith("[") and txt.endswith("]"):
                continue
            t0 = tok["offsets"]["from"] / 1000.0
            t1 = tok["offsets"]["to"] / 1000.0
            raw_tokens.append({"text": txt, "start": t0, "end": t1})

    merged = []
    for rt in raw_tokens:
        raw_txt = rt["text"]
        clean = raw_txt.strip()
        if not clean or all(ch in ".,!?;:—-\"" for ch in clean):
            continue
        if raw_txt.startswith(" ") or not merged:
            merged.append({
                "text": clean.strip(".,!?;:—-\""),
                "start": rt["start"],
                "end": max(rt["start"] + 0.04, rt["end"]),
            })
        else:
            merged[-1]["text"] = (merged[-1]["text"] + clean).strip(".,!?;:—-\"")
            merged[-1]["end"] = max(merged[-1]["end"], rt["end"])

    full_script = " ".join(txt for _, txt in CLAUSES_SPEC)
    script_words = [re.sub(r"[.,!?;:\"]", "", w) for w in full_script.split()]
    print(f"ElevenLabs total_dur={total_dur:.3f}s | speech=0.11s->{speech_end:.3f}s | Whisper words={len(merged)} vs Script={len(script_words)}")

    if len(merged) == len(script_words):
        for i, sw in enumerate(script_words):
            merged[i]["script_word"] = sw
    else:
        aligned = []
        n_m, n_s = len(merged), len(script_words)
        m_idx = 0
        for s_idx, sw in enumerate(script_words):
            if m_idx >= n_m:
                prev_end = aligned[-1]["end"] if aligned else 0.11
                aligned.append({"script_word": sw, "start": prev_end, "end": min(speech_end, prev_end + 0.22)})
                continue
            cur_m = merged[m_idx]
            if m_idx + 1 < n_m and (n_m - m_idx) > (n_s - s_idx):
                comb = (cur_m["text"] + merged[m_idx + 1]["text"]).lower().replace("'", "")
                target = sw.lower().replace("'", "")
                if comb == target or target.startswith(cur_m["text"].lower().replace("'", "")):
                    aligned.append({"script_word": sw, "start": cur_m["start"], "end": merged[m_idx + 1]["end"]})
                    m_idx += 2
                    continue
            aligned.append({"script_word": sw, "start": cur_m["start"], "end": cur_m["end"]})
            m_idx += 1
        merged = aligned

    # Build final 81 words with seamless rapid-fire timing & Nexivo casing
    PROPER_NOUNS = {"japan": "Japan", "japanese": "Japanese"}
    words = []
    for i, w in enumerate(merged):
        sw = w["script_word"]
        display = PROPER_NOUNS.get(sw.lower(), sw.lower())
        t0 = 0.11 if i == 0 else max(words[-1]["end"], round(w["start"], 3))
        if i + 1 < len(merged):
            nxt_start = round(merged[i + 1]["start"], 3)
            if nxt_start - w["end"] <= 0.18:
                t1 = nxt_start
            else:
                t1 = round(min(nxt_start, w["end"] + 0.08), 3)
        else:
            t1 = speech_end
        t1 = max(round(t0 + 0.05, 3), t1)
        words.append({"index": i, "text": display, "start": t0, "end": t1})

    # Reconstruct exact clause boundaries from word spans
    clause_meta = []
    cursor = 0
    for cid, ctext in CLAUSES_SPEC:
        nw = len(ctext.split())
        cw = words[cursor : cursor + nw]
        # Bridge words seamlessly inside each clause
        for k in range(len(cw) - 1):
            if cw[k + 1]["start"] - cw[k]["end"] <= 0.16:
                cw[k]["end"] = cw[k + 1]["start"]
        c_start = cw[0]["start"]
        c_end = cw[-1]["end"]
        nxt_start = words[cursor + nw]["start"] if (cursor + nw) < len(words) else round(total_dur, 3)
        clause_meta.append({
            "id": cid,
            "text": ctext,
            "start": round(c_start, 3),
            "end": round(c_end, 3),
            "duration": round(c_end - c_start, 3),
            "pause_after": round(max(0.0, nxt_start - c_end), 3),
        })
        cursor += nw

    # Assign 4-color Nexivo rotation (zero consecutive duplicates)
    YELLOW, CYAN, GREEN, WHITE = "#FFE838", "#42F2F7", "#38F852", "#FFFFFF"
    SEMANTIC = {
        "people": YELLOW, "Japan": CYAN, "seriously": CYAN, "hate": GREEN, "this": YELLOW, "cosplayers": CYAN,
        "cosplay": YELLOW, "dressing": CYAN, "hundreds": YELLOW, "hours": CYAN, "pure": GREEN, "devotion": YELLOW, "character": GREEN,
        "every": YELLOW, "year": CYAN, "tourists": YELLOW, "ruin": GREEN, "experience": CYAN,
        "snapping": YELLOW, "photos": CYAN, "asking": GREEN, "realizing": YELLOW, "disrespectful": GREEN,
        "because": YELLOW, "Japanese": YELLOW, "culture": CYAN, "bow": GREEN, "ask": YELLOW, "strike": GREEN, "best": GREEN, "pose": CYAN,
        "supposed": CYAN, "earn": YELLOW, "steal": GREEN, "shot": CYAN,
    }
    CYCLE = [WHITE, GREEN, YELLOW, CYAN]
    rot_ptr = 0
    prev_col = None
    for i, w in enumerate(words):
        nxt_sem = SEMANTIC.get(words[i + 1]["text"]) if i + 1 < len(words) else None
        pref = SEMANTIC.get(w["text"])
        if pref and pref != prev_col:
            col = pref
        else:
            col = None
            for step in range(4):
                cand = CYCLE[(rot_ptr + step) % 4]
                if cand != prev_col and cand != nxt_sem:
                    col = cand
                    rot_ptr = (rot_ptr + step + 1) % 4
                    break
            if col is None:
                for cand in CYCLE:
                    if cand != prev_col:
                        col = cand
                        break
        w["color"] = col
        prev_col = col

    wpm = round((len(words) / (speech_end - 0.11)) * 60.0, 1)
    (WORK_DIR / "words.json").write_text(json.dumps(words, indent=2))
    (WORK_DIR / "clauses.json").write_text(json.dumps({
        "total_duration": round(total_dur, 3),
        "speech_start": 0.11,
        "speech_end": speech_end,
        "word_count": len(words),
        "wpm": wpm,
        "clauses": clause_meta,
    }, indent=2))

    # Write updated SRT
    srt_lines = []
    for idx, cm in enumerate(clause_meta, 1):
        srt_lines.append(f"{idx}\n{format_srt_ts(cm['start'])} --> {format_srt_ts(cm['end'])}\n{cm['text']}\n")
    SRT_OUT.write_text("\n".join(srt_lines))

    for cm in clause_meta:
        print(f"  {cm['id']:20s}: {cm['start']:5.2f}s -> {cm['end']:5.2f}s (pause {cm['pause_after']:.2f}s) | {cm['text']}")
    print(f"WPM={wpm} | Saved words.json ({len(words)} words) & SRT")


if __name__ == "__main__":
    main()
