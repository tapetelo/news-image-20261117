#!/usr/bin/env python3
"""Render the 17 Nov 2026 world-news front page to entry.png.

Local-only Pillow renderer. The graded program is main.py (stdlib only);
this file just produces the pre-rendered image that main.py copies.
Story list and wording come from RESEARCH.md in this directory.
"""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

# ---- palette: newsprint ----
PAPER = (250, 246, 236)
INK = (24, 24, 24)
MUTED = (74, 70, 64)
RULE = (150, 140, 126)
ACCENT = (158, 28, 28)
BLUE = (28, 62, 110)
TEAL = (18, 96, 92)
GOLD = (176, 128, 24)
CARD = (255, 253, 248)
SKY = (178, 205, 226)
SEA = (96, 138, 178)
LAND = (196, 178, 140)


def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", name), size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, face, size, width_px):
    """Greedy wrap of `text` to fit `width_px` using the real font metrics."""
    f = font(face, size)
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= width_px:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, face, size, width_px, color=INK, leading=None):
    """Draw wrapped paragraph; return y just below the last line."""
    f = font(face, size)
    step = leading or int(size * 1.22)
    for line in wrap(draw, text, face, size, width_px):
        draw.text((x, y), line, font=f, fill=color)
        y += step
    return y


def card(draw, box, fill=CARD, outline=RULE, width=1):
    draw.rounded_rectangle(box, radius=6, fill=fill, outline=outline, width=width)


def kicker(draw, x, y, text, color=ACCENT):
    draw.text((x, y), text, font=font(SANS_B, 11), fill=color)
    return y + 15


# ---------------------------------------------------------------- masthead
def draw_masthead(draw):
    draw.rectangle([0, 0, W, 96], fill=INK)
    draw.text((512, 10), "THE WORLD TODAY", font=font(SERIF_B, 40),
              fill=(250, 246, 236), anchor="ma")
    draw.text((512, 58), "TUESDAY 17 NOVEMBER 2026  •  ONE DAY, ONE PAGE, EVERY STORY",
              font=font(SANS_B, 15), fill=(214, 196, 160), anchor="ma")
    draw.line([24, 96, W - 24, 96], fill=ACCENT, width=4)


# ------------------------------------------------------------ hero scenes
def scene_kerch(draw, x, y, w, h):
    """Broken bridge span sinking into the strait, drones overhead."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=SEA)
    # deck, left and right, with a gap in the middle
    deck_y = y + h - 62
    draw.rectangle([x, deck_y, x + w * 0.38, deck_y + 8], fill=(60, 58, 56))
    draw.rectangle([x + w * 0.62, deck_y, x + w, deck_y + 8], fill=(60, 58, 56))
    # fallen span, tilted, half-submerged
    draw.polygon([(x + w * 0.40, deck_y + 2), (x + w * 0.60, deck_y + 2),
                  (x + w * 0.57, y + h - 14), (x + w * 0.46, y + h - 14)],
                 fill=(96, 92, 88))
    # splash where the span hit the water
    for sx in (x + w * 0.44, x + w * 0.52, x + w * 0.58):
        draw.arc([sx - 8, y + h - 22, sx + 8, y + h - 4], 180, 360,
                 fill=(240, 244, 248), width=2)
    # support towers
    for tx in (x + 26, x + w - 40):
        draw.rectangle([tx, deck_y - 46, tx + 12, deck_y], fill=(70, 68, 66))
    # smoke from the fallen span
    for cx, cy, r in ((x + w * 0.52, deck_y - 6, 12), (x + w * 0.47, deck_y - 18, 9),
                      (x + w * 0.55, deck_y - 26, 7)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 118, 112))
    # drones: small dark crosses in the sky
    for dx, dy in ((x + 46, y + 14), (x + w - 60, y + 10), (x + w * 0.5, y + 22),
                   (x + w * 0.72, y + 30), (x + 90, y + 34)):
        draw.line([dx - 7, dy, dx + 7, dy], fill=INK, width=2)
        draw.line([dx, dy - 5, dx, dy + 5], fill=INK, width=2)


def scene_gulf(draw, x, y, w, h):
    """Radar base under drone attack; tankers burning in the strait."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 176, 110))
    draw.rectangle([x, y + h - 30, x + w, y + h], fill=(52, 92, 128))
    # radar dome + tower on a low island
    draw.rectangle([x + w * 0.62, y + h - 74, x + w * 0.62 + 10, y + h - 30],
                   fill=(70, 68, 66))
    draw.pieslice([x + w * 0.60, y + h - 96, x + w * 0.60 + 34, y + h - 62],
                  180, 360, fill=(240, 240, 235))
    # incoming drones as dark triangles with trails
    for dx, dy in ((x + 40, y + 22), (x + 120, y + 12), (x + 200, y + 30)):
        draw.polygon([(dx, dy + 6), (dx + 16, dy), (dx, dy - 6)], fill=INK)
        draw.line([dx + 18, dy, dx + 40, dy], fill=INK, width=2)
    # two tankers, one with a fire plume
    for tx in (x + 14, x + w * 0.30):
        draw.rectangle([tx, y + h - 24, tx + 74, y + h - 12], fill=(40, 40, 44))
        draw.rectangle([tx + 30, y + h - 36, tx + 40, y + h - 24], fill=(60, 58, 56))
    fx, fy = x + w * 0.30 + 37, y + h - 38
    for r, col in ((16, (226, 110, 30)), (10, (240, 178, 40)), (5, (250, 226, 110))):
        draw.ellipse([fx - r, fy - r, fx + r, fy + r], fill=col)


