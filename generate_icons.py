#!/usr/bin/env python3
"""Generate 4 app icon options for AI Text Detector."""

from PIL import Image, ImageDraw, ImageFont
import math
import os

SIZE = 1024
OUTPUT = "/Users/reda/Desktop/AI detector/AITextDetector/AppIcons"

# Colors
BLACK = (0, 0, 0)
DARK_BG = (12, 14, 12)
GREEN = (56, 158, 81)
LIGHT_GREEN = (72, 190, 100)
DARK_GREEN = (30, 80, 45)
WHITE = (255, 255, 255)
GRAY = (140, 140, 140)
RED = (220, 60, 60)
ORANGE = (240, 160, 40)
YELLOW = (220, 200, 50)


def draw_rounded_rect(draw, bbox, radius, fill):
    """Draw a rounded rectangle."""
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle(bbox, radius=radius, fill=fill)


def draw_circle(draw, cx, cy, r, fill=None, outline=None, width=1):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=width)


def get_font(size):
    """Try to get a bold system font."""
    paths = [
        "/System/Library/Fonts/SFCompact-Bold.otf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/SF-Pro-Display-Bold.otf",
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


# ── OPTION 1: Magnifying glass with "AI" ──
def icon_option_1():
    img = Image.new("RGB", (SIZE, SIZE), DARK_BG)
    draw = ImageDraw.Draw(img)

    cx, cy = SIZE // 2, SIZE // 2 - 30

    # Concentric rings
    for i, alpha in enumerate([25, 35, 50, 70]):
        r = 420 - i * 80
        ring_color = (56, 158, 81, alpha)
        draw_circle(draw, cx, cy, r, outline=(20 + i*8, 60 + i*15, 25 + i*8), width=2)

    # Green filled circle (AI badge)
    draw_circle(draw, cx, cy, 180, fill=GREEN)
    # Inner lighter circle
    draw_circle(draw, cx, cy, 155, fill=(46, 140, 70))

    # "AI" text
    font_ai = get_font(140)
    bbox = draw.textbbox((0, 0), "AI", font=font_ai)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 15), "AI", fill=WHITE, font=font_ai)

    # Magnifying glass handle (bottom-right)
    handle_angle = math.radians(40)
    gx = cx + int(140 * math.cos(handle_angle))
    gy = cy + int(140 * math.sin(handle_angle))
    ex = cx + int(340 * math.cos(handle_angle))
    ey = cy + int(340 * math.sin(handle_angle))
    draw.line([(gx, gy), (ex, ey)], fill=WHITE, width=36)
    # Glass ring
    draw_circle(draw, cx + 30, cy + 20, 195, outline=(255, 255, 255, 180), width=16)

    # Sparkles
    for sx, sy, ss in [(280, 140, 20), (320, 200, 14), (700, 300, 16)]:
        draw_star(draw, sx, sy, ss, WHITE)

    img.save(os.path.join(OUTPUT, "icon_option_1.png"))
    return img


# ── OPTION 2: Shield with checkmark + "AI" ──
def icon_option_2():
    img = Image.new("RGB", (SIZE, SIZE), DARK_BG)
    draw = ImageDraw.Draw(img)

    cx, cy = SIZE // 2, SIZE // 2

    # Dark gradient background circle
    draw_circle(draw, cx, cy, 440, fill=(18, 25, 18))
    draw_circle(draw, cx, cy, 360, fill=(22, 35, 22))

    # Shield shape (using polygon)
    shield_points = []
    # Top arc
    for a in range(0, 181):
        rad = math.radians(a)
        x = cx + int(220 * math.cos(math.radians(180 + a)))
        y = cy - 140 + int(80 * math.sin(math.radians(180 + a)))
        shield_points.append((x, y))
    # Bottom point
    shield_points.append((cx + 220, cy + 50))
    shield_points.append((cx, cy + 280))
    shield_points.append((cx - 220, cy + 50))

    draw.polygon(shield_points, fill=GREEN)

    # Inner shield
    inner_points = []
    for a in range(0, 181):
        x = cx + int(185 * math.cos(math.radians(180 + a)))
        y = cy - 120 + int(65 * math.sin(math.radians(180 + a)))
        inner_points.append((x, y))
    inner_points.append((cx + 185, cy + 40))
    inner_points.append((cx, cy + 240))
    inner_points.append((cx - 185, cy + 40))
    draw.polygon(inner_points, fill=(36, 120, 55))

    # "AI" text centered in shield
    font_ai = get_font(180)
    bbox = draw.textbbox((0, 0), "AI", font=font_ai)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 10), "AI", fill=WHITE, font=font_ai)

    # Small checkmark badge (bottom-right)
    bcx, bcy = cx + 160, cy + 180
    draw_circle(draw, bcx, bcy, 55, fill=LIGHT_GREEN)
    # Checkmark
    draw.line([(bcx - 25, bcy), (bcx - 5, bcy + 22), (bcx + 30, bcy - 20)], fill=WHITE, width=10)

    img.save(os.path.join(OUTPUT, "icon_option_2.png"))
    return img


