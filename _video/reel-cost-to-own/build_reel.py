#!/usr/bin/env python3
"""Draft Instagram reel: cost to own a home, for Devin Desaulniers.

Renders a 1080x1920, 30 fps H.264/AAC MP4 plus stills and sources.md.
Numbers are computed in this file from the inputs documented in sources.md.
Nothing here is posted.

Usage:
  python3 build_reel.py --preview 8
  python3 build_reel.py
"""

from __future__ import annotations

import math
import subprocess
import wave
import zipfile
from pathlib import Path

import numpy as np
import shapefile
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
CACHE = ROOT / "cache"
ART = Path("/opt/cursor/artifacts")
HEADSHOT = REPO / "assets" / "img" / "devin-headshot-800.jpg"

W, H = 1080, 1920
FPS = 30
DURATION = 58.0
NFRAMES = int(DURATION * FPS)

# Brand, sampled from assets/css/styles.css
NIGHT = (13, 27, 42)
NIGHT2 = (10, 22, 36)
BLUE = (52, 116, 182)
BLUE_DARK = (36, 87, 140)
BLUE_DEEP = (23, 58, 94)
SKY = (147, 189, 230)
WHITE = (255, 255, 255)
INK_ON = (232, 240, 246)
MUTED = (151, 169, 187)
GREY = (176, 186, 196)
TRACK = (28, 46, 66)
GOLD = (232, 196, 126)  # reserved; the reel does not use a gold badge

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIFB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"
SANSM = "/usr/share/fonts/truetype/macos/Inter-Medium.ttf"
SANSS = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"
SANSB = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"

# Safe zone: keep type out of the top 250 px and the bottom 350 px.
TOP, BOTTOM = 270, 1560
LEFT, RIGHT = 76, 1004


def font(path, size):
    return ImageFont.truetype(path, size)


F = {
    "eye": font(SANSS, 26),
    "h1": font(SERIF, 78),
    "h2": font(SERIF, 64),
    "h3": font(SERIF, 52),
    "num": font(SERIFB, 92),
    "pct": font(SERIFB, 68),
    "body": font(SANSM, 34),
    "body2": font(SANS, 30),
    "small": font(SANS, 24),
    "tiny": font(SANS, 22),
    "city": font(SANSB, 34),
    "month": font(SANS, 26),
    "name": font(SERIF, 60),
    "endsub": font(SANSS, 28),
}


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, xy, fnt, fill, max_w, line_h, anchor="lt"):
    x, y = xy
    lines = wrap(text, fnt, max_w)
    for i, line in enumerate(lines):
        yy = y + i * line_h
        if anchor == "mt":
            draw.text((x, yy), line, font=fnt, fill=fill, anchor="mt")
        else:
            draw.text((x, yy), line, font=fnt, fill=fill, anchor="lt")
    return y + len(lines) * line_h


# ---------------------------------------------------------------------------
# Affordability math. See sources.md for every input.
# ---------------------------------------------------------------------------

def ca_monthly(loan, annual, n=360):
    """Canadian fixed mortgage: quoted rate compounded semi-annually."""
    i = (1 + annual / 2) ** (1 / 6) - 1
    return loan * i * (1 + i) ** n / ((1 + i) ** n - 1)


def us_monthly(loan, annual, n=360):
    i = annual / 12.0
    return loan * i * (1 + i) ** n / ((1 + i) ** n - 1)


def build_results():
    us_2018 = (4.75 + 4.63 + 4.62 + 4.55) / 4 / 100
    us_2026 = (7.28 + 7.40 + 7.40 + 7.32 + 7.24) / 5 / 100
    # StatCan publishes this median only in 2024 constant dollars ($82,900).
    # Back out an estimated 2018 nominal using Canada all-items CPI.
    van_2018_income = round(82900 * (133.4 / 160.9) / 100) * 100

    specs = [
        ("van18", "Vancouver", 1_032_400, 0.0377, van_2018_income, 2.56116 / 1000, ca_monthly, "CAD"),
        ("van26", "Vancouver", 1_068_600, 0.0466, 89900, 3.36394 / 1000, ca_monthly, "CAD"),
        ("la18", "Los Angeles", 749_000, us_2018, 72563, 0.01, us_monthly, "USD"),
        ("la26", "Los Angeles", 1_000_000, us_2026, 100145, 0.01, us_monthly, "USD"),
        ("ny18", "New York", 549_000, us_2018, 78478, 0.20919 * 0.06, us_monthly, "USD"),
        ("ny26", "New York", 745_000, us_2026, 102139, 0.19972 * 0.06, us_monthly, "USD"),
    ]
    out = {"us_2018": us_2018, "us_2026": us_2026, "van_2018_income": van_2018_income}
    for key, name, price, rate, income, tax_rate, payfn, cur in specs:
        loan = price * 0.80
        mtg = payfn(loan, rate)
        tax_m = price * tax_rate / 12
        monthly = mtg + tax_m
        share = (monthly * 12) / income
        out[key] = {
            "name": name,
            "price": price,
            "rate": rate,
            "income": income,
            "tax_rate": tax_rate,
            "mortgage": mtg,
            "tax_monthly": tax_m,
            "monthly": monthly,
            "share": share,
            "pct": int(round(share * 100)),
            "monthly_r": int(round(monthly / 10) * 10),
            "cur": cur,
        }
    return out


R = build_results()


def money(n, cur=""):
    return f"${n:,.0f}"


# ---------------------------------------------------------------------------
# Map
# ---------------------------------------------------------------------------

# North America Albers (sphere), standard parallels 29.5 / 45.5, origin 23N 96W.
_P1 = math.radians(29.5)
_P2 = math.radians(45.5)
_P0 = math.radians(23.0)
_L0 = math.radians(-96.0)
_N = 0.5 * (math.sin(_P1) + math.sin(_P2))
_C = math.cos(_P1) ** 2 + 2 * _N * math.sin(_P1)
_R0 = math.sqrt(_C - 2 * _N * math.sin(_P0)) / _N


def project(lon, lat):
    phi = math.radians(lat)
    lam = math.radians(lon)
    rho = math.sqrt(max(1e-12, _C - 2 * _N * math.sin(phi))) / _N
    theta = _N * (lam - _L0)
    return rho * math.sin(theta), _R0 - rho * math.cos(theta)


