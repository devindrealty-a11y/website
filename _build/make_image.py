"""Featured image generator for blog posts (1200x630 JPG + WebP, branded).

Renders a small HTML template with headless Chrome, then encodes with ffmpeg:
    python3 make_image.py ../_posts/2026-10-06-some-slug.md          # only if missing
    python3 make_image.py --force ../_posts/2026-10-06-some-slug.md  # re-render after editing title/card/photo fields
    python3 make_image.py --all                                       # every post missing an image
    python3 make_image.py --force --bg /path/photo.jpg --photo-credit "Name / Wikimedia Commons (CC BY 4.0)" \\
        --out-dir /workspace/blog-brief/photo-samples ../_posts/YYYY-MM-DD-slug.md
Output: assets/img/blog/<YYYY-MM-DD>-<slug>.jpg and .webp (build.py also calls this for posts missing an image).
--out-dir writes the JPG/WebP there instead, and never touches the live assets/img/blog/ files.

A real licensed photo of the place the post is about should be set as the background (see BLOG.md).
The plain-blue gradient is used only when no photo is given.

Optional front matter used on the graphic (every figure must come from the post's cited sources):
    card_stat: "-8.4%"                                   big key number
    card_stat_label: "Metro Vancouver home sales, Sept 2026 vs Sept 2025"
    card_takeaway: "Short takeaway text"                 used instead of a number when the story has none
    card_chart_title: "Sales change by type, year over year"
    card_chart:                                          simple horizontal bar chart (2-5 bars)
      - label: Apartments
        value: -18.6
        display: "-18.6%"
    card_photo: assets/img/blog/photos/place.jpg         real place photo (required for place-specific posts)
    card_photo_position: center 35%                      optional CSS background-position
    card_photo_credit: "Name / Wikimedia Commons (CC BY 4.0)"
    card_photo_credit_url: https://commons.wikimedia.org/wiki/File:Example.jpg
The source line on the image comes from the first entry in `sources` (publisher + date).
"""
import os, sys, re, html, json, shutil, subprocess, tempfile, datetime
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG_DIR = os.path.join(ROOT, "assets", "img", "blog")
W, H = 1200, 630
MAX_BYTES = 200_000
esc = lambda s: html.escape(str(s), quote=True)

