# Devin Desaulniers — Real Estate Associate, Axford Real Estate

Static site for GitHub Pages, custom domain **https://devindesaulniers.ca/** (CNAME in repo root).

Pages:
- `index.html` — home / profile, with the qualifying form in the contact section
- `contact.html` — the same qualifying form, plus phone, email, and brokerage details
- `buyers.html` — buyer info, neighbourhood guides, "Send me listings" form
- `home-evaluation.html` — free market evaluation: email and property address
- `buyer-opinion.html` — his take on a property you're considering
- `tenants.html` — standalone landing page for the $1,500 tenant-paid relocation rental service (link this from ads/social)
- `listings.html` — active residential homes for sale in Greater Vancouver and the Fraser Valley (REALTOR.ca DDF®)
- `rentals.html` — active residential homes for rent in the same area, with rent shown per month
- `rent-report.html` — weekly asking-rent report for people moving to Greater Vancouver (medians by city and bedroom, week-over-week change, new listings, best-value homes)
- `market-report/` — monthly Tri-Cities, BC sales report (benchmark, sales, listings) built from `_build/market_data/*.json`. See `_build/MARKET_REPORT.md`.
- `videos.html` — property video tours from Devin's YouTube channel (not listings)
- `blog/` — blog index, posts, RSS feed, generated from Markdown in `_posts/` (see **`_build/BLOG.md`** for how to add a post)
- `true-cost-of-owning-a-home-bc.html` — lead-magnet guide to monthly costs besides the mortgage in the Tri-Cities, BC (property tax, strata, insurance, maintenance, utilities), with an estimator. Built from `_build/true_cost_page.py`.

`_promo/` is an unpublished promotion kit (Meta ads, Google Business Profile posts, YouTube text, communities, and a 4-week rollout). GitHub Pages runs Jekyll on this repo, and Jekyll does not publish that folder. `_config.yml` excludes it as well. Do not add a `.nojekyll` file.