def ensure_shapefiles():
    """Natural Earth 50m, public domain. 110m admin-1 is United States only."""
    dest = CACHE / "ne50"
    need = dest / "ne_50m_admin_0_countries.shp"
    if need.exists():
        return dest
    dest.mkdir(parents=True, exist_ok=True)
    pairs = {
        "ne_50m_admin_0_countries.zip": "https://naciscdn.org/naturalearth/50m/cultural/ne_50m_admin_0_countries.zip",
        "ne_50m_admin_1_states_provinces.zip": "https://naciscdn.org/naturalearth/50m/cultural/ne_50m_admin_1_states_provinces.zip",
    }
    import urllib.request
    for name, url in pairs.items():
        zpath = dest / name
        if not zpath.exists():
            urllib.request.urlretrieve(url, zpath)
        with zipfile.ZipFile(zpath) as zf:
            zf.extractall(dest)
    return dest


def shape_rings(shape, step):
    pts = shape.points
    parts = list(shape.parts) + [len(pts)]
    for i in range(len(parts) - 1):
        ring = pts[parts[i] : parts[i + 1]]
        if len(ring) < 4:
            continue
        # Drop the far-north arctic clutter and tiny specks.
        if len(ring) < 12:
            continue
        if step > 1 and len(ring) > 40:
            ring = ring[::step]
            if ring[0] != ring[-1]:
                ring = ring + [ring[0]]
        yield ring


def load_map():
    folder = ensure_shapefiles()
    keep = {"Canada", "United States of America", "Mexico"}
    land = []
    countries = shapefile.Reader(str(folder / "ne_50m_admin_0_countries.shp"))
    for sr in countries.iterShapeRecords():
        name = sr.record.as_dict().get("NAME")
        if name not in keep:
            continue
        for ring in shape_rings(sr.shape, step=2):
            arr = np.array([project(xy[0], xy[1]) for xy in ring], dtype=np.float64)
            land.append((name, arr))
    regions = []
    states = shapefile.Reader(str(folder / "ne_50m_admin_1_states_provinces.shp"))
    for sr in states.iterShapeRecords():
        rec = sr.record.as_dict()
        admin = rec.get("admin") or ""
        name = rec.get("name") or ""
        if admin not in ("Canada", "United States of America"):
            continue
        for ring in shape_rings(sr.shape, step=3):
            arr = np.array([project(xy[0], xy[1]) for xy in ring], dtype=np.float64)
            regions.append((admin, name, arr))
    return land, regions


LAND, REGIONS = load_map()

CITIES = {
    "Vancouver": (-123.12, 49.28),
    "Los Angeles": (-118.24, 34.05),
    "New York": (-74.01, 40.71),
    "Miami": (-80.19, 25.77),
}
CITY_XY = {k: project(*v) for k, v in CITIES.items()}


def bbox(pts_list):
    xs, ys = [], []
    for pts in pts_list:
        xs.append(pts[:, 0].min())
        xs.append(pts[:, 0].max())
        ys.append(pts[:, 1].min())
        ys.append(pts[:, 1].max())
    return min(xs), min(ys), max(xs), max(ys)


NA_BBOX = bbox([p for _, p in LAND])
BC_PTS = [p for admin, name, p in REGIONS if name == "British Columbia"]
BC_BBOX = bbox(BC_PTS)


def box_from_lonlat(lon0, lat0, lon1, lat1):
    pts = [project(lon, lat) for lon in (lon0, lon1) for lat in (lat0, lat1)]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


# Southern Canada through Florida, so the arctic does not shrink the continent.
VIEW_BOX = box_from_lonlat(-130, 24, -66, 56)


def camera_fit(box, rect, pad=0.90):
    minx, miny, maxx, maxy = box
    l, t, r, b = rect
    pw, ph = max(maxx - minx, 1e-9), max(maxy - miny, 1e-9)
    scale = min((r - l) / pw, (b - t) / ph) * pad
    return {
        "cx": (minx + maxx) / 2,
        "cy": (miny + maxy) / 2,
        "scale": scale,
        "scx": (l + r) / 2,
        "scy": (t + b) / 2,
    }


CAM_HOOK = camera_fit(VIEW_BOX, (36, 900, 1044, 1460), 0.96)
CAM_CHART = camera_fit(VIEW_BOX, (36, 490, 1044, 900), 0.96)
CAM_BC = camera_fit(BC_BBOX, (20, 240, 1060, 1280), 0.82)
CAM_BC["scy"] = 700


def lerp_cam(a, b, t):
    return {k: lerp(a[k], b[k], t) for k in a}


def to_screen(pts, cam):
    x = cam["scx"] + (pts[:, 0] - cam["cx"]) * cam["scale"]
    y = cam["scy"] - (pts[:, 1] - cam["cy"]) * cam["scale"]
    return np.column_stack([x, y])


def poly_visible(scr):
    if scr.shape[0] < 3:
        return False
    return not (
        scr[:, 0].max() < -80
        or scr[:, 0].min() > W + 80
        or scr[:, 1].max() < -80
        or scr[:, 1].min() > H + 80
    )


FILL = {
    "Canada": (32, 74, 118),
    "United States of America": (24, 56, 92),
    "Mexico": (20, 46, 76),
}
BC_FILL = (52, 118, 176)


def draw_map(base, cam, highlight_bc=False, city_alpha=255):
    draw = ImageDraw.Draw(base)
    for name, pts in LAND:
        scr = to_screen(pts, cam)
        if not poly_visible(scr):
            continue
        draw.polygon([tuple(p) for p in scr], fill=FILL[name])
    # internal borders
    for admin, name, pts in REGIONS:
        scr = to_screen(pts, cam)
        if not poly_visible(scr):
            continue
        if highlight_bc and name == "British Columbia":
            draw.polygon([tuple(p) for p in scr], fill=BC_FILL)
        draw.line([tuple(p) for p in scr], fill=(86, 140, 186), width=2)
    for name, pts in LAND:
        scr = to_screen(pts, cam)
        if not poly_visible(scr):
            continue
        draw.line([tuple(p) for p in scr], fill=(168, 206, 230), width=3)
    return draw


