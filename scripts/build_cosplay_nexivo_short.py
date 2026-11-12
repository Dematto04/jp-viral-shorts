#!/usr/bin/env python3
"""
Full 30fps Nexivo 4-Act Loop Renderer (Glamour Cosplayer Edition) for:
  output/Never_Do_This_Cosplay_Japan_Short.mp4

Follows 100% of .agents/rules/viral-shorts-editing.md (Nexivo 8.8M-View 26-Second Blueprint):
- 1080x1920 @ 30fps, 25.63s (769 frames), 81 words (~190 WPM), <= 0.10s inter-sentence pauses
- 11 real-motion video shots (2.33s ASL; zero static stills; zero Japanese text overlays)
- All cosplayer-subject shots feature high-glamour, alluring Japanese Comiket cosplayers
- Keyframed Red Pointer Arrow (Frames 1-34 / 0.00s-1.13s): #FF1A1A fill, 6px #000000 stroke
  over Yamohachiko's platinum-silver hair & glowing blue backdrop (maximum contrast)
- Single-Word Rapid-Fire 4-Color Captions at (x=540, y=1385) with 1-2 frame horizontal motion-blur + 1.15x scaleX pop
- Audio mastered to -11.9 LUFS, True Peak -0.4 dBFS, stereo BGM -23.7 dB below Mid voice RMS
"""
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from nexivo_caption_arrow import draw_nexivo_caption, draw_nexivo_hook_arrow

WORK_DIR = ROOT / "output/cosplay_short_work"
PREP_DIR = WORK_DIR / "prep_clips_30fps_glam"
CLIP_DIR = ROOT / "assets/cosplay_short_clips"
GLAM_DIR = ROOT / "assets/cosplay_glam_clips"
OUT_DIR = ROOT / "output"
FONT_BLACK_PATH = str(ROOT / "assets/fonts/ArchivoBlack-Regular.ttf")

W, H, FPS = 1080, 1920, 30
CLAUSES_META = json.loads((WORK_DIR / "clauses.json").read_text())
WORDS = json.loads((WORK_DIR / "words.json").read_text())
DURATION = CLAUSES_META["total_duration"]
TOTAL_FRAMES = int(round(DURATION * FPS))

