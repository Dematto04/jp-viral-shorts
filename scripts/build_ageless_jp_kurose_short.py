#!/usr/bin/env python3
"""
60fps Production Renderer — "Why Japanese Women Look 25 at Age 45?!" (57.786s @ normal 1.0x ElevenLabs speed)

Updates per latest user feedback:
1. Normal 1.0x ElevenLabs voiceover speed (57.786s, 3,467 frames @ 60fps), word-locked via Whisper.
2. ALL @kurose watermarks completely removed.
3. 100% Real-World Camera Footage for Opening Hook & Climax:
   - S01 (0.00-2.75s) & S28 (57.12-57.79s seamless same-take loop): Umi Shinonome 4K Sony cinema-camera
     photobook making-of by sunlit hotel curtains (cand_shinonome_umi.mp4) — 100% real footage, alluring & clean.
   - S02 (2.75-4.82s) & S27 (55.95-57.12s): Mai Shiraishi real outdoor natural-sunlight handheld shoot
     (real_shiraishi_lookbook.mp4). Zero CG/AI/mobile-game commercial footage anywhere.
4. Creepy Nuts — "Bling-Bang-Bang-Born" BGM + clean quick_tip SFX (zero slap/bonk spam).
5. Grid-calibrated Red Arrows across all 1080x1920 shots with zero facial occlusion.
"""
from pathlib import Path
from functools import lru_cache
import json
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
WORK_DIR = ROOT / "output/ageless_jp_work"
PREP_DIR = WORK_DIR / "prep_clips_60fps_v4"
OUT_DIR = ROOT / "output"

FONT_EN_BLACK = ROOT / "assets/fonts/ArchivoBlack-Regular.ttf"
FONT_JP_BOLD = ROOT / "assets/fonts/ZenKakuGothicNew-Bold.ttf"

W, H, FPS = 1080, 1920, 60
CLAUSES_META = json.loads((WORK_DIR / "clauses.json").read_text())
DURATION = CLAUSES_META["total_duration"]
TOTAL_FRAMES = int(round(DURATION * FPS))
WORDS = json.loads((WORK_DIR / "words.json").read_text())

KANJI_GLOSSARIES = [
    (9.05,  10.25, "(美白 · Bihaku)"),
    (16.25, 17.52, "(日傘 · Higasa)"),
    (34.10, 35.30, "(納豆 · Natto)"),
    (44.45, 45.32, "(お風呂 · Ofuro)"),
]

AGL = ROOT / "assets/ageless_jp_clips"
CAND = ROOT / "assets/rentaru_candidates"
VID = ROOT / "assets/video"

UMI_CROP = "crop=iw*0.46:ih*0.82:iw*0.27:ih*0.02,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"

TRANS_HALF_DUR = {
    "spin_swirl": 0.17,   # 20 frames @60fps = 10 frames @30fps
    "whip_horiz": 0.15,   # 18 frames @60fps =  9 frames @30fps
    "push_vert":  0.10,   # 12 frames @60fps =  6 frames @30fps
    "zoom_punch": 0.085,  # 10 frames @60fps =  5 frames @30fps
}

