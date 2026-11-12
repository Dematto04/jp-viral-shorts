# Viral 60fps Japanese Cultural Shorts Production Blueprint (54s High-Retention Rule)

Apply these scripting, real-footage sourcing, curiosity thumbnail, motion-tile transition, grid-calibrated Red Arrow, typography, audio mastering, loop-engineering, and Python/FFmpeg rendering rules when producing full-minute (`48s–60s`, `1080x1920`, `60fps`) vertical cultural explainers, listicles, or lifestyle deep-dives on Japan. Distilled from the forensic analysis of 20 viral Shorts (`91.64M` combined views; see [INDEX.md](../../research/kurose_top20/INDEX.md)) and battle-tested production refinements.

---

## 1. Runtime, Natural `1.0x` Voiceover & Narrative Architecture

- **Target Runtime & Stream Spec**: `48.0s – 59.0s` (`54.0s`–`57.8s` sweet spot; `1080x1920` CFR at **`60/1 fps`**, `yuv420p`). Stays safely below YouTube Shorts' `60.0s` hard ceiling while maximizing watch-time weight.
- **ElevenLabs `1.0x` Pacing & Word-Lock Alignment**:
  - **Word Count & Natural Speed**: Write `130 – 160 words` (`~145 words` target) recorded via ElevenLabs v3 expressive tags (`[curious]`, `[whispers]`, `[laughs softly]`, `—` rhetorical dashes) and keep playback at **natural `1.0x` speed** (avoid `atempo` speed-warping unless explicitly requested by the user, preserving natural breath pockets and comedic micro-pauses).
  - **Silence Trim & Whisper Alignment**: Trim only leading/trailing digital silence (`0.12s` preroll + `0.06s` tail), transcribe with `/opt/homebrew/bin/whisper-cli` (`ggml-large-v3-turbo.bin`), and align word timestamps against ground-truth script tokens—stripping only `".,!?;:\"“”…"` so apostrophes in contractions/possessives (`JAPAN'S`, `THAT'S`, `DON'T`) stay intact—emitting `clauses.json`, `words.json`, and `.srt`.
- **Select 1 of 2 Structural Archetypes**:
  1. **Archetype A — 3-Pillar Escalating Decode (`70%` of corpus)**:
     - **Hook (`0.0s – 4.8s`, ~12–15 words)**: Open on an immediate curiosity gap (*"Why do so many Japanese women still look 25 even at age 45?!"*).
     - **Pillar 1 (`4.8s – 23.5s`, ~40–48 words)**: Visually dramatic daily habit + hard statistic (*e.g., `Bihaku (美白)` UV armor & `Higasa (日傘)` parasols in `35°C` heat; 80% of skin aging comes from UV rays*).
     - **Pillar 2 (`23.5s – 41.4s`, ~40–48 words)**: Systemic diet/commute mechanism + whispered ironic contrast (*e.g., whispered `"Instead of sugary sodas?"` -> unsweetened green tea, miso, sticky `Natto (納豆)`, `7,000+` train-transfer steps*).
     - **Pillar 3 (`41.4s – 57.1s`, ~38–45 words)**: Sensory nightly ritual + rapid 5-shot climax micro-montage (*e.g., `40°C` `Ofuro (お風呂)` soak vs. 3-minute shower -> circulation, stress relief, deep sleep, glass skin*).
     - **Double-Lock Loop Splice (`Final 0.60s – 0.72s`)**: Cut back to `Shot 01`'s exact continuous camera take on an unfinished bridge (`"That's..."`) completing at `0.00s`.
  2. **Archetype B — 5-Act Counter-Intuitive Deep Dive (`30%` of corpus)**:
     - **Act I (`0–4s`)** Stereotype shock -> **Act II (`4–16s`)** Hard stat/mandate -> **Act III (`16–32s`)** Indigenous concept + Kanji glossary -> **Act IV (`32–46s`)** Cynical loophole/twist -> **Act V (`46–56s`)** Takeaway + loop bridge.

