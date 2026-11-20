#!/usr/bin/env python3
"""Draw the news-image-20261120 entry: 'THE WORLD IN ONE DAY'.

A five-sector cyclone wheel. Each wedge holds one big flat-illustration
action scene (cyclone, protest crowd, handshake, batsman, children+globe)
with a bold one-line headline, kicker and fact line over a dark scrim in
the outer band. Header names the day; central medallion carries the 20.

PIL only, no external assets, fully deterministic.
Run:  python3 draw.py   ->  writes entry.png (1024x1024) next to this file.
"""

import math
import os

from PIL import Image, ImageChops, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
CX, CY = 512, 608          # wheel centre
R_OUT = 392                # wheel outer radius
R_MED = 138                # medallion radius
R_SCENE = 250              # scene band ends here; label band outside it
R_INNER = 150              # scenes start just outside the medallion

NAVY = (11, 18, 32)
MEDALLION = (12, 27, 46)
GOLD = (242, 183, 5)
GOLD_SOFT = (255, 205, 80)
WHITE = (255, 255, 255)
INK = (11, 21, 38)
SUBLINE = (165, 180, 205)
PALE = (226, 234, 245)

BOLD = "DejaVuSans-Bold.ttf"
REG = "DejaVuSans.ttf"

# sector: (mid angle deg, base colour, kicker, headline, fact)
SECTORS = [
    (-90, (18, 165, 148), "INDIA \u00b7 WEATHER", "AKVAN HITS ODISHA",
     "100 km/h \u00b7 105,000+ evacuated"),
    (-18, (229, 72, 77), "EUROPE \u00b7 YOUTH", "STUDENTS WALK OUT",
     "Strikes across Europe + UK"),
    (54, (245, 158, 11), "SHENZHEN \u00b7 DIPLOMACY", "ALBANESE MEETS XI",
     "Fifth meeting, APEC week"),
    (126, (34, 168, 92), "WELLINGTON \u00b7 CRICKET", "NICHOLLS 146*",
     "NZ 317/6 \u00b7 Phillips 118"),
    (198, (47, 128, 237), "EVERYWHERE \u00b7 CHILDREN", "WORLD CHILDREN'S DAY",
     "UN day for children's rights \u00b7 1989"),
]


def pol(r, deg):
    """Point at radius r and screen-polar angle deg (0=east, clockwise)."""
    a = math.radians(deg)
    return (CX + r * math.cos(a), CY + r * math.sin(a))


def chord(r, half=36.0):
    return 2.0 * r * math.sin(math.radians(half))


def row_span(y_abs, mid):
    """Horizontal span of the wedge at absolute y: (xmin, xmax) relative
    to the wheel centre, for points inside the annulus and within
    +/-33 deg of the sector mid-angle. Text rows are centred in this
    span, so nothing can overflow the wedge or flip order."""
    y = y_abs - CY
    xs = []
    x = -388
    while x <= 388:
        r = math.hypot(x, y)
        if R_INNER <= r <= 388:
            ang = math.degrees(math.atan2(y, x))
            diff = (ang - mid + 180.0) % 360.0 - 180.0
            if abs(diff) <= 33.0:
                xs.append(x)
        x += 2
    if not xs:
        return (-40, 40)
    return (min(xs), max(xs))


def font(name, size):
    return ImageFont.truetype(name, int(size))


def fit(name, text, size, max_w):
    """Largest font size (down to 14) whose text fits max_w."""
    while size > 14:
        f = font(name, size)
        if f.getlength(text) <= max_w:
            return f
        size -= 1
    return font(name, 14)


def disc(d, centre, r, fill, outline=None, width=1):
    x, y = centre
    d.ellipse([x - r, y - r, x + r, y + r], fill=fill,
              outline=outline, width=width)


def line_p(d, r1, a1, r2, a2, fill, width):
    d.line([pol(r1, a1), pol(r2, a2)], fill=fill, width=width)


