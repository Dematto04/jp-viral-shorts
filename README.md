# Japanese Viral Shorts Production Engine (`60fps` & `30fps`)

End-to-end Python + FFmpeg + Whisper production studio for high-retention Japanese cultural YouTube Shorts:

1. **48s–60s `60fps` Multi-Pillar Lifestyle Decode / Deep Dive**:
   - Blueprint: [.agents/rules/kurose-viral-shorts-blueprint.md](.agents/rules/kurose-viral-shorts-blueprint.md)
   - Features: `1080x1920 @ 60fps`, `100%` real-camera footage screening, cognitive-dissonance `Frame 0–5` thumbnail with native Apple Color Emoji (`💀`) sticker, 4-mode `3x3` mirror-tile inter-source transitions (`spin_swirl`, `whip_horiz`, `push_vert`, `zoom_punch`), `.05`-grid-calibrated Red Arrows, 2-color `ALL CAPS` single-word captions + Kanji glossaries, `quick_tip` SFX + vocal-pocket BGM (`-14.5 to -16.5 LUFS`, `+17 to +20.5 dB` Mid/Side), and same-take `"That's..." -> Shot 01` loop.
2. **24s–28s `30fps` High-Loop Etiquette / Taboo Short**:
   - Blueprint: [.agents/rules/viral-shorts-editing.md](.agents/rules/viral-shorts-editing.md)

## System Prerequisites (macOS)
- `/usr/bin/python3` with `Pillow` (`PIL`)
- `/opt/homebrew/bin/ffmpeg` & `ffprobe`
- `/opt/homebrew/bin/whisper-cli` (`ggml-large-v3-turbo.bin`)
- `yt-dlp` (for candidate B-roll downloads)

## End-to-End `60fps` Production Workflow
```bash
# 1. Align natural 1.0x ElevenLabs voiceover via Whisper -> words.json, clauses.json, .srt
/usr/bin/python3 scripts/align_ageless_eleven115.py

# 2. Master voiceover + vocal-pocket BGM + clean quick_tip SFX (-15.2 LUFS)
/usr/bin/python3 scripts/master_ageless_audio.py

# 3. (Optional) Generate .05/.10 coordinate calibration grids on 1080x1920 cropped shots
/usr/bin/python3 scripts/calibrate_ageless_shots.py

# 4. Render 60fps MP4 + Thumbnail + Contact Sheet + Arrow & Transition Audit Sheets + QC Report
/usr/bin/python3 scripts/build_ageless_jp_kurose_short.py && bash scripts/qc_ageless_short.sh
```