---

## 2. Disbelief / Curiosity-Gap Thumbnail & SEO Packaging

- **Cognitive-Dissonance Thumbnail Formula (Never Spoil the Topic)**:
  - Pair a captivating, youthful real-camera Japanese woman in `Shot 01` with a **2-line shock/disbelief claim** rather than a textbook summary title:
    - **Line 1 (`y = 1305`, `94px` `ArchivoBlack`, Pure White `#FFFFFF`, `15px` black stroke + shadow)**: Setup phrase (`"This Woman Is"`).
    - **Line 2 (`y = 1440`, `112px` `ArchivoBlack`, `16px` black stroke + shadow)**: Coral Red tension word (`"Over "`, `#FF4D4D`) + Canary Yellow number/hook (`"45?!"`, `#FFE600`) + **native Apple Color Emoji sticker (`💀`)**.
  - **Native Color Emoji Sticker Rendering**: Standard display fonts (`ArchivoBlack`) lack color emoji glyphs and draw blank boxes. Render emoji glyphs from `/System/Library/Fonts/Apple Color Emoji.ttc` at `160px` (`embedded_color=True`), crop and LANCZOS-resize to `~108px`, and composite over a `MaxFilter(17)` solid black sticker outline + Gaussian drop shadow.
  - **Frame-0 Burn-In + Safe Zone**: Burn the thumbnail banner + static **Red Pointer Arrow** (`scale=1.18` aimed at her outer hairline/cheek) into **`f0000–f0005` (`0.00s–0.10s` at `60fps`)** of the `.mp4` and export `*_Thumb.jpg`. Keep `y = 1280–1490` clear of both the subject's face/chest and YouTube Shorts' bottom UI bar (`y > 1620`).
- **Curiosity-Gap Title, Description & Tags**:
  - **Title (`< 55 chars`, zero mobile truncation)**: Frame as an unresolved disbelief hook with `💀` / `🇯🇵` + `#Japan` or `#shorts` (*e.g., `"She’s Over 45?! Japan’s Secret Is Crazy 💀 #Japan"`* or *`"Japan’s “Vampire” Rule That Stops Aging 💀🇯🇵 #shorts"`*).
  - **Description & Tags**: Front-load the curiosity hook in sentence 1, summarize the 3 named Japanese pillars with Kanji (`Bihaku 美白`, `Higasa 日傘`, `Natto 納豆`, `Ofuro お風呂`), end with a comment-bait question + 3-tier hashtags (`#shorts #japan #japaneseculture ...`), and supply `< 480 / 500` chars of comma-separated YouTube Studio search tags + a debate-triggering Pinned Comment.

---

## 3. 100% Real-Camera Footage Screening, Framing & Pacing

- **Strict Real-Camera Screening (Zero AI, Zero CG/Game TVCM)**:
  - Build and inspect (`read_file`) a `9:16` candidate contact sheet before editing. Select **100% real cinema/handheld camera footage** exhibiting natural skin texture, real wind in hair, natural sunlight/curtain shadows, and authentic Tokyo street/kitchen/bath environments (e.g., 4K photobook making-of shoots, street vlogs, documentary B-roll).
  - Exclude AI-generated clips, heavily airbrushed mobile-game commercials, and static images (`freezedetect` >= `0.45s` must report `0` frozen segments).
  - **Opening Hook Allure (`Shot 01` + `Shot N`)**: Anchor `Shot 01` (`0.00s–2.75s`) on a genuinely alluring, expressive real-camera shot of a Japanese woman making direct eye contact by natural light, cropping top/center (`e.g., crop=iw*0.46:ih*0.82:iw*0.27:ih*0.02`) so any bottom-corner source magazine text is `100%` off-frame. Ensure the source take runs continuously for `>= 3.8s` without internal cuts or dissolves so `Shot N` (`offset = t0 - 0.67s`) splices seamlessly into `Shot 01` (`offset = t0`).
