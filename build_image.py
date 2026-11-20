#!/usr/bin/env python3
"""Render entry.png: Friday 20 November 2026, 37 stories, one front page (v4).
Deterministic: no timestamps, no randomness. Pillow only."""
from PIL import Image, ImageDraw, ImageFont
import math, os

W = H = 1024
PAPER = (247, 242, 231); INK = (28, 32, 38); NAVY = (22, 40, 63)
GOLD = (201, 162, 39); RED = (176, 42, 33); CARD = (255, 253, 246)
GREY = (96, 96, 92); TAN = (222, 198, 150)
FD = "/usr/share/fonts/truetype/liberation/"
DD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    path = FD + name if os.path.exists(FD + name) else DD + name
    return ImageFont.truetype(path, size)
def serif_b(s): return F("LiberationSerif-Bold.ttf", s)
def serif(s): return F("LiberationSerif-Regular.ttf", s)
def serif_i(s): return F("LiberationSerif-Italic.ttf", s)
def sans_b(s): return F("LiberationSans-Bold.ttf", s)
def sans(s): return F("LiberationSans-Regular.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def tw(text, font):
    b = d.textbbox((0, 0), text, font=font); return b[2] - b[0]
def txt(x, y, text, font, fill=INK, anchor=None):
    d.text((x, y), text, font=font, fill=fill, anchor=anchor)
def rect(box, fill=None, outline=None, width=1):
    d.rectangle(box, fill=fill, outline=outline, width=width)
def rrect(box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)
def line(points, fill=INK, width=1):
    d.line(points, fill=fill, width=width, joint="curve")
def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, font) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines
def para(x, y, text, font, maxw, lh, fill=INK, max_lines=None):
    ls = wrap(text, font, maxw)
    if max_lines: ls = ls[:max_lines]
    for i, l in enumerate(ls): txt(x, y + i * lh, l, font, fill)
    return y + len(ls) * lh
def chip(x_right, y, label):
    f = sans_b(9); w_ = tw(label, f) + 12
    rrect([x_right - w_, y, x_right, y + 15], 4, fill=NAVY)
    txt(x_right - w_ + 6, y + 3, label, f, (255, 255, 255))
def hero(x, y, text, size, fill=(255, 255, 255), anchor="la", shadow=(0, 0, 0)):
    f = sans_b(size)
    if shadow: txt(x + 2, y + 2, text, f, shadow, anchor=anchor)
    txt(x, y, text, f, fill, anchor=anchor)
def card(x, y, w_, h):
    rect([x, y, x + w_, y + h], fill=CARD, outline=NAVY, width=1)
def card_head(x, y, w_, num, label, headline, body, hf=19, bf=11, blines=3):
    txt(x + 7, y, f"{num:02d}", sans_b(11), RED)
    txt(x + 30, y + 1, label, sans_b(9), NAVY)
    yy = para(x + 7, y + 14, headline, serif_b(hf), w_ - 14, int(hf * 1.12), INK, 2)
    para(x + 7, yy + 1, body, sans(bf), w_ - 14, int(bf * 1.25), (52, 52, 50), blines)

# ---------------- header ----------------
txt(12, 8, "THE WORLD IN ONE DAY", sans_b(11), NAVY)
txt(1012, 8, "FRIDAY'S NEWS \u2022 ONE PAGE \u2022 37 STORIES \u2022 6 CONTINENTS", sans_b(11), NAVY, anchor="ra")
line([(12, 26), (1012, 26)], NAVY, 2)
txt(512, 26, "Friday 20 November 2026", serif_b(40), INK, anchor="ma")
txt(512, 70, "Cyclone Akvan strikes India \u2022 Ballistic missiles hit Kyiv \u2022 COP31 deadlocked on final day \u2022 Asian AI sell-off",
    serif_i(16), RED, anchor="ma")
line([(12, 90), (1012, 90)], GOLD, 2)
# stat strip
stats = [("370,000+", "evacuated ahead of Cyclone Akvan"), ("3", "Dnipro bridges hit in Kyiv barrage"),
         ("\u22127%", "Asia shares' worst week since 2020"), ("2.3%", "Japan Oct headline CPI; BoJ eyed"),
         ("118", "Phillips' historic century vs India"), ("60.7%", "tumours shrank on daraxonrasib + chemo")]
