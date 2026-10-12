#!/usr/bin/env python3
"""Render the Meta ad creatives for the free moving guides as exact 1080px PNGs.

Writes the HTML sources to src/ and renders them with Playwright's Chromium.
Not published: the ads stay off until Devin approves the guides.

    python3 _promo/creatives/build_creatives.py            # write HTML and render PNGs
    python3 _promo/creatives/build_creatives.py --no-render
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_promo" / "creatives"
SRC = OUT / "src"
FONTS = ROOT / "guides" / "print" / "fonts"
IMG = ROOT / "guides" / "img"

# Photos are Pexels, CC0 or CC BY only, so an advertising composite raises no
# share-alike question. Credit lines stay on the image.
ITEMS = [
    {
        "file": "greater-vancouver-v1",
        "template": "cover",
        "photo": IMG / "vancouver-sunset.jpg",
        "pos": {"sq": "50% 62%", "story": "48% 60%"},
        "credit": "Photo: Adi K / Pexels",
        "kicker": "Free guide · Greater Vancouver",
        "title": "Moving to<br><em>Greater Vancouver</em>",
        "deck": "The insider’s guide. Rents, SkyTrain, and the first 30 days.",
        "points": [],
    },
    {
        "file": "greater-vancouver-v2",
        "template": "split",
        "photo": IMG / "gv-cover.jpg",
        "pos": {"sq": "50% 50%", "story": "50% 38%"},
        "credit": "Photo: Thomas K / Pexels",
        "kicker": "Free guide · Greater Vancouver",
        "title": "Before you<br><em>send a deposit</em>",
        "deck": "A practical guide for people moving to Greater Vancouver.",
        "points": [
            "September 2026 asking rents",
            "MLS benchmark prices",
            "SkyTrain and Compass fares",
            "A first-30-days checklist",
        ],
    },
    {
        "file": "greater-vancouver-v3",
        "template": "portrait",
        "photo": IMG / "skytrain-sunset.jpg",
        "pos": {"sq": "50% 55%", "story": "55% 55%"},
        "credit": "Photo: Glen Zi / Pexels",
        "kicker": "Free guide · Greater Vancouver",
        "title": "Rents, transit,<br><em>first 30 days</em>",
        "deck": "Devin Desaulniers has lived in Greater Vancouver for 28 years. This is what he tells people before they move.",
        "points": [],
    },
    {
        "file": "tri-cities-v1",
        "template": "cover",
        "photo": IMG / "buntzen-lake-dock.jpg",
        "pos": {"sq": "50% 100%", "story": "50% 45%"},
        "credit": "Photo: Ben Waardenburg, CC0, via Wikimedia Commons",
        "kicker": "Free guide · The Tri-Cities",
        "title": "Moving to<br><em>the Tri-Cities</em>",
        "deck": "Coquitlam, Port Coquitlam, Port Moody, Anmore and Belcarra.",
        "points": [],
    },
    {
        "file": "tri-cities-v2",
        "template": "split",
        "photo": IMG / "tc-cover.jpg",
        "pos": {"sq": "50% 50%", "story": "50% 42%"},
        "credit": "Photo: Adam Brown / Pexels",
        "kicker": "Free guide · The Tri-Cities",
        "title": "Three cities.<br><em>Two villages.</em>",
        "deck": "The insider’s guide to the Tri-Cities.",
        "points": [
            "Coquitlam, PoCo, Port Moody",
            "Anmore and Belcarra included",
            "Evergreen stations, named",
            "September 2026 benchmarks",
        ],
    },
    {
        "file": "tri-cities-v3",
        "template": "portrait",
        "photo": IMG / "lafarge-lake-lights.jpg",
        "pos": {"sq": "50% 55%", "story": "50% 55%"},
        "credit": "Photo: GoToVan, CC BY 2.0, via Wikimedia Commons",
        "kicker": "Free guide · The Tri-Cities",
        "title": "SkyTrain through<br><em>the Tri-Cities</em>",
        "deck": "Six Evergreen stations, West Coast Express, and what a place was listed for in September 2026.",
        "points": [],
    },
]

CSS = """
@font-face{font-family:Inter;src:url("FONTS/Inter-500.ttf") format("truetype");font-weight:500}
@font-face{font-family:Inter;src:url("FONTS/Inter-600.ttf") format("truetype");font-weight:600}
@font-face{font-family:Inter;src:url("FONTS/Inter-700.ttf") format("truetype");font-weight:700}
@font-face{font-family:Montserrat;src:url("FONTS/Montserrat-700.ttf") format("truetype");font-weight:700}
@font-face{font-family:Montserrat;src:url("FONTS/Montserrat-800.ttf") format("truetype");font-weight:800}
@font-face{font-family:Newsreader;src:url("FONTS/Newsreader-600.ttf") format("truetype");font-weight:600}
@font-face{font-family:Newsreader;src:url("FONTS/Newsreader-500i.ttf") format("truetype");font-weight:500;font-style:italic}
:root{--night:#0d1b2a;--ink:#132639;--blue:#3474b6;--sky:#93bde6;--on-night:#c9d5e1;--muted:#56616d}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--night)}
body.sq{width:1080px;height:1080px}
body.story{width:1080px;height:1920px}
.frame{position:relative;width:100%;height:100%;overflow:hidden;background:var(--night);color:#fff}
.photo{position:absolute;left:0;top:0;overflow:hidden}
.photo img{display:block;width:100%;height:100%;object-fit:cover}
.credit{position:absolute;z-index:3;margin:0;font-family:Inter,sans-serif;font-weight:500;font-size:15px;line-height:1.3;color:rgba(255,255,255,.92);text-shadow:0 1px 3px rgba(0,0,0,.8)}
.rule{position:absolute;z-index:2;background:var(--blue)}
.panel{position:absolute;z-index:2;display:flex;flex-direction:column;justify-content:center}
.kicker{margin:0 0 18px;font-family:Montserrat,sans-serif;font-weight:800;font-size:24px;letter-spacing:.16em;text-transform:uppercase;color:var(--sky)}
h1{margin:0;font-family:Newsreader,Georgia,serif;font-weight:600;line-height:.98;letter-spacing:-.015em;color:#fff}
h1 em{font-style:italic;font-weight:500;color:var(--sky)}
.deck{margin:22px 0 0;font-family:Inter,sans-serif;font-weight:500;font-size:30px;line-height:1.35;color:var(--on-night);text-wrap:balance}
ul{margin:30px 0 0;padding:0;list-style:none;display:grid;gap:16px}
li{display:flex;align-items:center;gap:16px;font-family:Inter,sans-serif;font-weight:600;font-size:29px;line-height:1.25;color:#fff}
li svg{flex:0 0 auto;width:38px;height:38px}
.bar{position:absolute;left:0;right:0;bottom:0;z-index:4;background:#fff;display:flex;align-items:center;gap:22px;padding:0 60px;color:var(--ink)}
.face{flex:0 0 auto;border-radius:50%;overflow:hidden;background:#ddd}
.face img{display:block;width:180%;height:auto;margin:-15% 0 0 -20%}
.who{flex:1 1 auto;min-width:0}
.who strong{display:block;font-family:Montserrat,sans-serif;font-weight:700;font-size:27px;letter-spacing:-.005em;color:var(--ink)}
.who span{display:block;margin-top:4px;font-family:Inter,sans-serif;font-weight:500;font-size:20px;color:var(--muted)}
.who span b{font-weight:600;color:var(--ink)}
.story .who .sep{display:none}
.story .who b{display:block;margin-top:2px}
.axford{flex:0 0 auto}
.axford img{display:block;width:auto}
.card{position:absolute;z-index:3;overflow:hidden;border:8px solid #fff;border-radius:18px;box-shadow:0 24px 60px rgba(0,0,0,.45);background:#444}
.card img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 10%}

/* Square 1080x1080 */
.sq .bar{height:140px}
.sq .face{width:88px;height:88px}
.sq .axford img{height:56px}
.sq .credit{top:26px;right:30px}

.sq.cover .photo{width:1080px;height:580px}
.sq.cover .rule{left:0;right:0;top:580px;height:8px}
.sq.cover .panel{left:0;right:0;top:588px;bottom:140px;padding:30px 60px 34px}
.sq.cover h1{font-size:100px}

.sq.split .photo{width:486px;height:940px}
.sq.split .rule{left:486px;top:0;width:8px;height:940px}
.sq.split .panel{left:494px;right:0;top:0;bottom:140px;padding:40px 56px}
.sq.split .kicker{font-size:21px;margin-bottom:16px}
.sq.split h1{font-size:82px}
.sq.split .deck{display:none}
.sq.split ul{margin-top:34px;gap:18px}
.sq.split li{font-size:28px}
.sq.split li svg{width:36px;height:36px}
.sq.split .credit{top:auto;right:auto;left:24px;bottom:160px;max-width:440px}

.sq.portrait .photo{width:1080px;height:540px}
.sq.portrait .rule{left:0;right:0;top:540px;height:8px}
.sq.portrait .panel{left:424px;right:60px;top:548px;bottom:140px;padding:30px 0 34px}
.sq.portrait .kicker{font-size:22px}
.sq.portrait h1{font-size:76px}
.sq.portrait .deck{font-size:25px;margin-top:18px}
.sq.portrait .card{left:60px;top:330px;width:316px;height:395px}
.sq.portrait .face{display:none}

/* Story 1080x1920 */
.story .bar{height:180px;padding:0 64px;gap:26px}
.story .face{width:112px;height:112px}
.story .axford img{height:70px}
.story .who strong{font-size:33px}
.story .who span{font-size:24px;margin-top:6px}
.story .credit{top:34px;right:34px;font-size:17px}
.story .kicker{font-size:28px;margin-bottom:24px}
.story .deck{font-size:38px;margin-top:28px}

.story.cover .photo{width:1080px;height:1060px}
.story.cover .rule{left:0;right:0;top:1060px;height:10px}
.story.cover .panel{left:0;right:0;top:1070px;bottom:180px;padding:40px 64px 48px}
.story.cover h1{font-size:124px}

.story.split .photo{width:1080px;height:860px}
.story.split .rule{left:0;right:0;top:860px;height:10px}
.story.split .panel{left:0;right:0;top:870px;bottom:180px;padding:40px 64px 48px}
.story.split h1{font-size:116px}
.story.split .deck{font-size:34px;margin-top:22px}
.story.split ul{margin-top:40px;gap:22px}
.story.split li{font-size:36px}
.story.split li svg{width:46px;height:46px}

.story.portrait .photo{width:1080px;height:1000px}
.story.portrait .rule{left:0;right:0;top:1000px;height:10px}
.story.portrait .panel{left:0;right:0;top:1010px;bottom:180px;padding:90px 64px 52px;justify-content:flex-start}
.story.portrait h1{font-size:120px}
.story.portrait .deck{font-size:40px}
.story.portrait .card{left:64px;top:510px;width:420px;height:525px}
.story.portrait .face{display:none}
"""

CHECK = (
    '<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="20" fill="#3474b6"/>'
    '<path d="M11.5 20.5l5.5 5.5 11.5-12" fill="none" stroke="#fff" stroke-width="3.6" '
    'stroke-linecap="round" stroke-linejoin="round"/></svg>'
)

HTML = """<!doctype html>
<html lang="en-CA"><head><meta charset="utf-8"><title>{file}</title>
<style>{css}</style></head>
<body class="{size} {template}">
<div class="frame">
  <div class="photo"><img alt="" src="{photo}" style="object-position:{pos}"></div>
  <p class="credit">{credit}</p>
  <div class="rule"></div>
  {card}
  <div class="panel">
    <p class="kicker">{kicker}</p>
    <h1>{title}</h1>
    <p class="deck">{deck}</p>
    {points}
  </div>
  <div class="bar">
    <div class="face"><img alt="" src="{face}"></div>
    <div class="who"><strong>Devin Desaulniers</strong><span>Real Estate Associate<i class="sep"> · </i><b>Axford Real Estate</b></span></div>
    <div class="axford"><img alt="Axford Real Estate" src="{axford}"></div>
  </div>
</div>
</body></html>
"""


def points_html(points):
    if not points:
        return ""
    lis = "".join(f"<li>{CHECK}<span>{p}</span></li>" for p in points)
    return f"<ul>{lis}</ul>"


def write_sources():
    SRC.mkdir(parents=True, exist_ok=True)
    css = CSS.replace("FONTS", FONTS.as_uri())
    axford = (ROOT / "assets/img/axford-logo.png").as_uri()
    face = (ROOT / "assets/img/devin-headshot-800.jpg").as_uri()
    portrait = (ROOT / "assets/img/devin-bw-720.jpg").as_uri()
    names = []
    for item in ITEMS:
        for size in ("sq", "story"):
            name = f"{item['file']}-{'1080x1080' if size == 'sq' else '1080x1920'}"
            card = (
                f'<div class="card"><img alt="Devin Desaulniers" src="{portrait}"></div>'
                if item["template"] == "portrait"
                else ""
            )
            html = HTML.format(
                file=name,
                css=css,
                size=size,
                template=item["template"],
                photo=item["photo"].as_uri(),
                pos=item["pos"][size],
                credit=item["credit"],
                kicker="Free guide" if (item["template"] == "split" and size == "sq") else item["kicker"],
                title=item["title"],
                deck=item["deck"],
                points=points_html(item["points"]),
                card=card,
                face=face,
                axford=axford,
            )
            (SRC / f"{name}.html").write_text(html)
            names.append(name)
    return names


def render(names):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name in names:
            w, h = (1080, 1080) if name.endswith("1080x1080") else (1080, 1920)
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            page.goto((SRC / f"{name}.html").as_uri())
            page.evaluate("document.fonts.ready")
            page.wait_for_function(
                "Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)"
            )
            page.screenshot(path=str(OUT / f"{name}.png"), clip={"x": 0, "y": 0, "width": w, "height": h})
            page.close()
            print(f"{name}.png")
        browser.close()


def main():
    names = write_sources()
    if "--no-render" not in sys.argv:
        render(names)


if __name__ == "__main__":
    main()
