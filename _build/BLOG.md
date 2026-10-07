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
first source, and "devindesaulniers.ca · Axford Real Estate" footer) with headless Chrome, and encodes
`assets/img/blog/<YYYY-MM-DD>-<slug>.jpg` and `.webp` with ffmpeg (each kept under 200 KB).
It needs `google-chrome` (or `CHROME=/path`) and `ffmpeg`, both on the box.

- `build.py` generates the image automatically for any post that doesn't have one yet. Nothing extra to run.
- Changed the title or card fields after the image exists? Re-render it:
  `cd _build && python3 make_image.py --force ../_posts/YYYY-MM-DD-slug.md && python3 build.py`
- Look at the JPG before committing (title fits, numbers correct).
- The image is used at the top of the post, as og:image / twitter:image, in the BlogPosting JSON-LD, and as the
  thumbnail on the blog index and the home-page strip. Alt text is generated from the card fields (or `image_alt`).
- Rules: every number on the image must come from the cited sources. Never use photos from news sites, and no
  AI-generated images of real people or real places. The generated graphic needs no photo at all.

## Content checklist (each post)
- One genuinely current story from a reputable source (published in the last week or so); link it under `sources`.
- 500-800 words, first person as Devin, plain language, 2-4 `##` subheadings, optional short FAQ (`### Question`).
- Use the word "newcomer" naturally where it fits (relocation, renting, first purchase).
- Summarise in your own words. Short quotes only, in quotation marks, attributed to the person/organisation.
- Every number, quote and fact must come from a cited source. Never invent stats, quotes, prices or predictions.
- BC advertising rules: no superlatives or misleading claims ("best", "#1", "guaranteed"), no promises about prices or returns.
- Write "Tri-Cities, BC". Relocation rental service facts if mentioned: $1,500 + GST paid by the tenant, $750 non-refundable at the start, $750 once a rental is secured, reach out 4-6 weeks before the move.
- Never claim Devin is "the best" or "top". Target searches with wording like "Looking for a realtor in Coquitlam?" instead.
- Images: the generated branded graphic only (step 1b). No photos from other publications.

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
