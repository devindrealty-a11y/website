"""Blog: turns Markdown posts in _posts/ into blog/ pages, blog/feed.xml and the home-page strip.

How to add a post: see _build/BLOG.md. No third-party packages needed (tiny built-in
front-matter + Markdown parser below), so `python3 build.py` works on a bare Python 3.9+.
"""
import os, re, json, html, datetime
from email.utils import format_datetime
from zoneinfo import ZoneInfo
from partials import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT, "_posts")
BLOG_DIR = os.path.join(ROOT, "blog")
TZ = ZoneInfo("America/Vancouver")
CATEGORIES = ["Buying", "Selling", "Renting", "Market news", "FAQ"]
CAT_CLASS = {"Buying": "buying", "Selling": "selling", "Renting": "renting", "Market news": "market", "FAQ": "faq"}
CTA_FOR_CAT = {"Buying": "buying", "Selling": "selling", "Renting": "renting", "Market news": "general", "FAQ": "general"}
FILENAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
BLOG_NAME = "Devin Desaulniers' Greater Vancouver Real Estate Blog"
BLOG_DESC = "Greater Vancouver and Tri-Cities, BC real estate news, explained in plain language by Devin Desaulniers, Real Estate Associate with Axford Real Estate."
DISCLAIMER = "This post is general information and my personal opinion, not legal, tax or financial advice."
BYLINE = "By Devin Desaulniers, Real Estate Associate, Axford Real Estate"

esc = lambda s: html.escape(str(s), quote=True)

class PostError(Exception):
    pass

# ---------------------------------------------------------------- front matter
def _unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return v

