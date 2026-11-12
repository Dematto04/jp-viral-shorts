#!/usr/bin/env python3
"""
Prepares all 28 60fps 1080x1920 clips in output/ageless_jp_work/prep_clips_60fps_v3/
and generates coordinate-grid calibration sheets (calib_grid_part1.jpg, calib_grid_part2.jpg)
at prog = 0.15, 0.50, 0.85 so every Red Arrow & Red Circle coordinate is measured with <0.01 precision!
"""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
WORK_DIR = ROOT / "output/ageless_jp_work"
PREP_DIR = WORK_DIR / "prep_clips_60fps_v3"
AGL = ROOT / "assets/ageless_jp_clips"
CAND = ROOT / "assets/rentaru_candidates"
VID = ROOT / "assets/video"

W, H, FPS = 1080, 1920, 60
DURATION = 50.290

FUKADA_CROP = "crop=iw*0.50:ih*0.92:iw*0.25:ih*0.04,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
TANAKA_CROP = "crop=iw*0.50:ih*0.92:iw*0.24:ih*0.04,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"

SHOTS_BASE = [
    ("S01_Hook_FukadaCandleGlam",    0.00,  2.10, AGL / "glam_fukada_minidress.mp4", 2.45,  "custom_crop", FUKADA_CROP),
    ("S02_Hook_TanakaSilkGown",      2.10,  4.20, AGL / "glam_tanaka_dress.mp4",     44.60, "custom_crop", TANAKA_CROP),
    ("S03_P1_VampireUVArmor",        4.20,  6.95, AGL / "complete_uv_protection.mp4", 3.80, "tall_card", None),
    ("S04_P1_BihakuPorcelain",       6.95,  8.88, AGL / "complete_uv_protection.mp4", 80.20,"tall_card", None),
    ("S05_P1_Tokyo35CParasol",       8.88, 10.50, AGL / "tokyo_heatwave_parasols.mp4",27.60,"custom_crop", "crop=iw*0.72:ih*0.92:iw*0.06:ih*0.04,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"),
    ("S06_P1_CloudyDayUmbrella",    10.50, 11.98, VID / "tokyo_pedestrian.mp4",       5.80, "custom_crop", "crop=iw*0.58:ih*0.95:iw*0.02:ih*0.02,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"),
    ("S07_P1_UVVisorShield",        11.98, 13.02, AGL / "uv_visor_demo.mp4",          3.10, "custom_crop", "crop=iw*0.46:ih*0.80:iw*0.34:ih*0.19,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"),
    ("S08_P1_LongArmGloves",        13.02, 13.92, AGL / "outdoor_uv_armor_walk.mp4", 72.40, "custom_crop", "crop=iw*0.62:ih*0.92:iw*0.34:ih*0.04,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"),
    ("S09_P1_BlackHigasa",          13.92, 15.34, AGL / "sunbarrier_full_armor_b.mp4",21.20,"tall_card", None),
    ("S10_P1_Bimajo80Pct",          15.34, 18.60, AGL / "bimajo_43yo_skin.mp4",      63.80, "tall_card", None),
    ("S11_P1_OmotesandoCrosswalk",  18.60, 20.68, AGL / "omotesando_summer_parasols.mp4", 12.20, "tall_card", None),
    ("S12_P2_RadiantSmile",         20.68, 23.92, AGL / "outdoor_uv_armor_walk.mp4", 32.00, "tall_card", None),
    ("S13_P2_SugarySodaFizz",       23.92, 25.92, AGL / "soda_pour_sugar.mp4",       12.20, "tall_card", None),
    ("S14_P2_GreenTeaPour",         25.92, 27.92, AGL / "green_tea_pour.mp4",         2.10, "tall_card", None),
    ("S15_P2_MisoSoupPot",          27.92, 29.30, AGL / "miso_soup_ladle.mp4",       11.80, "tall_card", None),
    ("S16_P2_StickyNattoWhip",      29.30, 30.78, AGL / "natto_sticky_whip.mp4",     30.50, "tall_card", None),
    ("S17_P2_TokyoSubway",          30.78, 33.05, VID / "subway_arriving.mp4",        2.60, "tall_card", None),
    ("S18_P2_TokyoStation7000",     33.05, 34.85, AGL / "tokyo_station_commuters_walk.mp4", 21.50, "tall_card", None),
    ("S19_P2_NimoRadiantBridge",    34.85, 36.05, CAND / "glam_nimo_shirai.mp4",     82.00, "custom_crop", "crop=iw*0.56:ih*0.88:iw*0.22:ih*0.04,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"),
    ("S20_P3_HinokiBathSteam",      36.05, 39.42, AGL / "hinoki_wooden_bath_steam.mp4", 28.00, "tall_card", None),
    ("S21_P3_ThreeMinShower",       39.42, 41.15, AGL / "clean_shower_water.mp4",     2.50, "tall_card", None),
    ("S22_P3_Ofuro40CSoak",         41.15, 44.30, AGL / "jp_girl_ofuro_routine.mp4", 61.50, "tall_card", None),
    ("S23_P3_HotSpringSpout",       44.30, 45.95, AGL / "onsen_steam_water.mp4",     14.00, "tall_card", None),
    ("S24_P3_WarmBathHand",         45.95, 46.85, AGL / "jp_salarywoman_ofuro_shower.mp4", 48.50, "tall_card", None),
    ("S25_P3_DeepSleep",            46.85, 47.95, AGL / "asian_woman_deep_sleep.mp4", 1.20, "tall_card", None),
    ("S26_P3_PostBathGlassSkin",    47.95, 48.80, AGL / "jp_girl_ofuro_routine.mp4", 23.80, "tall_card", None),
    ("S27_P3_FukadaOvernightSmile", 48.80, 49.72, AGL / "glam_fukada_minidress.mp4", 36.25, "custom_crop", "crop=iw*0.50:ih*0.92:iw*0.26:ih*0.04,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"),
    ("S28_Loop_MatchShot01",        49.72, 50.29, AGL / "glam_fukada_minidress.mp4",  1.88, "custom_crop", FUKADA_CROP),
]