# ==============================================================================
# 11-SHOT GLAMOUR COSPLAYER 30FPS TIMELINE (25.63s total, 2.33s ASL)
# ==============================================================================
SHOTS = [
    # Act I — Hook (0.00s - 5.05s): Yamohachiko (Platinum-silver hair, plunging white iridescent gown, blue glow)
    {
        "id": "S01_Hook_YamohachikoPlatinum",
        "start": 0.00, "end": 5.05,
        "src": GLAM_DIR / "glam_c106_yamohachiko.mp4",
        "offset": 96.20,
        "crop_x": 0.50,
        "crop_y": 0.0,
        "scale_h": 2040,
        "zoom": (1.02, 1.08),
    },
    # Act II — Sacred Craft A (5.05s - 7.65s): Puyon as Yor Forger in crimson off-shoulder mini-dress (Comiket C103)
    {
        "id": "S02_Glam_PuyonYorCrimson",
        "start": 5.05, "end": 7.65,
        "src": GLAM_DIR / "glam_c103_puyon.mp4",
        "offset": 10.20,
        "transpose": 1,
        "crop_x": 0.50,
        "crop_y": 0.05,
        "scale_h": 1980,
        "zoom": (1.01, 1.06),
    },
    # Act II — Sacred Craft B (7.65s - 10.42s): Kirara Midorikawa as Dark Magician Girl corset (Comiket C106)
    {
        "id": "S03_Glam_MidorikawaDMG",
        "start": 7.65, "end": 10.42,
        "src": GLAM_DIR / "glam_c106_midorikawa.mp4",
        "offset": 36.80,
        "transpose": 1,
        "crop_x": 0.50,
        "crop_y": 0.04,
        "scale_h": 1980,
        "zoom": (1.01, 1.06),
    },
    # Act III — The Violation: 3 Consecutive Jump-Cuts of Tourists Crowding & Snapping Without Asking (10.42s - 17.86s)
    {
        "id": "S04_ViolCutA_CrowdSneakSnap",
        "start": 10.42, "end": 13.00,
        "src": CLIP_DIR / "ikebukuro_day_parade.mp4",
        "offset": 26.80,
        "crop_x": 0.27,
        "zoom": (1.04, 1.09),
    },
    {
        "id": "S05_ViolCutB_CameraShoveClose",
        "start": 13.00, "end": 15.35,
        "src": CLIP_DIR / "ikebukuro_day_parade.mp4",
        "offset": 35.10,
        "crop_x": 0.25,
        "zoom": (1.10, 1.16),
    },
    {
        "id": "S06_ViolCutC_LungeIntoLane",
        "start": 15.35, "end": 17.86,
        "src": CLIP_DIR / "ikebukuro_day_parade.mp4",
        "offset": 84.60,
        "crop_x": 0.29,
        "zoom": (1.06, 1.12),
    },
    # Act IV — Cultural Pivot (17.86s - 19.72s): Respectful Comiket photographer circle around mini-dress cosplayer
    {
        "id": "S07_Pivot_RespectfulQueue",
        "start": 17.86, "end": 19.72,
        "src": CLIP_DIR / "comiket_summer_4k.mp4",
        "offset": 108.40,
        "crop_x": 0.50,
        "zoom": (1.00, 1.05),
    },
    # Climax Micro-Montage: 3 Rapid Alluring Cosplayer Shots ~1.0s Each (19.72s - 22.95s)
    {
        "id": "S08_ClimaxD_TwintailGlamNod",
        "start": 19.72, "end": 20.80,
        "src": CLIP_DIR / "comiket_c107_queues_b.mp4",
        "offset": 81.10,
        "crop_x": 0.50,
        "zoom": (1.03, 1.09),
    },
    {
        "id": "S09_ClimaxE_SilverCorsetGlam",
        "start": 20.80, "end": 21.75,
        "src": GLAM_DIR / "glam_c102_aethergazer.mp4",
        "offset": 7.20,
        "transpose": 1,
        "crop_x": 0.72,
        "crop_y": 0.14,
        "scale_h": 2480,
        "zoom": (1.01, 1.06),
    },
    {
        "id": "S10_ClimaxF_KikkaSeductiveWink",
        "start": 21.75, "end": 22.95,
        "src": GLAM_DIR / "glam_c107_kikka_gfl2.mp4",
        "offset": 63.95,
        "transpose": 1,
        "crop_x": 0.50,
        "crop_y": 0.0,
        "scale_h": 2260,
        "zoom": (1.01, 1.06),
        "zoom_anchor_y": 0.10,
        "shutter_flash_t": 22.11,
    },
    # Payoff / Loop Outro — Dark-Mode Midnight-Graded Glamour Cosplayer Gaze (22.95s - 25.71s)
    {
        "id": "S11_Payoff_MidnightGlamGaze",
        "start": 22.95, "end": DURATION,
        "src": GLAM_DIR / "glam_c106_takane.mp4",
        "offset": 85.10,
        "crop_x": 0.50,
        "crop_y": 0.0,
        "scale_h": 2040,
        "zoom": (1.04, 1.11),
        "night_grade": True,
    },
]


def prepare_30fps_clips():
    PREP_DIR.mkdir(parents=True, exist_ok=True)
    for idx, s in enumerate(SHOTS):
        out_mp4 = PREP_DIR / f"shot_{idx+1:02d}_{s['id']}.mp4"
        s["prep_path"] = out_mp4
        if out_mp4.exists() and out_mp4.stat().st_size > 20_000:
            continue
        dur = (s["end"] - s["start"]) + 0.25
        cx = s.get("crop_x", 0.50)
        cy = s.get("crop_y", 0.0)
        sh = s.get("scale_h", 1920)

        vf_parts = []
        if "transpose" in s:
            vf_parts.append(f"transpose={s['transpose']}")
        vf_parts.extend([
            f"scale=-2:{sh}:flags=lanczos",
            f"crop=1080:1920:(iw-1080)*{cx:.3f}:(ih-1920)*{cy:.3f}",
        ])
        if s.get("night_grade"):
            vf_parts.append("eq=contrast=1.18:brightness=-0.10:saturation=1.24")
        else:
            vf_parts.append("eq=contrast=1.04:saturation=1.08")
        vf_parts.extend([f"fps={FPS}", "format=yuv420p"])
        vf = ",".join(vf_parts)

        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{s['offset']:.2f}",
            "-i", str(s["src"]),
            "-t", f"{dur:.2f}",
            "-vf", vf,
            "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
            str(out_mp4),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[Prep 30fps Glam] {idx+1:02d}/{len(SHOTS)}: {s['id']} ({s['end']-s['start']:.2f}s)")