def scene_summits(draw, x, y, w, h):
    """Four flags / leaders' table in Manila, Shenzhen skyline behind."""
    draw.rectangle([x, y, x + w, y + h], fill=(196, 216, 236))
    # Shenzhen skyline
    base = y + h - 40
    for bx, bw, bh in ((x + 8, 26, 46), (x + 40, 20, 66), (x + 66, 30, 52),
                       (x + 102, 18, 78), (x + 126, 26, 58), (x + 158, 22, 70),
                       (x + 186, 30, 48), (x + 222, 24, 62), (x + 252, 28, 54),
                       (x + 286, 22, 44)):
        draw.rectangle([bx, base - bh, bx + bw, base], fill=(52, 76, 110))
    # summit table with four seats
    draw.rectangle([x + 60, base + 8, x + w - 60, base + 22], fill=(122, 64, 32))
    for sx in (x + 78, x + 132, x + 186, x + 240):
        draw.ellipse([sx, base - 14, sx + 16, base + 4], fill=(232, 214, 180))
        draw.rectangle([sx + 2, base + 2, sx + 14, base + 10], fill=(40, 60, 96))
    # small flags above the table
    for i, col in enumerate(((178, 34, 34), (30, 90, 160), (200, 60, 60),
                             (20, 120, 90))):
        fx = x + 88 + i * 52
        draw.line([fx, base - 46, fx, base - 16], fill=INK, width=2)
        draw.rectangle([fx, base - 46, fx + 26, base - 30], fill=col)


HEROES = [
    ("UKRAINE", "Bridge Falls Into Kerch Strait",
     "Ukraine says its forces collapsed the Kerch Bridge road arch and span "
     "again; Russia says it downed 1,441 drones.",
     scene_kerch),
    ("GULF WAR", "Iran Drones Hit US Radar Base",
     "Iran's Guards say drones hit a US radar at Sheikh Isa Air Base, Bahrain; "
     "the US struck a missile site on Qeshm Island; tankers hit in Hormuz.",
     scene_gulf),
    ("ASIA SUMMITS", "Trump, Xi, Putin: Shenzhen Thursday",
     "Trump held his first Quad summit in Manila on Tuesday — ahead of a "
     "first-ever Trump–Xi–Putin trilateral in Shenzhen on Thursday.",
     scene_summits),
]


