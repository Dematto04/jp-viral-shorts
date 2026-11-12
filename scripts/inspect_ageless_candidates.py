#!/usr/bin/env python3
"""
Generates timestamped 4x2 contact sheets (with 0.1-grid coordinate rulers!)
for every clip in assets/ageless_jp_clips/ plus key parasocial clips so we can
visually select exact timestamps and measure exact normalized (ux, uy) arrow targets.
"""
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path("/Users/digiex/Documents/deepseek-harness/default-workspace/jp_refusals_video")
CLIP_DIR = ROOT / "assets/ageless_jp_clips"
CAND_DIR = ROOT / "assets/rentaru_candidates"
VID_DIR = ROOT / "assets/video"
SHEET_DIR = ROOT / "output/ageless_jp_work/candidate_sheets"
SHEET_DIR.mkdir(parents=True, exist_ok=True)


def probe_dur(p: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(p)],
        capture_output=True, text=True,
    )
    try:
        return float(r.stdout.strip())
    except Exception:
        return 0.0


def build_sheet(mp4: Path, out_jpg: Path, n_samples: int = 12):
    dur = probe_dur(mp4)
    if dur <= 0.5:
        return
    cols = 4
    rows = math.ceil(n_samples / cols)
    tw, th = 360, 270
    sheet = Image.new("RGB", (cols * tw, rows * th), (15, 17, 22))
    draw = ImageDraw.Draw(sheet)

    for i in range(n_samples):
        t = round(0.3 + (dur - 0.8) * (i / max(1, n_samples - 1)), 2)
        tmp_png = SHEET_DIR / f"_tmp_{mp4.stem}_{i}.jpg"
        subprocess.run(
            [
                "ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(mp4),
                "-frames:v", "1", "-vf", f"scale={tw-6}:{th-6}:force_original_aspect_ratio=decrease,pad={tw-6}:{th-6}:(ow-iw)/2:(oh-ih)/2:color=black",
                str(tmp_png),
            ],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        if tmp_png.exists():
            im = Image.open(tmp_png).convert("RGB")
            gx, gy = (i % cols) * tw + 3, (i // cols) * th + 3
            sheet.paste(im, (gx, gy))
            draw.rectangle((gx, gy, gx + 150, gy + 22), fill=(0, 0, 0))
            draw.text((gx + 5, gy + 4), f"t={t:.1f}s / {dur:.0f}s", fill=(255, 230, 0))
            tmp_png.unlink(missing_ok=True)

    sheet.save(out_jpg, quality=88)
    print(f"Sheet: {out_jpg.name} ({dur:.1f}s)")


def main():
    clips = sorted(CLIP_DIR.glob("*.mp4")) + [
        CAND_DIR / "glam_tokyo_cafe.mp4",
        CAND_DIR / "glam_cherry.mp4",
        CAND_DIR / "glam_camitie.mp4",
        CAND_DIR / "yt_dayoff_1.mp4",
        VID_DIR / "train_station.mp4",
        VID_DIR / "subway_arriving.mp4",
    ]
    for p in clips:
        if p.exists() and p.stat().st_size > 100_000:
            build_sheet(p, SHEET_DIR / f"{p.stem}.jpg", n_samples=12)


if __name__ == "__main__":
    main()