def draw_cities(draw, cam, labels, alpha=255):
    for name in labels:
        x, y = to_screen(np.array([CITY_XY[name]]), cam)[0]
        if x < 20 or x > W - 20 or y < 180 or y > H - 200:
            continue
        r = 8
        draw.ellipse((x - r - 4, y - r - 4, x + r + 4, y + r + 4), fill=(13, 27, 42))
        col = BLUE if name == "Vancouver" else SKY
        draw.ellipse((x - r, y - r, x + r, y + r), fill=col)
        # label offset so it doesn't sit on the dot
        offsets = {
            "Vancouver": (14, -36),
            "Los Angeles": (14, 10),
            "New York": (14, -28),
            "Miami": (14, 8),
        }
        dx, dy = offsets[name]
        lx, ly = x + dx, y + dy
        anchor = "lt"
        if lx > W - 230:
            lx = x - 14
            anchor = "rt"
        tw = F["small"].getlength(name)
        if anchor == "lt":
            box = (lx - 8, ly - 4, lx + tw + 10, ly + 30)
        else:
            box = (lx - tw - 10, ly - 4, lx + 8, ly + 30)
        draw.rounded_rectangle(box, radius=6, fill=(8, 20, 34))
        draw.text((lx, ly), name, font=F["small"], fill=WHITE, anchor=anchor)


# ---------------------------------------------------------------------------
# Beats
# ---------------------------------------------------------------------------

BEATS = [
    ("hook", 0.0, 6.2),
    ("y2018", 6.2, 16.2),
    ("y2026", 16.2, 27.6),
    ("pop", 27.6, 35.2),
    ("invest", 35.2, 42.6),
    ("budget", 42.6, 48.6),
    ("cta", 48.6, 53.2),
    ("end", 53.2, 58.0),
]


def beat_at(t):
    for i, (name, a, b) in enumerate(BEATS):
        if a <= t < b or (i == len(BEATS) - 1 and t >= a):
            local = (t - a) / (b - a)
            return name, local, t - a, b - a
    return BEATS[-1][0], 1.0, 1.0, 1.0


def camera_at(t):
    name, local, elapsed, dur = beat_at(t)
    # Blend from the previous beat's camera over the first 1.1s.
    order = [b[0] for b in BEATS]
    idx = order.index(name)
    chartish = {"y2018", "y2026"}
    zoomed = {"pop", "invest", "cta", "end"}
    if name in zoomed:
        target = CAM_BC
    elif name == "budget":
        target = lerp_cam(CAM_CHART, CAM_BC, 0.35)
    elif name in chartish:
        target = CAM_CHART
    else:
        target = CAM_HOOK
    if idx == 0 or elapsed > 1.15:
        return target, name, local, elapsed
    prev_name = order[idx - 1]
    if prev_name in zoomed:
        prev = CAM_BC
    elif prev_name == "budget":
        prev = lerp_cam(CAM_CHART, CAM_BC, 0.35)
    elif prev_name in chartish:
        prev = CAM_CHART
    else:
        prev = CAM_HOOK
    return lerp_cam(prev, target, ease(elapsed / 1.15)), name, local, elapsed


def fade(elapsed, dur, inn=0.35, out=0.35):
    a = ease(elapsed / inn) if inn else 1
    b = ease((dur - elapsed) / out) if out else 1
    return max(0.0, min(1.0, min(a, b)))


def shade(color, alpha):
    """Blend a colour toward the night background by alpha 0..1 (1 = full colour)."""
    return tuple(int(lerp(NIGHT[i], color[i], alpha)) for i in range(3))


def vertical_wash(img, strength):
    """Darken toward the bottom so type stays readable. strength 0..1."""
    arr = np.asarray(img).astype(np.float32)
    y = np.linspace(0, 1, H)[:, None]
    # Keep the upper map, cover the lower type area.
    mask = np.clip((y - 0.28) / 0.42, 0, 1) ** 1.15
    mask = mask * (0.55 + 0.45 * strength)
    mask = mask[:, :, None]
    night = np.array(NIGHT, dtype=np.float32)
    arr = arr * (1 - mask) + night * mask
    img.paste(Image.fromarray(arr.astype(np.uint8)))


def rule(draw, y, alpha=1):
    draw.line((LEFT, y, LEFT + 56, y), fill=shade(SKY, alpha), width=3)


def footer(draw, lines, alpha, y=1420):
    """Source lines then the disclaimer, pinned above the bottom safe edge."""
    col = shade(MUTED, alpha)
    for line in lines:
        draw.text((LEFT, y), line, font=F["tiny"], fill=col, anchor="lt")
        y += 26
    draw.text(
        (LEFT, 1528),
        "General info, not financial advice. Figures are estimates.",
        font=F["tiny"],
        fill=shade((186, 198, 210), alpha),
        anchor="lt",
    )


def bar_row(draw, y, label, pct, monthly, color, progress, alpha, scale=80):
    name_c = shade(WHITE, alpha)
    sub_c = shade(MUTED, alpha)
    draw.text((LEFT, y), label, font=F["city"], fill=name_c, anchor="lt")
    draw.text((RIGHT, y - 10), f"{pct}%", font=F["pct"], fill=name_c, anchor="rt")
    ty = y + 52
    draw.rounded_rectangle((LEFT, ty, RIGHT, ty + 12), radius=6, fill=TRACK)
    width = (RIGHT - LEFT) * (pct / scale) * progress
    if width > 6:
        draw.rounded_rectangle((LEFT, ty, LEFT + width, ty + 12), radius=6, fill=shade(color, alpha))
    draw.text((LEFT, ty + 20), monthly, font=F["month"], fill=sub_c, anchor="lt")
    return ty + 58


def render(t):
    cam, name, local, elapsed = camera_at(t)
    _, _, _, dur = beat_at(t)
    img = Image.new("RGB", (W, H), NIGHT)
    highlight = name in ("pop", "invest", "cta", "end")
    draw_map(img, cam, highlight_bc=highlight)
    # city dots on map-forward beats
    d0 = ImageDraw.Draw(img)
    if name in ("hook", "y2018", "y2026", "pop"):
        labels = ["Vancouver", "Los Angeles", "New York"]
        if name == "hook":
            labels = labels + ["Miami"]
        draw_cities(d0, cam, labels)
    if name in ("hook", "y2018", "y2026"):
        # Solid panels keep type off the map. The window between them stays bright.
        band_top = 860 if name == "hook" else 500
        band_bot = 1500 if name == "hook" else 940
        cover = ImageDraw.Draw(img)
        cover.rectangle((0, 0, W, band_top), fill=NIGHT)
        cover.rectangle((0, band_bot, W, H), fill=NIGHT)
    elif name == "end":
        vertical_wash(img, 0.55)
        cover = ImageDraw.Draw(img)
        cover.rectangle((0, 760, W, H), fill=NIGHT)
    else:
        vertical_wash(img, 0.62 if name in ("invest", "budget", "cta") else 0.48)
    draw = ImageDraw.Draw(img)
    alpha = fade(elapsed, dur, 0.4, 0.32 if name != "end" else 0.0)
    # end card holds
    if name == "end":
        alpha = ease(min(1, elapsed / 0.45))

    if name == "hook":
        draw_hook(draw, alpha, elapsed)
    elif name == "y2018":
        draw_2018(draw, alpha, elapsed)
    elif name == "y2026":
        draw_2026(draw, alpha, elapsed)
    elif name == "pop":
        draw_pop(draw, alpha, elapsed)
    elif name == "invest":
        draw_invest(draw, alpha, elapsed)
    elif name == "budget":
        draw_budget(draw, alpha, elapsed)
    elif name == "cta":
        draw_cta(draw, alpha, elapsed)
    else:
        draw_end(img, draw, alpha)
    return img


