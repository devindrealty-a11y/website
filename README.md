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

## Forms
Forms are NOT connected. Paste your form-service endpoint(s) into `assets/js/config.js` (one spot). Until then, submitting shows a placeholder notice and sends nothing.

## Launch checklist
- Replace all placeholders (headshot, phone, brokerage address/phone, disclaimer, privacy policy, payment terms)
- Connect forms in `assets/js/config.js`
- Remove the `noindex` meta line and the draft banner in `_build/partials.py`, rebuild
- If using a custom domain, update `SITE` in `_build/partials.py` and add a `CNAME` file
