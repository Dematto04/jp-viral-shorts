#!/usr/bin/env python3
"""
Masters audio for the Cosplay Short using:
- User's uploaded ElevenLabs voiceover (output/cosplay_short_work/narration_full.wav)
- Creepy Nuts – "Bling-Bang-Bang-Born" viral chorus section (61.45s -> 87.16s: "Bling-bang-bang, bling-bang-bang-born!")
- Mid-frequency vocal-pocket EQ carve + stereo width on BGM so the viral chorus grooves cleanly behind the narrator
- Camera shutter SFX synced to ElevenLabs words ("snapping photos" @ 13.55s, "best pose" @ 22.11s)
- Two-pass EBU R128 loudness master to -11.9 LUFS, True Peak <= -0.2 dBFS
"""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK_DIR = ROOT / "output/cosplay_short_work"
BGM_PATH = ROOT / "assets/audio/bling_bang_bang_born.wav"
if not BGM_PATH.exists():
    BGM_PATH = ROOT / "assets/audio/bling_bang_bang_born_full.m4a"
SHUTTER_SFX = ROOT / "assets/sfx/shutter.wav"
WHOOSH_SFX = ROOT / "assets/sfx/whoosh_soft.wav"

# Exact onset of viral Chorus 1 ("Now singin' Bling-bang-bang, bling-bang-bang, bling-bang-bang-born!")
BGM_START_SEC = 61.45


def run_ebur128(wav_path: Path) -> str:
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(wav_path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True
    )
    return r.stderr


def main():
    clauses_meta = json.loads((WORK_DIR / "clauses.json").read_text())
    dur = clauses_meta["total_duration"]
    vo_in = WORK_DIR / "narration_full.wav"
    out_wav = WORK_DIR / "mastered_audio.wav"

    # Step 1: Compress & level center ElevenLabs voice cleanly
    vo_leveled = WORK_DIR / "vo_leveled.wav"
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(vo_in),
            "-af", (
                "highpass=f=80,"
                "acompressor=threshold=-19dB:ratio=2.2:attack=6:release=85:makeup=2.5dB,"
                "pan=stereo|c0=c0|c1=c0"
            ),
            "-ar", "48000", str(vo_leveled)
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    # Step 2: Slice viral chorus of Bling-Bang-Bang-Born (61.45s + dur), carve 2.15kHz vocal pocket,
    # apply smooth sidechain ducking under ElevenLabs voice so chorus grooves cleanly without vocal clash
    pre_mix = WORK_DIR / "pre_mix.wav"
    bgm_end = BGM_START_SEC + dur
    fc = (
        f"[0:a]asplit=2[vo][vo_sc];"
        f"[1:a]atrim={BGM_START_SEC:.3f}:{bgm_end:.3f},asetpts=PTS-STARTPTS,"
        f"highpass=f=45,equalizer=f=2150:t=q:w=1.0:g=-5.8,extrastereo=m=1.20,"
        f"volume=0.088,afade=t=in:st=0:d=0.16,afade=t=out:st={dur-0.28:.3f}:d=0.28[bgm_raw];"
        f"[bgm_raw][vo_sc]sidechaincompress=threshold=0.040:ratio=3.0:attack=12:release=220[bgm];"
        f"[2:a]volume=0.15,adelay=13550|13550[sh1];"
        f"[2:a]volume=0.19,adelay=22110|22110[sh2];"
        f"[3:a]volume=0.13,adelay=22950|22950[wh1];"
        f"[vo][bgm][sh1][sh2][wh1]amix=inputs=5:normalize=0,atrim=0:{dur:.3f}[out]"
    )
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(vo_leveled),
            "-i", str(BGM_PATH),
            "-i", str(SHUTTER_SFX),
            "-i", str(WHOOSH_SFX),
            "-filter_complex", fc,
            "-map", "[out]", "-ar", "48000", "-ac", "2", str(pre_mix)
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    # Step 3: Two-pass EBU R128 loudness normalization to -11.9 LUFS, TP=-0.2 dBFS
    p1 = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(pre_mix),
            "-af", "loudnorm=I=-11.9:TP=-0.2:LRA=3.5:print_format=json",
            "-f", "null", "-"
        ],
        capture_output=True, text=True, check=True
    )
    m = re.search(r"\{[\s\S]*\}", p1.stderr)
    stats = json.loads(m.group(0))
    ln_af = (
        f"loudnorm=I=-11.9:TP=-0.2:LRA=3.5:"
        f"measured_I={stats['input_i']}:"
        f"measured_TP={stats['input_tp']}:"
        f"measured_LRA={stats['input_lra']}:"
        f"measured_thresh={stats['input_thresh']}:"
        f"offset={stats['target_offset']}:linear=true,"
        f"alimiter=limit=0.96:level=false"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(pre_mix),
            "-af", ln_af,
            "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(out_wav)
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    report = run_ebur128(out_wav)
    summary_lines = [ln for ln in report.splitlines() if any(k in ln for k in ["I:", "LRA:", "Peak:"])]
    print("=== EBU R128 MASTER AUDIT (ElevenLabs + Bling-Bang-Bang-Born) ===")
    for ln in summary_lines[-6:]:
        print(" ", ln.strip())

    ms = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(out_wav),
            "-af", "pan=stereo|c0=0.5*c0+0.5*c1|c1=0.5*c0-0.5*c1,astats=metadata=1:reset=0",
            "-f", "null", "-"
        ],
        capture_output=True, text=True
    )
    rms_lines = [ln.strip() for ln in ms.stderr.splitlines() if "RMS level dB" in ln]
    print("=== MID / SIDE SEPARATION ===")
    for ln in rms_lines[:4]:
        print(" ", ln)


if __name__ == "__main__":
    main()
