# Launch checklist

Do this once, before 1 November 2026, when Devin decides to spend. This repo cannot do it for him. No ad account is created by the docs in `/ads`.

## 1. Brokerage

- [ ] Axford’s managing broker has seen [copy.md](copy.md) and [creative-briefs.md](creative-briefs.md) and approved them
- [ ] The ad identity is allowed to be Devin’s Facebook page and Instagram, with **Axford Real Estate** in the ad text
- [ ] Someone has confirmed the wording meets current BCFSA advertising rules for licensees (name and brokerage on the ad, nothing misleading). This folder is not legal advice
- [ ] `REALTOR®` is used as the CREA mark, not as a generic word for “agent” in a sentence that drops the ®
- [ ] Devin can reply to a new lead within one business day through November, including the week of 1 November

## 2. The site, unchanged but checked

- [ ] `https://devindesaulniers.ca/relocating-to-greater-vancouver.html` loads, and “Need a rental? Start here” opens the intake
- [ ] `https://devindesaulniers.ca/buyers.html` loads, and “Send me listings” reaches the form
- [ ] `https://devindesaulniers.ca/rentals.html` loads real listings (not the sample banner)
- [ ] A listing on the rentals page shows “Ask Devin about this rental”
- [ ] FormSubmit is **activated** for devin@axfordrealestate.ca, so a real submit is delivered and not held for the activation email. The site README explains that the first real submission triggers that email. Confirm delivery with a message he expects, then ignore that message on the ROI sheet
- [ ] Phone 604-809-1032 is the number he will answer

## 3. Creative files

- [ ] Stills exported at 1080 × 1080 and 1080 × 1920
- [ ] Fee still matches “$1,500 + GST” and “paid in two parts”
- [ ] No MLS photo, no address, no “SOLD”
- [ ] If the homepage video is used, Devin has watched it and every line is on the allowed-claims list

## 4. Meta

- [ ] Account currency is CAD
- [ ] Special ad category **Housing** is on before the audience is built
- [ ] Two campaigns, names from [targeting.md](targeting.md)
- [ ] Locations are the six origin cities (people who live there), English, age and gender left on the Housing locks
- [ ] Placements are the feeds, Stories, and Reels. Audience Network off if the UI allows
- [ ] Daily budgets $6 and $2, spending limits $180 and $60, dates 1–30 November 2026
- [ ] Objective is Traffic, optimization is landing page views
- [ ] Ads R1–R4 and B1–B4 pasted from [copy.md](copy.md), each with its URL from [landing-pages.md](landing-pages.md)
- [ ] Button is Learn more
- [ ] No pixel is required for this step. Do not block launch on the tracking plan
- [ ] Payment method is one Devin or the brokerage meant to use. This package does not add one

## 5. Google Ads

- [ ] Account currency is CAD
- [ ] One Search campaign, Search network only, Canada, English, presence targeting
- [ ] Maximize clicks, max CPC $4, daily budget $2, November limit $60, dates 1–30 November 2026
- [ ] Ad group A keywords, negatives, and the rental RSA from [copy.md](copy.md) and [targeting.md](targeting.md)
- [ ] Ad group B keywords and the relocation RSA
- [ ] Pins: “Devin Desaulniers” in headline position 1, description 1 in description position 1
- [ ] Final URL suffixes are the UTM strings in [landing-pages.md](landing-pages.md)
- [ ] Auto-tagging on
- [ ] Call asset 604-809-1032
- [ ] Sitelinks only after the ads are approved
- [ ] No conversion tag installed

## 6. The morning of Monday 2 November

- [ ] Both Meta campaigns and the Google campaign show as approved and delivering, or the disapproval reason is fixed without changing the offer
- [ ] Spend is pacing near $10 a day, not a lump sum
- [ ] One click of each final URL still lands on the right page
- [ ] The ROI sheet’s first row is started ([weekly-roi-check.md](weekly-roi-check.md))
- [ ] Next decision is Monday 9 November, not a mid-week budget increase

## Character check

The limits in [copy.md](copy.md) were checked against this file when the package was written. Re-run this from the repo root if anyone edits a headline:

```bash
python3 ads/check_copy_limits.py
```

The script only reads `ads/copy.md`. It does not call an ad platform.
