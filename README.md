# Devin Desaulniers — Real Estate Associate, Axford Real Estate

Static site for GitHub Pages, custom domain **https://devindesaulniers.ca/** (CNAME in repo root).

Pages:
- `index.html` — home / profile
- `buyers.html` — buyer info, neighbourhood guides, "Send me listings" form
- `tenants.html` — standalone landing page for the $1,500 tenant-paid relocation rental service (link this from ads/social)
- `blog/` — blog index, posts, RSS feed, generated from Markdown in `_posts/` (see **`_build/BLOG.md`** for how to add a post)

## Editing
HTML is generated from `_build/build.py` + `_build/partials.py` (header/footer shared). Edit those, then run:
```
cd _build && python3 build.py
```
(Or edit the HTML files directly if you prefer — just don't re-run the build afterwards.)

Every item still needing Devin's input is marked **[PLACEHOLDER: …]** (yellow highlight). Search the files for `PLACEHOLDER`.

## Forms (FormSubmit)
Both forms (buyers.html "Send me listings", tenants.html relocation intake) post via AJAX to
`https://formsubmit.co/ajax/devin@axfordrealestate.ca` — configured in one spot: `assets/js/config.js`.
- Email subjects: "New buyer listings request" / "New relocation rental intake" (table template, Reply-To = visitor's email).
- Spam: hidden honeypot field `_honey`. reCAPTCHA is not used by FormSubmit's AJAX flow, so nothing was disabled.
- Visitors see an on-page success (or error + call/email fallback) message.

**Activation (one-time):** the FIRST real submission makes FormSubmit send an activation email to
devin@axfordrealestate.ca. Devin must click "Activate Form" — submissions are not delivered until then
(the first one is held until activation). No test submission has been sent.
Tip: the activation email includes a random alias; replace the email address in both URLs in
`config.js` with `https://formsubmit.co/ajax/<alias>` to keep the address out of the page source.

## Pointing relocatingtovancouver.ca at the Tenants page (later — not bought yet)
A GitHub Pages repo can only have ONE custom domain, and this repo should keep Devin's main site.

**Recommended: a separate small repo for the landing page** (e.g. `devindrealty-a11y/relocatingtovancouver`)
1. Copy `tenants.html` → `index.html` in the new repo, plus `assets/` (or add a build target to `_build/build.py`
   that writes the landing page to a folder with links back to the main site as absolute URLs).
2. In the new repo: Settings → Pages → source `main` / root; Custom domain `relocatingtovancouver.ca` (this
   creates the `CNAME` file); tick "Enforce HTTPS" once the certificate is issued.
3. At the registrar, DNS for relocatingtovancouver.ca:
   - `A` @ → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
   - (optional) `AAAA` @ → 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153, 2606:50c0:8003::153
   - `CNAME` www → devindrealty-a11y.github.io
4. Verify the domain under GitHub account Settings → Pages (prevents domain takeover).
5. Update `og:url`/`og:image` on the landing page to the new domain, and add
   `<link rel="canonical" href="https://relocatingtovancouver.ca/">` to BOTH copies (this site's tenants.html too)
   so search engines treat the new domain as the main version.
Why: the ad/landing URL is the real domain (no redirect hop, HTTPS from GitHub, clean share previews),
and Google Ads requires the display domain to match the final landing URL's domain — a registrar
redirect to a github.io URL would fail that.

**Alternative (quickest, weaker): registrar URL forwarding** of relocatingtovancouver.ca →
`https://devindrealty-a11y.github.io/website/tenants.html` (301). Zero maintenance, but the address bar
and ad final URL show github.io, HTTPS on the bare forwarded domain depends on the registrar, and the
domain earns no search value of its own.

## SEO: schema, sitemap, robots
- Every page carries `RealEstateAgent` JSON-LD (`agent_jsonld()` in `_build/partials.py`). The sameAs and footer
  social links come from the `SOCIAL` list there (source: `/workspace/ai-seo/directory-claim-pack.md`).
  Axford is listed as `parentOrganization` because schema.org only allows `worksFor` on `Person`.
- `tenants.html` also carries `FAQPage` JSON-LD. It is generated from the same `FAQ_ITEMS` strings as the
  visible FAQ, so edit the FAQ in `build.py` only and the schema stays identical to the page text.
- `sitemap.xml` lists the live pages under https://devindesaulniers.ca/ (home, tenants, buyers, relocating-to-greater-vancouver). The Coquitlam redirect is omitted.
- `robots.txt` allows crawl and lists the Sitemap at https://devindesaulniers.ca/sitemap.xml (served at the domain root).
- `SITE` in `_build/partials.py` is `https://devindesaulniers.ca/`. Rebuild after changing it.
- Submit `sitemap.xml` in Google Search Console when ready.

## Launch checklist
- Replace all remaining placeholders (disclaimer, privacy policy, Axford-managed disclosure in the tenant FAQ, buyer services list, neighbourhood notes)
- Forms are connected to FormSubmit — Devin must click the activation email after the first real submission
- ~~Remove noindex and draft banner~~ Done (launched). Submit `sitemap.xml` in Search Console when ready.
- ~~Custom domain~~ Done: `devindesaulniers.ca` (CNAME + SITE). Enforce HTTPS once the cert is ready.

## Renamed guide (Oct 2026)
- The relocation guide is now `relocating-to-greater-vancouver.html` (built from `GV_*` in `_build/build.py`).
- `relocating-to-coquitlam.html` is a tiny redirect (meta refresh + JS + canonical to the new URL) so old links keep working.
  It is not in the sitemap and stays `noindex` (correct for a redirect).
- Brochure PDFs live in `assets/docs/` (compressed with Ghostscript `/printer`); cover thumbnails are `assets/img/brochure-*`.

## Axford Google reviews badge (count verified Oct 2, 2026; refresh periodically)
- Shows **only the five-star count**: "148 five-star Google reviews · Axford Real Estate". It sits above the final call to action
  on `tenants.html` (`#reviews`) and, in a compact form, in the footer on every page (`google_badge()` in `_build/partials.py`).
- The count (148 five-star reviews) was **verified Oct 2, 2026** from the Google Maps rating histogram for Axford Real Estate,
  2326 Clarke St, Port Moody. It goes stale as new reviews come in. Re-check the histogram every month or two, update
  `AXFORD_FIVE_STAR` and rebuild. Devin's choice: don't show the total count or the average rating.
- Link: `AXFORD_MAPS` = https://www.google.com/maps?cid=6001107873248015668 (place 0x548678dbf3a30647:0x534837d0c3bf7534).
- Logo: `assets/img/axford-badge-logo-160/320` (.webp/.jpg), trimmed from `buyer-bot/branding/axford-logo.jpeg`.
- No `AggregateRating` schema on purpose: the reviews belong to the brokerage, not Devin, and self-serving review markup
  is against Google's guidelines.

## Testimonials (Devin's Google Business Profile, added Oct 3, 2026)
- Verbatim quotes from "Devin Desaulniers Realtor" on Google (`TESTIMONIALS` in `_build/partials.py`). Trim only with "…",
  never change words or spelling. Attribute as first name + last initial. William Chen's review is excluded at Devin's request.
- Placement: tenants (Susan featured, Hugo, Aline; after the services/fee section), home (Thurza, Jackie, Jordan, Florian),
  buyers (Thurza, Florian, Tyson, Kyron). All use section id `#testimonials`.
- Badge "5.0 ★ on Google · 15 reviews" links to `DEVIN_GBP` = https://www.google.com/maps?cid=14841401548246613434
  (place 0x54867fa3745a1c7b:0xcdf74013342bfdba). Count as of Oct 3, 2026; update `DEVIN_GBP_COUNT` / `DEVIN_GBP_RATING` as reviews come in.
- No Review / AggregateRating schema on purpose (self-serving review markup is against Google's guidelines).

## Home-page relocation video (added Oct 6, 2026)
- Section `#video` on `index.html`, right after the hero ("Moving to Greater Vancouver?" + button to `tenants.html`). Built from `VIDEO_*` in `_build/build.py`; styles `.video-section` / `.video-frame` in `styles.css`.
- Files: `assets/video/greater-vancouver-relocation-ad.mp4` (1280x720 H.264 High, CRF 26, AAC 128k, `+faststart`, ~5.1 MB) and `-poster.jpg` (title frame at 4.0 s).
  Source (not in repo): `/workspace/video-bot/grand-tri-cities/grand-tri-cities-final.mp4`. Re-encode:
  `ffmpeg -i grand-tri-cities-final.mp4 -vf "scale=1280:720:flags=lanczos,format=yuv420p" -c:v libx264 -profile:v high -level 4.0 -preset veryslow -crf 26 -c:a aac -b:a 128k -ac 2 -movflags +faststart greater-vancouver-relocation-ad.mp4`
- `<video controls playsinline preload="metadata">`, no autoplay. Home page also carries `VideoObject` JSON-LD (absolute URLs, uploadDate 2026-10-06, PT32S).

## Blog (added Oct 6, 2026)
- Posts are Markdown files with front matter in `_posts/YYYY-MM-DD-slug.md`; `_build/blog.py` (called by `build.py`) generates
  `blog/<date>-<slug>.html`, `blog/index.html`, `blog/feed.xml`, the "Latest from the blog" strip on the home page (`#blog`, 3 newest)
  and the blog URLs in `sitemap.xml` (the sitemap is now generated by the build; don't hand-edit it).
- Step-by-step for adding a post (write file -> build -> commit -> push -> verify): **`_build/BLOG.md`**.
- Pages in `blog/` use `root="../"` in `head()` / `foot()` so shared header/footer links and assets resolve from the subfolder.
- Styles: "Blog" block at the end of `assets/css/styles.css`.
- Featured images: `_build/make_image.py` renders a branded 1200x630 JPG + WebP per post into `assets/img/blog/` (headless Chrome + ffmpeg;
  build.py calls it for posts missing an image). Used on the post, og/twitter image, BlogPosting JSON-LD and card thumbnails.
- Each post page ends with a call to action, an author box and the disclaimer. Topic and SEO rules for the daily routine: `/workspace/blog-brief/seo-brief.md`.
