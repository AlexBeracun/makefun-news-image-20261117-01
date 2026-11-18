# draw_news.py — renders entry.png (1024x1024) for the 17 November 2026 world-news image.
# Run locally with PIL (NOT part of the graded entry: the graded program main.ts only
# copies the finished entry.png). News facts were gathered from web reporting of
# 17 November 2026 and cross-checked across at least two sources each.
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
PAPER = (250, 246, 238)
NAVY = (20, 33, 61)
NAVY2 = (28, 48, 88)
RED = (178, 44, 36)
GOLD = (201, 162, 39)
TEAL = (31, 122, 109)
INK = (30, 30, 30)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
SKY = (178, 214, 235)
SEA = (52, 110, 158)
SEA2 = (38, 88, 132)

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
d.rectangle([0, 0, W, 118], fill=NAVY)
d.rectangle([0, 118, W, 122], fill=GOLD)
f_title = font(F_B, 56)
t = "THE WORLD IN ONE DAY"
d.text(((W - d.textlength(t, font=f_title)) / 2, 14), t, font=f_title, fill=WHITE)
f_date = font(F_B, 28)
t = "TUESDAY  ·  17 NOVEMBER 2026"
d.text(((W - d.textlength(t, font=f_date)) / 2, 76), t, font=f_date, fill=GOLD)

# ---------- lead story ----------
rounded(d, [28, 134, 996, 452], 10, fill=WHITE, outline=(210, 200, 180), width=2)
f_kick = font(F_B, 21)
d.text((48, 150), "LEAD STORY  —  EUROPE", font=f_kick, fill=RED)
f_head = font(F_B, 34)
y = draw_text_block(d, 48, 182, "Ukraine brings down part of the Kerch Bridge; Russia hits Kyiv bridges", f_head, NAVY, 560, 40)
f_body = font(F_R, 21)
draw_text_block(d, 48, y + 8,
                "Ukrainian strikes collapsed a road section of the bridge linking Russia to Crimea and halted all traffic. Overnight, Russian missiles damaged two bridges across the Dnipro in Kyiv, cutting heat and water.",
                f_body, INK, 560, 27)

# --- bridge illustration (right side of lead panel) ---
ix0, iy0, ix1, iy1 = 632, 150, 976, 436
d.rectangle([ix0, iy0, ix1, iy1], fill=SKY)
d.rectangle([ix0, 300, ix1, iy1], fill=SEA)
for wx in range(ix0, ix1, 46):
    d.arc([wx, 318, wx + 34, 336], 0, 180, fill=SEA2, width=3)
    d.arc([wx + 12, 372, wx + 46, 390], 0, 180, fill=SEA2, width=3)
# pylon + cables
d.rectangle([ix0 + 168, 176, ix0 + 178, 300], fill=NAVY2)
for cx in (ix0 + 40, ix0 + 90, ix0 + 250, ix0 + 300):
    d.line([ix0 + 173, 180, cx, 252], fill=(120, 130, 150), width=2)
# deck: left span intact, right span collapsed into the water
d.rectangle([ix0 + 8, 248, ix0 + 168, 262], fill=(70, 74, 82))
d.rectangle([ix0 + 178, 248, ix0 + 236, 262], fill=(70, 74, 82))
# collapsed segment, tilted down into the sea
d.polygon([(ix0 + 246, 252), (ix0 + 330, 252), (ix0 + 318, 330), (ix0 + 268, 318)], fill=(96, 100, 110))
d.rectangle([ix0 + 246, 252, ix0 + 330, 262], fill=(70, 74, 82))
# pillars
for px in (ix0 + 30, ix0 + 120, ix0 + 200):
    d.rectangle([px, 262, px + 12, 300], fill=(90, 94, 102))