def draw_coord_grid(im: Image.Image, label: str) -> Image.Image:
    out = im.resize((360, 640), Image.Resampling.BILINEAR)
    d = ImageDraw.Draw(out)
    gw, gh = out.size
    for k in range(1, 20):
        frac = k * 0.05
        x = int(round(gw * frac))
        y = int(round(gh * frac))
        is_major = (k % 2 == 0)
        col = (0, 255, 255) if is_major else (90, 140, 140)
        w = 2 if is_major else 1
        d.line([(x, 0), (x, gh)], fill=col, width=w)
        if 0.15 <= frac <= 0.80:
            d.line([(0, y), (gw, y)], fill=col, width=w)
        if is_major:
            d.rectangle((x + 2, 26, x + 28, 40), fill=(0, 0, 0))
            d.text((x + 4, 28), f".{k*5:02d}", fill=(255, 255, 0))
            if 0.20 <= frac <= 0.70:
                d.rectangle((2, y + 2, 28, y + 16), fill=(0, 0, 0))
                d.text((4, y + 3), f".{k*5:02d}", fill=(255, 255, 0))
    d.rectangle((0, 0, gw, 24), fill=(0, 0, 0))
    d.text((6, 5), label, fill=(255, 230, 0))
    return out


def main():
    PREP_DIR.mkdir(parents=True, exist_ok=True)
    prep_paths = []
    for idx, (sid, st, en, src, off, mode, crop_vf) in enumerate(SHOTS_BASE):
        out_mp4 = PREP_DIR / f"shot_{idx+1:02d}_{sid}.mp4"
        prep_paths.append(out_mp4)
        dur = (en - st) + (0.08 if idx in (0, 27) else 0.30)
        if mode == "tall_card":
            vf = (
                f"split=2[bg][fg];"
                f"[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=35,eq=brightness=-0.08[bg2];"
                f"[fg]crop=ih*1.12:ih:(iw-ih*1.12)/2:0,scale=1080:964[fg2];"
                f"[bg2][fg2]overlay=(W-w)/2:390,fps={FPS},format=yuv420p"
            )
            cmd = ["ffmpeg", "-y", "-ss", f"{off:.2f}", "-i", str(src), "-t", f"{dur:.2f}", "-filter_complex", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", str(out_mp4)]
        else:
            vf = f"{crop_vf},fps={FPS},format=yuv420p"
            cmd = ["ffmpeg", "-y", "-ss", f"{off:.2f}", "-i", str(src), "-t", f"{dur:.2f}", "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", str(out_mp4)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[Prep v3] {idx+1:02d}/28 {sid}")

    # Extract 3 calibration frames (prog=0.15, 0.50, 0.85) for the 20 visual/arrow shots
    inspect_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 26]
    half = len(inspect_indices) // 2
    for part_idx, subset in enumerate([inspect_indices[:half], inspect_indices[half:]], start=1):
        sheet = Image.new("RGB", (360 * 3, 640 * len(subset)), (12, 12, 16))
        for r_i, s_i in enumerate(subset):
            sid, st, en, *_ = SHOTS_BASE[s_i]
            sdur = en - st
            p_mp4 = prep_paths[s_i]
            for c_i, p_frac in enumerate([0.15, 0.50, 0.85]):
                lt = sdur * p_frac
                tmp = Path(f"/tmp/cal_{s_i}_{c_i}.jpg")
                subprocess.run(["ffmpeg", "-y", "-ss", f"{lt:.2f}", "-i", str(p_mp4), "-frames:v", "1", str(tmp)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if tmp.exists():
                    im = Image.open(tmp).convert("RGB")
                    grid_im = draw_coord_grid(im, f"S{s_i+1:02d} {sid[4:22]} p={p_frac:.2f}")
                    sheet.paste(grid_im, (c_i * 360, r_i * 640))
        out_jpg = WORK_DIR / f"calib_grid_part{part_idx}.jpg"
        sheet.save(out_jpg, quality=90)
        print("Saved", out_jpg)


if __name__ == "__main__":
    main()
