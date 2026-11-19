# Blog: how to add and publish a post

The blog lives at https://devindesaulniers.ca/blog/. Posts are Markdown files in `_posts/`;
`_build/build.py` (via `_build/blog.py`, no extra packages needed) turns them into:

- `blog/<YYYY-MM-DD>-<slug>.html`: the post page (title/meta description, canonical, og/twitter tags,
  BlogPosting JSON-LD, byline, featured image, Sources list, call to action, author box, disclaimer, older/newer links)
- `assets/img/blog/<YYYY-MM-DD>-<slug>.jpg` + `.webp`: the branded 1200x630 featured image (see step 1b)
- `blog/index.html`: all posts, newest first
- `blog/feed.xml`: RSS feed (newest 30)
- the "Latest from the blog" strip on `index.html` (3 newest) and the blog URLs in `sitemap.xml`

Never hand-edit anything in `blog/`, `sitemap.xml` or the strip on `index.html`: they are rebuilt every time.

## 0. Before choosing a topic (daily routine)

Read **`/workspace/blog-brief/seo-brief.md`** first. It has the priority list of evergreen FAQ posts
(title = the question, answer it in the first 2 sentences), searches to target, and the rules below.
Mark an FAQ item `[DONE <date> <url>]` in that brief once it's published. Weekdays default to one genuinely
current news story; use the brief's FAQ list for the weekly evergreen post or when there's no good news story.

## 1. Write the file

