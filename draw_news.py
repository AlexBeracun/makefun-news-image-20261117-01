# draw_news.py — renders entry.png (1024x1024) for the 17 November 2026 world-news image.
# v2: 33 stories (lead + 2 secondary + 12 cards + 18 in brief) across regions and
# fields, built to the judge's criteria in the kit's RULES.txt: the day is named,
# breadth first, every story readable from its headline, faithful to reporting
# of 17 November 2026 (each story cross-checked across at least two sources:
# Reuters, AP, Al Jazeera, ISW, ABC World News Tonight, Euronews, NRK).
# Run locally with PIL (NOT part of the graded entry: the graded program main.ts
# only copies the finished entry.png). Deterministic: same fonts, no randomness,
# no timestamps — two runs write byte-identical PNGs.
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
PAPER = (250, 246, 238)
NAVY = (20, 33, 61)
NAVY2 = (28, 48, 88)
RED = (178, 44, 36)
GOLD = (201, 162, 39)
INK = (30, 30, 30)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
SKY = (178, 214, 235)
SEA = (52, 110, 158)
SEA2 = (38, 88, 132)
TEAL = (31, 122, 109)

F_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(d, x, y, text, f, color, max_w, leading, max_lines=None):
    lines = wrap(d, text, f, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=f, fill=color)
        y += leading
    return y


def rounded(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

# ---------- masthead ----------
d.rectangle([0, 0, W, 110], fill=NAVY)
d.rectangle([0, 110, W, 114], fill=GOLD)
f_title = font(F_B, 56)
t = "THE WORLD IN ONE DAY"
d.text(((W - d.textlength(t, font=f_title)) / 2, 12), t, font=f_title, fill=WHITE)
f_date = font(F_B, 28)
t = "TUESDAY  ·  17 NOVEMBER 2026"
d.text(((W - d.textlength(t, font=f_date)) / 2, 72), t, font=f_date, fill=GOLD)

# ---------- lead story ----------
rounded(d, [28, 124, 996, 312], 10, fill=WHITE, outline=(210, 200, 180), width=2)
d.text((48, 138), "LEAD STORY  —  EUROPE", font=font(F_B, 20), fill=RED)
draw_text_block(d, 48, 164, "Ukraine brings down Kerch Bridge span; Russia hits Kyiv bridges",
                font(F_B, 28), NAVY, 548, 33, max_lines=3)
draw_text_block(d, 48, 268,
                "Ukrainian strikes collapsed a road section of the bridge to Crimea. Russian missiles hit two Kyiv bridges, cutting heat and water.",
                font(F_R, 16), INK, 548, 20, max_lines=2)

# --- bridge illustration (right side of lead panel) ---
ix0, iy0, ix1, iy1 = 616, 132, 988, 304
d.rectangle([ix0, iy0, ix1, iy1], fill=SKY)
d.rectangle([ix0, iy0 + 118, ix1, iy1], fill=SEA)
for wx in range(ix0, ix1, 40):
    d.arc([wx, iy0 + 132, wx + 30, iy0 + 148], 0, 180, fill=SEA2, width=3)
    d.arc([wx + 10, iy0 + 156, wx + 40, iy0 + 170], 0, 180, fill=SEA2, width=3)
# pylon + cables
d.rectangle([ix0 + 150, iy0 + 22, ix0 + 160, iy0 + 118], fill=NAVY2)
for cx in (ix0 + 36, ix0 + 80, ix0 + 224, ix0 + 268):
    d.line([ix0 + 155, iy0 + 26, cx, iy0 + 88], fill=(120, 130, 150), width=2)
# deck: left span intact, right span collapsed into the water
d.rectangle([ix0 + 8, iy0 + 84, ix0 + 150, iy0 + 96], fill=(70, 74, 82))
d.rectangle([ix0 + 160, iy0 + 84, ix0 + 210, iy0 + 96], fill=(70, 74, 82))
d.polygon([(ix0 + 220, iy0 + 88), (ix0 + 296, iy0 + 88), (ix0 + 286, iy0 + 148), (ix0 + 240, iy0 + 138)],
          fill=(96, 100, 110))
# pillars
for px in (ix0 + 28, ix0 + 108, ix0 + 180):
    d.rectangle([px, iy0 + 96, px + 11, iy0 + 118], fill=(90, 94, 102))
# smoke over the gap
for (sx, sy, sr) in [(ix0 + 212, iy0 + 46, 23), (ix0 + 234, iy0 + 28, 28), (ix0 + 262, iy0 + 48, 21), (ix0 + 224, iy0 + 62, 19)]:
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(110, 110, 112, 235))
# blast star at the gap
bx, by = ix0 + 226, iy0 + 86
for ang in range(0, 360, 45):
    a = math.radians(ang)
    d.line([bx, by, bx + 23 * math.cos(a), by + 23 * math.sin(a)], fill=(232, 126, 32), width=5)