def parse_front_matter(text, fn):
    if not text.startswith("---"):
        raise PostError(f"{fn}: must start with a '---' front matter block")
    parts = text.split("\n")
    try:
        end = next(i for i in range(1, len(parts)) if parts[i].strip() == "---")
    except StopIteration:
        raise PostError(f"{fn}: front matter is not closed with '---'")
    meta, cur_list, cur_item = {}, None, None
    for ln, raw in enumerate(parts[1:end], start=2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        m_item = re.match(r"^\s+-\s+(\w+)\s*:\s*(.*)$", raw) or re.match(r"^-\s+(\w+)\s*:\s*(.*)$", raw)
        m_cont = re.match(r"^\s+(\w+)\s*:\s*(.*)$", raw)
        m_top = re.match(r"^(\w+)\s*:\s*(.*)$", raw)
        if m_item and cur_list is not None:
            cur_item = {m_item.group(1): _unquote(m_item.group(2))}
            meta[cur_list].append(cur_item)
        elif m_cont and cur_item is not None:
            cur_item[m_cont.group(1)] = _unquote(m_cont.group(2))
        elif m_top:
            k, v = m_top.group(1), m_top.group(2).strip()
            if v == "":
                meta[k] = []; cur_list, cur_item = k, None
            else:
                meta[k] = _unquote(v); cur_list, cur_item = None, None
        else:
            raise PostError(f"{fn} line {ln}: can't read front matter line: {raw!r}")
    body = "\n".join(parts[end + 1:]).strip("\n")
    return meta, body

# ---------------------------------------------------------------- markdown (small subset)
def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", html.unescape(re.sub(r"<[^>]+>", "", s)).lower()).strip("-")

def inline(t):
    t = html.escape(t, quote=False)
    codes = []
    t = re.sub(r"`([^`]+)`", lambda m: codes.append(m.group(1)) or f"\x00{len(codes)-1}\x00", t)
    def link(m):
        text, url = m.group(1), m.group(2).strip().replace('"', "%22")
        ext = ' target="_blank" rel="noopener"' if re.match(r"https?://", url) else ""
        return f'<a href="{url}"{ext}>{text}</a>'
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, t)
    t = re.sub(r"\*\*(?!\s)(.+?)(?<!\s)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?![\s*])(.+?)(?<![\s*])\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"(?<![\w])_(?![\s_])(.+?)(?<![\s_])_(?![\w])", r"<em>\1</em>", t)
    t = re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", t)
    return t

def markdown(md):
    out, para, lst, quote = [], [], None, []
    def flush_para():
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>"); para.clear()
    def flush_list():
        nonlocal lst
        if lst:
            tag, items = lst
            out.append(f"<{tag}>" + "".join(f"<li>{inline(' '.join(i))}</li>" for i in items) + f"</{tag}>")
            lst = None
    def flush_quote():
        if quote:
            out.append("<blockquote>" + "".join(f"<p>{inline(p)}</p>" for p in " ".join(quote).split("\x01")) + "</blockquote>"); quote.clear()
    def flush_all():
        flush_para(); flush_list(); flush_quote()
    lines = md.split("\n"); i = 0
    while i < len(lines):
        line = lines[i].rstrip(); i += 1
        if not line.strip():
            flush_para(); flush_quote()
            # a blank line ends a list unless the next line continues it
            if lst and not (i < len(lines) and re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i])):
                flush_list()
            continue
        if m := re.match(r"^(#{1,4})\s+(.+?)\s*#*$", line):
            flush_all()
            lvl = max(2, len(m.group(1)))
            txt = inline(m.group(2))
            out.append(f'<h{lvl} id="{slugify(txt)}">{txt}</h{lvl}>'); continue
        if re.match(r"^(\*{3,}|-{3,}|_{3,})$", line.strip()):
            flush_all(); out.append("<hr>"); continue
        if m := re.match(r"^\s*([-*+])\s+(.*)$", line):
            flush_para(); flush_quote()
            if not lst or lst[0] != "ul": flush_list(); lst = ("ul", [])
            lst[1].append([m.group(2)]); continue
        if m := re.match(r"^\s*\d+[.)]\s+(.*)$", line):
            flush_para(); flush_quote()
            if not lst or lst[0] != "ol": flush_list(); lst = ("ol", [])
            lst[1].append([m.group(1)]); continue
        if lst and line.startswith(("  ", "\t")):
            lst[1][-1].append(line.strip()); continue
        if m := re.match(r"^>\s?(.*)$", line):
            flush_para(); flush_list()
            quote.append(m.group(1) if m.group(1).strip() else "\x01"); continue
        if line.lstrip().startswith("<") and not para:
            flush_all(); block = [line]
            while i < len(lines) and lines[i].strip():
                block.append(lines[i]); i += 1
            out.append("\n".join(block)); continue
        flush_list(); flush_quote(); para.append(line.strip())
    flush_all()
    return "\n".join(out)

# ---------------------------------------------------------------- load + validate
def fmt_date(d):
    return f"{d:%B} {d.day}, {d.year}"

def today_local():
    return datetime.datetime.now(TZ).date()

def load_posts(include_future=False):
    posts, errors = [], []
    if not os.path.isdir(POSTS_DIR):
        return posts
    for fn in sorted(os.listdir(POSTS_DIR)):
        if not fn.endswith(".md"):
            continue
        try:
            posts.append(load_one(fn))
        except PostError as e:
            errors.append(str(e))
    if errors:
        raise SystemExit("Blog post errors (fix and re-run build.py):\n  - " + "\n  - ".join(errors))
    slugs = [p["out"] for p in posts]
    if len(slugs) != len(set(slugs)):
        raise SystemExit("Blog: two posts produce the same URL; rename one file.")
    live = []
    for p in posts:
        if p["draft"]:
            print(f"  blog: skipped draft {p['file']}")
        elif p["date"] > today_local() and not include_future:
            print(f"  blog: skipped future-dated {p['file']} (publishes when the build runs on/after {p['date']})")
        else:
            live.append(p)
    live.sort(key=lambda p: (p["date"], p["file"]), reverse=True)  # newest first
    import make_image
    for p in live:
        if not p["image_custom"]:
            make_image.generate(p, p["meta"])  # no-op if the image already exists
    return live