# ==============================================================================
# 28-SHOT REAL-FOOTAGE 60FPS TIMELINE (57.786s — 1.0x ElevenLabs Locked)
# ==============================================================================
SHOTS = [
    # --- HOOK (0.00 - 4.82s): 100% Real 4K Gravure Making-Of & Natural Daylight Footage ---
    {
        "id": "S01_Hook_UmiRealGlam",
        "start": 0.00, "end": 2.75,
        "src": AGL / "cand_shinonome_umi.mp4", "offset": 5.32,
        "mode": "custom_crop", "crop_vf": UMI_CROP,
        "zoom": (1.00, 1.05),
        "trans_out": "zoom_punch",
        "arrow": {
            "kfs": [(0.00, 0.38, 0.33), (0.30, 0.40, 0.30), (0.65, 0.42, 0.28), (1.00, 0.42, 0.26)],
            "angle": 12,
        },
    },
    {
        "id": "S02_Hook_ShiraishiNaturalSun",
        "start": 2.75, "end": 4.82,
        "src": AGL / "real_shiraishi_lookbook.mp4", "offset": 7.50,
        "mode": "custom_crop",
        "crop_vf": "crop=iw*0.52:ih*0.94:iw*0.18:ih*0.03,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "zoom": (1.02, 1.08),
        "trans_out": "spin_swirl",  # 360° Spin-Swirl into Pillar 1!
    },

    # --- PILLAR 1: BIHAKU & HIGASA UV ARMOR (4.82 - 23.56s) ---
    {
        "id": "S03_P1_VampireUVArmor",
        "start": 4.82, "end": 8.05,
        "src": AGL / "complete_uv_protection.mp4", "offset": 3.80,
        "mode": "tall_card", "zoom": (1.00, 1.06),
        "blur_bar": (0.54, 0.71),
        "trans_out": "zoom_punch",
        "arrow": {
            "kfs": [(0.00, 0.64, 0.46), (0.15, 0.64, 0.46), (0.45, 0.65, 0.46), (0.78, 0.58, 0.47), (1.00, 0.55, 0.47)],
            "angle": 150,
        },
    },
    {
        "id": "S04_P1_BihakuPorcelain",
        "start": 8.05, "end": 10.28,
        "src": AGL / "complete_uv_protection.mp4", "offset": 80.20,
        "mode": "tall_card", "zoom": (1.02, 1.08),
        "blur_bar": (0.60, 0.71),
        "trans_out": "push_vert",
        "arrow": {
            "kfs": [(0.00, 0.64, 0.41), (0.50, 0.64, 0.40), (1.00, 0.63, 0.40)],
            "angle": 155,
        },
    },
    {
        "id": "S05_P1_Tokyo35CParasol",
        "start": 10.28, "end": 11.95,
        "src": AGL / "tokyo_heatwave_parasols.mp4", "offset": 27.60,
        "mode": "custom_crop",
        "crop_vf": "crop=iw*0.72:ih*0.92:iw*0.06:ih*0.04,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "zoom": (1.03, 1.10),
        "trans_out": "zoom_punch",
        "red_circle": {
            "kfs": [(0.00, 0.36, 0.28), (0.15, 0.42, 0.27), (0.50, 0.60, 0.23), (0.85, 0.68, 0.22), (1.00, 0.71, 0.22)],
            "rx": 0.25, "ry": 0.06,
        },
        "arrow": {
            "kfs": [(0.00, 0.24, 0.32), (0.15, 0.30, 0.31), (0.50, 0.46, 0.27), (0.85, 0.54, 0.26), (1.00, 0.57, 0.26)],
            "angle": -35,
        },
    },
    {
        "id": "S06_P1_CloudyDayUmbrella",
        "start": 11.95, "end": 13.78,
        "src": VID / "tokyo_pedestrian.mp4", "offset": 5.80,
        "mode": "custom_crop",
        "crop_vf": "crop=iw*0.58:ih*0.95:iw*0.02:ih*0.02,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "zoom": (1.00, 1.05),
        "trans_out": "whip_horiz",
        "arrow": {
            "kfs": [(0.00, 0.40, 0.45), (0.15, 0.38, 0.45), (0.45, 0.33, 0.45), (0.78, 0.21, 0.45), (1.00, 0.14, 0.45)],
            "angle": 140,
        },
    },
    {
        "id": "S07_P1_UVVisorShield",
        "start": 13.78, "end": 14.96,
        "src": AGL / "uv_visor_demo.mp4", "offset": 3.10,
        "mode": "custom_crop",
        "crop_vf": "crop=iw*0.46:ih*0.80:iw*0.34:ih*0.19,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "zoom": (1.02, 1.08),
        "trans_out": "zoom_punch",
        "arrow": {
            "kfs": [(0.00, 0.30, 0.49), (0.15, 0.31, 0.48), (0.50, 0.33, 0.46), (0.85, 0.39, 0.41), (1.00, 0.41, 0.39)],
            "angle": 25,
        },
    },
    {
        "id": "S08_P1_LongArmGloves",
        "start": 14.96, "end": 15.95,
        "src": AGL / "outdoor_uv_armor_walk.mp4", "offset": 72.40,
        "mode": "custom_crop",
        "crop_vf": "crop=iw*0.62:ih*0.92:iw*0.34:ih*0.04,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "zoom": (1.02, 1.08),
        "trans_out": "zoom_punch",
        "arrow": {
            "kfs": [(0.00, 0.45, 0.46), (0.15, 0.48, 0.48), (0.50, 0.68, 0.60), (0.85, 0.74, 0.62), (1.00, 0.76, 0.63)],
            "angle": 115,
        },
    },
    {
        "id": "S09_P1_BlackHigasa",
        "start": 15.95, "end": 17.58,
        "src": AGL / "sunbarrier_full_armor_b.mp4", "offset": 21.20,
        "mode": "tall_card", "zoom": (1.03, 1.10),
        "trans_out": "whip_horiz",
        "arrow": {
            "kfs": [(0.00, 0.26, 0.42), (0.15, 0.33, 0.43), (0.50, 0.48, 0.45), (0.85, 0.70, 0.44), (1.00, 0.76, 0.44)],
            "angle": 90,
        },
    },
    {
        "id": "S10_P1_Bimajo80Pct",
        "start": 17.58, "end": 21.15,
        "src": AGL / "bimajo_43yo_skin.mp4", "offset": 63.80,
        "mode": "tall_card", "zoom": (1.00, 1.07),
        "blur_bar": (0.55, 0.68),
        "trans_out": "push_vert",
        "arrow": {
            "delay_s": 1.72,
            "kfs": [(0.00, 0.41, 0.43), (0.50, 0.42, 0.43), (0.85, 0.45, 0.43), (1.00, 0.46, 0.43)],
            "angle": 15,
        },
        "emote": {
            "kind": "shout_bang",
            "delay_s": 1.72,
            "kfs": [(0.00, 0.26, 0.30), (1.00, 0.26, 0.30)],
        },
    },
    {
        "id": "S11_P1_OmotesandoCrosswalk",
        "start": 21.15, "end": 23.56,
        "src": AGL / "omotesando_summer_parasols.mp4", "offset": 12.20,
        "mode": "tall_card", "zoom": (1.00, 1.06),
        "trans_out": "spin_swirl",  # 360° Spin-Swirl into Pillar 2!
        "arrow": {
            "kfs": [(0.00, 0.46, 0.49), (0.50, 0.44, 0.49), (1.00, 0.41, 0.49)],
            "angle": 75,
        },
    },

    # --- PILLAR 2: ZERO LIQUID SUGAR, FERMENTED DIET & 7,000+ STEPS (23.56 - 41.38s) ---
    {
        "id": "S12_P2_RadiantSmile",
        "start": 23.56, "end": 27.52,
        "src": AGL / "outdoor_uv_armor_walk.mp4", "offset": 32.00,
        "mode": "tall_card", "zoom": (1.02, 1.07),
        "trans_out": "push_vert",
    },
    {
        "id": "S13_P2_SugarySodaFizz",
        "start": 27.52, "end": 29.96,
        "src": AGL / "soda_pour_sugar.mp4", "offset": 12.20,
        "mode": "tall_card", "zoom": (1.03, 1.11),
        "trans_out": "whip_horiz",
        "arrow": {
            "kfs": [(0.00, 0.38, 0.40), (0.15, 0.40, 0.40), (0.50, 0.45, 0.41), (0.85, 0.53, 0.41), (1.00, 0.56, 0.41)],
            "angle": 15,
        },
        "emote": {
            "kind": "anger_vein",
            "kfs": [(0.00, 0.76, 0.35), (1.00, 0.76, 0.35)],
        },
    },
    {
        "id": "S14_P2_GreenTeaPour",
        "start": 29.96, "end": 32.12,
        "src": AGL / "green_tea_pour.mp4", "offset": 2.10,
        "mode": "tall_card", "zoom": (1.02, 1.08),
        "trans_out": "zoom_punch",
        "arrow": {
            "kfs": [(0.00, 0.78, 0.42), (0.15, 0.80, 0.42), (0.50, 0.86, 0.43), (0.85, 0.90, 0.44), (1.00, 0.91, 0.44)],
            "angle": 35,
        },
    },
    {
        "id": "S15_P2_MisoSoupPot",
        "start": 32.12, "end": 33.65,
        "src": AGL / "miso_soup_ladle.mp4", "offset": 11.80,
        "mode": "tall_card", "zoom": (1.03, 1.10),
        "trans_out": "zoom_punch",
        "arrow": {
            "kfs": [(0.00, 0.58, 0.43), (0.15, 0.60, 0.43), (0.50, 0.63, 0.44), (0.85, 0.76, 0.45), (1.00, 0.78, 0.45)],
            "angle": 55,
        },
    },
    {
        "id": "S16_P2_StickyNattoWhip",
        "start": 33.65, "end": 35.35,
        "src": AGL / "natto_sticky_whip.mp4", "offset": 30.50,
        "mode": "tall_card", "zoom": (1.03, 1.10),
        "trans_out": "whip_horiz",
        "red_circle": {
            "kfs": [(0.00, 0.44, 0.46), (0.15, 0.46, 0.46), (0.50, 0.55, 0.46), (0.85, 0.65, 0.46), (1.00, 0.67, 0.46)],
            "rx": 0.22, "ry": 0.10,
        },
        "arrow": {
            "kfs": [(0.00, 0.34, 0.40), (0.15, 0.36, 0.40), (0.50, 0.45, 0.40), (0.85, 0.55, 0.40), (1.00, 0.57, 0.40)],
            "angle": 50,
        },
    },
    {
        "id": "S17_P2_TokyoSubway",
        "start": 35.35, "end": 37.98,
        "src": VID / "subway_arriving.mp4", "offset": 2.60,
        "mode": "tall_card", "zoom": (1.00, 1.06),
        "trans_out": "zoom_punch",
    },
    {
        "id": "S18_P2_TokyoStation7000",
        "start": 37.98, "end": 40.25,
        "src": AGL / "tokyo_station_commuters_walk.mp4", "offset": 21.50,
        "mode": "tall_card", "zoom": (1.00, 1.07),
        "trans_out": "push_vert",
        "arrow": {
            "kfs": [(0.00, 0.33, 0.52), (0.15, 0.36, 0.52), (0.48, 0.45, 0.53), (0.82, 0.60, 0.54), (1.00, 0.66, 0.54)],
            "angle": 135,
        },
    },
    {
        "id": "S19_P2_NimoRadiantBridge",
        "start": 40.25, "end": 41.38,
        "src": CAND / "glam_nimo_shirai.mp4", "offset": 82.00,
        "mode": "custom_crop",
        "crop_vf": "crop=iw*0.56:ih*0.88:iw*0.14:ih*0.04,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "zoom": (1.00, 1.05),
        "trans_out": "spin_swirl",  # 360° Spin-Swirl into Pillar 3!
    },

    # --- PILLAR 3: NIGHTLY 40°C OFURO HOT BATH RITUAL (41.38 - 57.12s) ---
    {
        "id": "S20_P3_HinokiBathSteam",
        "start": 41.38, "end": 45.36,
        "src": AGL / "hinoki_wooden_bath_steam.mp4", "offset": 28.00,
        "mode": "tall_card", "zoom": (1.02, 1.08),
        "trans_out": "push_vert",
        "arrow": {
            "kfs": [(0.00, 0.75, 0.56), (0.50, 0.76, 0.56), (1.00, 0.78, 0.56)],
            "angle": 40,
        },
    },
    {
        "id": "S21_P3_ThreeMinShower",
        "start": 45.36, "end": 47.20,
        "src": AGL / "clean_shower_water.mp4", "offset": 2.50,
        "mode": "tall_card", "zoom": (1.02, 1.08),
        "trans_out": "push_vert",
        "arrow": {
            "kfs": [(0.00, 0.53, 0.34), (0.50, 0.54, 0.34), (1.00, 0.57, 0.34)],
            "angle": 20,
        },
    },
    {
        "id": "S22_P3_Ofuro40CSoak",
        "start": 47.20, "end": 50.88,
        "src": AGL / "jp_girl_ofuro_routine.mp4", "offset": 61.50,
        "mode": "tall_card", "zoom": (1.00, 1.07),
        "blur_bar": (0.56, 0.67),
        "trans_out": "whip_horiz",
        "arrow": {
            "delay_s": 1.30,
            "kfs": [(0.00, 0.40, 0.42), (0.50, 0.40, 0.42), (0.85, 0.38, 0.41), (1.00, 0.38, 0.41)],
            "angle": 15,
        },
    },

    # --- 5-SHOT CLIMAX MICRO-MONTAGE (50.88 - 57.12s) ---
    {
        "id": "S23_P3_HotSpringSpout",
        "start": 50.88, "end": 52.75,
        "src": AGL / "onsen_steam_water.mp4", "offset": 14.00,
        "mode": "tall_card", "zoom": (1.02, 1.09),
        "trans_out": "zoom_punch",
        "arrow": {
            "kfs": [(0.00, 0.24, 0.43), (0.50, 0.24, 0.43), (1.00, 0.24, 0.43)],
            "angle": 150,
        },
    },
    {
        "id": "S24_P3_WarmBathHand",
        "start": 52.75, "end": 53.75,
        "src": AGL / "jp_salarywoman_ofuro_shower.mp4", "offset": 48.50,
        "mode": "tall_card", "zoom": (1.04, 1.12),
        "trans_out": "push_vert",
    },
    {
        "id": "S25_P3_DeepSleep",
        "start": 53.75, "end": 54.88,
        "src": AGL / "asian_woman_deep_sleep.mp4", "offset": 1.20,
        "mode": "tall_card", "zoom": (1.02, 1.10),
        "trans_out": "zoom_punch",
    },
    {
        "id": "S26_P3_PostBathGlassSkin",
        "start": 54.88, "end": 55.95,
        "src": AGL / "jp_girl_ofuro_routine.mp4", "offset": 23.80,
        "mode": "tall_card", "zoom": (1.04, 1.12),
        "blur_bar": (0.58, 0.70),
        "trans_out": "zoom_punch",
    },
    {
        "id": "S27_P3_ShiraishiRealSmile",
        "start": 55.95, "end": 57.12,
        "src": AGL / "real_shiraishi_lookbook.mp4", "offset": 45.35,
        "mode": "custom_crop",
        "crop_vf": "crop=iw*0.52:ih*0.94:iw*0.42:ih*0.03,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "zoom": (1.02, 1.08),
        "trans_out": "zoom_punch",
    },

    # --- DOUBLE-LOCK INFINITE LOOP BRIDGE (57.12 - 57.786s -> Seamless Same-Take into S01 @5.32s!) ---
    {
        "id": "S28_Loop_UmiMatchShot01",
        "start": 57.12, "end": DURATION,
        "src": AGL / "cand_shinonome_umi.mp4", "offset": 4.65,
        "mode": "custom_crop", "crop_vf": UMI_CROP,
        "zoom": (1.00, 1.00),
        "arrow": {
            "kfs": [(0.00, 0.38, 0.34), (1.00, 0.38, 0.33)],
            "angle": 12,
        },
    },
]