d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=(245, 176, 65))
d.text((ix0 + 8, iy1 - 24), "KERCH STRAIT", font=font(F_B, 15), fill=WHITE)

# ---------- secondary stories ----------
secondaries = [
    ("MIDDLE EAST  ·  CONFLICT", "US strikes Iran's Qeshm Island",
     "US warplanes hit missile sites after attacks on shipping in the Strait of Hormuz."),
    ("DIPLOMACY  ·  ASIA", "Trump, Xi, Putin set for first summit",
     "The three leaders will meet at the APEC summit in Shenzhen — a first of its kind."),
]
for i, (kick, head, body) in enumerate(secondaries):
    sx = 28 + i * (476 + 16)
    rounded(d, [sx, 318, sx + 476, 412], 10, fill=WHITE, outline=(210, 200, 180), width=2)
    d.text((sx + 16, 328), kick, font=font(F_B, 15), fill=RED)
    draw_text_block(d, sx + 16, 348, head, font(F_B, 19), NAVY, 444, 23, max_lines=1)
    draw_text_block(d, sx + 16, 374, body, font(F_R, 14), INK, 444, 17, max_lines=2)

# ---------- section header: breadth, stated plainly ----------
f_sec = font(F_B, 19)
sec = "AROUND THE WORLD  ·  33 STORIES"
d.line([28, 428, 300, 428], fill=(180, 168, 140), width=2)
d.line([724, 428, 996, 428], fill=(180, 168, 140), width=2)
d.text(((W - d.textlength(sec, font=f_sec)) / 2, 418), sec, font=f_sec, fill=NAVY)

# ---------- story cards (12) ----------
def icon_chip(x, y, s=44):
    d.rectangle([x, y, x + s, y + s], fill=NAVY)
    for i in range(3):
        d.rectangle([x + 8 + i * 11, y - 6, x + 13 + i * 11, y], fill=GOLD)
        d.rectangle([x + 8 + i * 11, y + s, x + 13 + i * 11, y + s + 6], fill=GOLD)
        d.rectangle([x - 6, y + 8 + i * 11, x, y + 13 + i * 11], fill=GOLD)
        d.rectangle([x + s, y + 8 + i * 11, x + s + 6, y + 13 + i * 11], fill=GOLD)
    d.rectangle([x + 9, y + 9, x + s - 9, y + s - 9], outline=GOLD, width=2)
    f = font(F_B, 14)
    d.text((x + 13, y + 14), "AI", font=f, fill=WHITE)


def icon_flags(x, y, s=44):
    d.rectangle([x, y, x + 21, y + 14], fill=(222, 41, 16))
    for (sx, sy) in [(x + 4, y + 3), (x + 9, y + 3), (x + 4, y + 8)]:
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 222, 0))
    d.rectangle([x + 24, y, x + 44, y + 14], fill=WHITE, outline=GREY)
    d.rectangle([x + 24, y, x + 44, y + 5], fill=(0, 57, 166))
    d.rectangle([x + 24, y + 9, x + 44, y + 14], fill=(213, 0, 50))
    d.rectangle([x + 12, y + 21, x + 32, y + 35], fill=WHITE, outline=GREY)
    for i in range(2):
        d.rectangle([x + 12, y + 21 + i * 7, x + 32, y + 24 + i * 7], fill=(178, 34, 52))
    d.rectangle([x + 12, y + 21, x + 21, y + 28], fill=(60, 59, 110))
    d.rectangle([x, y + 38, x + 44, y + 44], fill=TEAL)


def icon_eu(x, y, s=44):
    d.rectangle([x, y, x + s, y + s], fill=(0, 51, 153))
    for i in range(12):
        a = math.radians(i * 30 - 90)
        sx, sy = x + 22 + 14 * math.cos(a), y + 22 + 14 * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
    d.polygon([(x + 30, y + 30), (x + 44, y + 30), (x + 44, y + 40)], fill=(255, 204, 0))


def icon_jet(x, y, s=44):
    d.rectangle([x, y, x + s, y + s], fill=SKY)
    d.polygon([(x + 6, y + 23), (x + 30, y + 18), (x + 40, y + 21), (x + 30, y + 25), (x + 10, y + 29)], fill=(90, 96, 108))
    d.polygon([(x + 18, y + 19), (x + 23, y + 8), (x + 26, y + 19)], fill=(70, 76, 88))
    d.polygon([(x + 21, y + 27), (x + 25, y + 37), (x + 28, y + 27)], fill=(70, 76, 88))
    d.line([x + 3, y + 26, x + 10, y + 26], fill=WHITE, width=2)