sx = 12
for i, (n, cap) in enumerate(stats):
    w_ = 167 if i < 5 else 165
    txt(sx + w_ // 2, 94, n, serif_b(24), RED, anchor="ma")
    ls = wrap(cap, sans(9), w_ - 8)
    for j, l in enumerate(ls): txt(sx + w_ // 2, 120 + j * 11, l, sans(9), INK, anchor="ma")
    if i: line([(sx, 94), (sx, 138)], GOLD, 1)
    sx += w_
line([(12, 140), (1012, 140)], NAVY, 1)
# region strip (segments sum to 37)
regions = [("EUROPE 8", 8, (43, 84, 150)), ("AMERICAS 7", 7, (46, 125, 72)), ("ASIA-PACIFIC 8", 8, (176, 42, 33)),
           ("MIDEAST 5", 5, (201, 140, 40)), ("AFRICA 3", 3, (110, 70, 140)), ("OCEANIA 4", 4, (32, 128, 140)),
           ("WORLD / SPACE 2", 2, (70, 70, 70))]
rx = 12
for label, n, col in regions:
    w_ = 96 if label.startswith("WORLD") else int(908 * n / 35)
    rect([rx, 144, rx + w_, 160], fill=col)
    f = sans_b(11 if w_ > 90 else 9)
    txt(rx + w_ // 2, 147, label, f, (255, 255, 255), anchor="ma")
    rx += w_

# ---------------- lead cards ----------------
LY, LH, LW = 166, 196, 328
def lead_bg(x, y): rect([x, y, x + LW, y + 100], fill=(200, 220, 235), outline=NAVY, width=1)

# Lead 1: Akvan coast map
x = 12; card(x, LY, LW, LH); lead_bg(x, LY)
rect([x, LY, x + 150, LY + 100], fill=(238, 222, 175))  # land
d.polygon([(x + 150, LY), (x + 190, LY + 28), (x + 165, LY + 62), (x + 205, LY + 100), (x + 150, LY + 100)], fill=(238, 222, 175))
rect([x + 150, LY, x + LW, LY + 100], fill=(70, 130, 180))
d.polygon([(x + 150, LY), (x + 190, LY + 28), (x + 165, LY + 62), (x + 205, LY + 100), (x + 150, LY + 100)], fill=(238, 222, 175))
for cx, cy, r, col in [(70, 30, 16, (250, 244, 210)), (52, 74, 10, (250, 244, 210))]:
    d.ellipse([x + cx - r, LY + cy - r, x + cx + r, LY + cy + r], fill=col)
txt(x + 8, LY + 6, "ODISHA", sans_b(11), NAVY); txt(x + 8, LY + 19, "INDIA", sans_b(9), NAVY)
txt(x + LW - 8, LY + 82, "BAY OF BENGAL", sans_b(10), (255, 255, 255), anchor="ra")
# cyclone spiral
ccx, ccy = x + 252, LY + 52
for r in (34, 26, 18, 10):
    d.arc([ccx - r, ccy - r, ccx + r, ccy + r], start=20, end=300, fill=(255, 255, 255), width=4)
    d.arc([ccx - r, ccy - r, ccx + r, ccy + r], start=200, end=140, fill=(210, 235, 250), width=3)
d.ellipse([ccx - 5, ccy - 5, ccx + 5, ccy + 5], fill=RED)
for i in range(7):  # rain streaks
    rx_ = x + 215 + i * 14; line([(rx_, LY + 78), (rx_ - 7, LY + 92)], (190, 225, 245), 2)
# dashed track to landfall
for t in range(9):
    px = ccx - t * 9; py = ccy + int(14 * math.sin(t * 0.7)) - t
    d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=GOLD)
d.ellipse([x + 168, LY + 40, x + 180, LY + 52], fill=RED, outline=(255, 255, 255), width=2)
txt(x + 184, LY + 36, "Gopalpur", sans_b(10), NAVY)
rrect([x, LY + 82, x + 168, LY + 100], 0, fill=RED); txt(x + 7, LY + 86, "LANDFALL \u00b7 GUSTS 90 KM/H", sans_b(10), (255, 255, 255))
card_head(x, LY + 102, LW, 1, "ODISHA, INDIA \u00b7 STORM", "Cyclone Akvan makes landfall in eastern India",
          "Severe storm crosses near Gopalpur Friday morning; 370,000 evacuated, 423 rescue teams, winds 70\u201380 gusting 90 km/h; no major damage reported. (Hindu BusinessLine, IMD)", hf=20, bf=10)

# Lead 2: Kyiv night skyline
x = 348; card(x, LY, LW, LH)
rect([x, LY, x + LW, LY + 100], fill=(16, 24, 48), outline=NAVY, width=1)
for i in range(28):  # stars (fixed pattern)
    px = x + 8 + (i * 53) % 310; py = LY + 5 + (i * 29) % 34
    d.ellipse([px, py, px + 2, py + 2], fill=(240, 240, 210))
d.ellipse([x + 282, LY + 8, x + 306, LY + 32], fill=(238, 230, 190))  # moon
blds = [(0, 46, 34), (36, 34, 28), (66, 52, 40), (108, 30, 30), (140, 44, 36), (178, 26, 30), (210, 50, 38), (250, 36, 28), (280, 46, 48)]
for bx, bh, bw in blds:
    rect([x + bx, LY + 100 - bh, x + bx + bw, LY + 100], fill=(8, 12, 26))
    for wy in range(LY + 100 - bh + 6, LY + 94, 11):
        for wx in range(x + bx + 5, x + bx + bw - 4, 9):
            if (wx + wy) % 3: rect([wx, wy, wx + 4, wy + 5], fill=(250, 200, 90))
d.polygon([(x + 152, LY + 62), (x + 168, LY + 40), (x + 184, LY + 62)], fill=(8, 12, 26))  # dome base
d.arc([x + 152, LY + 34, x + 184, LY + 66], 180, 360, fill=(8, 12, 26), width=8)
line([(x + 236, LY + 58), (x + 236, LY + 78)], (8, 12, 26), 4); line([(x + 236, LY + 58), (x + 258, LY + 58)], (8, 12, 26), 3)  # crane
for i, (ax, ay) in enumerate([(40, 14), (110, 8), (185, 18), (250, 6), (70, 26), (215, 28)]):  # missile trails + bursts
    line([(x + ax, LY + ay + 26), (x + ax + 42, LY + ay)], (250, 170, 80), 2)
    bx_, by_ = x + ax + 46, LY + ay
    for a in range(0, 360, 45):
        line([(bx_, by_), (bx_ + int(8 * math.cos(math.radians(a))), by_ + int(8 * math.sin(math.radians(a))))], (255, 210, 90), 2)
for fx in (52, 168, 272):  # fires
    d.ellipse([x + fx, LY + 88, x + fx + 22, LY + 100], fill=(230, 110, 40))
    d.ellipse([x + fx + 5, LY + 84, x + fx + 17, LY + 96], fill=(250, 170, 60))
rrect([x, LY, x + 196, LY + 18], 0, fill=RED); txt(x + 7, LY + 4, "OVERNIGHT \u00b7 BALLISTIC MISSILES", sans_b(10), (255, 255, 255))
card_head(x, LY + 102, LW, 2, "KYIV, UKRAINE \u00b7 WAR", "Russia fires overnight ballistic-missile barrage at Kyiv",
          "3 killed, 3 bridges across the Dnipro damaged, fires in three districts. (Reuters, livefromeurope)", hf=20, bf=10)

# Lead 3: COP31 globe + thermometer
x = 684; card(x, LY, LW, LH)
rect([x, LY, x + LW, LY + 100], fill=(214, 233, 240), outline=NAVY, width=1)
gx, gy, gr = x + 82, LY + 54, 44
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(64, 130, 190), outline=NAVY, width=2)
d.polygon([(gx - 30, gy - 22), (gx - 12, gy - 30), (gx - 8, gy - 12), (gx - 22, gy - 6)], fill=(86, 160, 90))
d.polygon([(gx - 14, gy + 2), (gx - 2, gy + 0), (gx - 6, gy + 26), (gx - 14, gy + 20)], fill=(86, 160, 90))
d.polygon([(gx + 12, gy - 26), (gx + 30, gy - 18), (gx + 24, gy - 4), (gx + 10, gy - 10)], fill=(86, 160, 90))
d.polygon([(gx + 8, gy + 8), (gx + 20, gy + 6), (gx + 18, gy + 22), (gx + 8, gy + 18)], fill=(86, 160, 90))
tx_ = x + 168  # thermometer
rect([tx_ + 8, LY + 12, tx_ + 24, LY + 84], fill=(255, 255, 255), outline=NAVY, width=2)
rect([tx_ + 11, LY + 34, tx_ + 21, LY + 84], fill=RED)
d.ellipse([tx_ + 2, LY + 78, tx_ + 30, LY + 106], fill=RED, outline=NAVY, width=2)
for i in range(5): line([(tx_ + 24, LY + 18 + i * 14), (tx_ + 32, LY + 18 + i * 14)], NAVY, 2)
txt(tx_ + 38, LY + 10, "+1.5\u00b0", sans_b(13), RED)
rrect([x + 200, LY + 14, x + LW - 6, LY + 92], 6, fill=RED)
for i, l in enumerate(["ANTALYA \u00b7 NOV 20", "COP31", "FINAL DAY", "\u2014 DEADLOCK"]):
    f = sans_b(20 if i == 1 else 11)
    txt(x + 207, LY + 22 + i * 19, l, f, (255, 255, 255))
card_head(x, LY + 102, LW, 3, "ANTALYA, T\u00dcRKIYE \u00b7 CLIMATE", "COP31 reaches final day deadlocked",
          "Closing draft omits fossil-fuel phase-out and the $120bn adaptation target; Panama vows to block; \u201c35 by 35\u201d clean-power goal stays. (Reuters, AP)", hf=20, bf=10)

# ---------------- mid cards (poster rule) ----------------
MY, MH, MW = 368, 140, 195
def mid(x, y, num, label, headline, body, hf=16):
    card(x, y, MW, MH)
    card_head(x, y + 68, MW, num, label, headline, body, hf=hf, bf=10, blines=2)
def banner(x, y, bg):
    rect([x, y, x + MW, y + 64], fill=bg, outline=NAVY, width=1)

# 4 Markets: candlesticks
x, y = 12, MY; mid(x, y, 4, "SEOUL/TOKYO \u00b7 MARKETS", "AI sell-off sinks Asia to worst week since 2020",
    "Nikkei \u22124.5%, Kospi \u22124.7%, Taiex \u22126.4%; SoftBank \u221214.6%. (Reuters)")
banner(x, y, (18, 26, 40))
for gx in range(x + 12, x + 120, 18): line([(gx, y + 4), (gx, y + 60)], (52, 68, 92), 1)
for gy_ in range(y + 12, y + 60, 16): line([(x + 4, gy_), (x + 118, gy_)], (52, 68, 92), 1)
candles = [(14, 18, 30, True), (30, 24, 38, False), (46, 20, 32, True), (62, 30, 46, False), (78, 26, 40, True), (94, 36, 52, False)]
pts = []
for cx, top, bot, up in candles:
    col = (60, 190, 110) if up else (225, 70, 60)
    line([(x + cx + 5, y + top - 5), (x + cx + 5, y + bot + 5)], col, 2)
    rect([x + cx, y + top, x + cx + 10, y + bot], fill=col)
    pts.append((x + cx + 5, y + (top + bot) // 2))
line(pts, (240, 90, 80), 2)
hero(x + MW - 8, y + 14, "\u22127%", 34, (255, 120, 100), anchor="ra")
chip(x + MW - 6, y + 48, "REUTERS")

# 5 Mercury
x = 213; mid(x, y, 5, "MERCURY \u00b7 SPACE", "BepiColombo reaches Mercury after 8 years",
    "ESA/JAXA probe ends 6bn-mile trip; insertion Saturday. (Guardian, ESA)")
banner(x, y, (12, 14, 30))
for i in range(16):
    px = x + 6 + (i * 37) % 180; py = y + 4 + (i * 23) % 24
    d.ellipse([px, py, px + 2, py + 2], fill=(235, 235, 210))
d.ellipse([x + 18, y + 12, x + 78, y + 56], fill=(165, 162, 155), outline=(220, 218, 210), width=2)
for cx, cy, r in [(36, 26, 7), (58, 40, 5), (48, 18, 4)]:
    d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r], outline=(120, 118, 112), width=2)
d.arc([x + 8, y + 2, x + 120, y + 62], 300, 80, fill=GOLD, width=2)
rect([x + 104, y + 22, x + 118, y + 36], fill=(200, 200, 205))  # probe body
for i in range(3):
    for j in range(2): rect([x + 122 + i * 9, y + 18 + j * 11, x + 129 + i * 9, y + 27 + j * 11], fill=(70, 110, 190), outline=(160, 190, 235), width=1)
line([(x + 110, y + 36), (x + 96, y + 48)], (200, 200, 205), 2)
hero(x + 8, y + 38, "6BN MILES", 26, (255, 225, 130))
chip(x + MW - 6, y + 5, "ESA \u00b7 BBC")

# 6 Brussels: EU + UK flags
x = 414; mid(x, y, 6, "BRUSSELS \u00b7 EUROPE", "Burnham holds second EU\u2013UK reset summit",
    "Hosts UK PM; food, emissions & youth-mobility deals. (AP, Le Monde)")
banner(x, y, (200, 214, 228))
rect([x, y + 48, x + MW, y + 64], fill=(90, 96, 105))
for bx in range(8, 180, 34): rect([x + bx, y + 38, x + bx + 24, y + 64], fill=(70, 76, 86))
line([(x + 42, y + 8), (x + 42, y + 50)], NAVY, 3); line([(x + 128, y + 8), (x + 128, y + 50)], NAVY, 3)
rect([x + 42, y + 8, x + 84, y + 32], fill=(30, 60, 150))
for i in range(8):
    a = math.radians(i * 45); px = x + 63 + int(8 * math.cos(a)); py = y + 20 + int(8 * math.sin(a))
    d.polygon([(px, py - 3), (px + 2, py + 2), (px - 2, py + 2)], fill=GOLD)
rect([x + 128, y + 8, x + 170, y + 32], fill=(40, 50, 140))
line([(x + 128, y + 8), (x + 170, y + 32)], (255, 255, 255), 4); line([(x + 170, y + 8), (x + 128, y + 32)], (255, 255, 255), 4)
line([(x + 149, y + 8), (x + 149, y + 32)], (255, 255, 255), 6); line([(x + 128, y + 20), (x + 170, y + 20)], (255, 255, 255), 6)
line([(x + 149, y + 8), (x + 149, y + 32)], RED, 3); line([(x + 128, y + 20), (x + 170, y + 20)], RED, 3)
rrect([x + 14, y + 36, x + MW - 14, y + 62], 4, fill=NAVY)
hero(x + MW // 2, y + 40, "RESET TALKS", 25, (255, 255, 255), anchor="ma", shadow=None)
chip(x + MW - 6, y + 5, "AP")

# 7 Tokyo bars
x = 615; mid(x, y, 7, "TOKYO \u00b7 ECONOMY", "Japan inflation hits 2.3%; BoJ hike eyed",
    "Oct CPI rises from 2.1%; core 2.2%, above 2% target. (FXStreet)")
banner(x, y, (240, 238, 228))
for i, bh in enumerate([14, 20, 26, 32, 42]):
    col = RED if i == 4 else (70, 110, 170)
    rect([x + 10 + i * 20, y + 56 - bh, x + 26 + i * 20, y + 56], fill=col)
line([(x + 6, y + 22), (x + 112, y + 22)], RED, 2)
for dx in range(x + 6, x + 112, 8): line([(dx, y + 22), (dx + 4, y + 22)], (240, 238, 228), 2)
txt(x + 8, y + 6, "2% TARGET", sans_b(9), RED)
hero(x + MW - 8, y + 24, "2.3%", 36, RED, anchor="ra", shadow=None)
chip(x + MW - 6, y + 5, "STATISTICS BUREAU")

# 8 Beijing yield curves
x = 816; mid(x, y, 8, "BEIJING \u00b7 RATES", "China holds lending rates for 18th month",
    "1-yr LPR 3.00%, 5-yr 3.50% as expected. (Reuters, PBoC)")
banner(x, y, (20, 30, 48))
p1 = [(x + 10 + i * 16, y + 40 - i * 2) for i in range(6)]
p2 = [(x + 10 + i * 16, y + 30 - i * 3) for i in range(6)]
line(p1, (110, 190, 240), 3); line(p2, GOLD, 3)
for p in (p1[-1], p2[-1]): d.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=(255, 255, 255))
txt(x + 104, y + 6, "18TH MONTH", sans_b(10), (180, 200, 230))
hero(x + 102, y + 18, "3.00%", 27, (140, 210, 250), shadow=None)
hero(x + 102, y + 42, "3.50%", 27, (255, 215, 110), shadow=None)
chip(x + MW - 6, y + 5, "PBoC \u00b7 REUTERS")

# row 2
MY2 = MY + MH + 6
# 9 Wellington cricket
x, y = 12, MY2; mid(x, y, 9, "WELLINGTON \u00b7 CRICKET", "Phillips makes history with 118 vs India",
    "Centuries vs India in all 3 formats in one year; NZ 368. (Reuters, ICC)")
banner(x, y, (46, 130, 62))
rect([x + 78, y + 6, x + 118, y + 58], fill=(232, 214, 170))
line([(x + 98, y + 6), (x + 98, y + 58)], (190, 170, 130), 1)
for sx_ in (86, 110):
    for k in range(3): rect([x + sx_ + k * 4, y + 10, x + sx_ + k * 4 + 3, y + 24], fill=(240, 220, 150))
    for k in range(3): rect([x + sx_ + k * 4, y + 42, x + sx_ + k * 4 + 3, y + 56], fill=(240, 220, 150))
line([(x + 128, y + 46), (x + 150, y + 30)], (150, 100, 50), 5)  # bat
for i in range(4): d.ellipse([x + 138 + i * 9, y + 18 - i * 2, x + 144 + i * 9, y + 24 - i * 2], fill=(235, 235, 235))
hero(x + 10, y + 12, "118", 40, (255, 255, 255))
txt(x + 12, y + 50, "NZ 368", sans_b(10), (255, 255, 210))
chip(x + MW - 6, y + 5, "ICC")

# 10 Rome strike crowd
x = 213; mid(x, y, 10, "ROME \u00b7 LABOUR", "Italy's CGIL holds 24-hr general strike",
    "Unions rally in ~100 squares vs 2027 budget; transit hit. (ANSA)")
banner(x, y, (228, 222, 205))
for i, hx in enumerate(range(10, 180, 26)):
    hy = y + 44 + (i % 2) * 6
    d.ellipse([x + hx, hy - 14, x + hx + 14, hy], fill=(70, 60, 55))
    d.pieslice([x + hx - 3, hy - 2, x + hx + 17, hy + 16], 180, 360, fill=(90, 70, 60) if i % 2 else (60, 80, 110))
    if i % 2 == 0:
        line([(x + hx + 16, hy - 2), (x + hx + 16, hy - 22)], NAVY, 2)
        rect([x + hx + 8, y + 14, x + hx + 26, y + 24], fill=(255, 255, 255), outline=NAVY, width=1)
d.polygon([(x + 168, y + 6), (x + 186, y + 10), (x + 168, y + 15)], fill=(200, 50, 50))
rect([x + 156, y + 6, x + 168, y + 15], fill=(50, 150, 80))
rrect([x + 12, y + 22, x + MW - 12, y + 50], 4, fill=(255, 255, 255))
hero(x + MW // 2, y + 28, "100 SQUARES", 22, NAVY, anchor="ma", shadow=None)
chip(x + MW - 6, y + 5, "ANSA")

# 11 Mato Grosso forest
x = 414; mid(x, y, 11, "MATO GROSSO \u00b7 LAND", "Lula visits ailing Chief Raoni, 94",
    "Recognises Kayapo & Yudja ancestral lands (Kapot Nhinore). (One Turn)")
banner(x, y, (120, 180, 110))
d.ellipse([x + 150, y + 4, x + 182, y + 30], fill=(250, 205, 80))
for cx, cy, r, col in [(20, 30, 22, (34, 120, 55)), (58, 20, 26, (52, 150, 70)), (98, 32, 24, (30, 105, 50)),
                        (140, 24, 22, (60, 160, 80)), (44, 48, 24, (44, 140, 62)), (120, 50, 22, (38, 125, 58))]:
    d.ellipse([x + cx - r, y + cy - r // 2, x + cx + r, y + cy + r // 2 + 12], fill=col)
river = [(x + 6, y + 58), (x + 50, y + 48), (x + 90, y + 56), (x + 130, y + 46), (x + 190, y + 54)]
line(river, (90, 170, 220), 5)
for bx, by in [(70, 12), (96, 8)]:
    d.arc([x + bx, y + by, x + bx + 12, y + by + 8], 200, 340, fill=INK, width=2)
    d.arc([x + bx + 10, y + by, x + bx + 22, y + by + 8], 200, 340, fill=INK, width=2)
hero(x + MW // 2, y + 20, "ANCESTRAL LANDS", 19, (255, 255, 255), anchor="ma")
chip(x + MW - 6, y + 5, "ONE TURN")

# 12 Barcelona pill
x = 615; mid(x, y, 12, "BARCELONA \u00b7 HEALTH", "Daraxonrasib + chemo shrinks tumours in 60.7%",
    "Early trial, 61 patients, at ENA; no chemo-only comparison. (EORTC, PA)")
banner(x, y, (235, 240, 245))
rrect([x + 10, y + 16, x + 92, y + 46], 15, fill=(255, 255, 255), outline=NAVY, width=2)
rrect([x + 10, y + 16, x + 51, y + 46], 15, fill=RED)
rect([x + 38, y + 17, x + 51, y + 45], fill=RED)
for cx, cy, r in [(112, 16, 6), (126, 26, 8), (110, 38, 5), (130, 44, 5)]:
    d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r], outline=(70, 120, 180), width=2)
line([(x + 116, y + 20), (x + 122, y + 24)], (70, 120, 180), 2); line([(x + 122, y + 30), (x + 114, y + 35)], (70, 120, 180), 2)
rect([x + 20, y + 50, x + 34, y + 56], fill=RED); rect([x + 24, y + 46, x + 30, y + 60], fill=RED)
hero(x + MW - 8, y + 26, "60.7%", 30, RED, anchor="ra", shadow=None)
chip(x + MW - 6, y + 5, "EORTC")

# 13 Turin tennis
x = 816; mid(x, y, 13, "TURIN \u00b7 TENNIS", "Alcaraz\u2013Cobolli, Medvedev\u2013Tiafoe close groups",
    "ATP Finals group stage ends Friday; semis Saturday. (ATP)", hf=15)
banner(x, y, (36, 110, 160))
d.polygon([(x + 18, y + 12), (x + 178, y + 12), (x + 190, y + 56), (x + 6, y + 56)], fill=(52, 140, 90))
line([(x + 18, y + 12), (x + 178, y + 12)], (255, 255, 255), 2); line([(x + 6, y + 56), (x + 190, y + 56)], (255, 255, 255), 2)
line([(x + 58, y + 13), (x + 48, y + 55)], (255, 255, 255), 1); line([(x + 138, y + 13), (x + 148, y + 55)], (255, 255, 255), 1)
line([(x + 98, y + 12), (x + 98, y + 56)], (255, 255, 255), 2)
line([(x + 10, y + 34), (x + 186, y + 34)], (20, 20, 30), 3)
d.arc([x + 30, y + 4, x + 130, y + 44], 20, 160, fill=(250, 230, 120), width=2)
d.ellipse([x + 126, y + 22, x + 138, y + 34], fill=(215, 235, 90), outline=(255, 255, 255), width=1)
hero(x + MW // 2, y + 38, "ATP FINALS", 24, (255, 255, 255), anchor="ma")
chip(x + MW - 6, y + 5, "ATP")

# ---------------- bottom block ----------------
BY, BH = 662, 250
# LEFT: filled world map
rect([12, BY, 262, BY + BH], fill=NAVY, outline=NAVY, width=1)
txt(22, BY + 8, "WHERE IT HAPPENED", sans_b(13), (255, 255, 255))
MX0, MY0, MW2, MH2 = 20, BY + 32, 234, 166
def mp(px, py): return (MX0 + px * MW2 / 200, MY0 + py * MH2 / 140)
def poly(pts, fill=TAN):
    d.polygon([mp(a, b) for a, b in pts], fill=fill)
poly([(8, 28), (38, 18), (58, 24), (54, 40), (40, 44), (34, 58), (24, 52), (12, 40)])            # N America
poly([(36, 62), (50, 60), (56, 74), (50, 96), (42, 108), (36, 88), (32, 72)])                    # S America
poly([(88, 26), (104, 20), (112, 30), (106, 40), (94, 40), (88, 34)])                            # Europe
poly([(90, 46), (108, 42), (118, 56), (112, 84), (100, 98), (92, 76), (88, 58)])                 # Africa
poly([(110, 28), (140, 22), (168, 30), (172, 46), (150, 52), (138, 44), (124, 50), (114, 40)])   # Asia
poly([(140, 58), (156, 56), (160, 68), (146, 72), (138, 66)])                                    # SE Asia
poly([(158, 88), (180, 84), (186, 96), (172, 106), (160, 100)])                                  # Australia
poly([(184, 108), (192, 106), (190, 116), (184, 114)])                                           # NZ
pins = {1: (130, 46), 2: (108, 24), 3: (114, 32), 4: (162, 34), 5: (24, 124), 6: (93, 20), 7: (174, 36),
        8: (154, 32), 9: (188, 110), 10: (101, 30), 11: (46, 78), 12: (86, 32), 13: (97, 25)}
for n, (px, py) in pins.items():
    cx, cy = mp(px, py)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED, outline=(255, 255, 255), width=1)
    txt(cx, cy - 5, str(n), sans_b(8), (255, 255, 255), anchor="ma")
txt(22, BY + 206, "1\u20133 Lead \u00b7 4\u201313 Feature stories", sans_b(10), GOLD)
para(22, BY + 222, "Red numbers mark stories 1\u201313. Positions are approximate.", sans(9), 230, 12, (210, 218, 230), 2)

# RIGHT: ALSO ON briefs with bold red place lead-ins
AX = 270
txt(AX, BY + 2, "ALSO ON FRIDAY 20 NOVEMBER \u2014 24 MORE STORIES", sans_b(13), RED)
line([(AX, BY + 22), (1012, BY + 22)], GOLD, 2)
briefs = [
    (14, "SEOUL", "Ruling party moves to impeach Chief Justice Cho Hee-dae.", "SBS"),
    (15, "BOUGAINVILLE", "Rio Tinto pledges $370m Panguna repair.", "ABC, Reuters"),
    (16, "CANBERRA", "CBO warns AUKUS subs could shrink US fleet.", "Reuters"),
    (17, "FLORIDA", "St Johns River hits record 18.3 ft; four counties shut schools.", "AP"),
    (18, "IOWA", "Army sets noon detonation of 68 unstable barrels.", "AP"),
    (19, "TONGA", "El Ni\u00f1o drought bites.", "RNZ"),
    (20, "COPENHAGEN", "Parliament approves Greenland defence bill.", "AFP"),
    (21, "GLOBAL", "UN marks World Children's Day worldwide.", "UN News"),
    (22, "DAKAR", "President Faye enacts supplementary budget by decree.", "AFP"),
    (23, "HORMUZ", "Attacks on vessels in 96 hours, centre says.", "UKMTO"),
    (24, "NEW DELHI", "Pakistan minister to lead SCO dialogue team.", "The Hindu"),
    (25, "DOHA", "U17 World Cup: Australia stuns Argentina 2\u20130.", "FIFA"),
    (26, "HONG KONG", "Badminton Open semifinals decided.", "BWF"),
    (27, "TAIPEI", "Short-sell curbs in effect; two Russian bombers tracked.", "Reuters"),
    (28, "AL-DAHI, ISRAEL", "Mosque torched; Hebrew graffiti; backlash at Netanyahu.", "One Turn"),
    (29, "EUROPE", "Youth strike in 25+ countries over costs, militarisation.", "One Turn"),
    (30, "WASHINGTON", "Trump open to NATO-like guarantees for Ukraine.", "World Times Daily"),
    (31, "BOGOT\u00c1", "Protest tax plans amid US military presence row.", "World Times Daily"),
    (32, "LILONGWE", "Malawi fuel crisis sparks chaos nationwide.", "World Times Daily"),
    (33, "GAZA", "Civil Defence struggles as vehicles break down.", "World Times Daily"),
    (34, "BERLIN", "Zelenskyy meets German, British, French officials.", "nhoq"),
    (35, "BRAZIL", "Violent deaths hit series low, down 12.2% Jan\u2013Oct.", "1stHeadlines"),
    (36, "ALGIERS", "World Bank sees Algeria growth at 3.7%.", "1stHeadlines"),
    (37, "SANTIAGO", "Fuel relief bill may cost $813m.", "1stHeadlines"),
]
BF, BFL = sans(11), 11.5
def draw_brief(x, y, maxw, num, place, head, src):
    tokens = [(f"{num} ", sans_b(11), RED), (place + " \u2014 ", sans_b(11), RED),
              (head + " ", BF, INK), (f"({src})", sans(10), GREY)]
    words = []
    for text_, font_, col in tokens:
        for w_ in text_.split(" "):
            if w_: words.append((w_, font_, col))
    cx, cy = x, y
    for w_, font_, col in words:
        ww = tw(w_ + " ", font_)
        if cx + ww > x + maxw and cx > x: cx = x; cy += BFL
        txt(cx, cy, w_, font_, col); cx += ww
    return cy + BFL
colw = 367
for ci, half in enumerate((briefs[:12], briefs[12:])):
    cy = BY + 28
    for b in half: cy = draw_brief(AX + ci * (colw + 8), cy, colw, *b)

# ---------------- tomorrow / date check / footer ----------------
TY = BY + BH + 6
txt(512, TY, "TOMORROW: BepiColombo orbit insertion at Mercury \u00b7 Akvan's toll counted across Odisha \u00b7 COP31 text fight may run into the weekend (AFP)",
    sans_b(10), NAVY, anchor="ma")
DY = TY + 18
rrect([12, DY, 1012, DY + 52], 4, fill=(255, 253, 246), outline=RED, width=1)
dc = ("Trump\u2013Xi\u2013Putin Shenzhen summit + nuclear declaration \u00b7 Anthropic $83bn IPO pricing & Nasdaq debut (+17%, close $97.17) \u00b7 "
      "ICJ Myanmar Rohingya genocide verdict (9\u20136) \u00b7 GTA VI midnight launch \u00b7 $190.4m Van Gogh sale \u00b7 Voyager 1 one-light-day confirmation \u00b7 "
      "Senate 48\u201351 Iran war-powers vote \u00b7 Austrian & Dutch embassies damaged in Kyiv strikes \u00b7 Bukele registers for third-term bid (Feb 2027 vote) \u00b7 "
      "Fiona the hippo dies, 9, after swallowing a visitor's hat \u00b7 Pentagon: Iran war cost $48.3bn (testimony Thu) \u00b7 "
      "UK & Norway fund \u00a3100m+ for two fast attack boats for Ukraine \u00b7 Indonesia passes asset-forfeiture law (18-year wait) \u00b7 "
      "Migrant boat sinks off Senegal \u2014 4 dead, dozens missing.")
txt(20, DY + 5, "DATE CHECK", sans_b(10), RED)
txt(92, DY + 5, "First reported Thursday 19 Nov, so NOT shown as Friday's news:", sans_b(10), INK)
para(20, DY + 19, dc, sans(9), 984, 11, (52, 52, 50), 3)
FY = DY + 56
txt(512, FY, "Every story here happened, or was first reported, on Friday 20 November 2026 in at least one time zone. Claims are attributed, not stated as fact.",
    sans(9), GREY, anchor="ma")
txt(512, FY + 12, "Sources: Reuters, AP, AFP, BBC, IMD, UN News, ICC, EORTC, and others \u2014 full list in SOURCES.md. Original vector drawings.",
    sans(9), GREY, anchor="ma")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
