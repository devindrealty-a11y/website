#!/usr/bin/env python3
"""Draws the original straight-line transit schematic used in the relocation guides.
It is deliberately not a TransLink map: straight lines, TransLink's station order, not to scale.
Run directly to rewrite guides/transit-schematic.svg; import `svg()` to inline it in a page."""
from pathlib import Path

INK, BLUE, MUTED, LINE = "#132639", "#3474b6", "#56616d", "#e1e6eb"
EXPO, MILL, CANADA, WCE = "#132639", "#3474b6", "#1f8a70", "#7a2e4a"
F_LABEL = 'font-family="Montserrat,Arial,sans-serif" font-weight="800" letter-spacing="1.6"'
F_TEXT = 'font-family="Inter,Arial,sans-serif"'

W = 700

def svg(standalone: bool = False) -> str:
    o = []
    H = 560
    head = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="transitTitle transitDesc">'
    o.append(head)
    o.append('<title id="transitTitle">Schematic of SkyTrain and the West Coast Express</title>')
    o.append('<desc id="transitDesc">An original straight-line diagram drawn for this guide. It is not a TransLink map and it is not to scale. '
             'Canada Line runs from Waterfront to Richmond–Brighouse with a branch to YVR–Airport. Expo Line runs from Waterfront through Commercial–Broadway, Burnaby and New Westminster into Surrey. '
             'Millennium Line, west to east: VCC–Clark, Commercial–Broadway, Renfrew, Rupert, Gilmore, Brentwood Town Centre, Holdom, Sperling–Burnaby Lake, Lake City Way, Production Way–University, Lougheed Town Centre, '
             'Burquitlam, Moody Centre, Inlet Centre, Coquitlam Central, Lincoln, Lafarge Lake–Douglas. The last six are the Evergreen Extension, part of the Millennium Line. '
             'West Coast Express, west to east: Waterfront, Moody Centre, Coquitlam Central, Port Coquitlam, Pitt Meadows, Maple Meadows, Port Haney, Mission City.</desc>')
    o.append(f'<rect width="{W}" height="{H}" rx="12" fill="#f4f6f8"/>')

    def label(x, y, text, color, size=10.5, anchor="start"):
        o.append(f'<text x="{x}" y="{y}" {F_LABEL} font-size="{size}" fill="{color}" text-anchor="{anchor}">{text}</text>')

    def txt(x, y, text, size=13, color=INK, weight=600, anchor="middle"):
        o.append(f'<text x="{x}" y="{y}" {F_TEXT} font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{text}</text>')

    def dot(x, y, color, r=6, ring=False):
        if ring:
            o.append(f'<circle cx="{x}" cy="{y}" r="{r+1}" fill="#fff" stroke="{color}" stroke-width="3.5"/>')
        else:
            o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')

    # ---- Canada Line ----
    y = 58
    label(28, y - 22, "CANADA LINE", CANADA)
    txt(135, y - 22, "Waterfront to Richmond, with a branch to the airport.", 12, MUTED, 500, "start")
    o.append(f'<line x1="60" y1="{y}" x2="400" y2="{y}" stroke="{CANADA}" stroke-width="7" stroke-linecap="round"/>')
    o.append(f'<line x1="250" y1="{y}" x2="250" y2="{y+30}" stroke="{CANADA}" stroke-width="7" stroke-linecap="round"/>')
    dot(60, y, CANADA, 7, True); dot(400, y, CANADA, 7); dot(250, y + 30, CANADA, 7)
    txt(60, y + 24, "Waterfront", 12.5); txt(400, y + 24, "Richmond–Brighouse", 12.5); txt(266, y + 34, "YVR–Airport", 12.5, INK, 600, "start")
    txt(W - 28, y + 46, "SeaBus: Waterfront ⇄ Lonsdale Quay", 12, MUTED, 500, "end")

    # ---- Expo Line ----
    y = 150
    label(28, y - 22, "EXPO LINE", EXPO)
    txt(118, y - 22, "Waterfront through Burnaby and New Westminster into Surrey. Rings are transfers.", 12, MUTED, 500, "start")
    o.append(f'<line x1="60" y1="{y}" x2="672" y2="{y}" stroke="{EXPO}" stroke-width="7" stroke-linecap="round"/>')
    stops = [(60, "Waterfront", True), (205, "Commercial–Broadway", True), (350, "Metrotown", False), (500, "New Westminster", False), (672, "King George", False)]
    for x, name, ring in stops:
        dot(x, y, EXPO, 6, ring)
    txt(60, y + 24, "Waterfront", 12.5, INK, 600, "start"); txt(205, y + 24, "Commercial–Broadway", 12.5); txt(350, y + 24, "Metrotown", 12.5)
    txt(500, y + 24, "New Westminster", 12.5); txt(672, y + 24, "King George", 12.5, INK, 600, "end")

    # ---- Millennium Line ----
    y = 290
    label(28, y - 62, "MILLENNIUM LINE", MILL)
    txt(165, y - 62, "The Evergreen Extension is the east end of this line. You stay on the same train.", 12, MUTED, 500, "start")
    xs = [30 + i * 26 for i in range(11)] + [350 + i * 60 for i in range(6)]  # dense west, wide Evergreen
    # city bands
    def band(x1, x2, text, fill, color):
        o.append(f'<rect x="{x1}" y="{y-40}" width="{x2-x1}" height="20" rx="10" fill="{fill}"/>')
        label((x1 + x2) / 2, y - 26, text, color, 9.5, "middle")
    band(xs[0] - 22, xs[3] + 22, "VANCOUVER · 4", "#e8f0f9", "#24578c")
    band(xs[4] - 8, xs[10] + 14, "BURNABY · 7", "#e8f0f9", "#24578c")
    band(xs[11] - 16, xs[16] + 16, "TRI-CITIES · 6 STATIONS", "#d7e6f6", "#173a5e")
    o.append(f'<line x1="{xs[0]}" y1="{y}" x2="{xs[16]}" y2="{y}" stroke="{MILL}" stroke-width="7" stroke-linecap="round"/>')
    names = ["VCC–Clark", "Commercial–Broadway", "Renfrew", "Rupert", "Gilmore", "Brentwood Town Centre", "Holdom", "Sperling–Burnaby Lake", "Lake City Way", "Production Way–University", "Lougheed Town Centre",
             "Burquitlam", "Moody Centre", "Inlet Centre", "Coquitlam Central", "Lincoln", "Lafarge Lake–Douglas"]
    rings = {1, 9, 10}
    for i, x in enumerate(xs):
        if i >= 11:
            dot(x, y, "#173a5e", 8)
        elif i in rings:
            dot(x, y, MILL, 6, True)
        else:
            dot(x, y, MILL, 4.5)
    # labels: west stations only for transfers; all six Evergreen stations
    def two(x, y1, a, b, size=12.5, anchor="middle"):
        txt(x, y1, a, size, INK, 600, anchor); txt(x, y1 + 15, b, size, INK, 600, anchor)
    two(xs[0], y + 60, "VCC–", "Clark", 12, "start")
    two(xs[1] - 10, y + 26, "Commercial–", "Broadway", 12, "start")
    two(xs[9], y + 26, "Production", "Way–Univ.", 12)
    two(xs[10], y + 60, "Lougheed", "Town Ctr", 12)
    txt(xs[11], y + 26, "Burquitlam", 13)
    two(xs[12], y + 60, "Moody", "Centre", 13)
    two(xs[13], y + 26, "Inlet", "Centre", 13)
    two(xs[14], y + 60, "Coquitlam", "Central", 13)
    txt(xs[15], y + 26, "Lincoln", 13)
    two(xs[16], y + 60, "Lafarge Lake–", "Douglas", 13)
    # legend
    ly = y + 100
    o.append(f'<circle cx="40" cy="{ly}" r="5" fill="#fff" stroke="{MILL}" stroke-width="3.5"/>')
    txt(54, ly + 4, "Change here for the Expo Line", 12, MUTED, 500, "start")
    o.append(f'<circle cx="290" cy="{ly}" r="7" fill="#173a5e"/>')
    txt(304, ly + 4, "Evergreen Extension stations (Coquitlam and Port Moody)", 12, MUTED, 500, "start")

    # ---- West Coast Express ----
    y = 480
    label(28, y - 30, "WEST COAST EXPRESS", WCE)
    txt(205, y - 30, "Weekday rush hour only: westbound mornings, eastbound afternoons.", 12, MUTED, 500, "start")
    xw = [60 + i * 87 for i in range(8)]  # 60..669
    o.append(f'<line x1="{xw[0]}" y1="{y}" x2="{xw[-1]}" y2="{y}" stroke="{WCE}" stroke-width="6" stroke-linecap="round"/>')
    wn = ["Waterfront", "Moody Centre", "Coquitlam Central", "Port Coquitlam", "Pitt Meadows", "Maple Meadows", "Port Haney", "Mission City"]
    for i, (x, n) in enumerate(zip(xw, wn)):
        dot(x, y, WCE, 6)
        anchor = "start" if i == 0 else ("end" if i == 7 else "middle")
        txt(x, y + (24 if i % 2 == 0 else 44), n, 12.5, INK, 600, anchor)
    txt(W - 28, H - 14, "Original schematic drawn for this guide. Not a TransLink map. Not to scale. Checked 11 October 2026.", 10.5, MUTED, 500, "end")
    o.append("</svg>")
    out = "\n".join(o)
    if standalone:
        out = out.replace("<svg ", '<svg style="font-family:Inter,Arial,sans-serif" ', 1)
    return out

def main() -> None:
    p = Path(__file__).resolve().parent.parent / "guides" / "transit-schematic.svg"
    p.write_text(svg(standalone=True), encoding="utf-8")


if __name__ == "__main__":
    main()