SUPERLATIVE_ERR = re.compile(r"\b(best|top|#1|number[- ]one|leading|top[- ]rated)\s+(realtor|real estate agent|agent|associate)s?\b", re.I)
SUPERLATIVE_WARN = re.compile(r"\b(best|guarantee[sd]?|guaranteed|#1|number one)\b", re.I)

def load_one(fn, with_meta=False):
    m = FILENAME_RE.match(fn)
    if not m:
        raise PostError(f"{fn}: file name must look like YYYY-MM-DD-short-slug.md (lowercase letters, digits, hyphens)")
    text = open(os.path.join(POSTS_DIR, fn), encoding="utf-8").read().replace("\r\n", "\n")
    meta, body = parse_front_matter(text, fn)
    for k in ("title", "date", "summary", "category"):
        if not str(meta.get(k, "")).strip():
            raise PostError(f"{fn}: missing required front matter field '{k}'")
    try:
        d = datetime.date.fromisoformat(meta["date"])
    except ValueError:
        raise PostError(f"{fn}: date must be YYYY-MM-DD, got {meta['date']!r}")
    if d.isoformat() != m.group(1):
        raise PostError(f"{fn}: front matter date {d} doesn't match the file name date {m.group(1)}")
    if meta["category"] not in CATEGORIES:
        raise PostError(f"{fn}: category must be one of {CATEGORIES}, got {meta['category']!r}")
    sources = meta.get("sources") or []
    if not isinstance(sources, list) or not sources:
        raise PostError(f"{fn}: needs at least one entry under 'sources:'")
    for s in sources:
        if not s.get("title") or not re.match(r"https?://", s.get("url", "")):
            raise PostError(f"{fn}: every source needs a title and an http(s) url: {s}")
    if len(meta["summary"]) > 320:
        raise PostError(f"{fn}: summary is {len(meta['summary'])} characters; keep it to 1-2 sentences (max 320)")
    desc = meta.get("description") or meta["summary"]
    if len(desc) > 320:
        raise PostError(f"{fn}: description is too long (max 320 characters)")
    image = meta.get("image", "").lstrip("/")
    if image:
        if not os.path.isfile(os.path.join(ROOT, image)):
            raise PostError(f"{fn}: image {image!r} not found in the repo (use a site asset path like assets/img/x.jpg)")
        if not meta.get("image_alt"):
            raise PostError(f"{fn}: image_alt is required when you set a custom image")
    cta = meta.get("cta") or CTA_FOR_CAT[meta["category"]]
    if cta not in CTAS:
        raise PostError(f"{fn}: cta must be one of {list(CTAS)}")
    updated = meta.get("updated")
    if updated:
        try: datetime.date.fromisoformat(updated)
        except ValueError: raise PostError(f"{fn}: updated must be YYYY-MM-DD")
    if re.search(r"^#\s", body, re.M):
        print(f"  blog: note: {fn} uses '# ' headings in the body; the title is the page H1, so they render as H2")
    text_all = " ".join([meta["title"], meta["summary"], desc, body])
    if re.search(r"Tri-Cities(?!,\s*(BC|B\.C\.))", text_all):
        raise PostError(f"{fn}: always write 'Tri-Cities, BC' (found bare 'Tri-Cities')")
    if m_s := SUPERLATIVE_ERR.search(text_all):
        raise PostError(f"{fn}: superlative claim {m_s.group(0)!r} breaks BC advertising rules; rephrase")
    for m_w in SUPERLATIVE_WARN.finditer(body):
        print(f"  blog: check wording in {fn}: {body[max(0, m_w.start()-40):m_w.end()+40]!r} (no superlatives or promises)")
    if not re.search(r"\]\(/(tenants|buyers)\.html", body):
        raise PostError(f"{fn}: link at least once, with descriptive anchor text, to /tenants.html (renting/relocation) or /buyers.html (buying)")
    words = len(re.findall(r"[A-Za-z0-9$%][\w$%.,'’-]*", re.sub(r"<[^>]+>", " ", body)))
    out = f"{m.group(1)}-{m.group(2)}.html"
    stem = out[:-5]
    image_custom = bool(image)
    if not image:
        image = f"assets/img/blog/{stem}.jpg"
    webp = re.sub(r"\.(jpe?g|png)$", ".webp", image)
    post = {
        "file": fn, "out": out, "url": f"{SITE}blog/{out}", "title": meta["title"], "date": d,
        "updated": updated or d.isoformat(), "summary": meta["summary"], "description": desc,
        "category": meta["category"], "sources": sources, "image": image, "image_alt": meta.get("image_alt", ""),
        "cta": cta, "draft": str(meta.get("draft", "")).lower() in ("true", "yes", "1"),
        "body_md": body, "body_html": markdown(body), "words": words,
        "image_custom": image_custom, "image_webp": webp if webp != image else "", "meta": meta,
    }
    if not post["image_alt"]:
        import make_image
        post["image_alt"] = make_image.default_alt(make_image.card_data(post, meta))
    return (post, meta) if with_meta else post