def find_chrome():
    for c in (os.environ.get("CHROME"), "google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        if c and shutil.which(c):
            return shutil.which(c)
    raise SystemExit("make_image: no Chrome/Chromium found (set CHROME=/path/to/chrome)")

def image_stem(post):
    return post["out"][:-5]  # 2026-10-06-slug

def image_paths(post):
    stem = image_stem(post)
    return (f"assets/img/blog/{stem}.jpg", f"assets/img/blog/{stem}.webp")

def resolve_photo(path):
    if not path:
        return ""
    p = path if os.path.isabs(path) else os.path.join(ROOT, path)
    if not os.path.isfile(p):
        raise SystemExit(f"make_image: background photo not found: {path}")
    return os.path.abspath(p)

def _num(v):
    try: return float(str(v).replace("%", "").replace("+", "").replace("\u2212", "-").replace(",", ""))
    except ValueError: raise SystemExit(f"make_image: card_chart value {v!r} is not a number")

def card_data(post, meta, photo_credit=None, photo_position=None):
    chart = []
    for b in meta.get("card_chart") or []:
        v = _num(b.get("value", ""))
        chart.append({"label": b.get("label", ""), "value": v, "display": b.get("display") or f"{v:+g}"})
    src = post["sources"][0]
    sdate = ""
    if re.match(r"^\d{4}-\d{2}-\d{2}$", src.get("date", "")):
        d = datetime.date.fromisoformat(src["date"]); sdate = f"{d:%b} {d.day}, {d.year}"
    source_line = "Source: " + ", ".join(x for x in (src.get("publisher") or src["title"], sdate) if x)
    credit = meta.get("card_photo_credit", "") if photo_credit is None else photo_credit
    position = (meta.get("card_photo_position", "") if photo_position is None else photo_position) or "center center"
    size = (meta.get("card_photo_size", "") or "cover").strip() or "cover"
    return {"title": post["title"], "category": post["category"], "stat": meta.get("card_stat", ""),
            "stat_label": meta.get("card_stat_label", ""), "takeaway": meta.get("card_takeaway", ""),
            "chart_title": meta.get("card_chart_title", ""), "chart": chart, "source": source_line,
            "photo_credit": credit or "", "photo_position": position, "photo_size": size}

def default_alt(c):
    parts = [f"Branded graphic for the blog post \u201c{c['title']}\u201d ({c['category']})."]
    if c["stat"]:
        parts.append(f"Key figure: {c['stat']}" + (f", {c['stat_label']}." if c["stat_label"] else "."))
    elif c["takeaway"]:
        parts.append(f"Takeaway: {c['takeaway']}")
    if c["chart"]:
        parts.append(f"Bar chart{(' of ' + c['chart_title'].lower()) if c['chart_title'] else ''}: "
                     + "; ".join(f"{b['label']} {b['display']}" for b in c["chart"]) + ".")
    parts.append(c["source"] + ".")
    if c.get("photo_credit"):
        parts.append(f"Background photo: {c['photo_credit']}.")
    return " ".join(parts)

def render_html(c, bg_url=""):
    mark = "file://" + os.path.join(ROOT, "assets/img/devin-mark.png")
    side = ""
    if c["stat"] or c["takeaway"] or c["chart"]:
        top = (f'<div class="stat">{esc(c["stat"])}</div><div class="stat-label">{esc(c["stat_label"])}</div>' if c["stat"]
               else (f'<div class="takeaway">{esc(c["takeaway"])}</div>' if c["takeaway"] else ""))
        bars = ""
        if c["chart"]:
            mx = max(abs(b["value"]) for b in c["chart"]) or 1
            rows = "".join(
                f'<div class="bar-row"><span class="bl">{esc(b["label"])}</span>'
                f'<span class="track"><span class="bar {"neg" if b["value"] < 0 else "pos"}" style="width:{max(3, abs(b["value"]) / mx * 100):.1f}%"></span></span>'
                f'<span class="bv">{esc(b["display"])}</span></div>' for b in c["chart"])
            ct = f'<div class="ct">{esc(c["chart_title"])}</div>' if c["chart_title"] else ""
            bars = f'<div class="chart">{ct}{rows}</div>'
        side = f'<div class="side">{top}{bars}</div>'
    if bg_url:
        pos = c.get("photo_position") or "center center"
        body_bg = "#173a5e"
        layers = (
            f'<div class="bg" style="background-image:url(\'{esc(bg_url)}\');background-size:{esc(c.get("photo_size") or "cover")};background-position:{esc(pos)}"></div>'
            f'<div class="overlay"></div>'
        )
        credit = f'<div class="credit">Photo: {esc(c["photo_credit"])}</div>' if c.get("photo_credit") else ""
        photo_css = """
.bg{position:absolute;inset:0;background-size:cover;background-repeat:no-repeat}
.overlay{position:absolute;inset:0;background:linear-gradient(180deg,rgba(12,28,46,.34) 0%,rgba(12,28,46,.50) 52%,rgba(12,28,46,.70) 100%),linear-gradient(90deg,rgba(23,58,94,.28) 0%,rgba(23,58,94,.10) 60%,rgba(23,58,94,.14) 100%)}
h1{text-shadow:0 2px 18px rgba(0,0,0,.45)}
.credit{position:absolute;left:64px;bottom:96px;z-index:2;font-size:14px;color:rgba(255,255,255,.86);letter-spacing:.01em;max-width:520px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-shadow:0 1px 8px rgba(0,0,0,.55)}
"""
    else:
        body_bg = "linear-gradient(135deg,#173a5e 0%,#24578c 45%,#3474b6 100%)"
        layers = ""
        credit = ""
        photo_css = ""
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{font-family:"Inter",system-ui,sans-serif;background:{body_bg};color:#fff;position:relative}}
.ring{{position:absolute;right:-140px;top:-160px;width:520px;height:520px;border-radius:50%;border:70px solid rgba(255,255,255,.05);z-index:1;pointer-events:none}}
.main{{position:absolute;left:64px;top:56px;right:64px;bottom:118px;display:flex;gap:44px;align-items:center;z-index:2}}
.left{{flex:1;min-width:0;height:100%;display:flex;flex-direction:column;justify-content:center}}
.cat{{align-self:flex-start;background:#fff;color:#173a5e;font-family:"Montserrat",sans-serif;font-weight:700;font-size:20px;letter-spacing:.12em;text-transform:uppercase;padding:9px 18px;border-radius:999px;margin-bottom:26px}}
h1{{font-family:"Montserrat",sans-serif;font-weight:700;line-height:1.12;font-size:60px;color:#fff;overflow:hidden}}
.side{{flex:0 0 430px;background:#fff;color:#1f2933;border-radius:22px;padding:30px 32px;box-shadow:0 18px 40px rgba(0,0,0,.25)}}
.stat{{font-family:"Montserrat",sans-serif;font-weight:700;font-size:88px;line-height:1;color:#3474b6;letter-spacing:-.02em}}
.stat-label{{font-size:21px;line-height:1.3;color:#5b6670;margin-top:10px}}
.takeaway{{font-family:"Montserrat",sans-serif;font-weight:600;font-size:30px;line-height:1.25;color:#173a5e}}
.chart{{margin-top:22px;padding-top:18px;border-top:2px solid #e8f0f9}}
.ct{{font-size:16px;font-weight:600;color:#808082;text-transform:uppercase;letter-spacing:.08em;margin-bottom:12px}}
.bar-row{{display:flex;align-items:center;gap:12px;margin:9px 0}}
.bl{{flex:0 0 118px;font-size:19px;font-weight:600;color:#173a5e;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.track{{flex:1;height:22px;background:#f0f2f5;border-radius:6px;overflow:hidden}}
.bar{{display:block;height:100%;border-radius:6px}}
.bar.pos{{background:#3474b6}} .bar.neg{{background:#808082}}
.bv{{flex:0 0 78px;text-align:right;font-family:"Montserrat",sans-serif;font-weight:700;font-size:20px;color:#1f2933}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:86px;background:#fff;display:flex;align-items:center;gap:16px;padding:0 64px;z-index:3}}
.foot img.mark{{height:52px;width:auto}}
.site{{font-family:"Montserrat",sans-serif;font-weight:600;font-size:21px;color:#808082;white-space:nowrap}}
.site b{{color:#3474b6;font-weight:700}}
.src{{margin-left:auto;font-size:17px;color:#808082;text-align:right;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}}
.foot img.ax{{height:30px;width:auto;margin-left:18px}}
{photo_css}
</style></head><body>{layers}<div class="ring"></div>
<div class="main"><div class="left"><div class="cat">{esc(c["category"])}</div><h1 id="t">{esc(c["title"])}</h1></div>{side}</div>
{credit}
<div class="foot"><img class="mark" src="{mark}" alt=""><span class="site"><b>devindesaulniers.ca</b> · Axford Real Estate</span>
<span class="src">{esc(c["source"])}</span></div>
<script>
// shrink the title until it fits its column (max 5 lines)
var t=document.getElementById('t'),box=t.parentNode,s=60;
function over(){{return t.scrollHeight>box.clientHeight-80||t.getBoundingClientRect().height>5*s*1.12+2}}
while(s>30&&over()){{s-=2;t.style.fontSize=s+'px'}}
</script></body></html>'''

def prepare_bg(src, dest):
    """Copy a reasonably sized JPEG into the temp dir so Chrome can load it locally."""
    r = subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", "scale=1920:-2", "-q:v", "2", dest],
        capture_output=True, text=True)
    if r.returncode != 0 or not os.path.isfile(dest):
        shutil.copy2(src, dest)

def generate(post, meta, force=False, bg=None, photo_credit=None, photo_position=None, out_dir=None):
    stem = image_stem(post)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        jpg, webp = os.path.join(out_dir, stem + ".jpg"), os.path.join(out_dir, stem + ".webp")
        jpg_rel, webp_rel = jpg, webp
        force = True
    else:
        jpg_rel, webp_rel = image_paths(post)
        jpg, webp = os.path.join(ROOT, jpg_rel), os.path.join(ROOT, webp_rel)
    if not force and os.path.isfile(jpg) and os.path.isfile(webp):
        return jpg_rel
    if not shutil.which("ffmpeg"):
        raise SystemExit("make_image: ffmpeg is required to encode the JPG/WebP")
    os.makedirs(IMG_DIR, exist_ok=True)
    c = card_data(post, meta, photo_credit=photo_credit, photo_position=photo_position)
    photo = bg if bg is not None else meta.get("card_photo", "")
    with tempfile.TemporaryDirectory() as td:
        page, png = os.path.join(td, "card.html"), os.path.join(td, "card.png")
        bg_url = ""
        if photo:
            bg_tmp = os.path.join(td, "bg.jpg")
            prepare_bg(resolve_photo(photo), bg_tmp)
            bg_url = "file://" + quote(bg_tmp, safe="/:")
        open(page, "w", encoding="utf-8").write(render_html(c, bg_url=bg_url))
        cmd = [find_chrome(), "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--mute-audio",
               "--allow-file-access-from-files", "--force-device-scale-factor=1", f"--window-size={W},{H}",
               "--virtual-time-budget=4000", f"--user-data-dir={os.path.join(td, 'profile')}", f"--screenshot={png}", "file://" + page]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if not os.path.isfile(png):
            raise SystemExit("make_image: Chrome did not produce a screenshot\n" + (r.stderr or r.stdout or "")[-2000:])
        crop = f"crop={W}:{H}:0:0,format=yuv420p"
        for q in (3, 4, 5, 7, 9):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", png, "-vf", crop, "-q:v", str(q), jpg], check=True)
            if os.path.getsize(jpg) <= MAX_BYTES: break
        for q in (85, 78, 70, 60):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", png, "-vf", f"crop={W}:{H}:0:0", "-c:v", "libwebp", "-quality", str(q), webp], check=True)
            if os.path.getsize(webp) <= MAX_BYTES: break
    print(f"  image: {jpg_rel} ({os.path.getsize(jpg)//1024} KB) + .webp ({os.path.getsize(webp)//1024} KB)")
    return jpg_rel

def _parse_args(argv):
    force, do_all = False, False
    out_dir = bg = photo_credit = photo_position = None
    files = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--force":
            force = True; i += 1
        elif a == "--all":
            do_all = True; i += 1
        elif a in ("--out-dir", "--bg", "--photo-credit", "--photo-position"):
            if i + 1 >= len(argv):
                raise SystemExit(f"make_image: {a} needs a value")
            val = argv[i + 1]
            if a == "--out-dir": out_dir = val
            elif a == "--bg": bg = val
            elif a == "--photo-credit": photo_credit = val
            else: photo_position = val
            i += 2
        elif a.startswith("--"):
            raise SystemExit(f"make_image: unknown option {a}")
        else:
            files.append(a); i += 1
    return force, do_all, out_dir, bg, photo_credit, photo_position, files

if __name__ == "__main__":
    sys.path.insert(0, HERE)
    import blog
    force, do_all, out_dir, bg, photo_credit, photo_position, files = _parse_args(sys.argv[1:])
    if do_all:
        files = [os.path.join(blog.POSTS_DIR, f) for f in sorted(os.listdir(blog.POSTS_DIR)) if f.endswith(".md")]
    if not files:
        raise SystemExit(__doc__)
    for f in files:
        post, meta = blog.load_one(os.path.basename(f), with_meta=True)
        generate(post, meta, force=force, bg=bg, photo_credit=photo_credit,
                 photo_position=photo_position, out_dir=out_dir)