def draw_hook(draw, alpha, elapsed):
    y = 300
    draw.text((LEFT, y), "COST TO OWN", font=F["eye"], fill=shade(SKY, alpha), anchor="lt")
    rule(draw, y + 40, alpha)
    y = 380
    y = draw_wrapped(
        draw,
        "What share of income does a home take?",
        (LEFT, y),
        F["h1"],
        shade(WHITE, alpha),
        RIGHT - LEFT,
        88,
    )
    y += 18
    draw_wrapped(
        draw,
        "Metro Vancouver, set beside U.S. cities. An estimate for a typical home.",
        (LEFT, y),
        F["body"],
        shade(INK_ON, alpha),
        RIGHT - LEFT,
        44,
    )
    chips_y = 760
    chips = ["Typical home", "20% down", "30 years"]
    x = LEFT
    for chip in chips:
        tw = F["small"].getlength(chip)
        draw.rounded_rectangle((x, chips_y, x + tw + 28, chips_y + 46), radius=8, fill=shade(BLUE_DEEP, alpha))
        draw.text((x + 14, chips_y + 10), chip, font=F["small"], fill=shade(SKY, alpha))
        x += tw + 42
    draw.text(
        (LEFT, 1532),
        "General info, not financial advice. Figures are estimates.",
        font=F["tiny"],
        fill=shade(MUTED, alpha),
    )


def draw_2018(draw, alpha, elapsed):
    prog = ease(min(1, max(0, (elapsed - 0.35) / 0.9)))
    draw.text((LEFT, 286), "DECEMBER 2018", font=F["eye"], fill=shade(SKY, alpha))
    rule(draw, 326, alpha)
    draw.text((LEFT, 348), "Share of income", font=F["h2"], fill=shade(WHITE, alpha))
    draw.text(
        (LEFT, 424),
        "Mortgage plus property tax. An estimate.",
        font=F["body2"],
        fill=shade(INK_ON, alpha),
    )
    y = 980
    rows = [
        ("van18", BLUE),
        ("la18", SKY),
        ("ny18", GREY),
    ]
    for key, col in rows:
        row = R[key]
        monthly = f"about {money(row['monthly_r'])} a month"
        y = bar_row(draw, y, row["name"], row["pct"], monthly, col, prog, alpha)
        y += 18
    footer(
        draw,
        [
            "Dec 2018 prices. Vancouver income is a 2018 estimate.",
            "L.A. tax is the 1% base. N.Y. is NYC Class 1, before caps.",
            "Vancouver tax uses the 2019 city rate. Map: Natural Earth.",
        ],
        alpha,
    )


def draw_2026(draw, alpha, elapsed):
    prog = ease(min(1, max(0, (elapsed - 0.3) / 0.9)))
    draw.text((LEFT, 286), "OCTOBER 2026", font=F["eye"], fill=shade(SKY, alpha))
    rule(draw, 326, alpha)
    draw.text((LEFT, 344), "The share, now", font=F["h2"], fill=shade(WHITE, alpha))
    y = 960
    rows = [("van26", BLUE), ("la26", SKY), ("ny26", GREY)]
    for key, col in rows:
        row = R[key]
        monthly = f"about {money(row['monthly_r'])} a month"
        y = bar_row(draw, y, row["name"], row["pct"], monthly, col, prog, alpha)
        y += 8
    note = (
        "Vancouver’s payment is higher than in 2018. "
        "Its share is lower, because income rose. "
        f"Miami’s median listing was {money(496000)}. "
        "It is not in the bars: property tax there is not one metro rate."
    )
    draw_wrapped(draw, note, (LEFT, y + 6), F["small"], shade(INK_ON, alpha), RIGHT - LEFT, 32)
    footer(
        draw,
        [
            "Oct 2026 prices. Income: Vancouver 2024, U.S. cities 2025.",
            "L.A. tax is the 1% base. N.Y. is NYC Class 1, before caps.",
            "Sources on screen are estimates. Map: Natural Earth.",
        ],
        alpha,
    )


def draw_pop(draw, alpha, elapsed):
    # count-up
    prog = ease(min(1, elapsed / 0.8))
    n = int(round(53270 * prog))
    draw.text((LEFT, 980), "BRITISH COLUMBIA", font=F["eye"], fill=shade(SKY, alpha))
    rule(draw, 1020, alpha)
    draw.text((LEFT, 1044), "Population fell", font=F["h2"], fill=shade(WHITE, alpha))
    draw.text((LEFT, 1130), f"{n:,}", font=F["num"], fill=shade(WHITE, alpha))
    draw_wrapped(
        draw,
        "fewer people in the 12 months to April 1, 2026. Down 0.9%, to 5,646,420.",
        (LEFT, 1240),
        F["body"],
        shade(INK_ON, alpha),
        RIGHT - LEFT,
        44,
    )
    draw_wrapped(
        draw,
        "That is the whole province, not only Metro Vancouver.",
        (LEFT, 1360),
        F["body2"],
        shade(SKY, alpha),
        RIGHT - LEFT,
        40,
    )
    footer(draw, ["BC Stats, quarterly highlights, released June 17, 2026."], alpha)