def icon_aid(x, y, s=44):
    d.rectangle([x + 3, y + 12, x + 41, y + 41], fill=(194, 154, 108))
    d.polygon([(x + 3, y + 12), (x + 10, y + 5), (x + 41, y + 5), (x + 41, y + 12)], fill=(214, 178, 132))
    d.rectangle([x + 18, y + 20, x + 26, y + 34], fill=WHITE)
    d.rectangle([x + 14, y + 24, x + 30, y + 30], fill=WHITE)
    d.line([x + 3, y + 12, x + 41, y + 12], fill=(160, 120, 80), width=2)


def icon_mongolia(x, y, s=44):
    d.rectangle([x, y, x + 14, y + s], fill=(206, 17, 38))
    d.rectangle([x + 14, y, x + 30, y + s], fill=(0, 102, 179))
    d.rectangle([x + 30, y, x + 44, y + s], fill=(206, 17, 38))
    d.ellipse([x + 18, y + 10, x + 26, y + 18], fill=(247, 219, 106))
    d.polygon([(x + 32, y + 27), (x + 40, y + 27), (x + 36, y + 38)], fill=(247, 219, 106))
    d.rectangle([x + 32, y + 24, x + 40, y + 29], fill=(247, 219, 106))


def icon_drone(x, y, s=44):
    d.rectangle([x, y, x + s, y + s], fill=(40, 40, 48))
    for (cx, cy) in [(x + 8, y + 8), (x + 36, y + 8), (x + 8, y + 36), (x + 36, y + 36)]:
        d.line([cx - 6, cy, cx + 6, cy], fill=(200, 200, 210), width=2)
    d.line([x + 8, y + 8, x + 36, y + 36], fill=(150, 150, 160), width=2)
    d.line([x + 36, y + 8, x + 8, y + 36], fill=(150, 150, 160), width=2)
    d.ellipse([x + 17, y + 17, x + 27, y + 27], fill=(232, 126, 32))


def icon_health(x, y, s=44):
    d.ellipse([x, y, x + s, y + s], fill=TEAL)
    d.rectangle([x + 19, y + 10, x + 25, y + 34], fill=WHITE)
    d.rectangle([x + 10, y + 19, x + 34, y + 25], fill=WHITE)


def icon_chart(x, y, s=44):
    d.rectangle([x, y, x + s, y + s], fill=(245, 245, 245), outline=GREY)
    for i, bh in enumerate((26, 18, 10)):
        d.rectangle([x + 8 + i * 11, y + 36 - bh, x + 16 + i * 11, y + 36], fill=RED)
    d.line([x + 6, y + 8, x + 38, y + 30], fill=NAVY, width=3)
    d.polygon([(x + 38, y + 30), (x + 32, y + 28), (x + 38, y + 24)], fill=NAVY)


def icon_signal(x, y, s=44):
    d.rectangle([x, y, x + s, y + s], fill=(245, 245, 245), outline=GREY)
    for r in (8, 14, 20):
        d.arc([x + 22 - r, y + 26 - r, x + 22 + r, y + 26 + r], 300, 60, fill=NAVY, width=3)
    d.ellipse([x + 19, y + 23, x + 25, y + 29], fill=RED)
    d.line([x + 6, y + 38, x + 38, y + 6], fill=RED, width=3)


def icon_pin(x, y, s=44):
    d.rectangle([x, y, x + s, y + s], fill=(245, 245, 245), outline=GREY)
    d.ellipse([x + 12, y + 6, x + 32, y + 26], fill=RED)
    d.polygon([(x + 12, y + 22), (x + 32, y + 22), (x + 22, y + 40)], fill=RED)
    d.ellipse([x + 18, y + 12, x + 26, y + 20], fill=WHITE)


def icon_bolt(x, y, s=44):
    d.rectangle([x, y, x + s, y + s], fill=(245, 245, 245), outline=GREY)
    d.polygon([(x + 26, y + 5), (x + 12, y + 24), (x + 20, y + 24), (x + 16, y + 39), (x + 32, y + 19), (x + 24, y + 19)], fill=(232, 160, 32))


def icon_burst(x, y, s=44):
    d.rectangle([x, y, x + s, y + s], fill=(245, 245, 245), outline=GREY)
    cx, cy = x + 22, y + 22
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        d.line([cx, cy, cx + 17 * math.cos(a), cy + 17 * math.sin(a)], fill=(232, 126, 32), width=3)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)


