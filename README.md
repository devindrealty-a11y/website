# Devin Desaulniers — Real Estate Associate, Axford Real Estate (DRAFT)

Static site for GitHub Pages. **Draft — not final.** Search engines are blocked via `<meta name="robots" content="noindex">` until launch.

Pages:
- `index.html` — home / profile
- `buyers.html` — buyer info, neighbourhood guides, "Send me listings" form
- `tenants.html` — standalone landing page for the $1,500 tenant-paid relocation rental service (link this from ads/social)

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

## Launch checklist
- Replace all placeholders (headshot, phone, brokerage address/phone, disclaimer, privacy policy, payment terms)
- Forms are connected to FormSubmit — Devin must click the activation email after the first real submission
- Remove the `noindex` meta line and the draft banner in `_build/partials.py`, rebuild
- If using a custom domain, update `SITE` in `_build/partials.py` and add a `CNAME` file