- **Framing Modes & Clean Watermark-Free Canvas**:
  - **Zero Watermarks**: Keep the entire video `100%` free of `@kurose` or third-party channel watermarks unless explicitly requested.
  - **`tall_card` vs. `custom_crop`**: For wide `16:9` documentary proof clips, either center a `1080x964` foreground card (`y = 390..1354`) over a `sigma=35` Gaussian-blurred, darkened (`brightness=-0.08`) `1080x1920` duplicate background (`tall_card`), or apply a targeted `custom_crop` to fill `1080x1920`. Mask distracting burned-in source subtitles inside `tall_card` clips using a feathered (`radius=20`) Gaussian blur band (`blur_bar`).
- **Shot Pacing (`26–30` Shots, `~2.0s` ASL)**:
  - Interleave **parasocial beauty anchors** (`Shot 01, 02, 12, 19, 27, 28`) with **literal physical proof B-roll** (`UV visors, 35°C parasols, soda vs. green tea pour, miso ladle, sticky natto, Tokyo Station commuters, hinoki bath steam`), accelerating to **`0.9s–1.2s` cuts** during 3-item lists and the 5-shot climax montage (`50.8s–57.1s`).

---

## 4. 4-Mode Motion-Tile Inter-Source Transition Engine

Hard jump-cuts between unrelated source videos feel abrupt. Apply a `60fps` **Motion-Tile Transition** across every inter-source cut, synthesized over a **`3x3` mirrored canvas** (`FLIP_LEFT_RIGHT` / `FLIP_TOP_BOTTOM` surrounding the center frame at `540x960` working resolution, upscaled to `1080x1920`) so rotation, whip, and zoom-out edges stay seamless with zero black borders:

1. **`spin_swirl` (`±0.17s` / `20 frames` @ `60fps` — Act & Pillar Boundaries)**:
   - Outgoing half (`u < 0.5`): `ease = (2u)^2.2`, scale `1.0 -> 0.70`, angle `0° -> -150°`; Incoming half (`u >= 0.5`): symmetric settle from `+150° -> 0°`. Blend **5 angular blur taps** (`±26°` span) across the `3x3` mirror tile.
2. **`whip_horiz` (`±0.15s` / `18 frames` @ `60fps` — Contrast Pivots, e.g., Soda -> Green Tea)**:
   - Horizontal whip (`dx = ±1.18 * w * p^2.5`) with mid-whip pull-back (`scale = 1.0 - 0.44 * sin(πp/2)`), blending **7 horizontal streak taps** (`±0.24 * w`).
3. **`push_vert` (`±0.10s` / `12 frames` @ `60fps` — Sequential Evidence Steps)**:
   - Build a `4x`-tall vertical mirror strip (`flip(out), out, in, flip(in)`), translate vertically via smoothstep `u^2(3 - 2u)` with **5 vertical motion-blur taps** (`±0.08 * h * sin(πu)`).
4. **`zoom_punch` (`±0.085s` / `10 frames` @ `60fps` — Rapid List & Montage Cuts)**:
   - Outgoing `1.00x -> 1.42x` punch-in (`p^2.2`) into incoming `0.72x -> 1.00x` settle, blending **4 radial scale taps**.
- **HUD Layering Rule**: Hide shot-bound graphics (`arrow`, `red_circle`, `emote`) while `in_transition=True` so pointers never smear across scenes, while keeping the center-locked caption crisp above the transition.

---

## 5. Grid-Calibrated Red Arrow, Circle & Manga Emote System

