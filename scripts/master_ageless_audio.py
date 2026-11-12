#!/usr/bin/env python3
"""
Masters output/ageless_jp_work/mastered_audio.wav (57.786s @ normal 1.0x ElevenLabs speed) with:
1. User's ElevenLabs v3 voiceover at natural 1.0x speed (narration_full.wav), centered in Mono Mid
2. Creepy Nuts — "Bling-Bang-Bang-Born" (assets/audio/bling_bang_bang_born.wav, viral chorus @61.45s)
   with 2.15 kHz vocal-pocket EQ carve and smooth sidechain ducking under VO
3. Clean, non-fatiguing SFX design (ZERO wood_bonk_pop / ZERO whip_crack_slap):
   - quick_tip.wav        : 6 crisp educational tip/stat/glossary chimes (Bihaku, Higasa, 80%, Natto, 7,000 steps, 40°C)
   - whoosh_whip_fast.wav : 5 clean air swishes at the 3 Pillar Spin-Swirl boundaries & 2 key Whip-Horiz pivots
   - kabuki_pon_chime.wav : 1 traditional Japanese accent on Ofuro reveal
   - shutter.wav          : 2 subtle framing clicks at 0.05s opener & 57.12s loop bridge
"""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK_DIR = ROOT / "output/ageless_jp_work"
SFX_DIR = ROOT / "assets/sfx"
BGM_PATH = ROOT / "assets/audio/bling_bang_bang_born.wav"
if not BGM_PATH.exists():
    BGM_PATH = ROOT / "assets/audio/bling_bang_bang_born_full.m4a"

BGM_START_SEC = 61.45

SHUTTER_SFX = SFX_DIR / "shutter.wav"
WHOOSH_FAST = SFX_DIR / "whoosh_whip_fast.wav"
QUICK_TIP   = SFX_DIR / "quick_tip.wav"
KABUKI_PON  = SFX_DIR / "kabuki_pon_chime.wav"