@lru_cache(None)
def get_font(path_str: str, size: int):
    return ImageFont.truetype(path_str, max(14, int(size)))


def eval_kfs(kfs: list, prog: float, cur_z: float) -> tuple[int, int]:
    prog = max(0.0, min(1.0, prog))
    if len(kfs) == 1 or prog <= kfs[0][0]:
        ux, uy = kfs[0][1], kfs[0][2]
    elif prog >= kfs[-1][0]:
        ux, uy = kfs[-1][1], kfs[-1][2]
    else:
        ux, uy = kfs[-1][1], kfs[-1][2]
        for i in range(len(kfs) - 1):
            f0, x0, y0 = kfs[i]
            f1, x1, y1 = kfs[i + 1]
            if f0 <= prog <= f1:
                alpha = (prog - f0) / max(1e-6, f1 - f0)
                ux = x0 + (x1 - x0) * alpha
                uy = y0 + (y1 - y0) * alpha
                break
    sx = int(round(W * (0.5 + (ux - 0.5) * cur_z)))
    sy = int(round(H * (0.5 + (uy - 0.5) * cur_z)))
    return sx, sy


def prepare_60fps_clips():
    PREP_DIR.mkdir(parents=True, exist_ok=True)
    for idx, s in enumerate(SHOTS):
        out_mp4 = PREP_DIR / f"shot_{idx+1:02d}_{s['id']}.mp4"
        s["prep_path"] = out_mp4
        if out_mp4.exists() and out_mp4.stat().st_size > 20_000:
            continue
        dur = (s["end"] - s["start"]) + (0.08 if idx == len(SHOTS) - 1 else 0.30)
        if s["mode"] == "tall_card":
            vf = (
                f"split=2[bg][fg];"
                f"[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=35,eq=brightness=-0.08[bg2];"
                f"[fg]crop=ih*1.12:ih:(iw-ih*1.12)/2:0,scale=1080:964[fg2];"
                f"[bg2][fg2]overlay=(W-w)/2:390,fps={FPS},format=yuv420p"
            )
            cmd = [
                "ffmpeg", "-y", "-ss", f"{s['offset']:.2f}", "-i", str(s["src"]),
                "-t", f"{dur:.2f}", "-filter_complex", vf,
                "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", str(out_mp4),
            ]
        elif s["mode"] == "custom_crop":
            vf = f"{s['crop_vf']},fps={FPS},format=yuv420p"
            cmd = [
                "ffmpeg", "-y", "-ss", f"{s['offset']:.2f}", "-i", str(s["src"]),
                "-t", f"{dur:.2f}", "-vf", vf,
                "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", str(out_mp4),
            ]
        else:
            vf = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps={FPS},format=yuv420p"
            cmd = [
                "ffmpeg", "-y", "-ss", f"{s['offset']:.2f}", "-i", str(s["src"]),
                "-t", f"{dur:.2f}", "-vf", vf,
                "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", str(out_mp4),
            ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[Prep 60fps v4] {idx+1:02d}/{len(SHOTS)}: {s['id']} ({dur:.2f}s)")


# ==============================================================================
# 4-MODE MOTION-TILE TRANSITION ENGINE
# ==============================================================================
def build_mirror_tile_3x3(small_rgb: Image.Image) -> Image.Image:
    sw, sh = small_rgb.size
    flip_x = small_rgb.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    flip_y = small_rgb.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    flip_xy = flip_x.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    tile = Image.new("RGB", (sw * 3, sh * 3))
    rows = [
        (flip_xy, flip_y, flip_xy),
        (flip_x,  small_rgb, flip_x),
        (flip_xy, flip_y, flip_xy),
    ]
    for r_i, row in enumerate(rows):
        for c_i, im in enumerate(row):
            tile.paste(im, (c_i * sw, r_i * sh))
    return tile


def blend_images(imgs: list[Image.Image]) -> Image.Image:
    acc = imgs[0]
    for k in range(1, len(imgs)):
        acc = Image.blend(acc, imgs[k], 1.0 / (k + 1))
    return acc


def apply_spin_swirl(rgb_img: Image.Image, u: float) -> Image.Image:
    hw, hh = 540, 960
    small = rgb_img.resize((hw, hh), Image.Resampling.BILINEAR)
    tile = build_mirror_tile_3x3(small)
    cx, cy = hw * 1.5, hh * 1.5

    if u < 0.5:
        p = max(0.0, min(1.0, u * 2.0))
        ease = p ** 2.2
        scale = 1.0 - 0.30 * ease
        base_deg = -150.0 * ease
        blur_span = 26.0 * (p ** 1.4)
    else:
        q = max(0.0, min(1.0, (1.0 - u) * 2.0))
        ease = q ** 2.2
        scale = 1.0 - 0.30 * ease
        base_deg = +150.0 * ease
        blur_span = 26.0 * (q ** 1.4)

    crop_w = int(round(hw / max(0.45, scale)))
    crop_h = int(round(hh / max(0.45, scale)))
    x0 = int(round(cx - crop_w / 2.0))
    y0 = int(round(cy - crop_h / 2.0))

    samples = []
    for tap in (-1.0, -0.5, 0.0, 0.5, 1.0):
        ang = base_deg + tap * blur_span
        rot = tile.rotate(ang, resample=Image.Resampling.BILINEAR, center=(cx, cy))
        sub = rot.crop((x0, y0, x0 + crop_w, y0 + crop_h)).resize((hw, hh), Image.Resampling.BILINEAR)
        samples.append(sub)
    return blend_images(samples).resize((W, H), Image.Resampling.BILINEAR)


def apply_whip_horiz(rgb_img: Image.Image, u: float) -> Image.Image:
    hw, hh = 540, 960
    small = rgb_img.resize((hw, hh), Image.Resampling.BILINEAR)
    tile = build_mirror_tile_3x3(small)
    cx, cy = hw * 1.5, hh * 1.5

    if u < 0.5:
        p = max(0.0, min(1.0, u * 2.0))
        scale = 1.0 - 0.44 * math.sin(math.pi * 0.5 * p)
        dx = hw * 1.18 * (p ** 2.5)
        streak = hw * 0.24 * (p ** 1.5)
    else:
        q = max(0.0, min(1.0, (1.0 - u) * 2.0))
        scale = 1.0 - 0.44 * math.sin(math.pi * 0.5 * q)
        dx = -hw * 1.18 * (q ** 2.5)
        streak = hw * 0.24 * (q ** 1.5)

    crop_w = int(round(hw / max(0.45, scale)))
    crop_h = int(round(hh / max(0.45, scale)))

    samples = []
    for tap in (-1.0, -0.66, -0.33, 0.0, 0.33, 0.66, 1.0):
        cur_cx = cx + dx + tap * streak
        x0 = max(0, min(tile.width - crop_w, int(round(cur_cx - crop_w / 2.0))))
        y0 = max(0, min(tile.height - crop_h, int(round(cy - crop_h / 2.0))))
        sub = tile.crop((x0, y0, x0 + crop_w, y0 + crop_h)).resize((hw, hh), Image.Resampling.BILINEAR)
        samples.append(sub)
    return blend_images(samples).resize((W, H), Image.Resampling.BILINEAR)


def apply_push_vert(out_rgb: Image.Image, in_rgb: Image.Image, u: float) -> Image.Image:
    hw, hh = 540, 960
    s_out = out_rgb.resize((hw, hh), Image.Resampling.BILINEAR)
    s_in = in_rgb.resize((hw, hh), Image.Resampling.BILINEAR)

    tall = Image.new("RGB", (hw, hh * 4))
    tall.paste(s_out.transpose(Image.Transpose.FLIP_TOP_BOTTOM), (0, 0))
    tall.paste(s_out, (0, hh))
    tall.paste(s_in, (0, hh * 2))
    tall.paste(s_in.transpose(Image.Transpose.FLIP_TOP_BOTTOM), (0, hh * 3))

    ease = u * u * (3.0 - 2.0 * u)
    base_y = hh + ease * hh
    streak = hh * 0.08 * math.sin(math.pi * max(0.0, min(1.0, u)))

    samples = []
    for tap in (-1.0, -0.5, 0.0, 0.5, 1.0):
        y0 = max(0, min(hh * 3, int(round(base_y + tap * streak))))
        samples.append(tall.crop((0, y0, hw, y0 + hh)))
    return blend_images(samples).resize((W, H), Image.Resampling.BILINEAR)


def apply_zoom_punch(rgb_img: Image.Image, u: float) -> Image.Image:
    hw, hh = 540, 960
    small = rgb_img.resize((hw, hh), Image.Resampling.BILINEAR)
    tile = build_mirror_tile_3x3(small)
    cx, cy = hw * 1.5, hh * 1.5

    if u < 0.5:
        p = max(0.0, min(1.0, u * 2.0))
        base_scale = 1.0 + 0.42 * (p ** 2.2)
        span = 0.10 * p
    else:
        q = max(0.0, min(1.0, (1.0 - u) * 2.0))
        base_scale = 1.0 - 0.28 * (q ** 2.2)
        span = 0.08 * q

    samples = []
    for tap in (-1.0, -0.33, 0.33, 1.0):
        sc = max(0.50, base_scale + tap * span)
        cw = int(round(hw / sc))
        ch = int(round(hh / sc))
        x0 = int(round(cx - cw / 2.0))
        y0 = int(round(cy - ch / 2.0))
        samples.append(tile.crop((x0, y0, x0 + cw, y0 + ch)).resize((hw, hh), Image.Resampling.BILINEAR))
    return blend_images(samples).resize((W, H), Image.Resampling.BILINEAR)


# ==============================================================================
# FOREGROUND HUD, ARROWS, EMOTES & CAPTIONS (ZERO WATERMARK!)
# ==============================================================================
def draw_arrow_tip_at(canvas: Image.Image, tx: int, ty: int, angle_deg: float, t: float = 0.0, scale: float = 1.0):
    rad = math.radians(angle_deg)
    ux, uy = math.cos(rad), math.sin(rad)
    px, py = -uy, ux
    gap = (6.0 + 4.5 * (0.5 + 0.5 * math.sin(t * 13.0))) * scale

    d_tip = gap
    d_neck = gap + 64.0 * scale
    d_tail = gap + 142.0 * scale
    w_head = 46.0 * scale
    w_shaft = 19.0 * scale

    def pt(d_back: float, w_perp: float) -> tuple[float, float]:
        return (tx - d_back * ux + w_perp * px, ty - d_back * uy + w_perp * py)

    pts = [
        pt(d_tip, 0.0),
        pt(d_neck, -w_head),
        pt(d_neck, -w_shaft),
        pt(d_tail, -w_shaft),
        pt(d_tail, +w_shaft),
        pt(d_neck, +w_shaft),
        pt(d_neck, +w_head),
    ]

    draw = ImageDraw.Draw(canvas)
    shadow_pts = [(x + 5, y + 6) for x, y in pts]
    draw.polygon(shadow_pts, fill=(0, 0, 0, 185))
    draw.polygon(pts, fill=(255, 18, 18, 255), outline=(255, 255, 255, 255), width=max(4, int(round(8 * scale))))


def draw_emote(canvas: Image.Image, emote_cfg: dict, prog: float, cur_z: float, t: float, local_t: float):
    if local_t < emote_cfg.get("delay_s", 0.0):
        return
    d = ImageDraw.Draw(canvas)
    kind = emote_cfg["kind"]
    cx, cy = eval_kfs(emote_cfg["kfs"], prog, cur_z)
    pulse = 1.0 + 0.08 * math.sin(t * 16.0)
    if kind == "anger_vein":
        r = int(round(38 * pulse))
        for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            p1 = (cx + dx * r, cy + dy * 10)
            p2 = (cx + dx * 10, cy + dy * 10)
            p3 = (cx + dx * 10, cy + dy * r)
            d.line([p1, p2, p3], fill=(255, 255, 255, 255), width=14, joint="curve")
            d.line([p1, p2, p3], fill=(255, 22, 22, 255), width=8, joint="curve")
    elif kind == "shout_bang":
        bw, bh = int(round(85 * pulse)), int(round(52 * pulse))
        d.rounded_rectangle((cx - bw, cy - bh, cx + bw, cy + bh), radius=26, fill=(255, 255, 255, 245), outline=(0, 0, 0, 255), width=6)
        f = get_font(str(FONT_EN_BLACK), int(round(64 * pulse)))
        d.text((cx, cy), "!!!", font=f, fill=(255, 20, 20, 255), anchor="mm")


@lru_cache(None)
def get_skull_sticker(size_px: int = 106) -> Image.Image:
    emoji_font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 160)
    raw = Image.new("RGBA", (240, 240), (0, 0, 0, 0))
    rd = ImageDraw.Draw(raw)
    rd.text((24, 24), "💀", font=emoji_font, embedded_color=True)
    bbox = raw.getbbox() or (24, 24, 184, 184)
    glyph = raw.crop(bbox).resize((size_px, size_px), Image.Resampling.LANCZOS)

    pad = 18
    out = Image.new("RGBA", (size_px + pad * 2, size_px + pad * 2), (0, 0, 0, 0))
    alpha = glyph.split()[3]
    stroke_mask = alpha.filter(ImageFilter.MaxFilter(17))
    shadow_mask = stroke_mask.filter(ImageFilter.GaussianBlur(radius=4))

    shadow_img = Image.new("RGBA", glyph.size, (0, 0, 0, 220))
    stroke_img = Image.new("RGBA", glyph.size, (0, 0, 0, 255))
    out.paste(shadow_img, (pad + 6, pad + 8), shadow_mask)
    out.paste(stroke_img, (pad, pad), stroke_mask)
    out.paste(glyph, (pad, pad), glyph)
    return out