def arc_at(d, centre, r, start, end, fill, width):
    x, y = centre
    d.arc([x - r, y - r, x + r, y + r], start, end, fill=fill, width=width)


def arc_wheel(d, r, start, end, fill, width):
    d.arc([CX - r, CY - r, CX + r, CY + r], start, end, fill=fill, width=width)


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def rrect_points(cx, cy, w, h, angle_deg):
    a = math.radians(angle_deg)
    ca, sa = math.cos(a), math.sin(a)
    pts = []
    for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2),
                   (w / 2, h / 2), (-w / 2, h / 2)):
        pts.append((cx + dx * ca - dy * sa, cy + dx * sa + dy * ca))
    return pts


# ---------------------------------------------------------------- scenes
# Each scene draws on its own layer, in wheel polar coordinates, inside
# one wedge (mid angle). The layer is clipped to the wedge afterwards.

def scene_cyclone(d, mid):
    """Huge spiral, rain streaks, waves on a coastline."""
    s = pol(215, mid)
    # spiral arms around the eye
    for rr, start, col, wd in (
            (26, 15, WHITE, 12), (50, 140, (127, 231, 216), 12),
            (74, 255, WHITE, 11), (92, 30, (127, 231, 216), 10)):
        arc_at(d, s, rr, start, start + 295, col, wd)
    disc(d, s, 15, WHITE)
    disc(d, s, 6, (11, 110, 99))
    # rain: diagonal white streaks across the outer scene band
    for k in range(7):
        a = mid - 30 + k * 10
        line_p(d, 292, a, 258, a - 7, (220, 250, 248), 5)
    # waves hugging the inner edge (wheel-centred arcs)
    arc_wheel(d, 172, mid - 33, mid + 33, WHITE, 8)
    arc_wheel(d, 192, mid - 33, mid + 33, (127, 231, 216), 7)
    # wind swirls at the wedge sides
    arc_at(d, pol(205, mid - 27), 17, 200, 140, WHITE, 6)
    arc_at(d, pol(205, mid + 27), 17, 20, 320, WHITE, 6)
    # one arm spills up toward the label band
    arc_at(d, s, 118, 300, 355, (127, 231, 216), 10)


def scene_crowd(d, mid):
    """Raised fists, placards and a megaphone on diagonal lines."""
    # crowd mass along the inner edge
    arc_wheel(d, 178, mid - 34, mid + 34, (20, 27, 46), 34)
    for k in range(5):
        a = mid - 27 + k * 13.5
        disc(d, pol(192, a), 14, (20, 27, 46))
    # raised fists: thick navy arms ending in fists, kept to the wedge
    # edges so they never cross the label rows in the middle
    for k in (-1, 1):
        a = mid + k * 26
        line_p(d, 200, a, 240, a + 3, (20, 27, 46), 18)
        disc(d, pol(248, a + 3), 18, (20, 27, 46), outline=WHITE, width=3)
    # placards: two upright cream boards at the wedge edges, each with
    # one bold mark (kept near-upright so they read as signs)
    marks = ("!", "star")
    for k, mark in enumerate(marks):
        a = mid + (-28 if k == 0 else 28)
        px, py = pol(255, a)
        d.line([(px, py + 30), pol(196, a)], fill=(20, 27, 46), width=7)
        board = rrect_points(px, py, 88, 62, (k - 0.5) * 16)
        d.polygon(board, fill=(255, 243, 214), outline=(20, 27, 46))
        if mark == "!":
            d.text((px, py - 2), "!", font=font(BOLD, 40),
                   fill=(20, 27, 46), anchor="mm")
        elif mark == "star":
            d.polygon(star_points(px, py, 20, 8), fill=GOLD,
                      outline=(20, 27, 46))
        else:
            bx, by = px, py
            d.polygon([(bx + 4, by - 20), (bx - 12, by + 4), (bx - 1, by + 4),
                       (bx - 5, by + 20), (bx + 12, by - 4), (bx + 1, by - 4)],
                      fill=(20, 27, 46))
    # megaphone at the lower side
    mx, my = pol(232, mid + 27)
    d.polygon([(mx - 34, my - 16), (mx + 28, my - 34), (mx + 28, my + 34),
               (mx - 34, my + 16)], fill=WHITE, outline=(20, 27, 46))
    d.line([(mx - 34, my - 16), (mx - 34, my + 16)], fill=(20, 27, 46),
           width=6)
    # motion lines
    for k in range(3):
        a = mid - 30 + k * 8
        line_p(d, 292, a, 272, a - 4, (255, 217, 217), 5)