# smoke over the gap
for (sx, sy, sr) in [(ix0 + 238, 196, 26), (ix0 + 262, 176, 32), (ix0 + 292, 198, 24), (ix0 + 250, 214, 22)]:
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(110, 110, 112, 235))
# blast star at the gap
bx, by = ix0 + 252, 250
for ang in range(0, 360, 45):
    a = math.radians(ang)
    d.line([bx, by, bx + 26 * math.cos(a), by + 26 * math.sin(a)], fill=(232, 126, 32), width=5)
d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(245, 176, 65))
d.text((ix0 + 8, iy1 - 26), "KERCH STRAIT", font=font(F_B, 16), fill=(255, 255, 255))

# ---------- six story cards ----------
cards = [
    ("TECH  ·  TRADE", "US tightens AI chip curbs on China",
     "Washington closed a loophole letting Chinese firms buy advanced AI chips via data centres abroad.", "chip"),
    ("DIPLOMACY  ·  ASIA", "Xi, Putin and Trump set for trilateral",
     "China confirmed the three leaders will meet at the APEC summit in Shenzhen — a first of its kind.", "flags"),
    ("EUROPE  ·  MIGRATION", "Five EU states plan Rwanda return hub",
     "Austria, Denmark, Germany, Greece and the Netherlands would send rejected asylum seekers to Rwanda.", "eu"),
    ("ASIA  ·  SECURITY", "Japan scrambles jets over Russian planes",
     "Tokyo launched fighter jets and protested after two suspected Russian aircraft violated its airspace.", "jet"),
    ("MIDDLE EAST", "West urges Israel to open Gaza crossings",
     "The UK, Australia, Canada and Italy demanded rapid aid access, describing conditions as catastrophic.", "aid"),
    ("ASIA  ·  POLITICS", "Mongolia's president resigns",
     "President Khurelsukh stepped down amid a growing corruption scandal in Ulaanbaatar.", "mongolia"),
]

gx, gy = 28, 468
cw, chh, gap = 312, 228, 16


def icon_chip(x, y):
    d.rectangle([x, y, x + 64, y + 64], fill=NAVY)
    for i in range(3):
        d.rectangle([x + 12 + i * 16, y - 8, x + 18 + i * 16, y], fill=GOLD)
        d.rectangle([x + 12 + i * 16, y + 64, x + 18 + i * 16, y + 72], fill=GOLD)
        d.rectangle([x - 8, y + 12 + i * 16, x, y + 18 + i * 16], fill=GOLD)
        d.rectangle([x + 64, y + 12 + i * 16, x + 72, y + 18 + i * 16], fill=GOLD)
    d.rectangle([x + 14, y + 14, x + 50, y + 50], outline=GOLD, width=2)
    f = font(F_B, 20)
    d.text((x + 19, y + 20), "AI", font=f, fill=WHITE)


def icon_flags(x, y):
    # China
    d.rectangle([x, y, x + 30, y + 20], fill=(222, 41, 16))
    for (sx, sy) in [(x + 6, y + 4), (x + 13, y + 4), (x + 6, y + 11)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 222, 0))
    # Russia
    d.rectangle([x + 34, y, x + 64, y + 20], fill=WHITE, outline=GREY)
    d.rectangle([x + 34, y, x + 64, y + 7], fill=(0, 57, 166))
    d.rectangle([x + 34, y + 13, x + 64, y + 20], fill=(213, 0, 50))
    # USA
    d.rectangle([x + 17, y + 30, x + 47, y + 50], fill=WHITE, outline=GREY)
    for i in range(3):
        d.rectangle([x + 17, y + 30 + i * 7, x + 47, y + 33 + i * 7], fill=(178, 34, 52))
    d.rectangle([x + 17, y + 30, x + 30, y + 40], fill=(60, 59, 110))