def draw_heroes(draw):
    top, hh = 108, 236
    cw = (W - 48 - 2 * 12) // 3
    for i, (kick, head, fact, scene) in enumerate(HEROES):
        x = 24 + i * (cw + 12)
        card(draw, [x, top, x + cw, top + hh])
        scene(draw, x + 8, top + 8, cw - 16, 108)
        y = top + 122
        y = kicker(draw, x + 10, y, kick)
        y = para(draw, x + 10, y, head, SERIF_B, 19, cw - 20, leading=22)
        para(draw, x + 10, y + 4, fact, SANS, 12, cw - 20, color=MUTED, leading=15)

# ------------------------------------------------------------- medium icons
def icon_chart(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(222, 232, 244))
    pts = [(x + 8, y + s - 14), (x + 20, y + s - 30), (x + 32, y + s - 20),
           (x + 44, y + s - 40), (x + 56, y + s - 48)]
    d.line(pts, fill=BLUE, width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=ACCENT)


def icon_virus(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(244, 224, 224))
    cx, cy = x + s // 2, y + s // 2
    for a in range(0, 360, 45):
        import math
        ex = cx + int(22 * math.cos(math.radians(a)))
        ey = cy + int(22 * math.sin(math.radians(a)))
        d.line([cx, cy, ex, ey], fill=ACCENT, width=2)
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=ACCENT)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(178, 44, 44))


def icon_dome(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(232, 228, 216))
    d.pieslice([x + 14, y + 12, x + 50, y + 40], 180, 360, fill=TEAL)
    d.rectangle([x + 12, y + 38, x + 52, y + 52], fill=TEAL)
    for cx in (x + 20, x + 32, x + 44):
        d.rectangle([cx - 2, y + 40, cx + 2, y + 52], fill=PAPER)


def icon_factory(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(226, 232, 226))
    d.polygon([(x + 10, y + 44), (x + 10, y + 26), (x + 24, y + 26),
               (x + 24, y + 34), (x + 38, y + 34), (x + 38, y + 26),
               (x + 54, y + 26), (x + 54, y + 44)], fill=(90, 88, 84))
    d.rectangle([x + 46, y + 12, x + 52, y + 26], fill=(120, 118, 112))
    for cx, cy, r in ((x + 50, y + 8, 5), (x + 56, y + 4, 4)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 148, 142))


def icon_plane(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(222, 232, 244))
    d.polygon([(x + 8, y + 40), (x + 46, y + 20), (x + 52, y + 24),
               (x + 30, y + 42), (x + 20, y + 52), (x + 14, y + 48)],
              fill=(52, 52, 56))
    for cx, cy, r in ((x + 52, y + 14, 7), (x + 58, y + 8, 5)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(140, 138, 132))


def icon_scales(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(232, 228, 216))
    d.line([x + 32, y + 12, x + 32, y + 50], fill=INK, width=3)
    d.line([x + 12, y + 18, x + 52, y + 18], fill=INK, width=3)
    for cx in (x + 14, x + 50):
        d.line([cx, y + 18, cx, y + 32], fill=INK, width=2)
        d.pieslice([cx - 9, y + 30, cx + 9, y + 44], 0, 180, fill=GOLD)
    d.ellipse([x + 28, y + 46, x + 36, y + 54], fill=INK)


def icon_globe(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(214, 232, 228))
    d.ellipse([x + 8, y + 8, x + 56, y + 56], fill=(96, 150, 190))
    d.ellipse([x + 18, y + 16, x + 34, y + 30], fill=(90, 160, 110))
    d.ellipse([x + 36, y + 34, x + 50, y + 48], fill=(90, 160, 110))
    d.arc([x + 8, y + 8, x + 56, y + 56], 200, 340, fill=(240, 200, 60), width=3)


