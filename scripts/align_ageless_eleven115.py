#!/usr/bin/env python3
"""
Aligns the 1.15x ElevenLabs voiceover (output/ageless_jp_work/narration_full.wav, 50.290s)
using output/ageless_jp_work/whisper_eleven115.json into:
- output/ageless_jp_work/clauses.json
- output/ageless_jp_work/words.json
- output/Why_Japanese_Women_Look_25_Short.srt

Preserves the exact comedic pause / throat-clear at 25.22s -> 25.96s between
whispered "Instead of sugary sodas?" and "Daily meals pair...".
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK_DIR = ROOT / "output/ageless_jp_work"
SRT_OUT = ROOT / "output/Why_Japanese_Women_Look_25_Short.srt"

CONNECTOR_WHITE = {
    "WHY", "SO", "MANY", "EVEN", "AT", "FIRST", "LIKE", "UNDER", "A", "CALLED",
    "IN", "AND", "ON", "THEY", "BECAUSE", "OF", "COMES", "FROM", "YOUR",
    "SECOND", "WITH", "INSTEAD", "PLUS", "TO", "OVER", "LASTLY", "EVERY",
    "THAT", "WHILE", "THEIR", "THAT'S...",
}

TOKEN_NORMALIZE = {
    "BEHAKU": "BIHAKU",
    "BIHAKU": "BIHAKU",
    "HIGASA": "HIGASA",
    "OFURO": "OFURO",
    "45": "45?!",
    "35-DEGREE": "35°C",
    "35": "35°C",
    "40-DEGREE": "40°C",
    "40": "40°C",
    "7000": "7,000",
    "7,000": "7,000",
    "SODAS": "SODAS?",
}

CLAUSES_SPEC = [
    ("c01_hook", 12, "Why so many Japanese women still look 25—even at age 45?!"),
    ("c02_p1a",  13, "First, Japanese women dodge sunlight like vampires under a beauty code called Bihaku."),
    ("c03_p1b",  19, "In 35-degree summer heat, and even on cloudy days, they wear UV visors, long-arm gloves, and black higasa parasols."),
    ("c04_p1c",  15, "Because dermatologists prove 80% of skin aging comes from UV rays, not your actual age."),
    ("c05_p2a",   8, "Second, they replace liquid sugar with fermented superfoods."),
    ("c06_p2b",  18, "Instead of sugary sodas? Daily meals pair unsweetened green tea with probiotic miso soup and sticky fermented natto."),
    ("c07_p2c",  15, "Plus, riding trains in Tokyo forces commuters to walk over 7,000 steps every single day."),
    ("c08_p3a",   9, "And lastly, Japan's nightly hot bath ritual called ofuro."),
    ("c09_p3b",  15, "Instead of rushing a 3-minute shower, Japanese women soak in 40-degree hot water every night."),
    ("c10_p3c",  16, "That heat boosts blood circulation, melts stress, and triggers deep sleep while their skin repairs overnight."),
    ("c11_loop",  1, "That's..."),
]

PUNCT_STRIP = ".,!?;:\"“”…"


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
    import subprocess
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(WORK_DIR / "narration_full.wav")],
        capture_output=True, text=True, check=True,
    )
    total_dur = round(float(r.stdout.strip()), 3)

    wdata = json.loads((WORK_DIR / "whisper_eleven115.json").read_text())
    merged = []
    pending_space = False

    for seg in wdata.get("transcription", []):
        for tok in seg.get("tokens", []):
            txt = tok.get("text", "")
            if txt.startswith("[") and txt.endswith("]"):
                continue
            t0 = tok["offsets"]["from"] / 1000.0
            t1 = tok["offsets"]["to"] / 1000.0
            has_lead_space = txt.startswith(" ")
            clean = txt.strip().strip(PUNCT_STRIP)
            if not clean:
                if has_lead_space:
                    pending_space = True
                continue
            if has_lead_space or pending_space or not merged:
                merged.append({
                    "text": clean,
                    "start": round(t0, 3),
                    "end": round(max(t0 + 0.04, t1), 3),
                })
                pending_space = False
            else:
                merged[-1]["text"] = (merged[-1]["text"] + clean).strip(PUNCT_STRIP)
                merged[-1]["end"] = round(max(merged[-1]["end"], t1), 3)

    expected_total = sum(cnt for _, cnt, _ in CLAUSES_SPEC)
    assert len(merged) == expected_total, (
        f"Expected {expected_total} tokens, got {len(merged)}:\n"
        + "\n".join(f"{i}: {m['text']} ({m['start']}->{m['end']})" for i, m in enumerate(merged))
    )

    clause_meta = []
    final_words = []
    srt_blocks = []
    cursor = 0

    for c_idx, (cid, cnt, ctext) in enumerate(CLAUSES_SPEC):
        cw = [dict(w) for w in merged[cursor : cursor + cnt]]
        cursor += cnt

        c_start = round(cw[0]["start"], 3)
        c_end = round(total_dur - 0.02, 3) if cid == "c11_loop" else round(cw[-1]["end"], 3)
        cw[-1]["end"] = c_end

        # Monotonic seamless word progression inside each clause, EXCEPT preserve throat-clear gap after "sodas?" in c06_p2b!
        for i in range(len(cw) - 1):
            if cw[i + 1]["start"] <= cw[i]["start"] + 0.04:
                cw[i + 1]["start"] = round(cw[i]["start"] + 0.08, 3)
            gap = cw[i + 1]["start"] - cw[i]["end"]
            if cid == "c06_p2b" and cw[i]["text"].upper() == "SODAS":
                # Keep comedic throat-clear silence free of stale text!
                cw[i]["end"] = round(min(cw[i + 1]["start"] - 0.05, cw[i]["end"] + 0.08), 3)
            elif gap <= 0.35:
                cw[i]["end"] = round(cw[i + 1]["start"], 3)
            else:
                cw[i]["end"] = round(cw[i]["end"] + 0.10, 3)

        nxt_clause_start = merged[cursor]["start"] if cursor < len(merged) else total_dur
        clause_meta.append({
            "id": cid,
            "text": ctext,
            "start": c_start,
            "end": c_end,
            "duration": round(c_end - c_start, 3),
            "pause_after": round(max(0.0, nxt_clause_start - c_end), 3),
        })

        row_preview = []
        for w in cw:
            up = w["text"].upper().strip(PUNCT_STRIP)
            disp = TOKEN_NORMALIZE.get(up, up)
            if cid == "c11_loop":
                disp = "THAT'S..."
            is_yellow = disp not in CONNECTOR_WHITE
            is_shrunk = (cid == "c06_p2b" and disp in {"INSTEAD", "OF", "SUGARY", "SODAS?"})
            item = {
                "text": disp,
                "start": round(w["start"], 3),
                "end": round(w["end"], 3),
                "yellow": is_yellow,
                "shrink": is_shrunk,
                "clause": cid,
            }
            final_words.append(item)
            row_preview.append(f"{disp}@{item['start']:.2f}")

        print(f"  {cid:10s} [{c_start:5.2f}s -> {c_end:5.2f}s | pause {clause_meta[-1]['pause_after']:.2f}s]: " + " | ".join(row_preview))
        srt_blocks.append(f"{c_idx + 1}\n{format_srt_ts(c_start)} --> {format_srt_ts(c_end)}\n{ctext}\n")

    speech_span = clause_meta[-1]["end"] - clause_meta[0]["start"]
    wpm = round((len(final_words) / speech_span) * 60.0, 1)
    hook_wpm = round((12 / clause_meta[0]["duration"]) * 60.0, 1)

    (WORK_DIR / "clauses.json").write_text(json.dumps({
        "total_duration": total_dur,
        "word_count": len(final_words),
        "wpm": wpm,
        "hook_wpm": hook_wpm,
        "clauses": clause_meta,
    }, indent=2))
    (WORK_DIR / "words.json").write_text(json.dumps(final_words, indent=2))
    SRT_OUT.write_text("\n".join(srt_blocks))

    yellow_cnt = sum(1 for w in final_words if w["yellow"])
    print(f"\nSaved {len(final_words)} words | Duration={total_dur:.3f}s | WPM={wpm} | Yellow={yellow_cnt}/{len(final_words)} ({100*yellow_cnt/len(final_words):.1f}%)")


if __name__ == "__main__":
    main()