def icon_eu(x, y):
    d.rectangle([x, y, x + 64, y + 64], fill=(0, 51, 153))
    for i in range(12):
        a = math.radians(i * 30 - 90)
        sx, sy = x + 32 + 20 * math.cos(a), y + 32 + 20 * math.sin(a)
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 204, 0))
    d.polygon([(x + 44, y + 44), (x + 64, y + 44), (x + 64, y + 58)], fill=(255, 204, 0))


def icon_jet(x, y):
    d.rectangle([x, y, x + 64, y + 64], fill=SKY)
    d.polygon([(x + 8, y + 34), (x + 44, y + 26), (x + 58, y + 30), (x + 44, y + 36), (x + 14, y + 42)], fill=(90, 96, 108))
    d.polygon([(x + 26, y + 28), (x + 34, y + 12), (x + 38, y + 28)], fill=(70, 76, 88))
    d.polygon([(x + 30, y + 40), (x + 36, y + 54), (x + 40, y + 40)], fill=(70, 76, 88))
    d.line([x + 4, y + 38, x + 14, y + 38], fill=WHITE, width=3)


def icon_aid(x, y):
    d.rectangle([x + 4, y + 18, x + 60, y + 60], fill=(194, 154, 108))
    d.polygon([(x + 4, y + 18), (x + 14, y + 8), (x + 60, y + 8), (x + 60, y + 18)], fill=(214, 178, 132))
    d.rectangle([x + 26, y + 30, x + 38, y + 50], fill=WHITE)
    d.rectangle([x + 20, y + 36, x + 44, y + 44], fill=WHITE)
    d.line([x + 4, y + 18, x + 60, y + 18], fill=(160, 120, 80), width=2)


def icon_mongolia(x, y):
    d.rectangle([x, y, x + 20, y + 64], fill=(206, 17, 38))
    d.rectangle([x + 20, y, x + 44, y + 64], fill=(0, 102, 179))
    d.rectangle([x + 44, y, x + 64, y + 64], fill=(206, 17, 38))
    d.ellipse([x + 26, y + 14, x + 38, y + 26], fill=(247, 219, 106))
    d.polygon([(x + 46, y + 40), (x + 58, y + 40), (x + 52, y + 56)], fill=(247, 219, 106))
    d.rectangle([x + 46, y + 36, x + 58, y + 42], fill=(247, 219, 106))


icons = {"chip": icon_chip, "flags": icon_flags, "eu": icon_eu, "jet": icon_jet, "aid": icon_aid, "mongolia": icon_mongolia}
f_ck = font(F_B, 17)
f_ch = font(F_B, 24)
f_cb = font(F_R, 17)

for i, (kicker, head, body, ic) in enumerate(cards):
    cx = gx + (i % 3) * (cw + gap)
    cy = gy + (i // 3) * (chh + gap)
    rounded(d, [cx, cy, cx + cw, cy + chh], 10, fill=WHITE, outline=(210, 200, 180), width=2)
    icons[ic](cx + 16, cy + 12)
    draw_text_block(d, cx + 92, cy + 16, kicker, f_ck, RED, cw - 108, 21, max_lines=2)
    yy = draw_text_block(d, cx + 16, cy + 82, head, f_ch, NAVY, cw - 32, 28, max_lines=2)
    draw_text_block(d, cx + 16, yy + 4, body, f_cb, INK, cw - 32, 20, max_lines=4)

# ---------- footer ----------
d.line([28, 952, 996, 952], fill=(180, 168, 140), width=2)
f_ft = font(F_R, 19)
ft = "Also: Depardieu admits assault charge  ·  Akeso shares plunge  ·  Hormuz tanker attacks"
d.text(((W - d.textlength(ft, font=f_ft)) / 2, 962), ft, font=f_ft, fill=GREY)
f_src = font(F_B, 17)
st = "WORLD NEWS OF TUESDAY 17 NOVEMBER 2026"
d.text(((W - d.textlength(st, font=f_src)) / 2, 990), st, font=f_src, fill=NAVY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
import os
print("bytes:", os.path.getsize("entry.png"))
