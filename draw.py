#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news infographic for make.fun.

One image, 1024x1024: a masthead naming the day, then a five-sector
"cyclone wheel" — the day's storm as a spinning disc, each of its five
sectors one of the day's stories. Everything is drawn with PIL shapes
and text, so every word is spelled exactly as written here.
"""
import math
import textwrap

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
OUT = "entry.png"

NAVY = (11, 21, 36)
NAVY_SOFT = (16, 30, 50)
GOLD = (232, 184, 64)
WHITE = (255, 255, 255)
MIST = (214, 224, 235)
FAINT = (148, 163, 184)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


F_DATE = font("DejaVuSans-Bold.ttf", 60)
F_KICK = font("DejaVuSans-Bold.ttf", 27)
F_SUB = font("DejaVuSans.ttf", 20)
F_SECT_KICK = font("DejaVuSans-Bold.ttf", 18)
F_HEAD = font("DejaVuSans-Bold.ttf", 26)
F_BODY = font("DejaVuSans.ttf", 18)
F_DISC_BIG = font("DejaVuSans-Bold.ttf", 88)
F_DISC_SMALL = font("DejaVuSans-Bold.ttf", 26)
F_DISC_TINY = font("DejaVuSans-Bold.ttf", 17)

# (kicker, headline, detail, sector colour, mid-angle in degrees)
STORIES = [
    (
        "INDIA  ·  WEATHER",
        "AKVAN HITS ODISHA",
        "Severe cyclone crosses the coast near Gopalpur at noon — "
        "winds 100 km/h; 105,000+ people evacuated to shelters.",
        (14, 124, 123),
        -90,
    ),
    (
        "EUROPE  ·  YOUTH",
        "STUDENTS WALK OUT",
        "Young people strike across Europe and the UK: “Fight for our "
        "futures, not their wars.”",
        (169, 50, 38),
        -17,
    ),
    (
        "SHENZHEN  ·  DIPLOMACY",
        "ALBANESE MEETS XI",
        "Australia’s PM meets China’s president in Shenzhen — their "
        "fifth formal meeting, on APEC week.",
        (156, 107, 26),
        55,
    ),
    (
        "WELLINGTON  ·  CRICKET",
        "NICHOLLS 146*",
        "New Zealand reach 317/6 on Day 2 of the first Test; Phillips "
        "hits 118 in a record year against India.",
        (30, 122, 70),
        127,
    ),
    (
        "EVERYWHERE  ·  CHILDREN",
        "WORLD CHILDREN’S DAY",
        "20 November marks the UN day for children’s rights — the date "
        "the 1989 Convention was adopted.",
        (31, 111, 178),
        199,
    ),
]

CX, CY = 512, 586
R_OUT, R_IN = 430, 148


def wrap(text, fnt, width_px):
    """Greedy word wrap to a pixel width."""
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if fnt.getlength(trial) <= width_px or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def point(angle_deg, radius):
    a = math.radians(angle_deg)
    return (CX + radius * math.cos(a), CY + radius * math.sin(a))


def draw_cyclone(d, cx, cy, r, colour, width=5):
    """A spiral of three broken arcs, like a storm seen from above."""
    for i, (rad, start, end) in enumerate(
        [(r, 20, 300), (r * 0.66, 140, 420), (r * 0.36, 260, 540)]
    ):
        box = [cx - rad, cy - rad, cx + rad, cy + rad]
        d.arc(box, start, end, fill=colour, width=width)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=colour)


def draw_megaphone(d, cx, cy, s, colour):
    d.polygon(
        [(cx - s, cy - s * 0.45), (cx + s * 0.7, cy - s * 0.9),
         (cx + s * 0.7, cy + s * 0.9), (cx - s, cy + s * 0.45)],
        fill=colour,
    )
    d.rectangle([cx - s * 1.25, cy - s * 0.25, cx - s * 0.85, cy + s * 0.55],
                fill=colour)


def draw_flags(d, cx, cy, s, colour):
    d.line([cx - s * 0.55, cy - s, cx - s * 0.55, cy + s], fill=colour, width=4)
    d.line([cx + s * 0.55, cy - s, cx + s * 0.55, cy + s], fill=colour, width=4)
    d.polygon([(cx - s * 0.55, cy - s), (cx - s * 0.05, cy - s * 0.72),
               (cx - s * 0.55, cy - s * 0.44)], fill=colour)
    d.polygon([(cx + s * 0.55, cy - s), (cx + s * 1.05, cy - s * 0.72),
               (cx + s * 0.55, cy - s * 0.44)], fill=GOLD)


def draw_cricket(d, cx, cy, s, colour):
    for k in range(3):
        x = cx - s * 0.55 + k * s * 0.22
        d.rectangle([x, cy - s * 0.5, x + 5, cy + s * 0.35], fill=colour)
    d.polygon([(cx + s * 0.1, cy - s), (cx + s * 0.45, cy - s * 0.85),
               (cx + s * 0.75, cy + s * 0.15), (cx + s * 0.4, cy + s * 0.3)],
              fill=colour)
    d.ellipse([cx + s * 0.55, cy + s * 0.55, cx + s * 0.95, cy + s * 0.95],
              fill=GOLD)


def draw_children(d, cx, cy, s, colour):
    for k, dx in enumerate((-0.7, 0, 0.7)):
        d.ellipse([cx + dx * s - s * 0.22, cy - s * 0.55,
                   cx + dx * s + s * 0.22, cy - s * 0.11], fill=colour)
    d.arc([cx - s * 0.7, cy - s * 0.3, cx + s * 0.7, cy + s * 0.9],
          15, 165, fill=colour, width=5)


ICONS = [draw_cyclone, draw_megaphone, draw_flags, draw_cricket, draw_children]


def main():
    img = Image.new("RGB", (SIZE, SIZE), NAVY)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.text((48, 22), "THE WORLD IN ONE DAY", font=F_KICK, fill=GOLD)
    d.text((48, 54), "FRIDAY 20 NOVEMBER 2026", font=F_DATE, fill=WHITE)
    d.text((48, 122), "Five stories that defined the day  ·  Sources: IMD · Reuters · ICC · UN",
           font=F_SUB, fill=FAINT)
    d.line([48, 150, SIZE - 48, 150], fill=GOLD, width=3)

    # ---- The wheel: five sectors around one storm ----------------------
    for (kicker, headline, detail, colour, angle) in STORIES:
        colour = tuple(min(255, int(c * 1.14)) for c in colour)
        d.pieslice([CX - R_OUT, CY - R_OUT, CX + R_OUT, CY + R_OUT],
                   angle - 35, angle + 35, fill=colour)
        # thin navy gap is left by the 2-degree inset on each side
        d.pieslice([CX - R_OUT, CY - R_OUT, CX + R_OUT, CY + R_OUT],
                   angle - 37, angle - 35, fill=NAVY)
        d.pieslice([CX - R_OUT, CY - R_OUT, CX + R_OUT, CY + R_OUT],
                   angle + 35, angle + 37, fill=NAVY)

        # faint concentric ring texture inside the sector, in a darker
        # tint of its own colour, laid down before the text
        dark = tuple(int(c * 0.55) for c in colour)
        sector_mask = Image.new("L", (SIZE, SIZE), 0)
        ImageDraw.Draw(sector_mask).pieslice(
            [CX - R_OUT, CY - R_OUT, CX + R_OUT, CY + R_OUT],
            angle - 35, angle + 35, fill=255)
        ring_mask = Image.new("L", (SIZE, SIZE), 0)
        rd = ImageDraw.Draw(ring_mask)
        for rr in (215, 295, 375):
            rd.arc([CX - rr, CY - rr, CX + rr, CY + rr],
                   angle - 33, angle + 33, fill=255, width=14)
        from PIL import ImageChops
        combined = ImageChops.multiply(sector_mask, ring_mask)
        tint = Image.new("RGB", (SIZE, SIZE), dark)
        img.paste(tint, (0, 0), combined)
        d = ImageDraw.Draw(img)

        # text block, centred on the sector's mid-line
        tx, ty = point(angle, 330)
        lines = [(kicker, F_SECT_KICK, GOLD)]
        for ln in wrap(headline, F_HEAD, 280):
            lines.append((ln, F_HEAD, WHITE))
        for ln in wrap(detail, F_BODY, 290):
            lines.append((ln, F_BODY, MIST))
        heights = [fnt.getbbox("Ag")[3] + 4 for _, fnt, _ in lines]
        total = sum(heights)
        y = ty - total / 2
        for (text, fnt, colour_text), h in zip(lines, heights):
            d.text((tx, y), text, font=fnt, fill=colour_text, anchor="ma")
            y += h

    # ---- Hub: the date medallion in the middle of the storm ------------
    d.ellipse([CX - R_IN, CY - R_IN, CX + R_IN, CY + R_IN],
              fill=(14, 58, 58), outline=GOLD, width=4)
    draw_cyclone(d, CX, CY - 62, 30, (120, 220, 215), width=4)
    d.text((CX, CY + 8), "20", font=F_DISC_BIG, fill=WHITE, anchor="mm")
    d.text((CX, CY + 78), "NOV", font=F_DISC_SMALL, fill=GOLD, anchor="ma")
    d.text((CX, CY + 108), "FIVE STORIES", font=F_DISC_TINY, fill=MIST, anchor="ma")

    img.save(OUT, optimize=True)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