def run_ebur128(wav_path: Path) -> str:
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(wav_path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    return r.stderr


def main():
    cdata = json.loads((WORK_DIR / "clauses.json").read_text())
    dur = cdata["total_duration"]
    vo_in = WORK_DIR / "narration_full.wav"
    out_wav = WORK_DIR / "mastered_audio.wav"

    # 1. Level & compress ElevenLabs 1.0x narrator dead-center (mono Mid channel)
    vo_leveled = WORK_DIR / "vo_leveled.wav"
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(vo_in),
            "-af", (
                "highpass=f=80,"
                "acompressor=threshold=-21dB:ratio=3.2:attack=5:release=75:makeup=3.5dB,"
                "alimiter=limit=0.90:level=false,"
                "pan=stereo|c0=c0|c1=c0"
            ),
            "-ar", "48000", str(vo_leveled),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    # 2. Clean 14-event SFX stem synced to 1.0x ElevenLabs timestamps
    sfx_events = [
        (SHUTTER_SFX, 0.05,  0.16),  # Hook opener framing click
        (WHOOSH_FAST, 4.72,  0.18),  # S02 -> S03 360° Spin-Swirl into Pillar 1
        (QUICK_TIP,   9.20,  0.17),  # (美白 · Bihaku) beauty code reveal
        (WHOOSH_FAST, 13.70, 0.14),  # S06 -> S07 Whip-Horiz into UV Armor burst
        (QUICK_TIP,   16.40, 0.16),  # (日傘 · Higasa) Kanji glossary reveal
        (QUICK_TIP,   19.30, 0.19),  # "80% of skin aging" key dermatologist stat pop
        (WHOOSH_FAST, 23.46, 0.18),  # S11 -> S12 360° Spin-Swirl into Pillar 2
        (WHOOSH_FAST, 29.88, 0.15),  # S13 -> S14 Whip-Horiz into Green Tea / Miso / Natto
        (QUICK_TIP,   34.90, 0.16),  # (納豆 · Natto) fermented superfood reveal
        (QUICK_TIP,   38.64, 0.17),  # "7,000 steps" commuter tip pop
        (WHOOSH_FAST, 41.28, 0.18),  # S19 -> S20 360° Spin-Swirl into Pillar 3
        (KABUKI_PON,  44.78, 0.13),  # (お風呂 · Ofuro) traditional bath ritual chime
        (QUICK_TIP,   48.48, 0.18),  # "40°C hot water" nightly soak tip pop
        (SHUTTER_SFX, 57.12, 0.14),  # S27 -> S28 Loop Bridge ("That's...") framing click
    ]

    sfx_stem = WORK_DIR / "sfx_stem.wav"
    cmd_sfx = ["ffmpeg", "-y", "-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
    fc_parts = []
    mix_labels = ["[0:a]"]
    for idx, (path, t_s, vol) in enumerate(sfx_events, start=1):
        cmd_sfx += ["-i", str(path)]
        ms = max(0, int(round(t_s * 1000)))
        lbl = f"[s{idx}]"
        fc_parts.append(
            f"[{idx}:a]aresample=48000,pan=stereo|c0=0.5*c0+0.5*c1|c1=0.5*c0+0.5*c1,"
            f"adelay={ms}|{ms},volume={vol*1.55:.3f}{lbl}"
        )
        mix_labels.append(lbl)

    fc_sfx = ";".join(fc_parts) + f";{''.join(mix_labels)}amix=inputs={len(mix_labels)}:normalize=0,atrim=0:{dur:.3f}[sfx_out]"
    cmd_sfx += ["-filter_complex", fc_sfx, "-map", "[sfx_out]", "-ar", "48000", "-ac", "2", str(sfx_stem)]
    subprocess.run(cmd_sfx, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 3. Combine Leveled Mono ElevenLabs 1.0x Voice + Sidechained Creepy Nuts BGM + Clean SFX Stem
    pre_mix = WORK_DIR / "pre_mix.wav"
    bgm_end = BGM_START_SEC + dur
    fc = (
        f"[0:a]asplit=2[vo][vo_sc];"
        f"[1:a]atrim={BGM_START_SEC:.3f}:{bgm_end:.3f},asetpts=PTS-STARTPTS,"
        f"highpass=f=48,equalizer=f=2150:t=q:w=1.05:g=-6.0,extrastereo=m=1.55,"
        f"volume=0.145,afade=t=in:st=0:d=0.18,afade=t=out:st={dur-0.24:.3f}:d=0.24[bgm_raw];"
        f"[bgm_raw][vo_sc]sidechaincompress=threshold=0.038:ratio=2.8:attack=10:release=210[bgm];"
        f"[vo][bgm][2:a]amix=inputs=3:normalize=0,atrim=0:{dur:.3f}[out]"
    )
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(vo_leveled),
            "-i", str(BGM_PATH),
            "-i", str(sfx_stem),
            "-filter_complex", fc,
            "-map", "[out]", "-ar", "48000", "-ac", "2", str(pre_mix),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    # 4. Two-pass EBU R128 loudness normalization targeting -15.2 LUFS
    p1 = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(pre_mix),
            "-af", "loudnorm=I=-15.2:TP=-0.3:LRA=2.2:print_format=json",
            "-f", "null", "-",
        ],
        capture_output=True, text=True, check=True,
    )
    m = re.search(r"\{[\s\S]*\}", p1.stderr)
    stats = json.loads(m.group(0))
    ln_af = (
        f"loudnorm=I=-15.2:TP=-0.3:LRA=2.2:"
        f"measured_I={stats['input_i']}:"
        f"measured_TP={stats['input_tp']}:"
        f"measured_LRA={stats['input_lra']}:"
        f"measured_thresh={stats['input_thresh']}:"
        f"offset={stats['target_offset']}:linear=true,"
        f"alimiter=limit=0.95:level=false"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(pre_mix),
            "-af", ln_af,
            "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(out_wav),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    report = run_ebur128(out_wav)
    summary_lines = [ln for ln in report.splitlines() if any(k in ln for k in ["I:", "LRA:", "Peak:"])]
    print("=== EBU R128 MASTER AUDIT (ElevenLabs 1.0x + Creepy Nuts + QuickTip SFX) ===")
    for ln in summary_lines[-6:]:
        print(" ", ln.strip())

    ms = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(out_wav),
            "-af", "pan=stereo|c0=0.5*c0+0.5*c1|c1=0.5*c0-0.5*c1,astats=metadata=1:reset=0",
            "-f", "null", "-",
        ],
        capture_output=True, text=True,
    )
    rms_lines = [ln.strip() for ln in ms.stderr.splitlines() if "RMS level dB" in ln]
    print("=== MID / SIDE SEPARATION ===")
    for ln in rms_lines[:3]:
        print(" ", ln)


if __name__ == "__main__":
    main()
