#!/usr/bin/env python3
"""
Reusable rendering primitives for the Nexivo 26-Second 30fps 4-Act Loop Blueprint (viral-shorts-editing.md):
1. Keyframed Red Pointer Arrow (Frames 1-34 / 0.00s-1.13s):
   - #FF1A1A fill, 6px #000000 outer stroke + subtle drop shadow
   - Smooth keyframed tip trajectory + clockwise rotation + 8-frame alpha fade-out (0.85s -> 1.13s)
2. Single-Word Rapid-Fire Caption System:
   - Strictly 1 word at a time at (x=540, y=1385)
   - BeVietnamPro-Bold ~82px, 11px #000000 outer contour + tight dark drop shadow
   - 1-2 Frame (0-66ms) Horizontal Motion-Blur + 1.15x scaleX Pop Entrance
   - 4-Color High-Luminance Metronome Rotation (#FFE838, #42F2F7, #38F852, #FFFFFF)
"""
from functools import lru_cache
import math
from PIL import Image, ImageDraw, ImageFont

FONT_BOLD_PATH = "/Users/digiex/Documents/ChatGPT/printer/MoneyPrinterTurbo/resource/fonts/BeVietnamPro-Bold.ttf"

HEX_TO_RGBA = {
    "#FFE838": (255, 232, 56, 255),   # Warm Yellow
    "#42F2F7": (66, 242, 247, 255),   # Sky Cyan
    "#38F852": (56, 248, 82, 255),    # Neon Mint Green
    "#FFFFFF": (255, 255, 255, 255),  # Pure White
}


@lru_cache(maxsize=64)
def get_font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD_PATH, size)


@lru_cache(maxsize=256)
def render_word_base_sprite(word: str, color_hex: str, font_px: int = 82) -> Image.Image:
    """Renders a crisp single-word RGBA sprite with 11px black contour and tight drop shadow."""
    font = get_font(font_px)
    # Measure bounding box with generous padding for stroke + shadow + horizontal blur
    dummy = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dummy)
    bbox = dd.textbbox((0, 0), word, font=font, stroke_width=12)
    tw = (bbox[2] - bbox[0]) + 80
    th = (bbox[3] - bbox[1]) + 60

    sprite = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(sprite)
    cx, cy = tw // 2, th // 2
    fill_rgba = HEX_TO_RGBA.get(color_hex, (255, 255, 255, 255))

    # Tight dark drop shadow (+4, +6)
    d.text(
        (cx + 4, cy + 6), word, font=font,
        fill=(0, 0, 0, 215), anchor="mm",
        stroke_width=12, stroke_fill=(0, 0, 0, 215)
    )
    # Crisp 11px #000000 outer contour + high-luminance fill
    d.text(
        (cx, cy), word, font=font,
        fill=fill_rgba, anchor="mm",
        stroke_width=11, stroke_fill=(0, 0, 0, 255)
    )
    return sprite