def icon_dots(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(244, 226, 224))
    for cx, cy, r in ((x + 18, y + 18, 6), (x + 38, y + 14, 5), (x + 48, y + 32, 7),
                      (x + 26, y + 36, 6), (x + 44, y + 48, 5), (x + 16, y + 48, 4)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 44, 44))


def icon_jet(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(222, 232, 244))
    d.ellipse([x + 6, y + 6, x + 26, y + 26], fill=(226, 90, 60))
    d.polygon([(x + 10, y + 46), (x + 50, y + 24), (x + 54, y + 28),
               (x + 28, y + 50), (x + 18, y + 54)], fill=(52, 52, 56))


def icon_tv(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(226, 226, 232))
    d.rectangle([x + 10, y + 14, x + 54, y + 44], fill=(40, 40, 44))
    d.line([x + 10, y + 14, x + 54, y + 44], fill=ACCENT, width=4)
    d.rectangle([x + 26, y + 44, x + 38, y + 50], fill=INK)
    d.text((x + 32, y + 22), "TV", font=font(SANS_B, 13), fill=(240, 240, 235),
           anchor="mm")


def icon_spiral(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(214, 228, 240))
    cx, cy = x + 32, y + 32
    for i, r in enumerate(range(4, 26, 3)):
        d.arc([cx - r, cy - r, cx + r, cy + r], i * 55, i * 55 + 150,
              fill=TEAL, width=3)


ICONS = {"chart": icon_chart, "virus": icon_virus, "dome": icon_dome,
         "factory": icon_factory, "plane": icon_plane, "scales": icon_scales,
         "globe": icon_globe, "dots": icon_dots, "jet": icon_jet,
         "tv": icon_tv, "spiral": icon_spiral}

MEDIUMS = [
    ("MARKETS", "Nvidia Doubles Sales; Dow Drops 849",
     "Nvidia Q3 revenue $115.8bn, up 103%; Dow fell 849 pts to 50,759.",
     "chart"),
    ("HEALTH", "Ebola Cases Top 11,000 in Congo",
     "WHO: DRC Ebola passes 11,000 cases, 5,400 deaths, 8 provinces.",
     "virus"),
    ("MONGOLIA", "Mongolian President Says He'll Resign",
     "Says he will quit over an alleged $25m bribe; parliament must accept.",
     "dome"),
    ("SERBIA", "Serbia's Students Take Their Seats",
     "Student List (140 of 250 seats) takes its seats in Belgrade.",
     "dome"),
    ("BANGLADESH", "Tear Gas on Garment Workers",
     "Police fired tear gas in Dhaka as workers blocked highways over pay.",
     "factory"),
    ("RUSSIA CRASH", "Military Plane Crashes; 19 Killed",
     "An-12 crashed in Siberia; ministry says all 19 aboard killed.",
     "plane"),
    ("MOZAMBIQUE", "Mondlane on Trial in Maputo",
     "Opposition leader faces five charges over 2024 protests; denies all.",
     "scales"),
    ("CLIMATE", "COP31 Split Over Fossil Fuels",
     "Ministers took over in Antalya as the draft split over fossil fuels.",
     "globe"),
    ("HEALTH", "US Loses Measles-Free Status",
     "PAHO: US lost measles-free status after 26 years; Mexico, Bolivia too.",
     "dots"),
    ("JAPAN", "Japan Scrambles Jets at Russians",
     "Suspected Russian jets entered airspace off Okinoshima; Japan protested.",
     "jet"),
    ("TURKEY", "Turkey Seizes Sözcü TV",
     "Police raided Sözcü TV pre-dawn, took it off air, detained four.",
     "tv"),
    ("WEATHER", "Cyclone Akvan Bears Down on India",
     "Akvan forecast to hit Nellore–Tuni ~noon Fri, winds 120–130 km/h.",
     "spiral"),
]


