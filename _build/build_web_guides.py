#!/usr/bin/env python3
"""Build the web editions of the relocation guides.

guides/_main-<slug>.html holds the page body (everything inside <main>). This script wraps it in the
site header and footer from partials.py, inlines the transit schematic between the
<!-- transit:start --> / <!-- transit:end --> markers, and writes guides/<slug>.html.
Run on its own or via build_guides.py.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "_build"))
import partials, transit_svg  # noqa: E402

MARK = re.compile(r"(<!-- transit:start -->)(.*?)(<!-- transit:end -->)", re.S)

# The guide pages set type heavier than the rest of the site; load the extra weights only here.
EXTRA_HEAD = (
    '<meta name="robots" content="noindex, nofollow">\n'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@700&family=Montserrat:wght@800'
    '&family=Newsreader:ital,opsz,wght@0,6..72,600;0,6..72,700;1,6..72,500&display=swap" rel="stylesheet">'
)

GUIDES = {
    "greater-vancouver": {
        "title": "Moving to Greater Vancouver: the relocation guide (October 2026) | Devin Desaulniers, Axford Real Estate",
        "desc": "Asking rents, September 2026 benchmark prices, SkyTrain and fares, schools, MSP, tenancy rules, property transfer tax "
                "and the first 30 days, with every figure dated and sourced. By Devin Desaulniers, Axford Real Estate, Port Moody.",
    },
    "tri-cities": {
        "title": "Moving to the Tri-Cities: the relocation guide (October 2026) | Devin Desaulniers, Axford Real Estate",
        "desc": "Coquitlam, Port Coquitlam, Port Moody, Anmore and Belcarra: the six Evergreen stations, September 2026 benchmark prices, "
                "asking rents, parks, SD43, the Buntzen pass and the first 30 days. By Devin Desaulniers, Axford Real Estate, Port Moody.",
    },
}


def build(slug: str, meta: dict) -> Path:
    body = (ROOT / "guides" / f"_main-{slug}.html").read_text(encoding="utf-8")
    body = re.sub(r"^\s*<main[^>]*>", "", body)
    body = re.sub(r"</main>\s*$", "", body)
    body = MARK.sub(lambda m: m.group(1) + "\n" + transit_svg.svg() + "\n" + m.group(3), body)
    html = (
        partials.head(meta["title"], meta["desc"], "guide", page_url=f"guides/{slug}.html",
                      body_class="guide-page", extra_head=EXTRA_HEAD, root="../", og_type="article")
        + body
        + partials.foot("../")
    )
    out = ROOT / "guides" / f"{slug}.html"
    out.write_text(html, encoding="utf-8")
    return out


def main() -> None:
    for slug, meta in GUIDES.items():
        out = build(slug, meta)
        print(f"{out.relative_to(ROOT)}  {out.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