def draw_invest(draw, alpha, elapsed):
    draw.text((LEFT, 300), "PRESALE BUYERS", font=F["eye"], fill=shade(SKY, alpha))
    rule(draw, 340, alpha)
    draw_wrapped(
        draw,
        "Investors stepped back",
        (LEFT, 370),
        F["h2"],
        shade(WHITE, alpha),
        RIGHT - LEFT,
        74,
    )
    # two figures
    draw.text((LEFT, 560), "About half", font=F["h3"], fill=shade(WHITE, alpha))
    draw.text((LEFT, 630), "of rennie’s presale buyers", font=F["body2"], fill=shade(INK_ON, alpha))
    draw.text((LEFT, 678), "in the three years before 2024.", font=F["body2"], fill=shade(INK_ON, alpha))
    draw.text((LEFT, 760), "26%", font=F["num"], fill=shade(WHITE, alpha))
    draw.text((LEFT, 870), "in the first half of 2024.", font=F["body"], fill=shade(INK_ON, alpha))
    draw.line((LEFT, 940, RIGHT, 940), fill=shade(BLUE_DEEP, alpha), width=2)
    draw_wrapped(
        draw,
        "Also in 2025, the U.S. added tariffs on many Canadian goods that fall outside the USMCA.",
        (LEFT, 980),
        F["body"],
        shade(INK_ON, alpha),
        RIGHT - LEFT,
        44,
    )
    footer(
        draw,
        [
            "rennie, August 14, 2024. Not a forecast.",
            "Tariffs: U.S. Executive Order 14193, amended March 6, 2025.",
        ],
        alpha,
    )


def draw_budget(draw, alpha, elapsed):
    draw.text((LEFT, 300), "FEDERAL BUDGET 2026", font=F["eye"], fill=shade(SKY, alpha))
    rule(draw, 340, alpha)
    draw.text((LEFT, 380), "Tabled November 5", font=F["body"], fill=shade(SKY, alpha))
    draw_wrapped(
        draw,
        "Ottawa proposes that foreign buyers could purchase new homes again.",
        (LEFT, 460),
        F["h3"],
        shade(WHITE, alpha),
        RIGHT - LEFT,
        64,
    )
    draw_wrapped(
        draw,
        "The ban on existing homes would run to January 1, 2029.",
        (LEFT, 760),
        F["body"],
        shade(INK_ON, alpha),
        RIGHT - LEFT,
        44,
    )
    # pill
    pill = "A proposal. Not law yet."
    tw = F["body2"].getlength(pill)
    draw.rounded_rectangle((LEFT, 920, LEFT + tw + 36, 980), radius=10, fill=shade(BLUE_DEEP, alpha))
    draw.text((LEFT + 18, 936), pill, font=F["body2"], fill=shade(SKY, alpha))
    footer(
        draw,
        ["Budget 2026, Department of Finance Canada, November 5, 2026."],
        alpha,
    )


def draw_cta(draw, alpha, elapsed):
    draw.text((LEFT, 360), "THE OPEN QUESTION", font=F["eye"], fill=shade(SKY, alpha))
    rule(draw, 400, alpha)
    draw_wrapped(
        draw,
        "Will Metro Vancouver prices be higher or lower in 2027?",
        (LEFT, 450),
        F["h2"],
        shade(WHITE, alpha),
        RIGHT - LEFT,
        76,
    )
    tw = F["body"].getlength("Comment below")
    by = 860
    draw.rounded_rectangle((LEFT, by, LEFT + tw + 48, by + 64), radius=12, fill=shade(BLUE, alpha))
    draw.text((LEFT + 24, by + 14), "Comment below", font=F["body"], fill=shade(WHITE, alpha))
    footer(draw, ["No prediction. A question for the comments."], alpha)


_HEAD = None


def headshot():
    global _HEAD
    if _HEAD is not None:
        return _HEAD
    im = Image.open(HEADSHOT).convert("RGB")
    # The site headshot has the brokerage wordmark behind him. Paint those
    # side bands back to the backdrop grey so broken letters do not show.
    bg = (201, 199, 200)
    px = im.load()
    w, _h = im.size
    for y in range(120, 400):
        for x in range(w):
            # Only the band beside the head. Lower than this is shoulder.
            if x <= 170 or x >= 448:
                px[x, y] = bg
    crop = im.crop((150, 20, 640, 760)).resize((340, 510), Image.Resampling.LANCZOS)
    mask = Image.new("L", crop.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, crop.size[0] - 1, crop.size[1] - 1), radius=24, fill=255)
    out = Image.new("RGBA", crop.size)
    out.paste(crop, (0, 0))
    out.putalpha(mask)
    _HEAD = out
    return out


def draw_end(img, draw, alpha):
    photo = headshot()
    # fade photo
    if alpha < 0.999:
        ph = photo.copy()
        a = ph.split()[-1].point(lambda p: int(p * alpha))
        ph.putalpha(a)
        img.paste(ph, (LEFT, 240), ph)
    else:
        img.paste(photo, (LEFT, 240), photo)
    draw = ImageDraw.Draw(img)
    draw.text((LEFT, 790), "Devin Desaulniers", font=F["name"], fill=shade(WHITE, alpha))
    draw.text((LEFT, 870), "Real Estate Associate", font=F["endsub"], fill=shade(INK_ON, alpha))
    draw.text((LEFT, 918), "Axford Real Estate", font=F["h3"], fill=shade(WHITE, alpha))
    rule(draw, 990, alpha)
    draw.text((LEFT, 1020), "devindesaulniers.ca", font=F["body"], fill=shade(SKY, alpha))
    draw.text((LEFT, 1076), "604-809-1032", font=F["body"], fill=shade(WHITE, alpha))
    draw_wrapped(
        draw,
        "Greater Vancouver, including the Tri-Cities, BC.",
        (LEFT, 1148),
        F["body2"],
        shade(INK_ON, alpha),
        RIGHT - LEFT,
        40,
    )
    draw.text(
        (LEFT, 1532),
        "General info, not financial advice. Figures are estimates.",
        font=F["tiny"],
        fill=shade(MUTED, alpha),
    )


# ---------------------------------------------------------------------------
# Audio: original synth bed. No third-party recording.
# ---------------------------------------------------------------------------