# ---------------------------------------------------------------- shared bits
def img_tag(p, root, cls, sizes, eager=False, alt=None):
    alt = p["image_alt"] if alt is None else alt
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    src = f'<source type="image/webp" srcset="{root}{esc(p["image_webp"])}">' if p["image_webp"] and os.path.isfile(os.path.join(ROOT, p["image_webp"])) else ""
    return (f'<picture class="{cls}">{src}<img src="{root}{esc(p["image"])}" width="1200" height="630" '
            f'sizes="{sizes}" alt="{esc(alt)}" {load} decoding="async"></picture>')

def cat_tag(cat):
    return f'<span class="post-cat post-cat--{CAT_CLASS[cat]}">{esc(cat)}</span>'

def post_card(p, href, heading="h2", root=""):
    thumb = f'<a class="post-thumb" href="{href}" tabindex="-1" aria-hidden="true">{img_tag(p, root, "", "(max-width: 639px) 92vw, 360px", alt="")}</a>'
    return (f'<article class="post-card">{thumb}<div class="post-card-body">'
            f'<div class="post-meta">{cat_tag(p["category"])}<time datetime="{p["date"].isoformat()}">{fmt_date(p["date"])}</time></div>'
            f'<{heading}><a href="{href}">{esc(p["title"])}</a></{heading}>'
            f'<p>{esc(p["summary"])}</p>'
            f'<a class="card-link" href="{href}" aria-label="Read: {esc(p["title"])}">Read the post {ICONS["arrow"]}</a>'
            f'</div></article>')

def rss_link(root):
    return f'<link rel="alternate" type="application/rss+xml" title="{esc(BLOG_NAME)}" href="{SITE}blog/feed.xml">'

def _jsonld(data):
    return '<script type="application/ld+json">\n' + json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/") + '\n</script>'

CTAS = {
 "buying": ("Thinking about buying in Greater Vancouver?",
            "I'm happy to talk through what this means for your budget and the neighbourhoods you're considering, especially here in the Tri-Cities, BC.",
            [("buyers.html#listings", "Get listings sent to me", "light"), ("buyers.html", "Buyer info &amp; neighbourhoods", "ghost")]),
 "selling": ("Thinking about selling?",
            "Every home and street is different. I'm happy to walk you through recent sales near you and what selling could look like for you.",
            [("index.html#contact", "Talk to me about selling", "light"), ("mailto:" + EMAIL + "?subject=Selling%20my%20home", "Email Devin", "ghost")]),
 "renting": ("Moving to Greater Vancouver and need a rental?",
            "My relocation rental service is $1,500 + GST, paid by the tenant ($750 non-refundable at the start, $750 once you secure a rental). Reach out 4–6 weeks before your move.",
            [("tenants.html", "See the relocation rental service", "light"), ("tenants.html#intake", "Start a rental search", "ghost")]),
 "general": ("Buying, selling or renting in Greater Vancouver?",
            "If you'd like to talk through what this means for your plans, I'm happy to help, whether you're buying, selling, or relocating and need a rental.",
            [("buyers.html", "Buying help", "light"), ("index.html#contact", "Selling help", "ghost"), ("tenants.html", "Renting help", "ghost")]),
}

