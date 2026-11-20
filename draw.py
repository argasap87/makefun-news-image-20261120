#!/usr/bin/env python3
"""news-image-20261120 -- polished cyclone-wheel infographic, drawn from scratch.

One 1024x1024 image: five news stories of Friday 20 November 2026 arranged as
saturated sectors of a cyclone wheel around a bold central medallion.
PIL only, no external assets. Every number is taken from the brief.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (10, 17, 32)
GOLD = (255, 201, 60)
WHITE = (255, 255, 255)
SUB = (169, 184, 204)
MED_FILL = (11, 42, 51)
SWIRL = (143, 245, 230)

CX, CY = 512, 585          # wheel centre
R_OUT = 395                # wheel outer radius
R_MED = 130                # central medallion radius

# (kicker, headline lines, body lines, sector fill, pictogram kind, layout)
# layout: r_text = text-block centre radius; off = extra (dx, dy) shift of the
# block; hcap/bcap/kcap = max pixel width for headline / body / kicker lines;
# pic_r / pic_size / pic_dang = pictogram radius, size, angle offset from the
# sector mid-angle. Side sectors are narrower, so their caps are tighter and
# their pictograms smaller; bottom sectors sit 12px lower so their kickers
# clear the medallion; bottom pictograms swing toward the sector edge so
# they do not crowd the last body line.
SECTORS = [
    ("INDIA · WEATHER", ["AKVAN HITS", "ODISHA"],
     ["Crosses coast near", "Gopalpur, noon — 100 km/h", "105,000+ evacuated."],
     (0, 191, 165), "cyclone",
     dict(r_text=245, off=(0, 0), hcap=235, bcap=230, kcap=240,
          pic_r=360, pic_size=40, pic_dang=0)),
    ("EUROPE · YOUTH", ["STUDENTS", "WALK OUT"],
     ["Strikes in Europe + UK", "“Fight for our futures,", "not their wars.”"],
     (255, 59, 48), "megaphone",
     dict(r_text=245, off=(0, 0), hcap=195, bcap=190, kcap=190,
          pic_r=368, pic_size=34, pic_dang=0)),
    ("SHENZHEN · DIPLOMACY", ["ALBANESE", "MEETS XI"],
     ["Australia's PM meets", "China's president —", "fifth meeting, APEC week."],
     (255, 158, 0), "flags",
     dict(r_text=255, off=(0, 0), hcap=235, bcap=200, kcap=200,
          pic_r=360, pic_size=38, pic_dang=-16)),
    ("WELLINGTON · CRICKET", ["NICHOLLS", "146*"],
     ["NZ reach 317/6 on Day 2", "1st Test. Phillips 118", "in a record year v India."],
     (0, 200, 83), "cricket",
     dict(r_text=255, off=(0, 0), hcap=235, bcap=200, kcap=200,
          pic_r=360, pic_size=38, pic_dang=18)),
    ("EVERYWHERE · CHILDREN", ["WORLD", "CHILDREN'S DAY"],
     ["20 November marks the UN", "day for children's rights", "1989 Convention adopted."],
     (30, 144, 255), "balloon",
     dict(r_text=245, off=(0, 0), hcap=195, bcap=190, kcap=190,
          pic_r=368, pic_size=34, pic_dang=0)),
]

# Vertical offsets of the text lines from the block centre.
OFF_KICK = -72
OFF_HEAD = (-34, 4)
OFF_BODY = (38, 62, 86)


def font_path(bold):
    cands = (["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]
             if bold else
             ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"])
    for p in cands:
        if os.path.exists(p):
            return p
    return None


BOLD_P = font_path(True)
REG_P = font_path(False)


def F(size, bold=True):
    p = BOLD_P if bold else REG_P
    return ImageFont.truetype(p, size) if p else ImageFont.load_default()


def fit(text, size, bold, max_w, min_size=15):
    """Largest font size (<= size) that fits text inside max_w pixels."""
    while size > min_size and F(size, bold).getlength(text) > max_w:
        size -= 1
    return F(size, bold)


def dark(color, f=0.35):
    return tuple(int(v * f) for v in color)


def light(color, f=0.6):
    """Mix a sector colour toward white (for pictogram halos)."""
    return tuple(int(v + (255 - v) * f) for v in color)


def spine(radius, mid_deg):
    a = math.radians(mid_deg)
    return (CX + radius * math.cos(a), CY + radius * math.sin(a))


def text_at(d, cx, cy, text, font, fill, stroke=None):
    d.text((cx, cy), text, font=font, fill=fill, anchor="mm",
           stroke_width=1 if stroke else 0, stroke_fill=stroke or fill)


# ---------------------------------------------------------------- pictograms
# Each draws a simple geometric icon centred at (cx, cy) with size s,
# in the given fill colour. All coordinates are fractions of s.

def pic_cyclone(d, cx, cy, s, fill):
    w = max(4, s // 9)
    for r, a0, a1 in ((0.16, 20, 300), (0.30, 140, 420), (0.44, 260, 540)):
        rr = r * s
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], a0, a1, fill=fill, width=w)
    r = 0.07 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


def pic_megaphone(d, cx, cy, s, fill):
    cone = [(-0.38 * s, -0.15 * s), (0.26 * s, -0.37 * s),
            (0.26 * s, 0.37 * s), (-0.38 * s, 0.15 * s)]
    d.polygon([(cx + x, cy + y) for x, y in cone], fill=fill)
    d.rectangle([cx - 0.30 * s, cy + 0.15 * s, cx - 0.15 * s, cy + 0.46 * s],
                fill=fill)
    for rr in (0.13, 0.23, 0.33):
        r = rr * s
        d.arc([cx + 0.30 * s - r, cy - r, cx + 0.30 * s + r, cy + r],
              -55, 55, fill=fill, width=max(3, s // 14))


def pic_flags(d, cx, cy, s, fill):
    w = max(4, s // 11)
    for px in (-0.26 * s, 0.26 * s):
        d.line([cx + px, cy - 0.44 * s, cx + px, cy + 0.48 * s],
               fill=fill, width=w)
        r = 0.05 * s
        d.ellipse([cx + px - r, cy - 0.50 * s, cx + px + r, cy - 0.40 * s],
                  fill=fill)
    d.polygon([(cx - 0.26 * s, cy - 0.44 * s), (cx - 0.26 * s, cy - 0.16 * s),
               (cx - 0.52 * s, cy - 0.30 * s)], fill=fill)
    d.polygon([(cx + 0.26 * s, cy - 0.44 * s), (cx + 0.26 * s, cy - 0.16 * s),
               (cx + 0.52 * s, cy - 0.30 * s)], fill=fill)


def pic_cricket(d, cx, cy, s, fill):
    # Bat: a rectangle rotated -40 degrees around its centre.
    bx, by = cx - 0.10 * s, cy + 0.10 * s
    lw, ll = 0.20 * s, 0.72 * s
    ang = math.radians(-40)
    ca, sa = math.cos(ang), math.sin(ang)
    pts = []
    for dx, dy in ((-lw / 2, -ll / 2), (lw / 2, -ll / 2),
                   (lw / 2, ll / 2), (-lw / 2, ll / 2)):
        pts.append((bx + dx * ca - dy * sa, by + dx * sa + dy * ca))
    d.polygon(pts, fill=fill)
    ballx, bally, br = cx + 0.30 * s, cy - 0.28 * s, 0.17 * s
    d.ellipse([ballx - br, bally - br, ballx + br, bally + br], fill=fill)
    d.arc([ballx - br * 0.6, bally - br, ballx + br * 0.6, bally + br],
          -60, 60, fill=BG, width=2)


def pic_balloon(d, cx, cy, s, fill):
    bx, by = cx - 0.02 * s, cy - 0.28 * s
    rx, ry = 0.26 * s, 0.31 * s
    d.ellipse([bx - rx, by - ry, bx + rx, by + ry], fill=fill)
    d.polygon([(cx - 0.08 * s, cy + 0.02 * s), (cx + 0.04 * s, cy + 0.02 * s),
               (cx - 0.02 * s, cy + 0.10 * s)], fill=fill)
    pts = [(cx - 0.02 * s, cy + 0.10 * s), (cx + 0.06 * s, cy + 0.22 * s),
           (cx - 0.06 * s, cy + 0.34 * s), (cx + 0.02 * s, cy + 0.46 * s)]
    d.line(pts, fill=fill, width=max(3, s // 16), joint="curve")


PICS = {"cyclone": pic_cyclone, "megaphone": pic_megaphone,
        "flags": pic_flags, "cricket": pic_cricket, "balloon": pic_balloon}


def check_layout(items):
    """Numeric self-check: every text line and pictogram must sit inside the
    wheel, clear of the medallion, and clear of the other pictograms."""
    problems = []
    for label, (x0, y0, x1, y1) in items:
        for cx, cy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
            if math.hypot(cx - CX, cy - CY) > R_OUT - 1:
                problems.append(f"{label!r} corner ({cx:.0f},{cy:.0f}) "
                                f"outside wheel")
        # Distance from medallion centre to the closest point of the box.
        nx = min(max(CX, x0), x1)
        ny = min(max(CY, y0), y1)
        if math.hypot(nx - CX, ny - CY) < R_MED + 2:
            problems.append(f"{label!r} touches medallion")
    pics = [(l, b) for l, b in items if l.endswith("-pic")]
    texts = [(l, b) for l, b in items if not l.endswith("-pic")]
    for pl, (px0, py0, px1, py1) in pics:
        for tl, (tx0, ty0, tx1, ty1) in texts:
            if px0 < tx1 - 1 and tx0 < px1 - 1 and py0 < ty1 - 1 and ty0 < py1 - 1:
                problems.append(f"{pl} overlaps text {tl!r}")
    if problems:
        print("LAYOUT CHECK: %d problem(s)" % len(problems))
        for p in problems:
            print("  -", p)
    else:
        print("LAYOUT CHECK: clean (%d items)" % len(items))


# ------------------------------------------------------------------- build

def build():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header.
    text_at(d, 512, 40, "THE WORLD IN ONE DAY", F(38, True), GOLD)
    text_at(d, 512, 92, "FRIDAY 20 NOVEMBER 2026", F(60, True), WHITE)
    text_at(d, 512, 148,
            "Five stories that defined the day  ·  Sources: IMD · Reuters · ICC · UN",
            F(23, False), SUB)
    d.line([(60, 178), (964, 178)], fill=GOLD, width=3)

    # Wheel sectors, clockwise from the top (mid angles -90, -18, 54, 126, 198).
    bbox = [CX - R_OUT, CY - R_OUT, CX + R_OUT, CY + R_OUT]
    items = []  # (label, (x0, y0, x1, y1)) for the layout self-check
    for i, (kicker, head, body, fill, kind, lay) in enumerate(SECTORS):
        mid = -90 + i * 72
        d.pieslice(bbox, mid - 34.5, mid + 34.5, fill=fill)
        # Deep dark swirl arcs, offset per radius so the wheel reads as turning.
        # Kept thin so they texture the fill without striking through the text.
        for radius, off in ((195, -9), (255, 0), (315, 9)):
            b = [CX - radius, CY - radius, CX + radius, CY + radius]
            d.arc(b, mid - 27 + off, mid + 27 + off, fill=dark(fill, 0.5),
                  width=8)
        # Gold speed ticks near the rim: two per sector, off the spine so
        # they never touch the pictogram. Cheap motion energy at thumbnail.
        for tang in (mid - 24, mid + 24):
            a = math.radians(tang)
            d.line([(CX + 362 * math.cos(a), CY + 362 * math.sin(a)),
                    (CX + 388 * math.cos(a), CY + 388 * math.sin(a))],
                   fill=GOLD, width=7)
        # Pictogram: light halo, then dark drop-shadow, then white icon.
        qx, qy = spine(lay["pic_r"], mid + lay["pic_dang"])
        ps = lay["pic_size"]
        halo = int(ps * 1.15)
        PICS[kind](d, qx, qy, halo, light(fill, 0.65))
        PICS[kind](d, qx + 2, qy + 3, ps, dark(fill, 0.55))
        PICS[kind](d, qx, qy, ps, WHITE)
        items.append((f"{kind}-pic", (qx - halo / 2, qy - halo / 2,
                                      qx + halo / 2, qy + halo / 2)))
        # Text block: stacked vertically on screen, centred on the spine.
        # (Stacking along the spine would splay the lines sideways on the
        # left/right sectors and flip their order on the bottom ones.)
        px, py = spine(lay["r_text"], mid)
        px += lay["off"][0]
        py += lay["off"][1]

        def place(text, cy, font, fill_c, stroke=None):
            w = font.getlength(text)
            h = font.getbbox(text)[3] - font.getbbox(text)[1]
            items.append((text, (px - w / 2, cy - h / 2,
                                 px + w / 2, cy + h / 2)))
            text_at(d, px, cy, text, font, fill_c, stroke=stroke)

        # Kicker.
        place(kicker, py + OFF_KICK, fit(kicker, 22, True, lay["kcap"]), GOLD)
        # Headline, two big lines; the cricket score line gets gold.
        for j, line in enumerate(head):
            colour = GOLD if (kind == "cricket" and j == 1) else WHITE
            place(line, py + OFF_HEAD[j], fit(line, 36, True, lay["hcap"]),
                  colour, stroke=dark(fill, 0.5))
        # Body, three short lines.
        for j, line in enumerate(body):
            place(line, py + OFF_BODY[j], fit(line, 20, False, lay["bcap"], 15),
                  WHITE)
    check_layout(items)

    # Gold frame ring around the wheel.
    d.ellipse(bbox, outline=GOLD, width=3)

    # Central medallion: bold swirl, giant 20, gold ring.
    d.ellipse([CX - R_MED, CY - R_MED, CX + R_MED, CY + R_MED], fill=MED_FILL)
    d.ellipse([CX - R_MED, CY - R_MED, CX + R_MED, CY + R_MED],
              outline=GOLD, width=7)
    d.ellipse([CX - R_MED + 12, CY - R_MED + 12, CX + R_MED - 12, CY + R_MED - 12],
              outline=(127, 231, 220), width=2)
    pic_cyclone(d, 512, 498, 64, SWIRL)
    text_at(d, 512, 592, "20", F(132, True), WHITE)
    text_at(d, 512, 668, "NOV", F(34, True), GOLD)
    text_at(d, 512, 694, "FIVE STORIES", F(20, True), WHITE)

    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build().save(out)
    print("wrote", out)