## Editing
HTML is generated from `_build/build.py` + `_build/partials.py` (header/footer shared). Edit those, then run:
```
cd _build && python3 build.py
```
(Or edit the HTML files directly if you prefer — just don't re-run the build afterwards.)

No placeholders remain: the footer disclaimer, the privacy page (`privacy.html`, built from `PRIVACY_URL` / `privacy` in `_build/build.py`), the Axford disclosure in the tenant FAQ, the buyer services list and the neighbourhood notes are all written. If you add or change a form, the chat widget or another third-party service, update `privacy.html` to match.

## Forms (FormSubmit)
The forms (the qualifying form on `index.html#qualify` and `contact.html`, buyers.html "Send me listings", tenants.html relocation intake, home-evaluation.html, buyer-opinion.html, the listing and rental inquiries, and the chat widget message) post via AJAX to
`https://formsubmit.co/ajax/devin@axfordrealestate.ca` — configured in one spot: `assets/js/config.js`.
- Email subjects include "New qualified lead: Buying, Coquitlam, 0-3 months", "New buyer listings request", "New relocation rental intake", "New free home evaluation", "New expert opinion request", and "New chat widget message" (table template, Reply-To = visitor's email).
- The qualifying form (`qualifiedLead`) asks buying / selling / renting, area, timeline, budget or home value or monthly rent, where they're moving from, then name, email, optional phone, optional message, and the same contact-consent checkbox as the other forms. GoatCounter events, sent with `window.goatcounter.count` and `event: true`, are `lead-form-start`, `lead-form-step-1` through `lead-form-step-6` when that step is first shown, and `lead-form-sent` only after FormSubmit accepts the message. Those names do not include the visitor's answers, name, email, phone, or message.
- `qualifiedLead`, `homeEvaluation`, `buyerOpinion`, `chatLead`, and `marketReport` were not test-submitted. The market-report form asks for a name, an email, and consent, then reveals that month's PDF. Its subject is `Market report download: <name>`. GoatCounter event `report-download` fires only after FormSubmit accepts it, and does not include the name or email.
- Spam: hidden honeypot field `_honey`. reCAPTCHA is not used by FormSubmit's AJAX flow, so nothing was disabled.
- Visitors see an on-page success (or error + call/email fallback) message.

## True cost guide sign-up

`true-cost-of-owning-a-home-bc.html` asks for a name, an email, and a consent checkbox. The form posts only to FormSubmit (`trueCostSignup` in `assets/js/config.js`), which emails `devin@axfordrealestate.ca`. The subject is `True cost guide sign-up: <name>`. GoatCounter event `true-cost-signup` fires only after FormSubmit accepts the signup, and it does not include the name or email. There is no mailing-list connection on this page. Do not test-submit. The first real FormSubmit submission still needs the activation click described below.

**Activation (one-time):** the FIRST real submission makes FormSubmit send an activation email to
devin@axfordrealestate.ca. Devin must click "Activate Form" — submissions are not delivered until then
(the first one is held until activation). No test submission has been sent.
Tip: the activation email includes a random alias; replace the email address in the URLs in
`config.js` with `https://formsubmit.co/ajax/<alias>` to keep the address out of the page source.

## Chat widget
Every page loads a self-hosted chat widget (`assets/js/chat.js`, styles at the end of `assets/css/styles.css`) from `foot()` in `_build/partials.py`. It replaces the Elfsight chatbot. The guided answers run in the browser. GoatCounter events, sent with `window.goatcounter.count` and `event: true`, use fixed names: `chat-opened` when the chat opens, `chat-buying`, `chat-renting`, `chat-relocating`, or `chat-selling` when a topic is chosen, `chat-lead-shown` when the message form opens, and `chat-message-sent` only after FormSubmit accepts the message. Those names do not include the visitor's name, email, phone, or message. count.js loads asynchronously, so an event that happens before `window.goatcounter.count` exists is queued and sent when the script loads. If the counter never loads, the count is skipped. The message form posts to the same FormSubmit URL as the other forms (`chatLead` in `assets/js/config.js`). It has not been test-submitted. The widget header reads “Devin Desaulniers, REALTOR®, Axford Real Estate”.

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
- `sitemap.xml` lists the live pages under https://devindesaulniers.ca/ (home, listings, rentals, rent-report, the Tri-Cities, BC market report index and each edition, tenants, buyers, home-evaluation, buyer-opinion, relocating-to-greater-vancouver, videos, privacy, terms, and the blog). The Coquitlam redirect is omitted. The rent report URL gets a `lastmod` from the latest Monday snapshot. Each market-report URL gets a `lastmod` from the edition's published date.
- `robots.txt` allows crawl and lists the Sitemap at https://devindesaulniers.ca/sitemap.xml (served at the domain root).
- `SITE` in `_build/partials.py` is `https://devindesaulniers.ca/`. Rebuild after changing it.
- Submit `sitemap.xml` in Google Search Console when ready.

## Launch checklist
- ~~Replace all remaining placeholders~~ Done: disclaimer, privacy page (`privacy.html`), Axford-managed disclosure in the tenant FAQ, buyer services list, neighbourhood notes.
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

## YouTube property tours
- The six tours are listed once in `YT_TOURS` (`_build/partials.py`, id + title). `YT_HOME` picks the three on the home page (`#tours`);
  `YT_BUYERS` in `_build/build.py` picks the three on `buyers.html#tours`; `videos.html` shows all six.
- These are video tours, not Devin's listings — keep the `YT_NOTE` line next to them and never label them "for sale", "sold" or "my listings".
- Each tour renders as a click-to-play button (`tour_card()`): only the `i.ytimg.com` thumbnail loads with the page. `assets/js/site.js`
  swaps in a `youtube-nocookie.com` player for `[data-yt]` on click. No `VideoObject` JSON-LD for YouTube videos.

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

## Listings search (DDF) — for sale and for rent

`listings.html` and `rentals.html` are live. `LISTINGS_LIVE` in `_build/partials.py` is `True`, so both pages are in the header, the footer, and `sitemap.xml`, and neither is `noindex`. They are built with the rest of the site (`cd _build && python3 build.py`).

Both cover Greater Vancouver and the Fraser Valley from the CREA REALTOR.ca DDF® National Shared Pool. For-sale rows are active residential listings. For-rent rows are active residential leases (commercial excluded). A listing is written to only one file. Sold and leased-completed listings are not stored.

The October 14, 2026 refresh wrote 21,212 homes for sale and 961 homes for rent. Asking rent on this feed does not arrive as `TransactionType` or `LeaseAmount`. The Web API has one Property collection and no lease class. `TransactionType` is not on the live Property entity, and a RETS compact read of the same destination returns a blank `TransactionType` for every row. The October 14, 2026 read found 961 active rows with a blank list price, `LeaseAmountFrequency` of Monthly, and a positive `TotalActualRent` (518 between $1,500 and $3,000, 302 between $3,000 and $6,000, and the rest scattered from under $500 to under $100,000). `LeaseAmount` was empty on all 22,264 rows. Those 961 are Single Family homes (apartments, houses, townhouses, and duplexes), and the RETS `Lease` column is filled on the same set. The sync files that pattern as a rental and stores `TotalActualRent` as the monthly rent. A sale that also has `TotalActualRent` stays a sale, because that figure is rent collected on an income property. None of the priced rows in this feed had `TotalActualRent` set.

Do not add a `.nojekyll` file. GitHub Pages runs Jekyll, which does not publish `_fixtures/`. That is what keeps the sample files off the live site.

### Secrets

Repository **Settings → Secrets and variables → Actions**:

| Secret | What it is |
| --- | --- |
| `DDF_USERNAME` | DDF destination username. On the Web API this is the OAuth client id. |
| `DDF_PASSWORD` | DDF destination password. On the Web API this is the OAuth client secret. |

No other secret names are read. The same pair feeds both JSON files. The workflow needs permission to push: **Settings → Actions → General → Workflow permissions → Read and write**.

### What the refresh does

`.github/workflows/ddf-listings.yml` runs every 12 hours (`0 */12 * * *` UTC) and from **Actions → Refresh DDF listings → Run workflow**. DDF rules require a refresh at least every 24 hours; this schedule stays inside that even if one run is delayed.

`scripts/fetch_ddf_listings.py` does one pull and writes both files:

1. If `DDF_USERNAME` or `DDF_PASSWORD` is missing, it prints a skip message and exits 0. It does not change `listings/data.json` or `listings/rentals.json`, and it does not fail the job.
2. It signs in to the DDF Web API (OData) at `https://ddfapi.realtor.ca/odata/v1`. The token request is `POST https://identity.crea.ca/connect/token` with `grant_type=client_credentials` and `scope=DDFApi_Read`.
3. If that API cannot be reached, or the token request is rejected, it falls back to the RETS feed at `https://data.crea.ca` (digest login, session cookie, Standard-XML search).
4. For-sale rows go to `listings/data.json`. Residential for-lease or for-rent rows go to `listings/rentals.json`. Commercial rows are dropped from both. Sold, leased-completed, and out-of-area records are dropped. Sold prices are never stored. Each search file keeps a light card (price, address, beds, baths, brokerage, first photo). Galleries and public remarks go in `listings/sale/{n}.json` and `listings/rent/{n}.json`, where `n` is the numeric listing id modulo 48. The page fetches a shard only when a home is opened. Sample fixtures keep photos and remarks inline and are not sharded. The workflow commits the whole `listings/` directory, including those shards and any deletions.
5. Rent is stored as dollars per month. `LeaseAmount` is preferred, then `ListPrice` / RETS `Price`, then `TotalActualRent` when the list price is blank and a frequency is set. `LeaseAmountFrequency` (or RETS `PricePerTime` / `LeasePerTime`) converts the figure: weekly × 52/12, bi-weekly × 26/12, semi-monthly × 2, bi-monthly (every two months) ÷ 2, annually ÷ 12. A blank frequency is treated as monthly when the amount came from `LeaseAmount` or `ListPrice`. `TotalActualRent` is used only when a frequency is present, so an unpriced sale is not relabeled as a rental. One-time and unrecognized frequencies are left out rather than shown as a monthly rent.
6. Photos stay remote `https` URLs. Each file is replaced in full, so a listing that leaves the feed disappears from that file. If one side has matches and the other does not, the empty side is still replaced.
7. If the feed returns records but none are kept on either side, the script exits 1 and does not wipe either file.

Opening a real listing (not the sample file) logs a view to the CREA DDF® Analytics Web Service at `https://analytics.crea.ca/LogEvents.svc/LogEvents` with `EventType=view`, the numeric listing id, the destination id from the feed login, and the page URL. That call is required by the June 2026 DDF rules. It runs on both pages and is skipped when the sample file is loaded or the destination id is missing.

Each card shows the listing brokerage, a link to that listing on REALTOR.ca, and a Powered by REALTOR.ca mark. Both pages name Axford Real Estate and include the CREA trademark line and the DDF disclaimer.

Check the logic without credentials: `python3 scripts/test_ddf_listings.py`.

### Local preview (sample data, never published)

```
python3 -m http.server 8765
```

Open `http://127.0.0.1:8765/listings.html?preview=1` and `http://127.0.0.1:8765/rentals.html?preview=1`.

`_fixtures/listings-sample.json` and `_fixtures/rentals-sample.json` are fictional (sample ids, sample brokerages, placeholder photos). On localhost each page loads its sample unless the URL has `?live=1`. On devindesaulniers.ca the pages load `listings/data.json` and `listings/rentals.json` only. `?preview=1` on the public site asks for `_fixtures/…`, which Jekyll does not publish, so the samples never appear there.

The detail-page inquiry forms post to FormSubmit (`listingInquiry` and `rentalInquiry` in `assets/js/config.js`), the same way as the other forms. They have not been test-submitted. The first real submission still needs Devin to activate FormSubmit. `privacy.html` describes those forms and the listing-view call to analytics.crea.ca.

## Weekly rent report

`rent-report.html` is the public page. `rent-report/newsletter.html` (Verdana, inline styles, noindex) and `rent-report/newsletter.txt` are the same week's summary, ready to paste into an email. `rent-report/history/YYYY-MM-DD.json` is the Monday snapshot (medians plus listing ids). `rent-report/history/series.json` is the chart series without the ids.

The page counts active residential asking rents from `listings/rentals.json`. It keeps a city, a bedroom count, and a rent from $800 to $40,000, and leaves out a missing city, a garage, or a size under 200 square feet. Medians and averages are rounded to the nearest dollar. Week-over-week change needs two snapshots and at least five homes in both weeks for that row. On the first run, "new" means the REALTOR.ca record was updated on or after Monday. After that, new means the listing id was not in the previous snapshot. Best value is asking rent per square foot at least 12% under the median for the same city and bedroom count (at most two homes per city).

`.github/workflows/rent-report.yml` runs every Monday at 15:00 UTC and from **Actions → Weekly rent report → Run workflow**. It does not call DDF. It reads whatever `listings/rentals.json` is already in the repo, so the 12-hour listing refresh should have run first. Check the logic without rewriting the page: `python3 scripts/test_rent_report.py`. Rebuild the page locally with `python3 scripts/build_rent_report.py`.

The rent report page (not the listing search) carries `Dataset` JSON-LD. `creator` is a `Person` (Devin Desaulniers, `worksFor` Axford Real Estate). `license` is `https://devindesaulniers.ca/terms.html`, which states that the listing data is provided through the CREA DDF® and is owned by the respective boards. It is not a Creative Commons license. `terms.html` is built by `_build/terms_page.py`.

Every page has the same offer under the header: "Want me to find yours? Tenant Relocation Service $1,500 + GST", linking to `tenants.html#intake`. Page visits are already counted with GoatCounter (`https://devindesaulniers.goatcounter.com/count`, no cookies). Those offer links also send an event named `cta-tenant-relocation`. `privacy.html` says so.