def cta_block(kind, root):
    h, body, btns = CTAS[kind]
    b = "".join(f'<a class="btn {"btn-light" if s == "light" else "btn-ghost-light"}" href="{u if u.startswith("mailto:") else root + u}">{t}</a>' for u, t, s in btns)
    return (f'<aside class="post-cta" aria-label="Get in touch">'
            f'<h2>{h}</h2><p>{body}</p>'
            f'<p class="post-cta-phone">Call or text me at <a href="{TEL}">{PHONE}</a>, or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>'
            f'<div class="btn-row">{b}<a class="btn btn-ghost-light" href="{TEL}">{ICONS["phone"]} Call or text {PHONE}</a></div></aside>')

def author_box(root):
    photo = picture(f"{root}assets/img/devin-headshot", (480,), 480, 600, "Devin Desaulniers, Real Estate Associate with Axford Real Estate", "author-photo", sizes_attr="96px")
    return (f'<aside class="author-box" aria-label="About the author">{photo}<div>'
            f'<span class="eyebrow">About the author</span>'
            f'<h2>Devin Desaulniers</h2>'
            f'<p>Real Estate Associate with <strong>Axford Real Estate</strong> in Port Moody, licensed since 2020. I\'ve lived in Greater Vancouver for 28 years and help buyers, sellers and newcomers relocating to Greater Vancouver and the Tri-Cities, BC.</p>'
            f'<p class="author-contact">Call or text <a href="{TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{root}index.html#about">More about me</a></p>'
            f'</div><img class="author-brokerage" src="{root}assets/img/axford-logo.png" alt="Axford Real Estate" width="120" height="26" loading="lazy"></aside>')