def scene_handshake(d, mid):
    """Two flags behind two figures shaking hands; gold sun behind."""
    # flag fields split down the wedge middle
    d.pieslice([CX - 300, CY - 300, CX + 300, CY + 300],
               mid - 34.5, mid, fill=(30, 79, 163))
    d.pieslice([CX - 300, CY - 300, CX + 300, CY + 300],
               mid, mid + 34.5, fill=(208, 52, 44))
    # Southern Cross stars on the blue half
    for rr, aa, sr in ((255, mid - 24, 7), (228, mid - 12, 5),
                       (262, mid - 10, 6), (240, mid - 27, 5),
                       (205, mid - 20, 4)):
        x, y = pol(rr, aa)
        d.polygon(star_points(x, y, sr, sr * 0.45), fill=WHITE)
    # big + small gold stars on the red half
    x, y = pol(245, mid + 17)
    d.polygon(star_points(x, y, 20, 8), fill=GOLD)
    for rr, aa in ((272, mid + 26), (218, mid + 27), (258, mid + 8)):
        x, y = pol(rr, aa)
        d.polygon(star_points(x, y, 8, 3.5), fill=GOLD)
    # gold sun behind the handshake
    disc(d, pol(210, mid), 48, GOLD)
    # two figures: crisp head-and-shoulder silhouettes, arms reaching
    # to the centre where the hands meet
    for side in (-1, 1):
        hx, hy = pol(258, mid + side * 15)
        disc(d, (hx, hy), 16, (20, 32, 46), outline=WHITE, width=3)
        shx, shy = pol(228, mid + side * 17)
        wax, way = pol(198, mid + side * 10)
        mx, my = (shx + wax) / 2.0, (shy + way) / 2.0
        ang = math.degrees(math.atan2(way - shy, wax - shx))
        d.polygon(rrect_points(mx, my, 46, 62, ang),
                  fill=(20, 32, 46), outline=WHITE)
        hx2, hy2 = pol(232, mid + side * 16)
        gx, gy = pol(214, mid)
        d.line([(hx2, hy2), (gx, gy)], fill=(20, 32, 46), width=14)
    # handshake burst at the meeting point
    bx, by = pol(214, mid)
    d.polygon(star_points(bx, by, 26, 11, n=8), fill=WHITE,
              outline=GOLD)
    disc(d, (bx, by), 8, GOLD)