def write_audio(path: Path):
    sr = 48000
    n = int(DURATION * sr)
    t = np.arange(n, dtype=np.float64) / sr
    # Slow fade over the whole reel.
    env = np.clip(t / 1.2, 0, 1) * np.clip((DURATION - t) / 1.4, 0, 1)
    # G minor-ish pad, original, no quoted melody.
    partials = [(196.00, 0.55), (233.08, 0.28), (293.66, 0.34), (392.00, 0.16)]
    pad = np.zeros(n)
    for freq, amp in partials:
        # slight detune between ears later
        pad += amp * np.sin(2 * math.pi * freq * t)
    trem = 0.86 + 0.14 * np.sin(2 * math.pi * 0.07 * t)
    pad *= 0.11 * env * trem
    rng = np.random.default_rng(27)
    noise = rng.normal(0, 1, n)
    # one-pole lowpass
    a = 0.012
    lp = np.empty(n)
    acc = 0.0
    for i in range(n):
        acc += a * (noise[i] - acc)
        lp[i] = acc
    lp *= 0.045 * env
    # very soft pulse, once a second, sine tick decayed
    pulse = np.zeros(n)
    period = int(sr * 1.15)
    click_n = int(sr * 0.18)
    decay = np.exp(-np.linspace(0, 5.5, click_n))
    tick = np.sin(2 * math.pi * 98 * np.arange(click_n) / sr) * decay
    for start in range(int(sr * 0.4), n - click_n, period):
        pulse[start : start + click_n] += tick
    pulse *= 0.05 * env
    left = pad + lp + pulse
    right = pad * 0.92 + np.roll(lp, 180) + pulse * 0.85
    stereo = np.column_stack([left, right])
    peak = np.max(np.abs(stereo))
    stereo *= 0.45 / peak
    pcm = np.clip(stereo * 32767, -32767, 32767).astype(np.int16)
    with wave.open(str(path), "w") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def sources_md():
    v18, v26 = R["van18"], R["van26"]
    la18, la26 = R["la18"], R["la26"]
    ny18, ny26 = R["ny18"], R["ny26"]

    def block(row):
        return (
            f"- Price used: {money(row['price'])} {row['cur']}\n"
            f"- Rate used: {row['rate']*100:.3f}%\n"
            f"- Income used: {money(row['income'])}\n"
            f"- Property-tax rate used: {row['tax_rate']*100:.3f}% of the price\n"
            f"- Mortgage: {money(row['mortgage'])}/month; tax: {money(row['tax_monthly'])}/month\n"
            f"- Ownership cost: {money(row['monthly'])}/month, {row['share']*100:.1f}% of income "
            f"(shown on screen as about {row['pct']}% and about {money(row['monthly_r'])}/month)\n"
        )

    return f"""# Cost to own — draft reel sources

Draft only. Not posted. Prepared for Devin Desaulniers, Real Estate Associate, Axford Real Estate.

This is an original reel. The public Instagram reel by @mosharifi.ca was used only as a pacing reference (hook, then a cost comparison, a local turn, a policy turn, a comment question, an end card). Its graphics, wording and figures were not copied. Every number below was taken from the source named, or computed from those inputs with the method in this note.

## Method

Affordability, as used on screen, is an **estimate**:

**annual mortgage payment + annual property tax, divided by median before-tax income.**

- Typical home: the price named for that city and month.
- Down payment: 20%. The loan is 80% of the price.
- Amortization: 30 years, 360 monthly payments. Canadian mortgages are often contracted on a shorter amortization. Thirty years is used here so the comparison is on one schedule, and it is labelled on screen.
- Canada rate math: the quoted annual rate is compounded semi-annually, which is the Canadian fixed-mortgage convention. Monthly rate i = (1 + r/2)^(1/6) − 1.
- U.S. rate math: monthly rate i = r/12.
- Payment = loan × i × (1+i)^360 / ((1+i)^360 − 1).
- Property tax = price × the rate below. It is not a quote from a tax bill.
- The result is an estimate. It leaves out heat, insurance, strata fees, maintenance, mortgage insurance (the 20% down payment is why insurance is left out), CMHC or U.S. mortgage insurance, and homestead or home-owner grants.
- Shares are rounded to the nearest percent on screen. Unrounded figures are in this note.
- On-screen line, on the data slides and the end card: "General info, not financial advice. Figures are estimates."

## December 2018 results

{block(v18)}
{block(la18)}
{block(ny18)}

## October 2026 results

{block(v26)}
{block(la26)}
{block(ny26)}

Vancouver’s estimated payment rose (about {money(v18['monthly_r'])} to about {money(v26['monthly_r'])} a month). Its share of income eased (about {v18['pct']}% to about {v26['pct']}%) because the income figure rose by more than the payment. Los Angeles moved the other way. That is the comparison the reel states. It is not a prediction.

## Prices

- **Metro Vancouver, December 2018.** MLS HPI composite benchmark for all residential homes in Greater Vancouver: **$1,032,400**. Real Estate Board of Greater Vancouver (now Greater Vancouver REALTORS), December 2018 statistics package, news release January 3, 2019. The benchmark is the board’s measure of a typical home, not an average sale price.
- **Metro Vancouver, October 2026.** MLS HPI composite benchmark for all residential properties: **$1,068,600**, down 5.2% from October 2025 and 0.7% from September 2026. Greater Vancouver REALTORS, “Buyers and sellers step back in October,” November 3, 2026. https://www.gvrealtors.ca/news/buyers-and-sellers-step-back-in-october
- **Los Angeles, New York and Miami, December 2018 and October 2026.** Realtor.com median listing price, via FRED (Federal Reserve Bank of St. Louis), not seasonally adjusted.
  - Los Angeles–Long Beach–Anaheim, CA (CBSA 31080), series MEDLISPRI31080. December 2018: **$749,000**. October 2026: **$1,000,000**.
  - New York–Newark–Jersey City (CBSA 35620), series MEDLISPRI35620. December 2018: **$549,000**. October 2026: **$745,000**.
  - Miami–Fort Lauderdale–West Palm Beach, FL (CBSA 33100), series MEDLISPRI33100. October 2026: **$496,000**. December 2018 was $390,000 and is not used on screen.
- A benchmark and a median listing are different measures. The reel labels them that way. They are not adjusted onto one index.

## Mortgage rates

- **Canada, both dates.** Bank of Canada, funds advanced, residential mortgages, uninsured, fixed rate, 5 years and over. Series **V122667786**. This is a volume-weighted average of what chartered banks charged that month, including renewals and refinances, not only new purchases. It matches a 20% down payment because it is the uninsured series. It is not the posted rate.
  - December 2018: **3.77%**.
  - September 2026: **4.66%**. Latest month published as of November 28, 2026 (the series lags). Used for the October 2026 estimate and labelled as the September rate in this note.
  - The posted 5-year conventional rate (series V80691335) was 5.34% in December 2018 and 6.19% in October and November 2026. Posted rates are list prices. They are not used in the payment.
- **United States.** Freddie Mac Primary Mortgage Market Survey, 30-year fixed, via FRED series **MORTGAGE30US**. The rate used is the average of the weekly readings in that month.
  - December 2018 weeks: 4.75, 4.63, 4.62, 4.55. Average **4.638%** (4.64% if rounded to two decimals; the payment uses the full average).
  - October 2026 weeks: 7.28, 7.40, 7.40, 7.32, 7.24. Average **7.328%**.

## Income

- **Vancouver, 2024 (used for the 2026 estimate).** Statistics Canada table 11-10-0190-01, median total income of economic families and persons not in an economic family, Vancouver CMA. **$89,900**. Quality indicator A. The table is published in 2024 constant dollars; for 2024 that is the same as current dollars. Total income is before tax, after government transfers. This is the closest annual StatCan series to a household median. It is not the census “household” concept: people who share a dwelling and are not related are not combined into one income. Release of the 2024 Canadian Income Survey: April 29, 2026. There is no 2025 or 2026 income figure yet. The reel says the income year.
- **Vancouver, 2018 (derived).** The same cell is published as **$82,900 in 2024 constant dollars**, quality indicator C (use is reasonable; the coefficient of variation is in the “good” band, 4% to 8%). StatCan did not publish that cell in 2018 current dollars in this table. This reel converts it with the Canada all-items CPI, annual average, 2002=100, table 18-10-0005-01: **133.4 in 2018** and **160.9 in 2024**. Estimated 2018 nominal median = 82,900 × 133.4 / 160.9 = 68,731, rounded to the nearest $100 = **$68,700**. That conversion assumes StatCan’s constant-dollar series uses this CPI. It is an estimate, and the 2018 Vancouver share is labelled as one.
- **United States, 2018.** U.S. Census Bureau, American Community Survey 1-year, median household income in the past 12 months, in 2018 dollars. ACS brief ACSBR/18-01, “Household Income: 2018” (the 2018 column).
  - Los Angeles–Long Beach–Anaheim: **$72,563** (margin of error ±$671).
  - New York–Newark–Jersey City, NY-NJ-PA: **$78,478** (±$729).
  - Miami–Fort Lauderdale–West Palm Beach: **$56,328** (±$732). Not used in a share, because Miami’s tax rate was not included.
- **United States, 2025 (used for the 2026 estimate).** U.S. Census Bureau, ACS brief ACSBR-028, “Household Income in States and Metropolitan Areas: 2025,” Appendix Table 2, 2025 ACS column, in 2025 inflation-adjusted dollars.
  - Los Angeles–Long Beach–Anaheim: **$100,145** (±$891).
  - New York–Newark–Jersey City, NY-NJ: **$102,139** (±$596).
  - Miami–Fort Lauderdale–West Palm Beach: **$83,261** (±$1,646). Not used in a share.

Income years do not match the price months. The 2026 bars use October 2026 prices with 2024 (Vancouver) and 2025 (U.S.) incomes, which are the latest medians published. If incomes rose after those surveys, the shares are a bit high.

## Property tax

Tax is price times a rate. It is not a looked-up bill, and it ignores home-owner grants, homestead exemptions and assessment caps unless noted.

- **Vancouver, 2026.** City of Vancouver, residential property tax rates, total of general purpose, provincial school, TransLink, BC Assessment, Metro Vancouver and the Municipal Finance Authority: **$3.36394 per $1,000** of taxable value (0.336394%). https://vancouver.ca/home-property-development/residential.aspx Applied to the regional benchmark. Rates differ by municipality. This is the City of Vancouver rate, used as an estimate for a home in the city.
- **Vancouver, 2018 price.** The full 2018 rate sheet could not be read as text from the city’s PDF. The adopted **2019** total residential rate, from Vancouver City Council’s May 14, 2019 rating report (Appendix A), is **$2.56116 per $1,000**. https://council.vancouver.ca/20190514/documents/a3.pdf That 2019 rate is applied to the December 2018 benchmark and labelled on screen (“Vancouver tax uses the 2019 city rate”). A modest difference in the 2018 rate would move the monthly tax by tens of dollars, not the rounded share.
- **Los Angeles, both years.** California Constitution article XIII A sets a general levy of **1%** of assessed value. For a purchase, assessed value starts at the price. Voter-approved bonds sit on top. The Los Angeles County Auditor-Controller’s 2025–26 Taxpayers’ Guide says that in most of the county the total rate does not exceed 1.25%. https://auditor.lacounty.gov/wp-content/uploads/2026/05/2025-2026-Taxpayers-Guide.pdf This reel uses **only the 1% base**, so the Los Angeles estimate is light. At 1.25% the shares would be about 64% (2018) and about 78% (2026). The ranking versus Vancouver does not flip at that ceiling. The on-screen line says the 1% base is what was used.
- **New York, both years.** New York City Department of Finance. Class 1 (one- to three-family homes) assessment ratio **6%** of market value. https://www.nyc.gov/site/finance/property/property-determining-your-assessed-value.page Class 1 tax rate **20.919%** of assessed value for 2018/19 and **19.972%** for 2026/27. https://www.nyc.gov/site/finance/property/property-tax-rates.page Statutory rate on price = 6% × the class rate: **1.255%** (2018/19) and **1.198%** (2026/27). State law caps how fast the assessed value can rise (6% a year and 20% over five years for Class 1), and exemptions lower many bills. A new buyer’s first bill can be under this statutory figure. The rate is NYC’s, applied to the metro median listing, which includes homes in New Jersey and elsewhere. Labelled on screen as NYC Class 1 before caps.

## Other on-screen facts

- **B.C. population.** BC Stats, Quarterly Population Highlights, reference date April 1, 2026, issue 26-01, released June 17, 2026. Population **5,646,420**. Change over the previous 12 months: **−53,270 (−0.9%)**. The same levels are reported from Statistics Canada table 17-10-0009-01 by other provincial statistical offices. The reel says this is the province, not only Metro Vancouver. https://www2.gov.bc.ca/assets/gov/data/statistics/people-population-community/population/quarterly_population_highlights.pdf
- **Presale investors.** rennie, “There’s a concrete anchor holding back Vancouver’s pre-sale market,” Roman Melzer, August 14, 2024. https://rennie.com/blog/theres-a-concrete-anchor-holding-back-vancouvers-pre-sale-market Investor purchases were **26%** of rennie’s presale transactions in the first half of 2024, down from **around 50%** over the prior three years. A later newspaper interview gave a different read of full-year 2025. That later figure is not used.
- **U.S. tariffs.** Executive Order 14193, February 1, 2025, imposed an additional 25% duty on articles that are products of Canada and 10% on Canadian energy. Federal Register, February 7, 2025. A March 6, 2025 amendment exempted goods that qualify for the USMCA preference and set potash outside that preference at 10%, effective March 7, 2025. The reel states that tariffs were added on many Canadian goods outside the USMCA. It does not claim a measured effect on home sales.
- **Budget 2026.** Department of Finance Canada, Budget 2026, tabled November 5, 2026. https://www.budget.canada.ca/2026/report-rapport/pdf/budget-2026.pdf The budget says: “Budget 2026 proposes to extend the ban on foreign purchases of existing residential properties for two years, to January 1, 2029, while exempting new residential properties.” It says legislation and a regulatory process would follow. The reel calls this a proposal, not law.

## What was left out

- **Miami’s share of income.** The October 2026 median listing ($496,000, Realtor.com via FRED MEDLISPRI33100) is stated. A single ownership share is not. The listing covers Miami–Fort Lauderdale–West Palm Beach, and property tax is a stack of county, city, school and district millages plus homestead exemptions. No one official rate fit that whole metro without inventing a blend.
- **The “7% of presale buyers” figure** that circulated from a first-quarter 2025 news report. A later 2026 interview with rennie’s lead analyst described 2025 as still near the 2024 share. The conflict is why only the August 2024 rennie article is used.
- **A causal link from 2025 tariffs to buyer counts.** No sourced housing number was tied to the tariff. The tariff is stated as its own fact.
- **S&P Case-Shiller dollar prices.** The index is not a home price. Listing medians were used instead.
- **Utilities, insurance and strata fees.** Not in the formula the reel defines.

## Map, music, type, photo

- **Map.** Natural Earth 1:110m cultural vectors (admin-0 countries and admin-1 states and provinces), public domain. https://www.naturalearthdata.com/ Projected with a North America Albers-style spherical projection for the animation. Coastlines are simplified at this scale on purpose.
- **Music.** Original synthesizer bed written for this reel in the build script (sine partials, a soft low-passed noise bed, and a quiet pulse). No third-party recording and no commercial song. No licence fee is due. Credit: original score, generated for this draft.
- **Type.** Inter (already on the machine; the site’s body face) and Liberation Serif as a stand-in for the site’s Newsreader headlines. Colours are the site tokens in `assets/css/styles.css`: night `#0d1b2a`, blue `#3474b6`, sky `#93bde6`.
- **Photo.** `assets/img/devin-headshot-800.jpg` from this site, cropped. The end card names Devin Desaulniers, Real Estate Associate, Axford Real Estate, devindesaulniers.ca, and 604-809-1032, and says Greater Vancouver, including the Tri-Cities, BC.

## Suggested caption (not posted)

What share of a household’s income does a typical home take?

This is an estimate for October 2026, set beside December 2018. Mortgage plus property tax, 20% down, 30 years. Metro Vancouver’s MLS benchmark barely moved. The payment still went up. The share eased, because incomes rose too. Los Angeles went the other way.

B.C.’s population fell by 53,270 in the 12 months to April 1, 2026 (BC Stats). rennie’s investor share of presale buyers was 26% in the first half of 2024, from about half in the three years before. Budget 2026, tabled November 5, proposes that foreign buyers could purchase new homes again. It is a proposal, not law.

Will Metro Vancouver prices be higher or lower in 2027? Comment below.

General info, not financial advice. Figures are estimates. Sources: Greater Vancouver REALTORS, Realtor.com, Bank of Canada, Freddie Mac, Statistics Canada, U.S. Census Bureau, City of Vancouver, BC Stats, rennie, Budget 2026.

#VancouverRealEstate #BCRealEstate #MetroVancouver #TriCitiesBC #GreaterVancouver
"""