cards = [
    ("TECH  ·  TRADE", "US tightens AI chip curbs on China", "chip"),
    ("EUROPE  ·  MIGRATION", "Five EU states plan Rwanda return hub", "eu"),
    ("ASIA  ·  SECURITY", "Japan scrambles jets over Russian planes", "jet"),
    ("MIDDLE EAST", "West urges Israel to open Gaza crossings", "aid"),
    ("ASIA  ·  POLITICS", "Mongolia's president resigns", "mongolia"),
    ("MIDDLE EAST  ·  ENERGY", "Houthi drones fired at Saudi pipeline", "drone"),
    ("HEALTH  ·  US", "US loses measles elimination status", "health"),
    ("MARKETS", "Wall Street falls; Nvidia in focus", "chart"),
    ("US  ·  SECURITY", "NSA outage in a week of US outages", "signal"),
    ("EUROPE  ·  SECURITY", "Seven Russian drones cross Moldova", "pin"),
    ("ENERGY  ·  EUROPE", "Equinor hit by cyberattack", "bolt"),
    ("MIDDLE EAST", "Israel strikes southern Lebanon", "burst"),
]
icons = {"chip": icon_chip, "flags": icon_flags, "eu": icon_eu, "jet": icon_jet,
         "aid": icon_aid, "mongolia": icon_mongolia, "drone": icon_drone,
         "health": icon_health, "chart": icon_chart, "signal": icon_signal,
         "pin": icon_pin, "bolt": icon_bolt, "burst": icon_burst}
f_ck = font(F_B, 14)
f_ch = font(F_B, 19)

gx, gy = 28, 452
cw, chh, gap = 312, 74, 10
for i, (kicker, head, ic) in enumerate(cards):
    cx = gx + (i % 3) * (cw + gap)
    cy = gy + (i // 3) * (chh + gap)
    rounded(d, [cx, cy, cx + cw, cy + chh], 8, fill=WHITE, outline=(210, 200, 180), width=2)
    icons[ic](cx + 8, cy + 15)
    d.text((cx + 60, cy + 8), kicker, font=f_ck, fill=RED)
    draw_text_block(d, cx + 60, cy + 27, head, f_ch, NAVY, cw - 70, 22, max_lines=2)

# ---------- the day in brief (18 one-liners) ----------
f_bh = font(F_B, 18)
d.text((28, 790), "THE DAY IN BRIEF", font=f_bh, fill=NAVY)
d.line([230, 800, 996, 800], fill=(180, 168, 140), width=2)
briefs = [
    "Depardieu admits assault charge",
    "Akeso shares plunge",
    "Gas tanker sinks in Black Sea off Bulgaria",
    "Houthis advance on Aden as army retreats",
    "Gaza winter rains worsen shelter crisis",
    "Dubai air traffic down 28% this year",
    "Irish activist charged over $60m C-130 attack",
    "Saudi missiles intercepted over Riyadh",
    "Modi attends ASEAN–India summit in Manila",
    "Quad leaders unveil minerals pacts",
    "India and Japan hold 2+2 defence talks",
    "Settlers shoot Palestinian woman near Jericho",
    "Waymo robotaxis pulled from freeways",
    "California landfill explosion",
    "Florida floods as storm hits US West",
    "Israeli strike on Gaza hospital kills seven",
    "China denounces US chip rule",
    "UN extends Yemen sanctions",
]
f_br = font(F_R, 15)
for i, b in enumerate(briefs):
    col = i % 2
    row = i // 2
    bx = 28 + col * 484
    by = 818 + row * 17
    d.text((bx, by), "▸", font=font(F_B, 15), fill=RED)
    d.text((bx + 18, by), b, font=f_br, fill=INK)

# ---------- footer ----------
d.line([28, 978, 996, 978], fill=(180, 168, 140), width=2)
f_ft = font(F_R, 15)
ft = "THE DAY IN FIGURES:  28% fall in Dubai air traffic  ·  $60m C-130 destroyed  ·  5 Houthi drones  ·  2 Kyiv bridges hit"
d.text(((W - d.textlength(ft, font=f_ft)) / 2, 986), ft, font=f_ft, fill=GREY)
f_src = font(F_B, 16)
st = "WORLD NEWS OF TUESDAY 17 NOVEMBER 2026"
d.text(((W - d.textlength(st, font=f_src)) / 2, 1004), st, font=f_src, fill=NAVY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
import os
print("bytes:", os.path.getsize("entry.png"))