# ---------------------------------------------------------------- pages
def post_page(p, newer=None, older=None):
    root = "../"
    og_image = p["image"]
    title_tag = f'{p["title"]} | Devin Desaulniers, Axford Real Estate'
    ld = {
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": p["title"][:110], "description": p["description"], "url": p["url"],
        "mainEntityOfPage": {"@type": "WebPage", "@id": p["url"]},
        "datePublished": p["date"].isoformat(), "dateModified": p["updated"],
        "author": {"@type": "Person", "name": "Devin Desaulniers", "jobTitle": "Real Estate Associate", "url": SITE,
                   "worksFor": {"@type": "RealEstateAgent", "name": BROKERAGE}},
        "publisher": {"@type": "Organization", "name": BROKERAGE, "url": SITE,
                      "logo": {"@type": "ImageObject", "url": SITE + "assets/img/axford-logo.png"},
                      "address": {"@type": "PostalAddress", "streetAddress": "2326 Clarke St", "addressLocality": "Port Moody",
                                  "addressRegion": "BC", "postalCode": "V3H 1Y8", "addressCountry": "CA"}},
        "image": [SITE + og_image], "articleSection": p["category"], "inLanguage": "en-CA", "wordCount": p["words"],
        "isPartOf": {"@type": "Blog", "name": BLOG_NAME, "url": SITE + "blog/"},
        "citation": [s["url"] for s in p["sources"]],
    }
    extra = (f'<meta property="article:published_time" content="{p["date"].isoformat()}">\n'
             f'<meta property="article:modified_time" content="{p["updated"]}">\n'
             f'<meta property="article:section" content="{esc(p["category"])}">\n'
             f'<meta property="article:author" content="Devin Desaulniers">\n'
             f'<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
             f'<meta property="og:image:alt" content="{esc(p["image_alt"])}">\n'
             f'<meta name="twitter:title" content="{esc(p["title"])}">\n<meta name="twitter:description" content="{esc(p["description"])}">\n'
             f'<meta name="twitter:image" content="{SITE}{og_image}">\n<meta name="twitter:image:alt" content="{esc(p["image_alt"])}">\n' + rss_link(root) + "\n" + _jsonld(ld))
    page = head(esc(title_tag), esc(p["description"]), "blog", og_image=og_image, page_url=f'blog/{p["out"]}',
                extra_head=extra, root=root, og_type="article")
    srcs = "".join(
        f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["title"])}</a>'
        + (f' <span class="src-meta">· {esc(s["publisher"])}' if s.get("publisher") else ' <span class="src-meta">')
        + (f', {fmt_date(datetime.date.fromisoformat(s["date"]))}' if re.match(r"^\d{4}-\d{2}-\d{2}$", s.get("date", "")) else "")
        + '</span></li>' for s in p["sources"])
    fig = f'<figure class="post-image">{img_tag(p, root, "", "(max-width: 919px) 92vw, 840px", eager=True)}</figure>'
    nav = ""
    if newer or older:
        nav = '<nav class="post-nav" aria-label="More posts">'
        nav += (f'<a class="pn-older" href="{older["out"]}"><small>Older post</small>{esc(older["title"])}</a>' if older else "<span></span>")
        nav += (f'<a class="pn-newer" href="{newer["out"]}"><small>Newer post</small>{esc(newer["title"])}</a>' if newer else "<span></span>")
        nav += "</nav>"
    avatar = picture(f"{root}assets/img/devin-headshot", (480,), 480, 600, "Devin Desaulniers", "byline-photo", sizes_attr="56px")
    page += f'''
<section class="page-hero post-hero">
  <div class="container narrow-wide">
    <a class="back-link" href="./">&larr; All blog posts</a>
    <div class="post-meta post-meta--hero">{cat_tag(p["category"])}<time datetime="{p["date"].isoformat()}">{fmt_date(p["date"])}</time></div>
    <h1>{esc(p["title"])}</h1>
    <p class="lead">{esc(p["summary"])}</p>
  </div>
</section>

<article class="section post">
  <div class="container narrow-wide">
    <div class="byline">{avatar}<div><strong>{BYLINE}</strong><span>Published <time datetime="{p["date"].isoformat()}">{fmt_date(p["date"])}</time> · Greater Vancouver &amp; Tri-Cities, BC</span></div></div>
    {fig}
    <div class="post-body">
{p["body_html"]}
    </div>
    <section class="post-sources" aria-labelledby="sources-h">
      <h2 id="sources-h">Sources</h2>
      <ol>{srcs}</ol>
    </section>
    {cta_block(p["cta"], root)}
    {author_box(root)}
    <p class="post-disclaimer">{DISCLAIMER}</p>
    {nav}
  </div>
</article>
'''
    return page + foot(root=root)

def index_page(posts):
    root = "../"
    ld = {"@context": "https://schema.org", "@type": "Blog", "name": BLOG_NAME, "description": BLOG_DESC,
          "url": SITE + "blog/", "inLanguage": "en-CA",
          "author": {"@type": "Person", "name": "Devin Desaulniers", "url": SITE},
          "publisher": {"@type": "Organization", "name": BROKERAGE},
          "blogPost": [{"@type": "BlogPosting", "headline": p["title"][:110], "url": p["url"],
                        "datePublished": p["date"].isoformat(), "author": {"@type": "Person", "name": "Devin Desaulniers"}}
                       for p in posts[:30]]}
    page = head("Blog: Greater Vancouver Real Estate News, Explained | Devin Desaulniers", esc(BLOG_DESC), "blog",
                page_url="blog/", extra_head=rss_link(root) + "\n" + _jsonld(ld), root=root)
    cards = "".join(post_card(p, p["out"], root="../") for p in posts) or '<p class="center">The first post is coming soon.</p>'
    cats = " · ".join(CATEGORIES)
    page += f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Blog</span>
    <h1>Greater Vancouver real estate news, explained</h1>
    <p class="lead">Each weekday I pick one local real estate story, link the original source, and share what I think it means for buyers, sellers and renters in Greater Vancouver and the Tri-Cities, BC.</p>
  </div>
</section>