- **Mandatory Cropped-Frame Grid Calibration (Zero Drift, Zero Face Occlusion)**:
  - `tall_card` (`y = 390..1354`) and `custom_crop` shift subject positions relative to raw `16:9` sources. Before locking coordinates, render a **`.05` / `.10` normalized calibration grid directly onto the prepared `1080x1920` clips** across `p = 0.00, 0.30, 0.65, 1.00` and inspect via `read_file`.
  - Define `3–5` `(prog, ux, uy)` keyframes per tracked shot (`60%–70%` of shots) and transform through active shot zoom (`sx = round(W * (0.5 + (ux - 0.5) * cur_z))`, `sy = round(H * (0.5 + (uy - 0.5) * cur_z))`) so the arrow tip stays locked onto moving parasols, visors, pouring tea, natto threads, and walking commuters.
  - On close-up faces (`S01, S04, S10, S22`), aim the arrow from **outer hair/cheek margins** (`0` eye, nose, or mouth occlusion).
  - Support `delay_s` mid-shot pop-ins (`0.80x -> 1.05x -> 1.00x` scale pop + `13 rad/s` axial oscillation) synced to spoken stats (`"80%"`, `"40°C"`), paired optionally with double-stroked **Red Oval Circles** (`#FFFFFF` outer + `#FF1414` inner) and manga reaction emotes (`"!!!"` shout pill, `💢` anger vein).

---

## 6. Center-Locked 2-Color Single-Word Captions & Kanji Glossaries

- **1 Word at a Time (`100% ALL CAPS`)**:
  - Render strictly **1 spoken word** at `(x = 540, y = 1155)` in `ArchivoBlack` `90px` (`45px` `50%` shrink on whispered ironic beats like `"INSTEAD OF SUGARY SODAS?"`), `12px` solid black stroke (`#000000`) + tight drop shadow, with a `2-frame` (`34ms`) `0.82x -> 1.05x -> 1.00x` pop entrance.
- **2-Color Semantic Highlight (`60%–75%` Canary Yellow / `25%–40%` Pure White)**:
  - **Canary Yellow (`#FFE600`)**: Nouns, active verbs, adjectives, numbers/temperatures (`25`, `45?!`, `35°C`, `80%`, `7,000`, `40°C`), and cultural terms.
  - **Pure White (`#FFFFFF`)**: Prepositions, articles, pronouns, and transitions (`WHY`, `IN`, `FIRST`, `LASTLY`, `THAT'S...`).
- **Bilingual Kanji Sub-Caption (`y = 1252`)**: Pin `(美白 · Bihaku)`, `(日傘 · Higasa)`, `(納豆 · Natto)`, `(お風呂 · Ofuro)` in `ZenKakuGothicNew-Bold` `50px` white with `7px` black stroke directly beneath the active word when spoken.

---

## 7. Audio Mastering, `quick_tip` SFX Discipline & Vocal-Pocket BGM

- **Clean SFX Palette (Zero Slap / Wood-Bonk Spam)**:
  - Place `12–15` clean accents across `~58s` (zero `whip_crack_slap` or `wood_bonk_pop` clutter):
    - **`quick_tip.wav` (`6` hits, `-15 to -16 dB`)**: Crisp UI chime on pillar headers, Kanji reveals, and key stats (`80%`, `7,000`, `40°C`).
    - **`whoosh_whip_fast.wav` (`5` hits, `-17 to -18 dB`)**: Synced to `spin_swirl` and `whip_horiz` transitions.
    - **`kabuki_pon_chime.wav` (`1` hit) + `shutter.wav` (`1–2` hits)**: Cultural climax accent and camera-flash hook texture.
- **Vocal-Pocket BGM & Broadcast Loudness Targets**:
  - Carve a vocal clarity pocket in stereo BGM (`equalizer=f=2150:t=q:w=1.2:g=-5.5,extrastereo=m=1.55`; **avoid Haas `adelay` on BGM**, which comb-filters and inflates Side RMS), sidechain-duck under mono-centered compressed voice, and master via `alimiter`:
    - **Integrated Loudness (`I`)**: **`-14.5 to -16.5 LUFS`** (`-15.2 LUFS` sweet spot).
    - **Loudness Range (`LRA`)**: **`1.5 – 2.3 LU`**; **True Peak (`TP`)**: **`<= -0.1 dBFS`**.
    - **Mid/Side Separation (`Mid RMS − Side RMS`)**: **`+17.0 to +20.5 dB`** (`Mid ~ -17.8 dB`, `Side ~ -35.3 dB`).

