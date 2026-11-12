#!/usr/bin/env python3
import concurrent.futures
import subprocess
from pathlib import Path

ROOT = Path("/Users/digiex/Documents/deepseek-harness/default-workspace/jp_refusals_video")
OUT = ROOT / "assets/ageless_jp_clips"
OUT.mkdir(parents=True, exist_ok=True)
YTDLP = str(ROOT / ".venv/bin/yt-dlp")

JOBS = [
    # 1. Hardcore Japanese UV Sun Armor (UV visor, face cover, long arm gloves, black Higasa parasol in 35C heat)
    ("nLLzStTrOQ4", "*00:00:00-00:00:16", "uv_visor_demo.mp4"),
    ("hFBVUkjX5Oc", "*00:00:02-00:01:15", "uv_visor_outdoor.mp4"),
    ("WiI6WYnUpfs", "*00:00:00-00:01:45", "tokyo_heatwave_parasols.mp4"),
    ("t7Y90_5UCXk", "*00:00:00-00:01:40", "sunbarrier_full_armor_a.mp4"),
    ("t7Y90_5UCXk", "*00:03:30-00:05:30", "sunbarrier_full_armor_b.mp4"),
    ("hvrZx1VtSrs", "*00:00:00-00:01:30", "hardcore_uv_girl_intro.mp4"),
    ("myIYQXSiIKQ", "*00:00:00-00:01:30", "complete_uv_protection.mp4"),
    ("t1zk47-NoPA", "*00:01:00-00:03:20", "omotesando_summer_parasols.mp4"),
    # 2. Ageless 43yo Japanese beauty ("Bihaku" porcelain skin)
    ("6GL3b4NYkmE", "*00:00:00-00:01:20", "bimajo_43yo_skin.mp4"),
    # 3. Pillar 2: Sugary soda contrast + Unsweetened Green Tea + Miso Soup + Sticky Natto
    ("J8UYEE_RUcI", "*00:00:00-00:00:17", "soda_pour_sugar.mp4"),
    ("Qbfu1jCB1vU", "*00:00:00-00:00:12", "green_tea_pour.mp4"),
    ("aPqtmM6n5g0", "*00:00:00-00:00:25", "matcha_whisk_asmr.mp4"),
    ("-sWlcDNctZE", "*00:00:25-00:01:45", "natto_stir_4k.mp4"),
    ("QURiHxJSLcs", "*00:04:00-00:06:30", "jp_breakfast_miso_teishoku.mp4"),
    ("e5adE24JfzY", "*00:06:00-00:08:20", "miso_soup_ladle.mp4"),
    # 4. Pillar 3: 3-minute Shower contrast + Nightly 40C Ofuro Hot Bath + Steam + Deep Sleep
    ("EY-N9UOKLPQ", "*00:00:00-00:00:11", "shower_spray_4k.mp4"),
    ("9iTwzZedi_Q", "*00:00:00-00:00:15", "shower_turn_on.mp4"),
    ("IJnbSQIerNI", "*00:00:15-00:01:35", "hinoki_wooden_bath_steam.mp4"),
    ("z6OnyS9zAjs", "*00:00:10-00:01:30", "onsen_steam_water.mp4"),
    ("3y2XSYfw9pM", "*00:00:00-00:02:15", "jp_girl_ofuro_routine.mp4"),
    ("tJS_EFRyPts", "*00:05:30-00:08:15", "jp_night_bath_skincare.mp4"),
    ("fvQqgu5hjgE", "*00:00:00-00:00:31", "asian_woman_deep_sleep.mp4"),
]


def fetch(job):
    vid, section, out_name = job
    dest = OUT / out_name
    if dest.exists() and dest.stat().st_size > 250_000:
        return f"SKIP {out_name} ({dest.stat().st_size // 1024} KB)"
    cmd = [
        YTDLP,
        f"https://www.youtube.com/watch?v={vid}",
        "-f", "bestvideo[height<=1080][ext=mp4]/best[height<=1080][ext=mp4]/best[height<=1080]",
        "--download-sections", section,
        "--no-playlist",
        "-o", str(dest),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if dest.exists() and dest.stat().st_size > 120_000:
        return f"OK   {out_name} ({dest.stat().st_size // 1024} KB)"
    return f"ERR  {out_name}: {r.stderr[-240:]}"


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        for res in ex.map(fetch, JOBS):
            print(res, flush=True)
