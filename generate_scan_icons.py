#!/usr/bin/env python3
"""Generate 6 variations of the Scan Frame app icon."""

from PIL import Image, ImageDraw, ImageFont
import math
import os

SIZE = 1024
OUTPUT = "/Users/reda/Desktop/AI detector/AITextDetector/AppIcons"

DARK_BG = (12, 14, 12)
GREEN = (56, 158, 81)
LIGHT_GREEN = (72, 190, 100)
WHITE = (255, 255, 255)


def get_font(size):
    paths = [
        "/System/Library/Fonts/SFCompact-Bold.otf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()


def get_font_medium(size):
    paths = [
        "/System/Library/Fonts/SFCompact-Medium.otf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()


def draw_circle(draw, cx, cy, r, fill=None, outline=None, width=1):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=width)


def draw_brackets(draw, x0, y0, x1, y1, length, width, color):
    """Draw corner brackets at 4 corners of a rect."""
    # Top-left
    draw.line([(x0, y0), (x0 + length, y0)], fill=color, width=width)
    draw.line([(x0, y0), (x0, y0 + length)], fill=color, width=width)
    # Top-right
    draw.line([(x1, y0), (x1 - length, y0)], fill=color, width=width)
    draw.line([(x1, y0), (x1, y0 + length)], fill=color, width=width)
    # Bottom-left
    draw.line([(x0, y1), (x0 + length, y1)], fill=color, width=width)
    draw.line([(x0, y1), (x0, y1 - length)], fill=color, width=width)
    # Bottom-right
    draw.line([(x1, y1), (x1 - length, y1)], fill=color, width=width)
    draw.line([(x1, y1), (x1, y1 - length)], fill=color, width=width)


def draw_scan_glow(draw, y, x0, x1, color, spread=20):
    """Draw a horizontal scan line with glow."""
    r, g, b = color
    for offset in range(spread, 0, -1):
        alpha_pct = (1.0 - (offset / spread)) ** 2
        c = (int(r * alpha_pct * 0.4), int(g * alpha_pct * 0.4), int(b * alpha_pct * 0.4))
        draw.line([(x0, y + offset), (x1, y + offset)], fill=c, width=1)
        draw.line([(x0, y - offset), (x1, y - offset)], fill=c, width=1)
    draw.line([(x0, y), (x1, y)], fill=color, width=3)


# ── 4A: Original refined — thicker brackets, stronger glow, no grid ──
def icon_4a():
    img = Image.new("RGB", (SIZE, SIZE), DARK_BG)
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2

    # Subtle inner rect
    draw.rounded_rectangle([140, 140, SIZE - 140, SIZE - 140], radius=70, fill=(18, 24, 18))

    # Brackets
    draw_brackets(draw, 190, 190, SIZE - 190, SIZE - 190, 130, 10, GREEN)

    # "AI" text
    font = get_font(300)
    bbox = draw.textbbox((0, 0), "AI", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 10), "AI", fill=WHITE, font=font)

    # Scan line with strong glow
    draw_scan_glow(draw, cy + 50, 210, SIZE - 210, LIGHT_GREEN, spread=25)
    draw_circle(draw, cx, cy + 50, 5, fill=LIGHT_GREEN)

    img.save(os.path.join(OUTPUT, "scan_4a.png"))


# ── 4B: Rounded brackets + green gradient background ──
def icon_4b():
    img = Image.new("RGB", (SIZE, SIZE), DARK_BG)
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2

    # Green gradient circle behind
    for r in range(380, 0, -1):
        alpha = r / 380
        c = (int(10 + 15 * (1 - alpha)), int(20 + 40 * (1 - alpha)), int(12 + 20 * (1 - alpha)))
        draw_circle(draw, cx, cy, r, fill=c)

    # Rounded brackets (using arcs)
    bracket_r = 320
    bw = 8
    # Top-left corner arc
    draw.arc([cx - bracket_r, cy - bracket_r, cx - bracket_r + 200, cy - bracket_r + 200],
             start=180, end=270, fill=GREEN, width=bw)
    # Top-right
    draw.arc([cx + bracket_r - 200, cy - bracket_r, cx + bracket_r, cy - bracket_r + 200],
             start=270, end=360, fill=GREEN, width=bw)
    # Bottom-left
    draw.arc([cx - bracket_r, cy + bracket_r - 200, cx - bracket_r + 200, cy + bracket_r],
             start=90, end=180, fill=GREEN, width=bw)
    # Bottom-right
    draw.arc([cx + bracket_r - 200, cy + bracket_r - 200, cx + bracket_r, cy + bracket_r],
             start=0, end=90, fill=GREEN, width=bw)

    # "AI" text
    font = get_font(280)
    bbox = draw.textbbox((0, 0), "AI", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 10), "AI", fill=WHITE, font=font)

    # Scan line
    draw_scan_glow(draw, cy + 60, 230, SIZE - 230, LIGHT_GREEN, spread=18)

    img.save(os.path.join(OUTPUT, "scan_4b.png"))