def draw_mediums(draw):
    top, rh = 356, 88
    cw = (W - 48 - 2 * 12) // 3
    for i, (kick, head, fact, key) in enumerate(MEDIUMS):
        r, c = divmod(i, 3)
        x = 24 + c * (cw + 12)
        y = top + r * (rh + 4)
        card(draw, [x, y, x + cw, y + rh])
        ICONS[key](draw, x + 8, y + 12, 64)
        tx = x + 80
        yy = kicker(draw, tx, y + 8, kick)
        yy = para(draw, tx, yy, head, SERIF_B, 15, cw - 90, leading=17)
        para(draw, tx, yy + 2, fact, SANS, 11, cw - 90, color=MUTED, leading=13)


# ---------------------------------------------------------------- world map
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-55, 62),
     (-55, 47), (-70, 42), (-80, 32), (-97, 26), (-105, 20), (-117, 33),
     (-125, 40), (-125, 49), (-150, 60)],
    [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -22), (-48, -28),
     (-58, -35), (-65, -41), (-70, -52), (-73, -37), (-80, -20)],
    [(-17, 15), (-10, 31), (10, 37), (20, 32), (32, 31), (43, 12), (51, 11),
     (48, -1), (40, -15), (32, -26), (20, -35), (12, -18), (9, 4), (-8, 5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (18, 56),
     (21, 55), (24, 59), (30, 60), (28, 65), (25, 71), (18, 70), (12, 65),
     (5, 60), (5, 58), (-5, 50)],
    [(30, 36), (28, 41), (35, 42), (40, 46), (48, 44), (52, 47), (55, 51),
     (60, 55), (68, 69), (75, 73), (90, 75), (110, 76), (130, 72), (160, 69),
     (178, 66), (162, 60), (158, 52), (142, 50), (140, 40), (135, 35),
     (127, 35), (122, 30), (120, 25), (110, 20), (105, 10), (100, 8),
     (98, 15), (92, 22), (88, 22), (80, 13), (77, 8), (72, 20), (66, 25),
     (58, 25), (52, 28), (48, 29), (44, 29), (40, 32), (36, 36)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (140, -38), (147, -39), (150, -37), (153, -27), (146, -19), (142, -11),
     (136, -12), (132, -12), (126, -14), (122, -17)],
]

# (number, lon, lat, dx, dy) — dx/dy nudge pins apart in crowded Europe
PINS = [
    (1, 38.0, 45.0, 10, -10), (2, 50.5, 26.2, 0, 0), (3, 121.0, 14.6, 10, -8),
    (4, 114.0, 22.5, -8, 10), (5, 23.0, -2.5, 0, 0), (6, 106.9, 47.9, 0, 0),
    (7, 20.5, 44.8, 10, 10), (8, 90.4, 23.8, 0, 0), (9, 86.0, 55.4, 0, 0),
    (10, 32.6, -25.9, 0, 0), (11, 30.7, 36.9, -10, 12), (12, 133.0, 36.3, 0, 0),
    (13, 29.0, 41.0, 12, 8), (14, 80.5, 15.8, 0, 0), (15, -77.0, 38.9, 0, 0),
    (16, 2.35, 48.86, -4, 12), (17, -0.1, 51.5, -16, -10),
    (18, 28.8, 47.0, 14, -6),
    (19, 45.0, 12.8, 0, 0), (20, 19.0, 47.5, -14, -10),
]


def draw_map(draw):
    mx, my, mw, mh = 24, 724, 540, 288
    card(draw, [mx, my, mx + mw, my + mh])
    draw.text((mx + 12, my + 8), "WHERE IT HAPPENED",
              font=font(SANS_B, 14), fill=INK)
    ox, oy, ow, oh = mx + 8, my + 34, mw - 16, mh - 76

    def project(lon, lat):
        return (ox + (lon + 180) / 360 * ow,
                oy + (75 - lat) / 135 * oh)

    draw.rectangle([ox, oy, ox + ow, oy + oh], fill=(196, 216, 236))
    for poly in CONTINENTS:
        draw.polygon([project(lon, lat) for lon, lat in poly], fill=LAND,
                     outline=(140, 126, 100))
    f = font(SANS_B, 7)
    for num, lon, lat, dx, dy in PINS:
        px, py = project(lon, lat)
        px, py = px + dx, py + dy
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=ACCENT,
                     outline=(255, 255, 255), width=1)
        draw.text((px, py), str(num), font=f, fill=(255, 255, 255), anchor="mm")
    lf = font(SANS, 9)
    draw.text((mx + 12, my + mh - 26),
              "Europe detail — 1 Kerch Strait · 7 Belgrade · 11 Antalya · "
              "13 Istanbul", font=lf, fill=MUTED)
    draw.text((mx + 12, my + mh - 14),
              "16 Paris · 17 London · 18 Chișinău · 20 Budapest",
              font=lf, fill=MUTED)