Path: `_posts/YYYY-MM-DD-short-slug.md` (lowercase letters, digits, hyphens; date = publish date in
Vancouver time). Example: `_posts/2026-10-07-bank-of-canada-rate-decision.md` -> `/blog/2026-10-07-bank-of-canada-rate-decision.html`.
The slug is permanent once published (it's the URL), so pick it carefully.

```markdown
---
title: "Plain-language headline (about 50-70 characters)"
date: 2026-10-07
category: Market news
summary: "1-2 sentences shown on the blog index, home strip, RSS and as the meta description."
description: "Optional: a different meta description (max 320 chars). Defaults to summary."
sources:
  - title: "Exact headline of the original article"
    publisher: Publisher name
    date: 2026-10-06
    url: https://example.com/original-article
  - title: "Second source (optional)"
    publisher: Another publisher
    date: 2026-10-06
    url: https://example.com/second
# featured image fields (optional, but use them whenever the source gives a real number):
card_stat: "−8.4%"                         # key number from the cited source, shown big on the image
card_stat_label: "Metro Vancouver home sales, Sept. 2026 vs. Sept. 2025"
# card_takeaway: "Short takeaway"          # instead of card_stat when the story has no headline number
card_chart_title: "Sales by type, year over year"
card_chart:                                # optional simple bar chart, 2-5 bars, real numbers from the source only
  - label: Apartments
    value: -18.6
    display: "−18.6%"
  - label: Detached
    value: 4.2
    display: "+4.2%"
# image_alt: "..."                         # optional override; otherwise alt text is built from title, number, chart and source
# featured image background (required for posts about a specific place — see step 1b):
# card_photo: assets/img/blog/photos/moody-centre-station.jpg
# card_photo_position: center 35%          # optional CSS background-position; use to keep the landmark in frame
# card_photo_size: 1800px auto             # optional CSS background-size (default cover) when the photo needs a tighter crop
# card_photo_credit: "Name / Wikimedia Commons (CC BY 4.0)"
# card_photo_credit_url: https://commons.wikimedia.org/wiki/File:Example.jpg
# optional:
# image: assets/img/some-site-asset.jpg   (custom image instead of the generated one; must exist in the repo; image_alt then required)
# cta: buying | selling | renting | general   (default comes from the category)
# updated: 2026-10-08                          (only if you revise a published post)
# draft: true                                  (build skips it)
---
Intro paragraph...

## First subheading

Body in Markdown...
```

Rules the build enforces (it stops with a clear error message if one is broken):
- Write "Tri-Cities, BC" every time (bare "Tri-Cities" fails the build).
- The body must link at least once, with descriptive anchor text, to `/tenants.html` (renting/relocation topics) or
  `/buyers.html` (buying). Also link `/relocating-to-greater-vancouver.html` where relevant.
- Superlative agent claims ("best realtor", "top agent", "#1 agent"...) fail the build; words like "best" or "guaranteed" print a warning to re-check.
- Required: `title`, `date` (must match the file name date), `summary` (max 320 chars), `category`, and at least one source with `title` + `url`.
- `category` is exactly one of: `Buying`, `Selling`, `Renting`, `Market news`, `FAQ`.
- Default call to action by category: Buying -> buying, Selling -> selling, Renting -> renting, Market news / FAQ -> general (links to buyers, contact and tenants pages, plus the 604-809-1032 call/text line).
- A post dated in the future is skipped until a build runs on/after that date (Vancouver time).
- Quote values that contain a colon (`:`) or start with a quote mark, as in the example. Keep each value on one line.

Supported Markdown: `##` / `###` headings (the title is the page H1, so start at `##`), paragraphs, `-` and `1.` lists,
`**bold**`, `*italic*`, `[links](https://...)`, `> quotes`, `---`. Internal links use root paths: `/tenants.html`,
`/buyers.html`, `/relocating-to-greater-vancouver.html`, `/index.html#contact`. External links open in a new tab.

The page adds the byline, featured image, the "Sources" list, the call to action, the author box (Devin Desaulniers,
Real Estate Associate, licensed since 2020, Axford Real Estate, call or text 604-809-1032) and the disclaimer
("This post is general information and my personal opinion, not legal, tax or financial advice.") automatically,
so don't repeat them in the body.

## 1b. Featured image (every post has one)

`_build/make_image.py` renders a branded 1200x630 graphic (brand blue #3474b6 / grey #808082, category tag, post title,
the `card_stat` + label or `card_takeaway`, optional bar chart from `card_chart`, "Source: <publisher>, <date>" from the
first source, and a white footer with Devin's mark, "devindesaulniers.ca · Axford Real Estate") with headless Chrome, and encodes
`assets/img/blog/<YYYY-MM-DD>-<slug>.jpg` and `.webp` with ffmpeg (each kept under 200 KB).
It needs `google-chrome` (or `CHROME=/path`) and `ffmpeg`, both on the box.

**Background photo (required on every post, including social reposts).** The featured image must use a real photograph
of the place the post is about as the background, with a dark gradient overlay so the title stays readable, and the
existing branded text graphics (category pill, title, stat card, footer) laid over top. Example: the Moody Centre
Station guide uses a photo of Moody Centre Station; a Coquitlam rent post uses a recognisable Coquitlam photo (such as
Lafarge Lake / Town Centre); a Canada-wide policy post uses a photo such as Parliament Hill; a Vancouver social repost
uses a Vancouver photo. Never publish a plain-blue, navy, or generic text card, and never pad a social graphic onto a
plain navy 1200×630 canvas. If Devin's own social post used a real photograph (not AI-generated), that photo may be
reused as his own content. If the social background looks AI-generated or has no licence, use a Wikimedia / Unsplash /
Pexels photo of the place and tell him. Ask him instead of silently falling back.

- Set `card_photo` to a file in the repo (keep source photos in `assets/img/blog/photos/`). Optional
  `card_photo_position` (CSS background-position, e.g. `center 35%`) keeps the landmark in the 1200×630 crop.
- `card_photo_credit` is drawn as a small line on the graphic. For CC BY / CC BY-SA photos also set
  `card_photo_credit_url` (the file page or landing page). The post page then shows a visible "Photo: …" credit
  under the image, linking to that URL. CC0, public-domain and Devin's own photos can omit the on-page line, but
  still log them (below).
- Where to get the photo: Wikimedia Commons (CC BY, CC BY-SA, CC0 or public domain), Unsplash, Pexels, or Devin's
  own photos. Never use photos from news sites, unlicensed stock, or AI-generated images of real people or real places.
- Log every photo, including samples that are not published yet, in `/workspace/blog-brief/photo-credits.md` (source
  URL, author, licence, and whether the post has been updated). Do not publish a photo until it is listed there.
- `build.py` generates the image automatically for any post that doesn't have one yet. Nothing extra to run.
- Changed the title, card fields or background photo after the image exists? Re-render it:
  `cd _build && python3 make_image.py --force ../_posts/YYYY-MM-DD-slug.md && python3 build.py`
- To render a preview without touching the live `assets/img/blog/` files:
  `cd _build && python3 make_image.py --force --bg /path/photo.jpg --photo-credit "Name / source (licence)" --photo-position "center 35%" --out-dir /workspace/blog-brief/photo-samples ../_posts/YYYY-MM-DD-slug.md`
- Look at the JPG before committing (title fits, numbers correct, the place is recognisable through the overlay).
- The image is used at the top of the post, as og:image / twitter:image, in the BlogPosting JSON-LD, and as the
  thumbnail on the blog index and the home-page strip. Alt text is generated from the card fields (or `image_alt`).
- Every number on the image must come from the cited sources.

**If headless Chrome hangs or times out**, use the CDP wrapper instead of calling `google-chrome` directly:

```bash
CHROME=/tmp/cdp9334/chrome-cdp python3 make_image.py --force ../_posts/YYYY-MM-DD-slug.md
```

If `/tmp/cdp9334/chrome-cdp` is missing, recreate it:

```bash
mkdir -p /tmp/cdp9334
cat > /tmp/cdp9334/chrome-cdp << 'EOF'
#!/bin/bash
# Wrapper mimicking `chrome --headless --screenshot=OUT --window-size=W,H URL` via the CDP Chrome on port 9334.
out=""; w=1200; h=630; url=""
for a in "$@"; do case "$a" in --screenshot=*) out="${a#--screenshot=}";; --window-size=*) s="${a#--window-size=}"; w="${s%,*}"; h="${s#*,}";; --*) ;; *) url="$a";; esac; done
if ! curl -s -m 3 localhost:9334/json/version >/dev/null; then
  nohup google-chrome --headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage --hide-scrollbars --allow-file-access-from-files --remote-debugging-port=9334 --user-data-dir=/tmp/cdp9334/profile about:blank >/tmp/cdp9334/chrome.log 2>&1 &
  for i in $(seq 20); do sleep 1; curl -s -m 2 localhost:9334/json/version >/dev/null && break; done
fi
exec node /tmp/cdp9334/shot.mjs "$url" "$out" "$w" "$h"
EOF
cat > /tmp/cdp9334/shot.mjs << 'EOF'
const [,, url, out, w, h] = process.argv;
const fs = await import('node:fs');
const t = await (await fetch(`http://localhost:9334/json/new?${encodeURIComponent(url)}`, {method:'PUT'})).json();
const ws = new WebSocket(t.webSocketDebuggerUrl);
let id = 0; const pend = {};
const send = (method, params={}) => new Promise(r => { const i=++id; pend[i]=r; ws.send(JSON.stringify({id:i,method,params})); });
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend[m.id]) pend[m.id](m.result); };
await new Promise(r => ws.onopen = r);
await send('Emulation.setDeviceMetricsOverride', {width:+w, height:+h, deviceScaleFactor:1, mobile:false});
await send('Page.enable');
await send('Page.navigate', {url});
await new Promise(r => setTimeout(r, 3000));
const res = await send('Page.captureScreenshot', {format:'png', clip:{x:0,y:0,width:+w,height:+h,scale:1}});
fs.writeFileSync(out, Buffer.from(res.data, 'base64'));
await fetch(`http://localhost:9334/json/close/${t.id}`);
ws.close(); process.exit(0);
EOF
chmod +x /tmp/cdp9334/chrome-cdp
```

## Content checklist (each post)
- One genuinely current story from a reputable source (published in the last week or so); link it under `sources`.
- 500-800 words, first person as Devin, plain language, 2-4 `##` subheadings, optional short FAQ (`### Question`).
- Use the word "newcomer" naturally where it fits (relocation, renting, first purchase).
- Summarise in your own words. Short quotes only, in quotation marks, attributed to the person/organisation.
- Every number, quote and fact must come from a cited source. Never invent stats, quotes, prices or predictions.
- BC advertising rules: no superlatives or misleading claims ("best", "#1", "guaranteed"), no promises about prices or returns.
- Write "Tri-Cities, BC". Relocation rental service facts if mentioned: $1,500 + GST paid by the tenant, $750 non-refundable at the start, $750 once a rental is secured, reach out 4-6 weeks before the move.
- Never claim Devin is "the best" or "top". Target searches with wording like "Looking for a realtor in Coquitlam?" instead.
- Images: the generated branded graphic only (step 1b), with a real licensed place photo as the background when the
  post is about a specific place. No photos from news sites or other publications, no unlicensed stock, and no
  AI-generated images of real people or real places. Log credits in `/workspace/blog-brief/photo-credits.md`.