def scene_cricket(d, mid):
    """Batsman mid-swing on a diagonal pitch, ball flying, stumps."""
    # pitch strip, diagonal across the wedge
    line_p(d, 168, mid - 28, 296, mid + 22, (239, 227, 194), 36)
    d.line([pol(168, mid - 28), pol(296, mid + 22)], fill=(255, 255, 255),
           width=3)
    # stumps at the lower end of the pitch
    for k in (-1, 0, 1):
        a = mid - 24 + k * 4
        line_p(d, 196, a, 214, a, GOLD, 8)
    line_p(d, 214, mid - 28, 214, mid - 20, GOLD, 5)
    # starburst + ball flying to the upper corner, clear of the labels
    bx, by = pol(350, mid - 33)
    d.polygon(star_points(bx, by, 34, 13, n=8), fill=WHITE)
    disc(d, (bx, by), 15, (200, 40, 40), outline=WHITE, width=3)
    arc_at(d, (bx, by), 9, 200, 340, WHITE, 2)
    for k in range(3):
        a = mid - 28 - k * 3
        line_p(d, 325 - k * 12, a, 310 - k * 12, a - 2, WHITE, 4)
    # batsman, scaled up: white kit, green helmet, mid-swing
    hx, hy = pol(238, mid + 4)
    disc(d, (hx, hy), 18, (245, 239, 224), outline=(20, 32, 46), width=3)
    arc_at(d, (hx, hy), 18, 180, 360, (34, 168, 92), 8)
    wx, wy = pol(196, mid + 8)
    sx, sy = pol(226, mid + 5)
    d.polygon([(sx - 24, sy - 16), (sx + 24, sy - 16), (wx + 16, wy + 14),
               (wx - 16, wy + 14)], fill=(245, 239, 224),
              outline=(20, 32, 46))
    d.line([(wx, wy), pol(162, mid - 2)], fill=(245, 239, 224), width=15)
    d.line([(wx, wy), pol(166, mid + 18)], fill=(245, 239, 224), width=15)
    # arms + bat sweeping up-outward
    ax, ay = pol(232, mid + 2)
    gx, gy = pol(266, mid - 8)
    d.line([(ax, ay), (gx, gy)], fill=(245, 239, 224), width=14)
    d.line([(gx, gy), pol(285, mid - 20)], fill=(247, 239, 216), width=20)
    d.line([(gx, gy), pol(285, mid - 20)], fill=(20, 32, 46), width=2)


def scene_children(d, mid):
    """Globe with land, joyful children, balloons and sparkles."""
    gx, gy = pol(230, mid)
    disc(d, (gx, gy), 80, (94, 168, 232), outline=WHITE, width=4)
    # land blobs kept inside the globe
    d.ellipse([gx - 58, gy - 52, gx - 10, gy - 8], fill=(63, 163, 77))
    d.ellipse([gx + 4, gy + 10, gx + 56, gy + 54], fill=(63, 163, 77))
    d.ellipse([gx + 20, gy - 54, gx + 58, gy - 20], fill=(63, 163, 77))
    arc_at(d, (gx, gy), 44, 200, 340, WHITE, 3)
    arc_at(d, (gx, gy), 64, 20, 160, WHITE, 3)
    # two children with raised arms, flanking the globe
    for side, col in ((-1, (255, 210, 63)), (1, (255, 107, 157))):
        hx, hy = pol(246, mid + side * 25)
        disc(d, (hx, hy), 17, (242, 196, 155), outline=(20, 32, 46),
             width=2)
        bx, by = pol(210, mid + side * 25)
        d.polygon([(bx - 22, by - 14), (bx + 22, by - 14), (bx + 14, by + 26),
                   (bx - 14, by + 26)], fill=col, outline=(20, 32, 46))
        ax, ay = pol(220, mid + side * 25)
        d.line([(ax, ay), pol(258, mid + side * 31)], fill=col, width=10)
        d.line([(ax, ay), pol(258, mid + side * 19)], fill=col, width=10)
    # balloons rising at the sides
    for rr, aa, col in ((292, mid - 28, (229, 72, 77)),
                        (300, mid + 4, (255, 210, 63)),
                        (290, mid + 28, (255, 107, 157))):
        bx, by = pol(rr, aa)
        d.line([(bx, by + 20), pol(rr - 42, aa)], fill=WHITE, width=3)
        disc(d, (bx, by), 22, col, outline=WHITE, width=3)
        d.polygon([(bx - 7, by + 20), (bx + 7, by + 20), (bx, by + 30)],
                  fill=col)
    # sparkles
    for rr, aa in ((168, mid - 30), (172, mid + 30), (268, mid - 14)):
        x, y = pol(rr, aa)
        d.polygon(star_points(x, y, 11, 4, n=4), fill=GOLD_SOFT)


SCENES = {
    -90: scene_cyclone,
    -18: scene_crowd,
    54: scene_handshake,
    126: scene_cricket,
    198: scene_children,
}


