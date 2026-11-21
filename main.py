#!/usr/bin/env python3
"""Draw a one-page newspaper front page summing up Saturday 21 November 2026.

Reads nothing, uses no network. Writes entry.png to $MAKEFUN_OUTPUT_DIR
(default /output). Fully deterministic: fixed layout, fixed palette, fixed
shapes, no randomness, no timestamps, no locale dependence.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (17, 17, 17)
SOFT_INK = (58, 54, 48)
RULE = (17, 17, 17)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
TEAL = (14, 116, 144)
MAP_LAND = (216, 210, 192)
MAP_LINE = (120, 112, 96)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)  # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None, align="left",
               width=None):
    """Draw lines of text; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in lines:
        if align == "center" and width is not None:
            lx = x + (width - draw.textlength(line, font=fnt)) // 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += leading
    return y


def vgrad(draw, box, top, bottom):
    """Vertical gradient fill inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0)
    for i in range(span):
        t = i / span
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=col)


def draw_vice_city(draw, box):
    """Sunset Vice City skyline art: gradient sky, sun, towers, palms, water."""
    x0, y0, x1, y1 = box
    vgrad(draw, box, (214, 48, 120), (250, 140, 60))
    # sun
    cx, cy, r = (x0 + x1) // 2 + 180, y0 + 62, 34
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 214, 130))
    draw.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6],
                 outline=(255, 214, 130), width=2)
    # skyline silhouettes (fixed heights, no randomness)
    base = y1 - 34
    towers = [(0, 96), (52, 128), (118, 84), (176, 142), (240, 104),
              (306, 150), (372, 92), (438, 132), (508, 88), (574, 146),
              (640, 108), (706, 138), (772, 96), (838, 128), (906, 100)]
    for dx, th in towers:
        tx = x0 + dx
        tw = 58
        draw.rectangle([tx, base - th, tx + tw, base], fill=(46, 16, 66))
        # lit windows: fixed grid
        for wy in range(base - th + 10, base - 8, 16):
            for wx in range(tx + 8, tx + tw - 8, 14):
                if (wx + wy) % 28 == 0:
                    draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 130))
    # palm silhouettes: trunk + radiating frond lines
    import math
    for px, ph in [(x0 + 96, 46), (x0 + 640, 54), (x0 + 900, 42)]:
        top = base - ph
        draw.line([(px, base), (px, top)], fill=(30, 10, 44), width=5)
        for deg in (-160, -120, -80, -40, -20):
            rad = math.radians(deg)
            ex = px + int(26 * math.cos(rad))
            ey = top + int(16 * math.sin(rad)) - 4
            draw.line([(px, top), (ex, ey)], fill=(30, 10, 44), width=4)
    # water strip with reflection streaks
    draw.rectangle([x0, y1 - 34, x1, y1], fill=(64, 24, 90))
    for i, (sx, sw) in enumerate([(60, 90), (220, 60), (380, 110), (560, 70),
                                  (720, 100), (860, 60)]):
        draw.line([(x0 + sx, y1 - 22 + (i % 3) * 6),
                   (x0 + sx + sw, y1 - 22 + (i % 3) * 6)],
                  fill=(255, 170, 110), width=3)


def draw_storm(draw, box):
    """Cyclone swirl: concentric arcs over a grey-teal sky, rain lines."""
    x0, y0, x1, y1 = box
    vgrad(draw, box, (58, 90, 110), (148, 168, 178))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 6
    for k, r in enumerate([14, 26, 38, 50, 62]):
        col = (246, 241, 229) if k % 2 == 0 else (30, 58, 95)
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=20 + k * 40,
                 end=300 + k * 40, fill=col, width=4)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(185, 28, 28))
    for rx in range(x0 + 12, x1 - 8, 22):
        draw.line([(rx, y0 + 10), (rx - 8, y0 + 34)], fill=(246, 241, 229),
                  width=2)


def draw_map(draw, box):
    """Stylised world map: rough continent blobs, red dots, labels."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, outline=MAP_LINE, width=2)
    ox, oy = x0 + 14, y0 + 8
    scale = 0.98
    continents = [
        [(8, 38), (30, 18), (70, 12), (95, 22), (88, 45), (70, 55),
         (55, 70), (40, 62), (22, 55), (8, 48)],                      # N America
        [(78, 78), (95, 72), (108, 88), (100, 120), (88, 132),
         (76, 105), (72, 88)],                                        # S America
        [(168, 30), (185, 18), (205, 20), (210, 38), (195, 48),
         (178, 45), (168, 38)],                                       # Europe
        [(175, 55), (200, 52), (215, 65), (208, 95), (195, 115),
         (182, 100), (172, 75)],                                      # Africa
        [(215, 18), (260, 10), (310, 15), (340, 30), (330, 55),
         (300, 70), (270, 62), (240, 55), (222, 40)],                 # Asia
        [(300, 105), (330, 100), (345, 112), (330, 128), (305, 122)],  # Australia
    ]
    for poly in continents:
        pts = [(ox + int(px * scale), oy + int(py * scale)) for px, py in poly]
        draw.polygon(pts, fill=MAP_LAND, outline=MAP_LINE)
    dots = [
        (66, 56, "VICE CITY"),    # Florida / Leonida
        (205, 40, "CRIMEA"),     # Black Sea
        (228, 74, "RIYADH"),     # Arabian peninsula
        (283, 64, "MYANMAR"),    # SE Asia
    ]
    lbl = SANS_B(11)
    for dx, dy, name in dots:
        px, py = ox + int(dx * scale), oy + int(dy * scale)
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                     outline=INK, width=1)
        draw.text((px + 9, py - 6), name, font=lbl, fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 26                      # side margin
    CW = W - 2 * MX              # content width

    # ---------- masthead ----------
    d.line([(MX, 30), (W - MX, 30)], fill=RULE, width=3)
    text_block(d, MX, 40, ["THE WORLD"], SERIF_B(58), align="center", width=CW)
    text_block(d, MX, 108, ["SATURDAY 21 NOVEMBER 2026"],
               SANS_B(26), align="center", width=CW)
    text_block(d, MX, 140, ["THE DAY IN ONE PICTURE  ·  FREE  ·  No. 325"],
               SANS(13), fill=SOFT_INK, align="center", width=CW)
    d.line([(MX, 160), (W - MX, 160)], fill=RULE, width=4)

    # ---------- lead hero: GTA VI launch weekend ----------
    draw_vice_city(d, (MX, 172, W - MX, 348))
    y = 360
    y = text_block(d, MX, y, ["GTA VI LAUNCH WEEKEND"], SERIF_B(44))
    y = text_block(d, MX, y + 2,
                   ["Vice City opens its doors — players spend the first "
                    "weekend in Leonida"],
                   SANS_B(20))
    y = text_block(d, MX, y + 4,
                   wrap(d, "Rockstar's blockbuster launched Thursday "
                        "19 November on PlayStation 5 and Xbox Series X|S — "
                        "Standard $79.99, Ultimate $99.99. No PC version, "
                        "no demo, no beta.", SANS(16), CW),
                   SANS(16), fill=SOFT_INK)
    d.line([(MX, 500), (W - MX, 500)], fill=RULE, width=2)

    # ---------- mid row ----------
    # left: Cyclone Akvan
    lx0, lx1 = MX, 500
    draw_storm(d, (lx0, 514, lx1, 592))
    y = text_block(d, lx0, 600, ["CYCLONE AKVAN"], SERIF_B(26))
    text_block(d, lx0, y + 2,
               wrap(d, "300,000 people evacuated as the cyclone sweeps "
                    "toward land.", SANS(15), lx1 - lx0),
               SANS(15), fill=SOFT_INK)
    # right: around the world
    rx0, rx1 = 524, W - MX
    y = text_block(d, rx0, 514, ["AROUND THE WORLD"], SANS_B(15), fill=RED)
    minis = [
        ("TRILATERAL DECLARATION",
         "Joint declaration issued 20 Nov, a day after the three-way meeting."),
        ("MISSILE OVER RIYADH",
         "Houthi missile fired at the Saudi capital, 20 Nov."),
        ("ICJ RULES ON MYANMAR",
         "World court delivers its genocide-case ruling, 19 Nov."),
    ]
    y += 6
    for head, body in minis:
        y = text_block(d, rx0, y, [head], SANS_B(16))
        y = text_block(d, rx0, y + 1,
                       wrap(d, body, SANS(14), rx1 - rx0),
                       SANS(14), fill=SOFT_INK)
        y += 8
    d.line([(MX, 700), (W - MX, 700)], fill=RULE, width=2)

    # ---------- lower section ----------
    # left: also on the wires
    y = text_block(d, MX, 714, ["ALSO ON THE WIRES"], SANS_B(15), fill=RED)
    wires = [
        "Anthropic IPO priced at $81.34bn — 19 Nov",
        "Anthropic valued at $1.5tn in new report — 20 Nov",
        "Crimean Bridge hit for a third time this week — 20 Nov",
        "GTA VI launch prices: $79.99 standard, $99.99 ultimate — 19 Nov",
    ]
    y += 6
    for item in wires:
        for line in wrap(d, "•  " + item, SANS(15), 520):
            y = text_block(d, MX, y, [line], SANS(15))
        y += 6
    # right: map
    mx0 = 584
    text_block(d, mx0, 714, ["WHERE IT HAPPENED"], SANS_B(15), fill=RED)
    draw_map(d, (mx0, 738, W - MX, 872))

    # ---------- red scam strip ----------
    d.rectangle([MX, 890, W - MX, 936], fill=RED)
    text_block(d, MX + 12, 896,
               wrap(d, "⚠ GTA 6 SCAMS: fake “free GTA VI” pages steal Google "
                    "logins; bogus PC installers spread infostealers; "
                    "20,000+ GTA-themed tokens, 8,800+ flagged malicious. "
                    "Rockstar: no free copies, no PC version, no airdrop.",
                    SANS_B(14), CW - 24),
               SANS_B(14), fill=(255, 255, 255))

    # ---------- date check ----------
    d.rectangle([MX, 950, W - MX, 998], outline=INK, width=2)
    text_block(d, MX + 10, 956,
               wrap(d, "DATE CHECK — GTA VI launched 19 Nov · Akvan "
                    "evacuations reported 20 Nov · ICJ Myanmar ruling "
                    "19 Nov · Anthropic IPO priced 19 Nov · Trilateral "
                    "declaration 20 Nov · Crimean Bridge third hit 20 Nov "
                    "· Houthi missile 20 Nov. Dates checked against "
                    "reporting of 19–20 Nov.",
                    SANS(12), CW - 20),
               SANS(12), fill=SOFT_INK)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG")
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