## 2. Build, check, commit, push

```bash
cd /workspace/devin-website
git pull --ff-only
# (write _posts/YYYY-MM-DD-slug.md)
cd _build && python3 build.py && cd ..   # prints "blog: N post(s) ... newest: blog/<file>.html" then "built"
git status --short                       # expect: the new _posts/ file, its assets/img/blog/ .jpg + .webp, blog/index.html, blog/feed.xml,
                                         # blog/<new post>.html, the previous newest post (gets a "Newer post" link),
                                         # index.html (home strip) and sitemap.xml. Nothing else. CNAME must not change.
git add _posts assets/img/blog blog index.html sitemap.xml
git commit -m "Blog: <post title>"
git push
```

Optional local preview: `python3 -m http.server 8000` in the repo root, then open http://localhost:8000/blog/.

## 3. Verify live (GitHub Pages rebuilds in about 1-2 minutes)

```bash
gh run list --repo devindrealty-a11y/website --limit 1          # wait for "pages build and deployment" = completed/success
for u in blog/ blog/<file>.html blog/feed.xml sitemap.xml; do
  curl -s -o /dev/null -w "%{http_code} $u\n" "https://devindesaulniers.ca/$u?nocache=$(date +%s)"
done                                                             # all 200
```

## Fixing or removing a post
- Fix: edit the Markdown, add `updated: YYYY-MM-DD`, rebuild, commit, push.
- Remove: delete the Markdown file (and its `assets/img/blog/` images) and rebuild; the build deletes the stale page from `blog/` and drops it from the index, feed and sitemap.
