#!/usr/bin/env python3
"""Render Meta ad creatives to exact 1080px PNGs. Not published."""
from pathlib import Path

ROOT = Path("/workspace")
OUT = ROOT / "_promo" / "creatives"
SRC = OUT / "src"
FONTS = ROOT / "guides" / "print" / "fonts"

ITEMS = [
    {
        "file": "greater-vancouver-v1",
        "photo": ROOT / "guides/img/kits-dusk.jpg",
        "credit": "Photo: Adam Jones, Ph.D., CC BY-SA 3.0, via Wikimedia Commons",
        "kicker": "Free guide",
        "title": "Moving to<br>Greater Vancouver",
        "deck": "The insider’s guide. Rents, SkyTrain, and the first 30 days.",
        "points": [],
        "headshot": False,
    },
    {
        "file": "greater-vancouver-v2",
        "photo": ROOT / "guides/img/canada-place.jpg",
        "credit": "Photo: Dietmar Rabich, CC BY-SA 4.0, via Wikimedia Commons",
        "kicker": "Free guide",
        "title": "Before you<br>send a deposit",
        "deck": "A practical guide for people moving to Greater Vancouver.",
        "points": [
            "September 2026 asking rents",
            "MLS benchmark prices",
            "SkyTrain and Compass fares",
            "A first-30-days checklist",
        ],
        "headshot": False,
    },
    {
        "file": "greater-vancouver-v3",
        "photo": ROOT / "guides/img/vancouver-skyline.jpg",
        "credit": "Photo: Larry Syverson, CC BY-SA 2.0, via Wikimedia Commons",
        "kicker": "Free guide",
        "title": "Rents, transit,<br>first 30 days",
        "deck": "Devin Desaulniers has lived here for 28 years.",
        "points": [],
        "headshot": True,
    },
    {
        "file": "tri-cities-v1",
        "photo": ROOT / "guides/img/port-moody-inlet.jpg",
        "credit": "Photo: Kalamazadkhan, CC BY-SA 4.0, via Wikimedia Commons",
        "kicker": "Free guide",
        "title": "Moving to<br>the Tri-Cities",
        "deck": "Coquitlam, Port Coquitlam, Port Moody, Anmore and Belcarra.",
        "points": [],
        "headshot": False,
    },
    {
        "file": "tri-cities-v2",
        "photo": ROOT / "guides/img/lafarge-lake.jpg",
        "credit": "Photo: Greg Salter, CC BY 2.5, via Wikimedia Commons",
        "kicker": "Free guide",
        "title": "Three cities.<br>Two villages.",
        "deck": "The insider’s guide to the Tri-Cities.",
        "points": [
            "Coquitlam, PoCo, Port Moody",
            "Anmore and Belcarra included",
            "Evergreen stations, named",
            "September 2026 benchmarks",
        ],
        "headshot": False,
    },
    {
        "file": "tri-cities-v3",
        "photo": ROOT / "guides/img/rocky-point.jpg",
        "credit": "Photo: Jeff Macleod, CC BY-SA 3.0, via Wikimedia Commons",
        "kicker": "Free guide",
        "title": "SkyTrain through<br>the Tri-Cities",
        "deck": "Stations, West Coast Express, and what a place costs.",
        "points": [],
        "headshot": True,
    },
]