# ── OPTION 3: Gauge meter (mini version of the result screen) ──
def icon_option_3():
    img = Image.new("RGB", (SIZE, SIZE), DARK_BG)
    draw = ImageDraw.Draw(img)

    cx, cy = SIZE // 2, SIZE // 2 + 40

    # Background circle
    draw_circle(draw, cx, cy - 20, 440, fill=(18, 25, 18))

    # Gauge arc - background
    arc_r = 300
    draw.arc([cx - arc_r, cy - arc_r, cx + arc_r, cy + arc_r],
             start=150, end=390, fill=(40, 45, 40), width=50)

    # Gauge arc - colored gradient (draw segments)
    colors_gradient = [
        (56, 180, 75),   # green
        (56, 180, 75),
        (100, 200, 60),
        (180, 200, 40),  # yellow
        (220, 180, 40),
        (240, 140, 40),  # orange
        (230, 80, 40),
        (220, 50, 50),   # red
    ]
    total_angle = 240
    segment = total_angle / len(colors_gradient)
    for i, color in enumerate(colors_gradient):
        start = 150 + i * segment
        end = start + segment + 1
        draw.arc([cx - arc_r, cy - arc_r, cx + arc_r, cy + arc_r],
                 start=start, end=end, fill=color, width=50)

    # "AI" text in center
    font_ai = get_font(200)
    bbox = draw.textbbox((0, 0), "AI", font=font_ai)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 30), "AI", fill=WHITE, font=font_ai)

    # Small "DETECTOR" text below
    font_sm = get_font_medium(64)
    bbox2 = draw.textbbox((0, 0), "DETECTOR", font=font_sm)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((cx - tw2 // 2, cy + th // 2 - 20), "DETECTOR", fill=GRAY, font=font_sm)

    img.save(os.path.join(OUTPUT, "icon_option_3.png"))
    return img


# ── OPTION 4: Clean minimal "AI" with scanning line ──
def icon_option_4():
    img = Image.new("RGB", (SIZE, SIZE), DARK_BG)
    draw = ImageDraw.Draw(img)

    cx, cy = SIZE // 2, SIZE // 2

    # Subtle background grid lines
    for i in range(0, SIZE, 60):
        draw.line([(i, 0), (i, SIZE)], fill=(20, 25, 20), width=1)
        draw.line([(0, i), (SIZE, i)], fill=(20, 25, 20), width=1)

    # Dark rounded rect background
    draw_rounded_rect(draw, [120, 120, SIZE - 120, SIZE - 120], 80, fill=(16, 22, 16))

    # Corner brackets (scan frame)
    bracket_len = 120
    bracket_w = 8
    corners = [
        (180, 180, 1, 1),   # top-left
        (SIZE-180, 180, -1, 1),  # top-right
        (180, SIZE-180, 1, -1),  # bottom-left
        (SIZE-180, SIZE-180, -1, -1),  # bottom-right
    ]
    for bx, by, dx, dy in corners:
        draw.line([(bx, by), (bx + bracket_len * dx, by)], fill=GREEN, width=bracket_w)
        draw.line([(bx, by), (bx, by + bracket_len * dy)], fill=GREEN, width=bracket_w)

    # "AI" large centered text
    font_ai = get_font(280)
    bbox = draw.textbbox((0, 0), "AI", font=font_ai)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 20), "AI", fill=WHITE, font=font_ai)

    # Scanning line (horizontal green line across the middle)
    scan_y = cy + 40
    # Glow effect
    for offset in range(15, 0, -1):
        alpha_pct = 1.0 - (offset / 15.0)
        g = int(158 * alpha_pct)
        r = int(56 * alpha_pct)
        color = (r, g, int(81 * alpha_pct))
        draw.line([(200, scan_y + offset), (SIZE - 200, scan_y + offset)], fill=color, width=1)
        draw.line([(200, scan_y - offset), (SIZE - 200, scan_y - offset)], fill=color, width=1)
    draw.line([(200, scan_y), (SIZE - 200, scan_y)], fill=LIGHT_GREEN, width=3)

    # Small dot on the scanning line
    draw_circle(draw, cx, scan_y, 6, fill=LIGHT_GREEN)

    img.save(os.path.join(OUTPUT, "icon_option_4.png"))
    return img


def draw_star(draw, cx, cy, size, color):
    """Draw a simple 4-point star/sparkle."""
    draw.line([(cx - size, cy), (cx + size, cy)], fill=color, width=3)
    draw.line([(cx, cy - size), (cx, cy + size)], fill=color, width=3)
    s2 = size // 2
    draw.line([(cx - s2, cy - s2), (cx + s2, cy + s2)], fill=color, width=2)
    draw.line([(cx + s2, cy - s2), (cx - s2, cy + s2)], fill=color, width=2)


if __name__ == "__main__":
    print("Generating icon 1: Magnifying Glass + AI...")
    icon_option_1()
    print("Generating icon 2: Shield + AI...")
    icon_option_2()
    print("Generating icon 3: Gauge Meter...")
    icon_option_3()
    print("Generating icon 4: Scan Frame + AI...")
    icon_option_4()
    print(f"\nAll 4 icons saved to: {OUTPUT}")