def build_standalone_thumbnail(base_rgb: Image.Image, out_path: Path):
    """Generates a standalone high-CTR 9:16 thumbnail featuring Yamohachiko + Red Arrow."""
    canvas = base_rgb.convert("RGBA")
    draw_nexivo_hook_arrow(canvas, t=0.60, cheek_xy=(0.47, 0.25), crown_xy=(0.53, 0.14))

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    f1 = ImageFont.truetype(FONT_BLACK_PATH, 80)
    f2 = ImageFont.truetype(FONT_BLACK_PATH, 84)
    f3 = ImageFont.truetype(FONT_BLACK_PATH, 84)

    lines = [
        ("NEVER Do This", f1, (255, 77, 77, 255), 1160),
        ("to Cosplayers", f2, (255, 255, 255, 255), 1265),
        ("in Japan!", f3, (255, 232, 56, 255), 1370),
    ]
    for txt, font, col, y in lines:
        d.text((W // 2 + 6, y + 8), txt, font=font, fill=(0, 0, 0, 230), anchor="mm", stroke_width=16, stroke_fill=(0, 0, 0, 230))
        d.text((W // 2, y), txt, font=font, fill=col, anchor="mm", stroke_width=13, stroke_fill=(0, 0, 0, 255))

    canvas.alpha_composite(overlay)
    canvas.convert("RGB").save(out_path, quality=95)


def compose_frame(base_rgb: Image.Image, shot: dict, t: float, local_t: float, dur: float) -> Image.Image:
    z0, z1 = shot.get("zoom", (1.0, 1.04))
    prog = max(0.0, min(1.0, local_t / max(0.001, dur)))
    cur_z = z0 + (z1 - z0) * prog
    if abs(cur_z - 1.0) > 0.003:
        zw, zh = int(round(W * cur_z)), int(round(H * cur_z))
        scaled = base_rgb.resize((zw, zh), Image.Resampling.BILINEAR)
        x0 = int((zw - W) * shot.get("zoom_anchor_x", 0.50))
        y0 = int((zh - H) * shot.get("zoom_anchor_y", 0.50))
        base_rgb = scaled.crop((x0, y0, x0 + W, y0 + H))

    # Subtle 1-frame tactile shutter flash on earned pose (S10 @ 21.80s)
    flash_t = shot.get("shutter_flash_t")
    if flash_t is not None and 0.0 <= (t - flash_t) < 0.065:
        strength = 1.24 if (t - flash_t) < 0.033 else 1.10
        base_rgb = ImageEnhance.Brightness(base_rgb).enhance(strength)

    canvas = base_rgb.convert("RGBA")

    # First-Second Thumb-Stopper Mechanic (Frames 1-34 / 0.00s - 1.13s)
    if t <= 1.14:
        draw_nexivo_hook_arrow(
            canvas,
            t=t,
            cheek_xy=(0.47, 0.25),
            crown_xy=(0.53, 0.14),
        )

    # Single-Word Rapid-Fire 4-Color Caption at (x=540, y=1385)
    draw_nexivo_caption(canvas, WORDS, t)
    return canvas


def main():
    prepare_30fps_clips()
    audio_wav = WORK_DIR / "mastered_audio.wav"

    final_mp4 = OUT_DIR / "Never_Do_This_Cosplay_Japan_Short.mp4"
    thumb_jpg = OUT_DIR / "Never_Do_This_Cosplay_Japan_Short_Thumb.jpg"
    contact_jpg = OUT_DIR / "Never_Do_This_Cosplay_Japan_Contact_Sheet.jpg"
    arrow_audit_jpg = OUT_DIR / "Never_Do_This_Cosplay_Japan_Hook_Arrow_Audit.jpg"

    writer = subprocess.Popen(
        [
            "ffmpeg", "-y",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
            "-i", "-",
            "-i", str(audio_wav),
            "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart",
            "-shortest", str(final_mp4),
        ],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    frame_bytes = W * H * 3
    cur_shot_idx = -1
    reader = None
    shot_mid_samples = {}
    arrow_samples = []
    arrow_sample_frames = {1, 6, 10, 16, 22, 26, 30, 35}

    for f_idx in range(TOTAL_FRAMES):
        t = f_idx / FPS
        s_idx = len(SHOTS) - 1
        for i, s in enumerate(SHOTS):
            if s["start"] <= t < s["end"]:
                s_idx = i
                break
        shot = SHOTS[s_idx]
        dur = shot["end"] - shot["start"]
        local_t = max(0.0, t - shot["start"])
        prog = local_t / max(0.001, dur)

        if s_idx != cur_shot_idx:
            if reader is not None:
                reader.stdout.close()
                reader.wait()
            cur_shot_idx = s_idx
            reader = subprocess.Popen(
                ["ffmpeg", "-i", str(shot["prep_path"]), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
            )

        raw = reader.stdout.read(frame_bytes) if reader else b""
        if len(raw) < frame_bytes:
            base = Image.new("RGB", (W, H), (14, 16, 22))
        else:
            base = Image.frombytes("RGB", (W, H), raw)

        if f_idx == 20:
            build_standalone_thumbnail(base, thumb_jpg)

        comp = compose_frame(base, shot, t, local_t, dur).convert("RGB")

        if f_idx in arrow_sample_frames:
            arrow_samples.append((f_idx, t, comp.copy()))

        if s_idx not in shot_mid_samples and prog >= 0.48:
            shot_mid_samples[s_idx] = (t, comp.copy())

        writer.stdin.write(comp.tobytes())
        if f_idx % 150 == 0 or f_idx == TOTAL_FRAMES - 1:
            print(f"[Render 30fps Glam] Frame {f_idx+1}/{TOTAL_FRAMES} ({t:.2f}s / {DURATION:.2f}s)")

    if reader is not None:
        reader.stdout.close()
        reader.wait()
    writer.stdin.close()
    writer.wait()

    # Build 11-Shot Contact Sheet (4 cols x 3 rows)
    cols, rows = 4, 3
    tw, th = 270, 480
    sheet = Image.new("RGB", (cols * tw, rows * th), (12, 14, 18))
    sd = ImageDraw.Draw(sheet)
    for idx in range(len(SHOTS)):
        if idx not in shot_mid_samples:
            continue
        st_t, img = shot_mid_samples[idx]
        tile = img.resize((tw - 6, th - 6), Image.Resampling.LANCZOS)
        gx, gy = (idx % cols) * tw + 3, (idx // cols) * th + 3
        sheet.paste(tile, (gx, gy))
        sd.rectangle((gx, gy, gx + 235, gy + 28), fill=(0, 0, 0))
        sd.text((gx + 6, gy + 6), f"S{idx+1:02d} @{st_t:.2f}s {SHOTS[idx]['id'][4:18]}", fill=(255, 232, 56))
    sheet.save(contact_jpg, quality=92)

    # Build 8-Frame Hook Red Arrow Trajectory Audit Sheet (4 cols x 2 rows)
    acols, arows = 4, 2
    audit = Image.new("RGB", (acols * tw, arows * th), (12, 14, 18))
    ad = ImageDraw.Draw(audit)
    for i, (f_i, st_t, img) in enumerate(arrow_samples[:8]):
        tile = img.resize((tw - 6, th - 6), Image.Resampling.LANCZOS)
        gx, gy = (i % acols) * tw + 3, (i // acols) * th + 3
        audit.paste(tile, (gx, gy))
        ad.rectangle((gx, gy, gx + 195, gy + 28), fill=(0, 0, 0))
        ad.text((gx + 6, gy + 6), f"f{f_i+1:03d} ({st_t:.2f}s)", fill=(66, 242, 247))
    audit.save(arrow_audit_jpg, quality=92)

    print(f"[Complete Glam] MP4: {final_mp4}")


if __name__ == "__main__":
    main()