<section class="section blog-index">
  <div class="container narrow-wide">
    <div class="blog-index-bar"><span>Topics: {cats}</span><a href="feed.xml">RSS feed</a></div>
    <div class="post-list">{cards}</div>
    <p class="post-disclaimer center" style="margin-top:28px">Posts are general information and my personal opinion, not legal, tax or financial advice.</p>
  </div>
</section>
'''
    return page + foot(root=root)

def home_strip(posts, n=3):
    if not posts:
        return ""
    cards = "".join(post_card(p, "blog/" + p["out"], heading="h3", root="") for p in posts[:n])
    return f'''<section class="section section--tint" id="blog">
  <div class="container">
    <div class="center narrow">
      <span class="eyebrow">From the blog</span>
      <h2>Latest from the blog</h2>
      <p class="lead">Greater Vancouver real estate news in plain language, with my take on what it means for you.</p>
    </div>
    <div class="post-strip">{cards}</div>
    <div class="center" style="margin-top:26px"><a class="btn btn-outline" href="blog/">See all posts {ICONS["arrow"]}</a></div>
  </div>
</section>'''

def feed_xml(posts, n=30):
    x = lambda s: html.escape(str(s), quote=False)
    now = posts[0]["date"] if posts else today_local()
    def rfc(d):  # posts carry a date only; stamp them 8:00 a.m. Vancouver time
        return format_datetime(datetime.datetime(d.year, d.month, d.day, 8, 0, tzinfo=TZ))
    items = "".join(f'''
  <item>
    <title>{x(p["title"])}</title>
    <link>{p["url"]}</link>
    <guid isPermaLink="true">{p["url"]}</guid>
    <pubDate>{rfc(p["date"])}</pubDate>
    <category>{x(p["category"])}</category>
    <dc:creator>Devin Desaulniers</dc:creator>
    <description>{x(p["summary"])}</description>
  </item>''' for p in posts[:n])
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">
<channel>
  <title>{x(BLOG_NAME)}</title>
  <link>{SITE}blog/</link>
  <atom:link href="{SITE}blog/feed.xml" rel="self" type="application/rss+xml"/>
  <description>{x(BLOG_DESC)}</description>
  <language>en-ca</language>
  <lastBuildDate>{rfc(now)}</lastBuildDate>{items}
</channel>
</rss>
'''

def write_blog(posts):
    """Write blog/index.html, one page per post and blog/feed.xml. Removes stale generated post pages."""
    os.makedirs(BLOG_DIR, exist_ok=True)
    keep = {"index.html", "feed.xml"} | {p["out"] for p in posts}
    for fn in os.listdir(BLOG_DIR):
        if fn.endswith(".html") and fn not in keep and FILENAME_RE.match(fn.replace(".html", ".md")):
            os.remove(os.path.join(BLOG_DIR, fn)); print(f"  blog: removed stale page blog/{fn}")
    for i, p in enumerate(posts):
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        open(os.path.join(BLOG_DIR, p["out"]), "w", encoding="utf-8").write(post_page(p, newer, older))
    open(os.path.join(BLOG_DIR, "index.html"), "w", encoding="utf-8").write(index_page(posts))
    open(os.path.join(BLOG_DIR, "feed.xml"), "w", encoding="utf-8").write(feed_xml(posts))
    print(f"  blog: {len(posts)} post(s) -> blog/ (index, feed.xml)" + (f"; newest: blog/{posts[0]['out']}" if posts else ""))

def sitemap_xml(static_pages, posts):
    urls = [f"  <url><loc>{SITE}{u}</loc></url>" for u in static_pages]
    if posts:
        urls.append(f"  <url><loc>{SITE}blog/</loc><lastmod>{posts[0]['date'].isoformat()}</lastmod></url>")
        urls += [f"  <url><loc>{p['url']}</loc><lastmod>{p['updated']}</lastmod></url>" for p in posts]
    else:
        urls.append(f"  <url><loc>{SITE}blog/</loc></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<!-- Live sitemap for {SITE} (generated by _build/build.py; do not edit by hand)\n'
            '     relocating-to-coquitlam.html is a redirect to relocating-to-greater-vancouver.html and is intentionally omitted. -->\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")