# ── 4C: Double brackets + dot matrix scanline ──
def icon_4c():
    img = Image.new("RGB", (SIZE, SIZE), DARK_BG)
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2

    draw.rounded_rectangle([130, 130, SIZE - 130, SIZE - 130], radius=60, fill=(16, 20, 16))

    # Outer brackets
    draw_brackets(draw, 180, 180, SIZE - 180, SIZE - 180, 120, 8, GREEN)
    # Inner brackets (smaller, lighter)
    draw_brackets(draw, 240, 240, SIZE - 240, SIZE - 240, 80, 5, (40, 120, 55))

    # "AI"
    font = get_font(260)
    bbox = draw.textbbox((0, 0), "AI", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 15), "AI", fill=WHITE, font=font)

    # Dot matrix scan line
    scan_y = cy + 55
    for x in range(220, SIZE - 220, 14):
        dist = abs(x - cx)
        max_dist = (SIZE - 440) / 2
        brightness = 1.0 - (dist / max_dist) * 0.5
        r = int(72 * brightness)
        g = int(190 * brightness)
        b = int(100 * brightness)
        dot_r = 4
        draw_circle(draw, x, scan_y, dot_r, fill=(r, g, b))

    # Subtle glow behind dots
    for offset in range(12, 0, -1):
        a = 1.0 - (offset / 12.0)
        c = (int(20 * a), int(60 * a), int(30 * a))
        draw.line([(220, scan_y + offset), (SIZE - 220, scan_y + offset)], fill=c, width=1)
        draw.line([(220, scan_y - offset), (SIZE - 220, scan_y - offset)], fill=c, width=1)

    img.save(os.path.join(OUTPUT, "scan_4c.png"))


# ── 4D: Full border frame + bold green "AI" ──
def icon_4d():
    img = Image.new("RGB", (SIZE, SIZE), DARK_BG)
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2

    # Outer rounded rect border
    draw.rounded_rectangle([80, 80, SIZE - 80, SIZE - 80], radius=90, fill=None, outline=(30, 50, 32), width=3)
    draw.rounded_rectangle([140, 140, SIZE - 140, SIZE - 140], radius=60, fill=(14, 20, 14))

    # Corner brackets - bright green
    draw_brackets(draw, 170, 170, SIZE - 170, SIZE - 170, 140, 10, GREEN)

    # "AI" in GREEN instead of white
    font = get_font(310)
    bbox = draw.textbbox((0, 0), "AI", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 10), "AI", fill=GREEN, font=font)

    # Thin white scan line
    scan_y = cy + 60
    draw_scan_glow(draw, scan_y, 200, SIZE - 200, (255, 255, 255), spread=12)

    # Small "DETECT" below
    font_sm = get_font_medium(56)
    bbox2 = draw.textbbox((0, 0), "DETECT", font=font_sm)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((cx - tw2 // 2, cy + 140), "DETECT", fill=(100, 110, 100), font=font_sm)

    img.save(os.path.join(OUTPUT, "scan_4d.png"))


# ── 4E: Crosshair / target style ──
def icon_4e():
    img = Image.new("RGB", (SIZE, SIZE), DARK_BG)
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2

    # Background circle
    draw_circle(draw, cx, cy, 420, fill=(16, 22, 16))

    # Crosshair rings
    draw_circle(draw, cx, cy, 340, outline=(30, 55, 35), width=2)
    draw_circle(draw, cx, cy, 260, outline=(35, 65, 40), width=2)

    # Crosshair lines (partial, with gap in center)
    gap = 120
    line_color = (40, 80, 45)
    # Horizontal
    draw.line([(cx - 340, cy), (cx - gap, cy)], fill=line_color, width=2)
    draw.line([(cx + gap, cy), (cx + 340, cy)], fill=line_color, width=2)
    # Vertical
    draw.line([(cx, cy - 340), (cx, cy - gap)], fill=line_color, width=2)
    draw.line([(cx, cy + gap), (cx, cy + 340)], fill=line_color, width=2)

    # Corner brackets
    draw_brackets(draw, 180, 180, SIZE - 180, SIZE - 180, 120, 8, GREEN)

    # "AI" text
    font = get_font(280)
    bbox = draw.textbbox((0, 0), "AI", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 10), "AI", fill=WHITE, font=font)

    # Scan line
    draw_scan_glow(draw, cy + 55, 200, SIZE - 200, LIGHT_GREEN, spread=15)

    img.save(os.path.join(OUTPUT, "scan_4e.png"))


# ── 4F: Minimal dark with green accent line only at bottom ──
def icon_4f():
    img = Image.new("RGB", (SIZE, SIZE), (8, 10, 8))
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2

    # Very subtle inner card
    draw.rounded_rectangle([100, 100, SIZE - 100, SIZE - 100], radius=80, fill=(14, 18, 14))

    # Thin corner brackets
    draw_brackets(draw, 160, 160, SIZE - 160, SIZE - 160, 100, 6, (40, 100, 50))

    # "AI" large, bold, white
    font = get_font(340)
    bbox = draw.textbbox((0, 0), "AI", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 40), "AI", fill=WHITE, font=font)

    # Green accent bar at bottom
    bar_y = cy + 160
    bar_h = 8
    draw.rounded_rectangle([220, bar_y, SIZE - 220, bar_y + bar_h], radius=4, fill=GREEN)

    # Subtle "detector" text
    font_sm = get_font_medium(52)
    bbox2 = draw.textbbox((0, 0), "detector", font=font_sm)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((cx - tw2 // 2, bar_y + 30), "detector", fill=(80, 90, 80), font=font_sm)

    img.save(os.path.join(OUTPUT, "scan_4f.png"))


if __name__ == "__main__":
    for name, fn in [
        ("4A - Refined Original", icon_4a),
        ("4B - Rounded Brackets + Gradient", icon_4b),
        ("4C - Double Brackets + Dot Matrix", icon_4c),
        ("4D - Green AI + White Scan", icon_4d),
        ("4E - Crosshair Target", icon_4e),
        ("4F - Ultra Minimal", icon_4f),
    ]:
        print(f"Generating {name}...")
        fn()
    print(f"\nAll 6 variations saved to: {OUTPUT}")