# ------------------------------------------------------------------- briefs
BRIEFS = [
    "Kyiv bridges hit — Russia struck 2 Kyiv bridges; 14 killed, 78 hurt.",
    "Drones over Chișinău — Moldova says 7 Russian drones entered airspace.",
    "Salavat refinery hit — Ukraine says it hit a refinery 1,200 km away.",
    "Tanker hit twice — LPG tanker Tara Gas struck again; 1 crew missing.",
    "Houthis hit Saudi pipeline — Houthis say 5 drones hit 2 pump stations.",
    "Third US carrier — A third US carrier strike group arrived in the Gulf.",
    "Brent near $93 — Brent ~$93.18 as Hormuz shipping stayed disrupted.",
    "S&P lowest since July — S&P 500 fell 1.03% to 7,340; Salesforce -9.5%.",
    "Bitcoin near $64,000 — Bitcoin slid to ~$64,000, down 13% in a week.",
    "US retail sales +0.2% — October sales rose 0.2% to $748.2bn, as expected.",
    "No Huang return — Nvidia chair says no plan to reinstate Jensen Huang.",
    "Anthropic IPO next — Anthropic prices IPO Wed at $70–$78; ticker ANT.",
    "178 sites hacked — Poisoned Optimizely script hit 178 sites (Mon).",
    "NSA network down — Classified NSANet went down Tue; NSA says maintenance.",
    "France marches — Pay strike drew 146,000 marchers; CGT claims 500,000+.",
    "Chase bug (Monday) — JPMorgan bug Mon delayed online banking and Zelle.",
    "Pattinson is Bond — Amazon MGM says Pattinson is the next Bond (Mon).",
    "Buried millions — Hungary recovered ~$19.5m in cash in a bribery probe.",
    "Houthis near Aden — Yemeni forces pulled back; Houthis now ~60 km away.",
    "UK sanctions settlers — Britain sanctioned 8 settlement firms and Tzav 9.",
    "Manila arrests — Philippine police detained ~300 in anti-Trump protests.",
    "Starshield row — Zelenskyy says caps cut drones off; SpaceX denies it.",
    "Rwanda return hub — 5 states plan return-hub talks with Rwanda.",
    "Seoul scrambles jets — South Korea scrambled jets over Russian aircraft.",
]


def draw_briefs(draw):
    bx, by, bw, bh = 576, 724, 424, 288
    card(draw, [bx, by, bx + bw, by + bh])
    draw.text((bx + 12, by + 8), "ALSO ON TUESDAY 17 NOVEMBER",
              font=font(SANS_B, 13), fill=INK)
    draw.line([bx + 12, by + 28, bx + bw - 12, by + 28], fill=RULE, width=1)
    f = font(SANS, 10)
    y = by + 32
    for i, line in enumerate(BRIEFS, 1):
        text = f"{i}. {line}"
        while draw.textlength(text, font=f) > bw - 24 and len(text) > 4:
            text = text[:-4].rstrip() + "…"
        draw.text((bx + 12, y), text, font=f, fill=INK)
        y += 10.2


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_heroes(draw)
    draw_mediums(draw)
    draw_map(draw)
    draw_briefs(draw)
    img.save(os.path.join(HERE, "entry.png"), optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