---

## 8. Python + FFmpeg `60fps` Render Pipeline & Mandatory Visual QC

1. **Toolchain**: Run Python scripts with system `/usr/bin/python3` (`PIL`), `/opt/homebrew/bin/ffmpeg`, and `/opt/homebrew/bin/whisper-cli`; use `.venv/bin/yt-dlp` strictly for YouTube media downloads.
2. **Two-Stage Streaming Compositor**:
   - **Stage 1 (`prepare_60fps_clips`)**: Pre-crop and normalize each shot (`+0.30s` transition tail buffer) to `1080x1920 @ 60fps` (`crf 17`) in a versioned cache directory.
   - **Stage 2 (`ShotClipReader` -> Pillow -> `ffmpeg` Pipe)**: Stream `rawvideo rgb24` frames per active shot, apply zoom/blur-bars, synthesize inter-shot Motion-Tile transitions, composite HUD + captions (`f0000–f0005` thumbnail banner), and pipe directly into `libx264` (`-crf 17 -pix_fmt yuv420p -movflags +faststart`) + `aac 192k`.
3. **Mandatory 5-Artifact Post-Render Verification (Inspect All Images via `read_file`)**:
   - `*_Thumb.jpg` & extracted MP4 `Frame 0`: Verify `This Woman Is / Over 45?! 💀` legibility, native color emoji, Red Arrow placement, and `100%` real-camera appeal.
   - `*_Contact_Sheet.jpg` (all shots): Confirm `0` `@kurose` watermarks, `0` AI/game-TVCM frames, and clean crop borders.
   - `*_Arrow_Tracking_Audit.jpg` (`4` progress columns `p = 0.16, 0.42, 0.66, 0.86` per tracked shot): Confirm every arrow tracks its moving target with `0` facial occlusion.
   - `*_Transitions_Audit.jpg` (`10`-frame strips across `spin_swirl`, `whip_horiz`, `push_vert`, `zoom_punch`): Confirm seamless `3x3` mirror-tile motion blur with `0` black edges.
   - `QC_REPORT_*.txt` (`ffprobe` + `blackdetect` + `freezedetect` + `ebur128` + Mid/Side `astats`): Verify `1080x1920 @ 60/1 fps`, `< 60.0s`, `0` black gaps, `0` frozen frames, `-14.5 to -16.5 LUFS`, `LRA 1.5–2.3 LU`, `TP <= -0.1 dBFS`, and `+17.0 to +20.5 dB` Mid/Side separation.

---

## 9. Viral Topic Selection & Comment-Bait Engineering

- **5 High-Velocity Topic Pillars**:
  1. **Beauty, Aging & Dating Signals** (`v03, v06, v07, v16–v19`): Decode why Japanese women stay youthful/slim, female intention signals, or cross-cultural beauty standards.
  2. **Hidden Social Taboos & Legal Traps** (`v02, v05, v10, v13, v14, v20`): Frame everyday objects (kimono collar/obi, sakura branches, school rules) as high-stakes social minefields.
  3. **Positive Cultural Shock ("Impossible to Unsee")** (`v01, v09`): Contrast global chaos with Japanese civic discipline.
  4. **Daily Survival & Kinetic Hacks** (`v04, v08, v15`): Heatwave parasols/cooling mist, seismic engineering, or commuter habits (*inemuri*).
  5. **Socio-Economic Paradoxes** (`v11, v12`): Counter-intuitive national statistics (hidden millionaires, low passport ownership despite #1 passport strength).
- **1 Comment-Bait Trigger per Video**: Plant one playful narrator provocation (e.g., whispered *"Instead of sugary sodas?"*, *"Distracting by what, exactly?"*, or polarizing food/habit challenge like sticky *Natto* + nightly `40°C` *Ofuro*) echoed in the Pinned Comment to drive comment velocity while the video loops in the background.