CSS = """
@font-face{font-family:Inter;src:url("FONTS/Inter-400.ttf") format("truetype");font-weight:400}
@font-face{font-family:Inter;src:url("FONTS/Inter-600.ttf") format("truetype");font-weight:600}
@font-face{font-family:Montserrat;src:url("FONTS/Montserrat-700.ttf") format("truetype");font-weight:700}
@font-face{font-family:Newsreader;src:url("FONTS/Newsreader-500.ttf") format("truetype");font-weight:500}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#0d1b2a}
body.sq{width:1080px;height:1080px}
body.story{width:1080px;height:1920px}
.frame{position:relative;width:100%;height:100%;overflow:hidden;color:#fff}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.sq .bg{object-position:center 35%}
.story .bg{object-position:center 30%}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,27,42,.35) 0%,rgba(13,27,42,.12) 36%,rgba(13,27,42,.78) 100%)}
.with-points .shade{background:linear-gradient(180deg,rgba(13,27,42,.45) 0%,rgba(13,27,42,.55) 42%,rgba(13,27,42,.88) 100%)}
.logo{position:absolute;top:36px;left:36px;background:#fff;border-radius:14px;padding:12px 14px 10px;z-index:2}
.logo img{height:64px;width:auto;display:block}
.story .logo{top:48px;left:48px}
.story .logo img{height:78px}
.credit{position:absolute;right:40px;z-index:2;margin:0;max-width:460px;text-align:right;font-family:Inter,sans-serif;font-size:13px;line-height:1.3;color:rgba(255,255,255,.9);text-shadow:0 1px 3px rgba(0,0,0,.75)}
.sq .credit{top:48px}
.story .credit{top:64px;font-size:15px}
.copy{position:absolute;left:48px;right:48px;z-index:2}
.sq .copy{bottom:148px}
.story .copy{bottom:230px}
.kicker{margin:0 0 14px;font-family:Montserrat,sans-serif;font-weight:700;font-size:22px;letter-spacing:.18em;text-transform:uppercase;color:#93bde6}
.story .kicker{font-size:26px;margin-bottom:18px}
h1{margin:0 0 12px;font-family:Newsreader,Georgia,serif;font-weight:500;font-size:84px;line-height:.96;letter-spacing:-.02em}
.story h1{font-size:104px;margin-bottom:18px}
.deck{margin:0;max-width:820px;font-family:Inter,sans-serif;font-size:28px;line-height:1.35;color:#e7eef6}
.story .deck{font-size:34px}
ul{margin:22px 0 0;padding:0;list-style:none}
li{margin:0 0 10px;padding-left:22px;position:relative;font-family:Inter,sans-serif;font-size:28px;line-height:1.3}
.story li{font-size:34px;margin-bottom:14px}
li:before{content:"";position:absolute;left:0;top:.45em;width:10px;height:10px;border-radius:50%;background:#3474b6}
.who{display:flex;align-items:center;gap:18px;margin-top:22px}
.who img{width:92px;height:116px;object-fit:cover;object-position:50% 15%;border-radius:12px}
.story .who img{width:120px;height:150px}
.who strong{display:block;font-family:Montserrat,sans-serif;font-size:26px}
.story .who strong{font-size:32px}
.who span{display:block;font-family:Inter,sans-serif;font-size:20px;color:#c9d5e1}
.story .who span{font-size:24px}
.bar{position:absolute;left:0;right:0;bottom:0;z-index:3;height:128px;background:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 40px}
.story .bar{height:190px;padding:0 48px}
.bar img{height:48px;width:auto}
.story .bar img{height:64px}
.bar span{font-family:Montserrat,sans-serif;font-weight:700;font-size:22px;letter-spacing:.04em;color:#132639}
.story .bar span{font-size:28px}
"""

HTML = """<!doctype html>
<html lang="en-CA"><head><meta charset="utf-8"><title>{file}</title>
<style>{css}</style></head>
<body class="{size}{points_class}">
<div class="frame">
  <img class="bg" alt="" src="{photo}">
  <div class="shade"></div>
  <div class="logo"><img alt="Devin Desaulniers" src="{logo}"></div>
  <p class="credit">{credit}</p>
  <div class="copy">
    <p class="kicker">{kicker}</p>
    <h1>{title}</h1>
    <p class="deck">{deck}</p>
    {points}
    {who}
  </div>
  <div class="bar">
    <img alt="Axford Real Estate" src="{axford}">
    <span>Axford Real Estate</span>
  </div>
</div>
</body></html>
"""


def points_html(points):
    if not points:
        return ""
    lis = "".join(f"<li>{p}</li>" for p in points)
    return f"<ul>{lis}</ul>"


def who_html(show, head):
    if not show:
        return ""
    return (
        '<div class="who"><img alt="" src="{head}">'
        "<div><strong>Devin Desaulniers</strong>"
        "<span>Real Estate Associate</span></div></div>"
    ).format(head=head)


def main():
    SRC.mkdir(parents=True, exist_ok=True)
    css = CSS.replace("FONTS", FONTS.as_uri())
    logo = (ROOT / "assets/img/devin-logo.png").as_uri()
    axford = (ROOT / "assets/img/axford-logo.png").as_uri()
    head = (ROOT / "assets/img/devin-headshot-480.jpg").as_uri()
    for item in ITEMS:
        for size in ("sq", "story"):
            name = f"{item['file']}-{'1080x1080' if size == 'sq' else '1080x1920'}.html"
            html = HTML.format(
                file=item["file"],
                css=css,
                size=size,
                points_class=" with-points" if item["points"] else "",
                photo=item["photo"].as_uri(),
                credit=item["credit"],
                kicker=item["kicker"],
                title=item["title"],
                deck=item["deck"],
                points=points_html(item["points"]),
                who=who_html(item["headshot"], head),
                logo=logo,
                axford=axford,
            )
            (SRC / name).write_text(html)
            print(name)


if __name__ == "__main__":
    main()
