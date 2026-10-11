#!/usr/bin/env python3
"""Build the relocation guides.

  python3 _build/build_guides.py            # inline the transit schematic, write PDFs, build web pages
  python3 _build/build_guides.py --preview /tmp/review   # also render every PDF page to PNG for review

PDFs are rendered by Playwright/Chromium from guides/print/*.html (fixed Letter pages, embedded fonts,
photos at 300 dpi for their printed size). Install once:  pip install playwright && python -m playwright install chromium
"""
import argparse, asyncio, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "_build"))
import transit_svg  # noqa: E402

GUIDES = {
    "greater-vancouver": "moving-to-greater-vancouver.pdf",
    "tri-cities": "moving-to-the-tri-cities.pdf",
}
MARK = re.compile(r"(<!-- transit:start -->)(.*?)(<!-- transit:end -->)", re.S)


def inline_schematic(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    new, n = MARK.subn(lambda m: m.group(1) + "\n" + transit_svg.svg() + "\n" + m.group(3), html)
    if n:
        path.write_text(new, encoding="utf-8")


async def render_pdf(src: Path, out: Path) -> None:
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(src.resolve().as_uri(), wait_until="networkidle")
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(250)
        await page.pdf(path=str(out), width="8.5in", height="11in", print_background=True,
                       prefer_css_page_size=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        await browser.close()


def preview(pdf: Path, outdir: Path, dpi: int = 110) -> int:
    import pymupdf
    outdir.mkdir(parents=True, exist_ok=True)
    for f in outdir.glob("page-*.png"):
        f.unlink()
    doc = pymupdf.open(pdf)
    for i, page in enumerate(doc):
        page.get_pixmap(dpi=dpi).save(outdir / f"page-{i + 1:02d}.png")
    return len(doc)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", help="directory for per-page PNG previews")
    ap.add_argument("--dpi", type=int, default=110)
    ap.add_argument("--only", choices=list(GUIDES), help="build a single guide")
    ap.add_argument("--no-pdf", action="store_true")
    args = ap.parse_args()

    transit_svg.main()
    for name, pdf_name in GUIDES.items():
        if args.only and name != args.only:
            continue
        src = ROOT / "guides" / "print" / f"{name}.html"
        inline_schematic(src)
        if args.no_pdf:
            continue
        out = ROOT / "guides" / pdf_name
        asyncio.run(render_pdf(src, out))
        size = out.stat().st_size / 1e6
        msg = f"{out.relative_to(ROOT)}  {size:.1f} MB"
        if args.preview:
            n = preview(out, Path(args.preview) / name, args.dpi)
            msg += f"  {n} pages -> {args.preview}/{name}"
        print(msg)

    try:
        import build_web_guides  # noqa: F401
        build_web_guides.main()
    except ImportError:
        pass


if __name__ == "__main__":
    main()