def draw_thumbnail_banner(canvas: Image.Image):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    f1 = get_font(str(FONT_EN_BLACK), 94)
    f2 = get_font(str(FONT_EN_BLACK), 112)

    # Line 1: Pure White setup ("This Woman Is")
    t1 = "This Woman Is"
    y1 = 1305
    d.text((W // 2 + 6, y1 + 8), t1, font=f1, fill=(0, 0, 0, 235), anchor="mm", stroke_width=18, stroke_fill=(0, 0, 0, 235))
    d.text((W // 2, y1), t1, font=f1, fill=(255, 255, 255, 255), anchor="mm", stroke_width=15, stroke_fill=(0, 0, 0, 255))

    # Line 2: Coral Red ("Over ") + Canary Yellow ("45?!") + Apple Color Emoji 💀
    t2_a = "Over "
    t2_b = "45?!"
    y2 = 1440
    w_a = d.textlength(t2_a, font=f2)
    w_b = d.textlength(t2_b, font=f2)
    skull = get_skull_sticker(108)
    gap_skull = 14
    total_w = w_a + w_b + gap_skull + 108
    start_x = (W - total_w) / 2.0

    # Draw "Over "
    xa = start_x + w_a / 2.0
    d.text((xa + 6, y2 + 8), t2_a, font=f2, fill=(0, 0, 0, 235), anchor="mm", stroke_width=20, stroke_fill=(0, 0, 0, 235))
    d.text((xa, y2), t2_a, font=f2, fill=(255, 77, 77, 255), anchor="mm", stroke_width=16, stroke_fill=(0, 0, 0, 255))

    # Draw "45?!"
    xb = start_x + w_a + w_b / 2.0
    d.text((xb + 6, y2 + 8), t2_b, font=f2, fill=(0, 0, 0, 235), anchor="mm", stroke_width=20, stroke_fill=(0, 0, 0, 235))
    d.text((xb, y2), t2_b, font=f2, fill=(255, 230, 0, 255), anchor="mm", stroke_width=16, stroke_fill=(0, 0, 0, 255))

    # Composite 💀 sticker
    sx = int(round(start_x + w_a + w_b + gap_skull - 18))
    sy = int(round(y2 - skull.height / 2.0 - 4))
    overlay.alpha_composite(skull, (sx, sy))

    canvas.alpha_composite(overlay)
    draw_arrow_tip_at(canvas, int(W * 0.38), int(H * 0.33), 12, t=0.0, scale=1.18)


def render_caption(canvas: Image.Image, t: float):
    active_w = None
    for w in WORDS:
        if w["start"] <= t < w["end"]:
            active_w = w
            break
    if not active_w:
        return

    local_dt = max(0.0, t - active_w["start"])
    if local_dt < 0.017:
        scale = 0.82
    elif local_dt < 0.034:
        scale = 1.05
    else:
        scale = 1.00

    base_px = 45 if active_w["shrink"] else 90
    font_px = int(round(base_px * scale))
    font = get_font(str(FONT_EN_BLACK), font_px)

    fill_col = (255, 230, 0, 255) if active_w["yellow"] else (255, 255, 255, 255)
    cx, cy = W // 2, 1155

    d = ImageDraw.Draw(canvas)
    txt = active_w["text"]
    d.text((cx + 6, cy + 7), txt, font=font, fill=(0, 0, 0, 225), anchor="mm", stroke_width=14, stroke_fill=(0, 0, 0, 225))
    d.text((cx, cy), txt, font=font, fill=fill_col, anchor="mm", stroke_width=12, stroke_fill=(0, 0, 0, 255))

    for k_start, k_end, k_txt in KANJI_GLOSSARIES:
        if k_start <= t <= k_end:
            kf = get_font(str(FONT_JP_BOLD), 50)
            d.text((cx + 4, 1252 + 4), k_txt, font=kf, fill=(0, 0, 0, 215), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0, 215))
            d.text((cx, 1252), k_txt, font=kf, fill=(255, 255, 255, 255), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0, 255))
            break


@lru_cache(None)
def get_feathered_blur_mask(by0: int, by1: int) -> Image.Image:
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.rectangle((0, by0, W, by1), fill=255)
    return mask.filter(ImageFilter.GaussianBlur(radius=20))


def prepare_broll_rgb(base_rgb: Image.Image, shot: dict, local_t: float) -> tuple[Image.Image, float, float]:
    dur = max(0.001, shot["end"] - shot["start"])
    prog = max(0.0, min(1.0, local_t / dur))
    z0, z1 = shot.get("zoom", (1.0, 1.04))
    cur_z = z0 + (z1 - z0) * prog

    if "blur_bar" in shot:
        by0_frac, by1_frac = shot["blur_bar"]
        by0, by1 = int(H * by0_frac), int(H * by1_frac)
        pad = 64
        ry0, ry1 = max(0, by0 - pad), min(H, by1 + pad)
        band = base_rgb.crop((0, ry0, W, ry1)).filter(ImageFilter.GaussianBlur(radius=34))
        if shot["id"].startswith("S03_"):
            dark = Image.new("RGB", band.size, (26, 30, 52))
            band = Image.blend(band, dark, 0.55)
        full_blur = base_rgb.copy()
        full_blur.paste(band, (0, ry0))
        mask = get_feathered_blur_mask(by0, by1)
        base_rgb = Image.composite(full_blur, base_rgb, mask)

    if abs(cur_z - 1.0) > 0.003:
        zw, zh = int(round(W * cur_z)), int(round(H * cur_z))
        scaled = base_rgb.resize((zw, zh), Image.Resampling.BILINEAR)
        x0 = (zw - W) // 2
        y0 = (zh - H) // 2
        base_rgb = scaled.crop((x0, y0, x0 + W, y0 + H))

    return base_rgb, prog, cur_z


def overlay_hud(broll_rgb: Image.Image, shot: dict, t: float, local_t: float, prog: float, cur_z: float, is_thumb: bool = False, in_transition: bool = False) -> Image.Image:
    canvas = broll_rgb.convert("RGBA")

    if is_thumb or t < 0.10:
        draw_thumbnail_banner(canvas)
        return canvas

    # Zero watermarks anywhere per user instruction!

    if not in_transition:
        if "red_circle" in shot:
            rc = shot["red_circle"]
            cx, cy = eval_kfs(rc["kfs"], prog, cur_z)
            rx = int(round(rc["rx"] * W * cur_z))
            ry = int(round(rc["ry"] * H * cur_z))
            d = ImageDraw.Draw(canvas)
            d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=(255, 255, 255, 255), width=14)
            d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=(255, 20, 20, 255), width=8)

        if "arrow" in shot:
            arr = shot["arrow"]
            delay_s = arr.get("delay_s", 0.0)
            if local_t >= delay_s:
                age = local_t - delay_s
                pop_sc = 0.80 + 0.25 * min(1.0, age / 0.06) if age < 0.06 else (1.05 - 0.05 * min(1.0, (age - 0.06) / 0.05))
                tx, ty = eval_kfs(arr["kfs"], prog, cur_z)
                draw_arrow_tip_at(canvas, tx, ty, arr["angle"], t=t, scale=pop_sc)

        if "emote" in shot:
            draw_emote(canvas, shot["emote"], prog, cur_z, t, local_t)

    render_caption(canvas, t)
    return canvas