def wedge_mask(mid):
    """White annular sector (r 150..390, mid +/-34.5 deg) on black."""
    m = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(m)
    md.pieslice([CX - 390, CY - 390, CX + 390, CY + 390],
                mid - 34.5, mid + 34.5, fill=255)
    md.ellipse([CX - R_INNER, CY - R_INNER, CX + R_INNER, CY + R_INNER],
               fill=0)
    return m


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # ---- header
    d.text((512, 52), "THE WORLD IN ONE DAY", font=font(BOLD, 52),
           fill=GOLD, anchor="mm")
    d.text((512, 108), "FRIDAY 20 NOVEMBER 2026", font=font(BOLD, 62),
           fill=WHITE, anchor="mm")
    d.text((512, 156),
           "Five stories that defined the day  \u00b7  Sources: IMD \u00b7 Reuters \u00b7 ICC \u00b7 UN",
           font=font(REG, 23), fill=SUBLINE, anchor="mm")
    d.line([(60, 182), (964, 182)], fill=GOLD, width=3)

    # ---- wheel base + scenes
    for mid, colour, _k, _h, _f in SECTORS:
        d.pieslice([CX - R_OUT, CY - R_OUT, CX + R_OUT, CY + R_OUT],
                   mid - 34.5, mid + 34.5, fill=colour)
    for mid, _c, _k, _h, _f in SECTORS:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        SCENES[mid](ld, mid)
        alpha = ImageChops.darker(layer.split()[3], wedge_mask(mid))
        img.paste(layer, (0, 0), alpha)

    # ---- dark scrim over the outer label band, then labels
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for mid, _c, _k, _h, _f in SECTORS:
        od.pieslice([CX - 390, CY - 390, CX + 390, CY + 390],
                    mid - 34.5, mid + 34.5, fill=(10, 17, 34, 115))
        od.pieslice([CX - R_SCENE, CY - R_SCENE, CX + R_SCENE, CY + R_SCENE],
                    mid - 34.5, mid + 34.5, fill=(0, 0, 0, 0))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img)

    # labels: three horizontal rows per wedge, stacked top-to-bottom
    # (kicker -> headline -> fact) around an anchor on the sector axis;
    # each row is centred in the wedge's actual horizontal span at its
    # own height, so side wedges cannot overflow and bottom wedges
    # cannot flip reading order.
    for mid, _c, kicker, headline, fact in SECTORS:
        ax, ay = pol(318, mid)
        for dy, text, size0, fill, name in (
                (-38, kicker, 19, GOLD, BOLD),
                (0, headline, 33, WHITE, BOLD),
                (38, fact, 19, PALE, REG)):
            y = ay + dy
            x0, x1 = row_span(y, mid)
            tx = CX + (x0 + x1) / 2.0
            sw = 3 if name == BOLD and size0 > 20 else 2
            d.text((tx, y), text,
                   font=fit(name, text, size0, (x1 - x0) - 14),
                   fill=fill, anchor="mm", stroke_width=sw,
                   stroke_fill=INK)

    # ---- gold rim, boundary ticks, medallion
    d.ellipse([CX - R_OUT, CY - R_OUT, CX + R_OUT, CY + R_OUT],
              outline=GOLD, width=4)
    for mid, _c, _k, _h, _f in SECTORS:
        b = mid + 36
        d.line([pol(R_OUT - 8, b), pol(R_OUT + 2, b)], fill=GOLD, width=4)
    d.ellipse([CX - R_MED, CY - R_MED, CX + R_MED, CY + R_MED],
              fill=MEDALLION, outline=GOLD, width=6)
    d.ellipse([CX - R_MED + 12, CY - R_MED + 12,
               CX + R_MED - 12, CY + R_MED - 12],
              outline=(242, 183, 5), width=2)
    d.text((512, 578), "20", font=font(BOLD, 148), fill=WHITE, anchor="mm")
    d.text((512, 666), "NOV", font=font(BOLD, 44), fill=GOLD, anchor="mm")
    d.text((512, 704), "FIVE STORIES", font=font(BOLD, 20), fill=GOLD,
           anchor="mm")

    img.save(OUT, "PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