def apply_horizontal_motion_blur(sprite: Image.Image, scale_x: float, blur_px: int) -> Image.Image:
    """Applies horizontal scaleX stretch + true 1D horizontal directional blur (zero vertical blur)."""
    w, h = sprite.size
    sw = max(1, int(round(w * scale_x)))
    stretched = sprite.resize((sw, h), Image.Resampling.BICUBIC) if abs(scale_x - 1.0) > 0.005 else sprite
    if blur_px <= 0:
        return stretched

    # Multi-tap 1D horizontal motion blur with Gaussian-weighted horizontal offsets
    pad = blur_px * 2 + 8
    out_w = sw + pad * 2
    accum = Image.new("RGBA", (out_w, h), (0, 0, 0, 0))
    taps = [
        (-blur_px, 0.12),
        (-blur_px // 2, 0.22),
        (0, 0.32),
        (blur_px // 2, 0.22),
        (blur_px, 0.12),
    ]
    r, g, b, a = stretched.split()
    for dx, weight in taps:
        tap_a = a.point(lambda p, wgt=weight: int(round(p * wgt)))
        tap_img = Image.merge("RGBA", (r, g, b, tap_a))
        accum.alpha_composite(tap_img, (pad + dx, 0))
    return accum


def draw_nexivo_caption(canvas: Image.Image, words: list[dict], t: float):
    """
    Draws the active single word at (x=540, y=1385) with 1-2 frame horizontal motion-blur pop entrance:
    - Frame 1 (0 - 33ms): scaleX = 1.15x + 10px horizontal directional blur
    - Frame 2 (33 - 66ms): scaleX = 1.05x + 4px horizontal directional blur
    - Frame 3+ (>= 66ms): crisp 1.00x focus
    """
    active = None
    for w in words:
        if w["start"] <= t < w["end"]:
            active = w
            break
    if not active:
        return

    dt = max(0.0, t - active["start"])
    base = render_word_base_sprite(active["text"], active["color"], font_px=82)
    if dt < 0.034:
        spr = apply_horizontal_motion_blur(base, scale_x=1.15, blur_px=10)
    elif dt < 0.068:
        spr = apply_horizontal_motion_blur(base, scale_x=1.05, blur_px=4)
    else:
        spr = base

    px = 540 - spr.width // 2
    py = 1385 - spr.height // 2
    canvas.alpha_composite(spr, (px, py))


def smoothstep(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0 * x)


def draw_nexivo_hook_arrow(
    canvas: Image.Image,
    t: float,
    cheek_xy: tuple[float, float],
    crown_xy: tuple[float, float],
):
    """
    Keyframed Red Pointer Arrow (Frames 1-34 / 0.00s - 1.133s at 30fps) per viral-shorts-editing.md Section 3:
    - Fill: #FF1A1A, Stroke: 6px #000000
    - 0.00s - 0.30s (f001-f009): Enters on left, pointing right/down (+20 deg screen angle) at subject's cheek/mouth
    - 0.30s - 0.85s (f010-f026): Tracks upward and rotates clockwise (+20 deg -> +85 deg, pointing straight down)
      at the top of the subject's cap/headpiece as she turns toward camera
    - 0.85s - 1.133s (f026-f034): Fades out (alpha 1.0 -> 0.0 over 8 frames)
    """
    if t < 0.0 or t > 1.135:
        return

    W, H = canvas.size
    cx0, cy0 = cheek_xy[0] * W, cheek_xy[1] * H
    cx1, cy1 = crown_xy[0] * W, crown_xy[1] * H

    if t <= 0.30:
        # Enter slightly from left into cheek target over first 0.18s, holding +20 deg angle
        enter_p = smoothstep(t / 0.22)
        tx = (cx0 - 42.0) + 42.0 * enter_p
        ty = (cy0 - 14.0) + 14.0 * enter_p
        angle_deg = 20.0
        alpha = 1.0
    elif t <= 0.85:
        p = smoothstep((t - 0.30) / (0.85 - 0.30))
        tx = cx0 + (cx1 - cx0) * p
        ty = cy0 + (cy1 - cy0) * p
        # Clockwise rotation in screen coordinates (+y down): +20 deg (right-down) -> +85 deg (nearly straight down)
        angle_deg = 20.0 + (85.0 - 20.0) * p
        alpha = 1.0
    else:
        tx, ty = cx1, cy1
        angle_deg = 85.0
        alpha = max(0.0, 1.0 - (t - 0.85) / (1.133 - 0.85))

    if alpha <= 0.01:
        return

    rad = math.radians(angle_deg)
    ux, uy = math.cos(rad), math.sin(rad)
    px, py = -uy, ux

    # Subtle kinetic micro-bob along pointing axis
    gap = 10.0 + 4.0 * math.sin(t * 18.0)
    d_tip = gap
    d_neck = gap + 64.0
    d_tail = gap + 150.0
    w_head = 46.0
    w_shaft = 19.0

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

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    a_fill = int(round(255 * alpha))
    a_shad = int(round(165 * alpha))

    shadow_pts = [(x + 5, y + 6) for x, y in pts]
    d.polygon(shadow_pts, fill=(0, 0, 0, a_shad))
    # #FF1A1A fill with crisp 6px #000000 stroke per Nexivo blueprint
    d.polygon(pts, fill=(255, 26, 26, a_fill), outline=(0, 0, 0, a_fill), width=6)
    canvas.alpha_composite(layer)