class ShotClipReader:
    def __init__(self, prep_path: Path):
        self.prep_path = prep_path
        self.proc = subprocess.Popen(
            ["ffmpeg", "-i", str(prep_path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )
        self.frames = {}
        self.next_idx = 0
        self.closed = False
        self.last_img = Image.new("RGB", (W, H), (14, 16, 22))

    def get_frame(self, local_f_idx: int) -> Image.Image:
        local_f_idx = max(0, local_f_idx)
        while not self.closed and self.next_idx <= local_f_idx:
            raw = self.proc.stdout.read(W * H * 3)
            if len(raw) < W * H * 3:
                self.close()
                break
            im = Image.frombytes("RGB", (W, H), raw)
            self.frames[self.next_idx] = im
            self.last_img = im
            old_k = self.next_idx - 24
            if old_k in self.frames:
                del self.frames[old_k]
            self.next_idx += 1
        return self.frames.get(local_f_idx, self.last_img)

    def close(self):
        if not self.closed:
            self.closed = True
            if self.proc.stdout:
                self.proc.stdout.close()
            self.proc.wait()


def render_video_and_assets():
    prepare_60fps_clips()
    audio_wav = WORK_DIR / "mastered_audio.wav"

    final_mp4 = OUT_DIR / "Why_Japanese_Women_Look_25_Short.mp4"
    thumb_jpg = OUT_DIR / "Why_Japanese_Women_Look_25_Short_Thumb.jpg"
    contact_jpg = OUT_DIR / "Why_Japanese_Women_Look_25_Contact_Sheet.jpg"
    track_audit_jpg = OUT_DIR / "Why_Japanese_Women_Look_25_Arrow_Tracking_Audit.jpg"
    trans_audit_jpg = OUT_DIR / "Why_Japanese_Women_Look_25_Transitions_Audit.jpg"

    writer = subprocess.Popen(
        [
            "ffmpeg", "-y",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
            "-i", "-",
            "-i", str(audio_wav),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            "-shortest", str(final_mp4),
        ],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    active_readers: dict[int, ShotClipReader] = {}

    def fetch_shot_broll(idx: int, t_global: float) -> tuple[Image.Image, float, float]:
        if idx not in active_readers:
            active_readers[idx] = ShotClipReader(SHOTS[idx]["prep_path"])
        sh = SHOTS[idx]
        loc_t = max(0.0, t_global - sh["start"])
        loc_f = int(round(loc_t * FPS))
        raw_im = active_readers[idx].get_frame(loc_f)
        return prepare_broll_rgb(raw_im, sh, loc_t)

    shot_mid_samples = {}
    shot_track_strips = {i: {} for i in range(len(SHOTS)) if ("arrow" in SHOTS[i] or "emote" in SHOTS[i])}

    audit_boundaries = [
        (1,  "Spin-Swirl (S02->S03 @4.82s)"),
        (3,  "Vert-Push  (S04->S05 @10.28s)"),
        (5,  "Whip-Horiz (S06->S07 @13.78s)"),
        (10, "Spin-Swirl (S11->S12 @23.56s)"),
        (12, "Whip-Horiz (S13->S14 @29.96s)"),
        (18, "Spin-Swirl (S19->S20 @41.38s)"),
        (0,  "Zoom-Punch (S01->S02 @2.75s)"),
    ]
    trans_audit_samples = {b_i: [] for b_i, _ in audit_boundaries}

    for f_idx in range(TOTAL_FRAMES):
        t = f_idx / FPS
        s_idx = len(SHOTS) - 1
        for i, s in enumerate(SHOTS):
            if s["start"] <= t < s["end"]:
                s_idx = i
                break

        for old_i in list(active_readers.keys()):
            if old_i < s_idx - 1:
                active_readers[old_i].close()
                del active_readers[old_i]

        shot = SHOTS[s_idx]
        loc_t = max(0.0, t - shot["start"])
        broll_cur, prog, cur_z = fetch_shot_broll(s_idx, t)

        in_trans = False
        out_kind = shot.get("trans_out")
        if out_kind and s_idx + 1 < len(SHOTS):
            hd = TRANS_HALF_DUR[out_kind]
            t_cut = shot["end"]
            if t >= t_cut - hd:
                in_trans = True
                u = 0.5 * (t - (t_cut - hd)) / hd
                if out_kind == "spin_swirl":
                    broll_cur = apply_spin_swirl(broll_cur, u)
                elif out_kind == "whip_horiz":
                    broll_cur = apply_whip_horiz(broll_cur, u)
                elif out_kind == "zoom_punch":
                    broll_cur = apply_zoom_punch(broll_cur, u)
                elif out_kind == "push_vert":
                    in_broll, _, _ = fetch_shot_broll(s_idx + 1, t)
                    broll_cur = apply_push_vert(broll_cur, in_broll, u)

        if not in_trans and s_idx > 0:
            prev_kind = SHOTS[s_idx - 1].get("trans_out")
            if prev_kind:
                hd = TRANS_HALF_DUR[prev_kind]
                t_cut = shot["start"]
                if t <= t_cut + hd:
                    in_trans = True
                    u = 0.5 + 0.5 * (t - t_cut) / hd
                    if prev_kind == "spin_swirl":
                        broll_cur = apply_spin_swirl(broll_cur, u)
                    elif prev_kind == "whip_horiz":
                        broll_cur = apply_whip_horiz(broll_cur, u)
                    elif prev_kind == "zoom_punch":
                        broll_cur = apply_zoom_punch(broll_cur, u)
                    elif prev_kind == "push_vert":
                        out_broll, _, _ = fetch_shot_broll(s_idx - 1, t)
                        broll_cur = apply_push_vert(out_broll, broll_cur, u)

        comp = overlay_hud(broll_cur, shot, t, loc_t, prog, cur_z, is_thumb=(f_idx == 0), in_transition=in_trans).convert("RGB")

        if f_idx == 0:
            comp.save(thumb_jpg, quality=95)
        if s_idx not in shot_mid_samples and prog >= 0.52 and not in_trans:
            shot_mid_samples[s_idx] = (t, comp.copy())

        if s_idx in shot_track_strips and not in_trans:
            for b_idx, target_p in enumerate([0.16, 0.42, 0.66, 0.86]):
                if b_idx not in shot_track_strips[s_idx] and prog >= target_p:
                    shot_track_strips[s_idx][b_idx] = (t, comp.copy())

        for b_i, _ in audit_boundaries:
            t_c = SHOTS[b_i]["end"]
            hd = TRANS_HALF_DUR[SHOTS[b_i]["trans_out"]]
            if (t_c - hd - 0.03) <= t <= (t_c + hd + 0.03) and (f_idx % 2 == 0) and len(trans_audit_samples[b_i]) < 10:
                trans_audit_samples[b_i].append((t, f_idx, comp.copy()))

        writer.stdin.write(comp.tobytes())
        if f_idx % 600 == 0 or f_idx == TOTAL_FRAMES - 1:
            print(f"[Render 60fps v4 1.0x] Frame {f_idx+1}/{TOTAL_FRAMES} ({t:.2f}s / {DURATION:.2f}s)", flush=True)

    for rd in active_readers.values():
        rd.close()
    writer.stdin.close()
    writer.wait()

    # 1. Save 28-Shot Contact Sheet
    cols = 4
    rows = math.ceil(len(SHOTS) / cols)
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
        tr_lbl = SHOTS[idx].get("trans_out", "loop")
        sd.text((gx + 6, gy + 6), f"S{idx+1:02d} @{st_t:.1f}s -> {tr_lbl}", fill=(255, 230, 0))
    sheet.save(contact_jpg, quality=92)

    # 2. Save 4-Point Arrow Tracking Audit
    tracked_ids = sorted(shot_track_strips.keys())
    audit = Image.new("RGB", (4 * tw, len(tracked_ids) * th), (12, 14, 18))
    ad = ImageDraw.Draw(audit)
    for r_i, s_idx in enumerate(tracked_ids):
        for c_i in range(4):
            if c_i not in shot_track_strips[s_idx]:
                continue
            st_t, img = shot_track_strips[s_idx][c_i]
            tile = img.resize((tw - 4, th - 4), Image.Resampling.LANCZOS)
            gx, gy = c_i * tw + 2, r_i * th + 2
            audit.paste(tile, (gx, gy))
            ad.rectangle((gx, gy, gx + 195, gy + 26), fill=(0, 0, 0))
            ad.text((gx + 5, gy + 5), f"S{s_idx+1:02d} #{c_i+1} @{st_t:.2f}s", fill=(0, 255, 255))
    audit.save(track_audit_jpg, quality=90)

    # 3. Save Frame-by-Frame Inter-Source Transition Proof Sheet
    t_cols = 10
    tw2, th2 = 180, 320
    tr_sheet = Image.new("RGB", (t_cols * tw2, len(audit_boundaries) * th2), (12, 14, 18))
    td = ImageDraw.Draw(tr_sheet)
    for r_i, (b_i, label) in enumerate(audit_boundaries):
        samps = trans_audit_samples[b_i]
        for c_i, (st_t, fn, img) in enumerate(samps[:t_cols]):
            tile = img.resize((tw2 - 2, th2 - 2), Image.Resampling.LANCZOS)
            gx, gy = c_i * tw2 + 1, r_i * th2 + 1
            tr_sheet.paste(tile, (gx, gy))
            td.rectangle((gx, gy, gx + 176, gy + 36), fill=(0, 0, 0))
            td.text((gx + 4, gy + 3), f"{label[:22]}", fill=(255, 110, 110))
            td.text((gx + 4, gy + 19), f"f{fn:04d} ({st_t:.2f}s)", fill=(255, 235, 0))
    tr_sheet.save(trans_audit_jpg, quality=92)

    print(
        f"[Complete] Video: {final_mp4} | Thumb: {thumb_jpg} | "
        f"Contact: {contact_jpg} | Tracking Audit: {track_audit_jpg}"
    )


if __name__ == "__main__":
    render_video_and_assets()