def render_video(out_mp4: Path, wav: Path):
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", str(wav),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
        "-crf", "18", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-movflags", "+faststart",
        "-shortest",
        str(out_mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    stills = {
        90: "reel-cost-to-own-cover.jpg",          # hook, settled
        110: "reel-cost-to-own-frame-01-hook.jpg",
        360: "reel-cost-to-own-frame-02-2018.jpg",  # 12.0s
        690: "reel-cost-to-own-frame-03-2026.jpg",  # 23.0s
        960: "reel-cost-to-own-frame-04-population.jpg",  # 32.0s
        1365: "reel-cost-to-own-frame-05-budget.jpg",  # 45.5s
        1680: "reel-cost-to-own-frame-06-end.jpg",  # 56.0s
    }
    try:
        for i in range(NFRAMES):
            t = i / FPS
            frame = render(t)
            if i in stills:
                ART.mkdir(parents=True, exist_ok=True)
                frame.save(ART / stills[i], quality=92, subsampling=0)
            proc.stdin.write(frame.tobytes())
            if i % 150 == 0:
                print(f"frame {i}/{NFRAMES}", flush=True)
    finally:
        if proc.stdin:
            proc.stdin.close()
        err = proc.stderr.read().decode("utf-8", "replace") if proc.stderr else ""
        code = proc.wait()
    if code != 0:
        tail = "\n".join(err.splitlines()[-40:])
        raise SystemExit(f"ffmpeg failed ({code})\n{tail}")
    print("ffmpeg ok", out_mp4)


def main():
    import sys
    if "--preview" in sys.argv:
        t = float(sys.argv[sys.argv.index("--preview") + 1])
        im = render(t)
        dest = Path("/tmp/reel-preview.jpg")
        im.save(dest, quality=90)
        print("wrote", dest, "beat", beat_at(t)[0])
        for key in ("van18", "la18", "ny18", "van26", "la26", "ny26"):
            row = R[key]
            print(f"{key}: {row['pct']}%  ${row['monthly_r']}/mo  exact {row['share']*100:.2f}%")
        return
    print("Results:")
    for key in ("van18", "la18", "ny18", "van26", "la26", "ny26"):
        row = R[key]
        print(f"  {key}: {row['pct']}%  ${row['monthly_r']}/mo  exact {row['share']*100:.2f}%  income {row['income']}")
    ART.mkdir(parents=True, exist_ok=True)
    text = sources_md()
    (ROOT / "sources.md").write_text(text)
    (ART / "sources.md").write_text(text)
    wav = ROOT / "cache" / "bed.wav"
    wav.parent.mkdir(parents=True, exist_ok=True)
    print("audio…", flush=True)
    write_audio(wav)
    out = ART / "reel-cost-to-own-draft.mp4"
    print("video…", flush=True)
    render_video(out, wav)
    # duration check
    probe = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_name,width,height,avg_frame_rate,sample_rate,channels",
         "-of", "default=nw=1", str(out)],
        text=True,
    )
    print(probe)


if __name__ == "__main__":
    main()
