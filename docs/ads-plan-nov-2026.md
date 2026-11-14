# Google Ads relocation trial — 21 days, $150 CAD (draft)

**Status:** Draft only. Nothing in this document spends money or creates an ad account. Devin sets up billing himself, approves this plan, and turns ads on only after the landing-page PR is live.

**Site:** [devindesaulniers.ca](https://devindesaulniers.ca)
**Agent:** Devin Desaulniers, Real Estate Associate
**Brokerage (required in every ad):** Axford Real Estate
**Contact:** devin@axfordrealestate.ca · 604-809-1032 · Port Moody, BC (licensed 2020)
**Landing page (all ads):** `https://devindesaulniers.ca/rental-before-you-arrive.html#intake`

This plan replaces the earlier ~$200/month Google + Meta draft. Meta (Facebook and Instagram) is out of scope here — Muse is running those. This is Google Search only.

---

## 1. Trial at a glance

| Item | Setting |
| ---- | ------- |
| Total budget | **$150 CAD** |
| Length | **21 days**, with a hard end date in the campaign |
| Daily budget | **$7.14 CAD** ($150 ÷ 21) |
| Network | Google Search only (uncheck Display Network and Search partners) |
| Campaigns | One Search campaign |
| Ad groups | Two tightly themed groups (merge into one if day-7 volume is thin) |
| Keywords | Phrase and exact match only |
| Bidding, week 1 | Maximize Clicks with a **$4.00 CAD max CPC cap** |
| Bidding, later | Switch to Maximize Conversions **only if** form conversions are recording |
| Goal | About **5 qualified leads** for the $1,500 + GST tenant relocation service |
| Success that covers the test | **One paid client** ($1,500 + GST) covers the $150 test ten times over |

**Rough click-cost estimates only (not a forecast, not a promise):** relocation and rental-help clicks in this market often land around $2–$4 CAD. At $150, that is roughly 40–75 clicks. If 5–10% of those people submit the form, you might see about 2–7 leads. Five qualified leads is possible; 2–4 may be more typical on a first test. Do not treat these numbers as targets Google will hit.

**Qualified lead:** a form submitted with name, email and phone, “Would you like professional help managing your rental search?” = Yes, and “Do you currently live in Greater Vancouver?” = No (or a clear out-of-area “moving from”). A “No” on paid help is still useful context, but it does not count toward the 5-lead goal.

---

## 2. BCFSA / advertising compliance

Every paid ad and the landing page must:

1. **Name the brokerage:** “Axford Real Estate” in ad text (headlines or descriptions, and callouts) and on the landing page.
2. **Identify Devin:** “Devin Desaulniers, Real Estate Associate” (or “REALTOR®” where accurate).
3. **Avoid superlatives:** Do not use “best”, “top”, “#1”, “leading”, “premier”, or similar unsubstantiated claims.
4. **No invented proof:** Do not claim review counts, sales volumes, or rankings unless they are verifiable and current on the site.
5. **No guaranteed outcomes:** No promise of finding a rental within a set number of days, or guaranteed savings.
6. **Fees:** Tenant relocation service is **$1,500 + GST, paid by the tenant in two parts** ($750 at the beginning of the engagement, non-refundable, and $750 once they successfully secure a rental). State the paid fee in rental ads.
7. **Place names:** Write **Tri-Cities, BC** in ad copy (not bare “Tri-Cities”). Keywords may match how people search, including without “, BC”.

### Google housing ads policy (US and Canada)

This campaign promotes a service that helps people rent a home, so it falls under Google’s housing / “Access to opportunities” rules for ads serving in Canada (and the US, if that location is turned on). Official policy: [Housing in personalized advertising](https://support.google.com/adspolicy/answer/16701755) and the [FAQ](https://support.google.com/adspolicy/answer/9997418).

- Do **not** target or exclude by age, gender, parental status, or marital status. Leave those demographics set to **Enable**.
- Do **not** target full postal / ZIP codes. City, province, country, and radius (minimum 1 km) are allowed. In Canada, the first three characters of a postal code (FSA) are allowed, but this plan uses provinces and city exclusions instead.
- When Google Ads asks you to certify housing, employment, or credit ads, accept the housing certification.

---

## 3. Landing page and tracking

**Final URL for every ad (including UTM):**

```
https://devindesaulniers.ca/rental-before-you-arrive.html?utm_source=google&utm_medium=cpc&utm_campaign=gv-reloc-rental-21d&utm_content={adgroupid}&utm_term={keyword}#intake
```

The form sits on that page (`#intake`), not on `tenants.html`. It asks: moving from, work or study location, budget, bedrooms, move date, currently live in Greater Vancouver (yes/no), want paid help (yes/no), name, email, phone. The button is **Build My Rental Search**. The fee disclosure matches the tenants page: $1,500 + GST, paid by the tenant in two parts ($750 at the beginning of the engagement, non-refundable, and $750 once you successfully secure a rental). Axford Real Estate is named on the form.

**Do not turn ads on until this landing page is live** (the draft PR must be approved and merged, and GitHub Pages must have finished building).

### What the site already records

- FormSubmit emails the submission to devin@axfordrealestate.ca, with UTM fields and `gclid` when they are in the URL.
- GoatCounter event `form-tenant` fires only after FormSubmit accepts the form (same event name as the tenants-page intake). Other site forms now queue the same way, so a slow-loading counter does not drop the event.
- A Google Ads conversion hook is in `assets/js/site.js` as `GOOGLE_ADS_CONVERSION_ID`. It is **empty on purpose**. No gtag script loads until that constant is filled with an `AW-…/…` ID. After the Google Ads conversion action exists, paste the ID, commit, and deploy, then test.

---

## 4. Campaign structure

**Campaign name:** `GV Relocation Rentals — 21-day $150 trial`
**Type:** Search
**Goal:** Leads (or “Website visits” / “Create a campaign without a goal’s guidance” if the new-account wizard pushes Performance Max — skip PMax and any AI Max “go beyond keywords” expansion for this test)
**Currency:** CAD
**Time zone:** America/Vancouver (Pacific Time)
**Budget:** $7.14/day, standard delivery
**Start / end:** Set both. End date is day 21. Pause manually if you need to stop sooner.
**Languages:** English
**Location options:** Presence — “Presence: People in or regularly in your included locations” (not “Presence or interest”). The keywords, not Google’s “interest in Vancouver,” do the filtering.

### Locations (include)

- Ontario, Canada
- Alberta, Canada
- British Columbia, Canada

### Locations (exclude)

Exclude Metro Vancouver / Greater Vancouver if Google offers it as one region. Otherwise exclude these municipalities so people already in the Lower Mainland do not use up the $7/day:

Vancouver, Burnaby, Richmond, Surrey, Coquitlam, Port Coquitlam, Port Moody, New Westminster, the City and District of North Vancouver, West Vancouver, Delta, the City and Township of Langley, White Rock, Maple Ridge, Pitt Meadows, Anmore, Belcarra, Lions Bay, Tsawwassen, Ladner.

People in the rest of B.C. (Victoria, Kelowna, Kamloops, Prince George, Nanaimo, and so on) stay included.

### Optional: United States

Leave the US **off** at launch so the $150 stays on Canadian movers. If search volume is very thin after day 7, you can add the United States (still exclude nothing extra unless a flood of irrelevant clicks appears) and keep Presence only. This is a decision for Devin, not a default.

### Bidding

1. **Days 1–7:** Maximize Clicks, max CPC cap **$4.00 CAD**. This is a starting cap based on the rough $2–$4 estimate above, not a researched bid. If impression share is almost zero, raise the cap slightly (for example $5) rather than removing it. If CPC is consistently under $2 and you are missing volume, you can leave the cap.
2. **After conversions appear** (at least a handful of `form-tenant` / Google Ads conversion pings): consider Maximize Conversions. Do not switch early with zero conversions — the budget is too small for the algorithm to learn.

---

## 5. Keywords

Match types: **phrase** (`"keyword"`) and **exact** (`[keyword]`) only. No broad match.

### Ad group A — Relocation rental agent / service

| Keyword | Phrase | Exact |
| ------- | ------ | ----- |
| relocation rental agent Vancouver | `"relocation rental agent Vancouver"` | `[relocation rental agent Vancouver]` |
| relocation rental agent Greater Vancouver | `"relocation rental agent Greater Vancouver"` | `[relocation rental agent Greater Vancouver]` |
| tenant relocation service Greater Vancouver | `"tenant relocation service Greater Vancouver"` | `[tenant relocation service Greater Vancouver]` |
| tenant relocation service Vancouver | `"tenant relocation service Vancouver"` | `[tenant relocation service Vancouver]` |
| rental relocation agent Vancouver | `"rental relocation agent Vancouver"` | `[rental relocation agent Vancouver]` |
| Vancouver tenant relocation | `"Vancouver tenant relocation"` | `[Vancouver tenant relocation]` |

### Ad group B — Before you arrive / moving here for a rental

| Keyword | Phrase | Exact |
| ------- | ------ | ----- |
| find a rental in Vancouver before I move | `"find a rental in Vancouver before I move"` | `[find a rental in Vancouver before I move]` |
| rental before I arrive Vancouver | `"rental before I arrive Vancouver"` | `[rental before I arrive Vancouver]` |
| moving to Coquitlam rental help | `"moving to Coquitlam rental help"` | `[moving to Coquitlam rental help]` |
| moving to Port Moody rental | `"moving to Port Moody rental"` | `[moving to Port Moody rental]` |
| moving to Port Coquitlam rental | `"moving to Port Coquitlam rental"` | `[moving to Port Coquitlam rental]` |
| moving to the Tri-Cities rental | `"moving to the Tri-Cities rental"` | `[moving to the Tri-Cities rental]` |
| help finding a rental in Coquitlam before I move | `"help finding a rental in Coquitlam before I move"` | `[help finding a rental in Coquitlam before I move]` |
| rent in Vancouver before I move | `"rent in Vancouver before I move"` | `[rent in Vancouver before I move]` |
| line up a rental before arriving Vancouver | `"line up a rental before arriving Vancouver"` | `[line up a rental before arriving Vancouver]` |

Paste the phrase and exact versions as separate keywords in each group. If a keyword gets zero impressions after two weeks and others are spending, you can pause the zero-impression exact versions to keep the list tidy.

---

## 6. Negative keywords (campaign level)

Add these as **phrase** negatives unless noted. The aim is to block bargain hunting, roommates, job seekers, students, and social-housing searches — not people who will pay $1,500 for help.

```
free
cheap
cheapest
room
rooms
roommate
room-mate
roommates
"room for rent"
craigslist
kijiji
"facebook marketplace"
padmapper
basement
"basement suite"
jobs
job
hiring
career
student
students
"student housing"
shelter
shelters
subsidized
"bc housing"
"low income"
"income assistance"
welfare
homeless
hostel
airbnb
"air bnb"
"short term"
"for sale"
"homes for sale"
"house for sale"
mortgage
"first time buyer"
internship
"co-op housing"
"cooperative housing"
"application fee"
"tenancy agreement template"
"standard lease"
"residential tenancy branch"
```

Do **not** add a bare `for rent` negative — it would also block useful searches like “help me find a rental in Vancouver before I move.”

After day 3, add more negatives from the Search terms report for anything off-brief (jobs, rooms, cheap listings, legal templates).

---

## 7. Paste-ready responsive search ads

Create **three** RSAs (you can put all three in both ad groups, or 2 in A and 1 in B). Pin **Axford Real Estate** to a headline position only if Google keeps dropping the brokerage name from the served combination; otherwise leave headlines unpinned so Google can test combinations. Every ad below already includes the brokerage, the paid fee, and “Tri-Cities, BC” somewhere in the asset list so a valid combination can show them.

Display path: `devindesaulniers.ca` / `relocation` / `rental-help`

Final URL: the UTM URL in section 3.

Character limits used below: headlines ≤ 30, descriptions ≤ 90.

### RSA 1 — Before you arrive

**Headlines (paste one per line):**

```
Moving to Greater Vancouver
Line Up a Rental First
Find a Rental Before You Move
Help Before You Arrive
$1,500 + GST Paid Service
Axford Real Estate
Devin Desaulniers
Rent in the Tri-Cities, BC
Search, Showings, Lease
Tell Me Your Move Date
Live Video Showings
Paid Tenant-Side Help
Lease Review Included
Port Moody Based Agent
Greater Vancouver Rentals
```

**Descriptions:**

```
Help finding a Greater Vancouver rental before you arrive. Axford Real Estate.
Paid tenant relocation: $1,500 + GST. Search, showings and lease review in Port Moody.
Moving to the Tri-Cities, BC or Greater Vancouver? Share your budget, commute and date.
This is a paid service ($1,500 + GST). Use the short form to start a rental search.
```

### RSA 2 — Paid service, clearly stated

**Headlines:**

```
Tenant Relocation Service
$1,500 + GST Paid Service
Axford Real Estate
Paid Tenant-Side Help
Moving to Greater Vancouver
Devin Desaulniers
Licensed REALTOR® Help
Rent in the Tri-Cities, BC
Line Up a Rental First
Moving From Ontario?
Moving From Alberta?
Tell Me Your Move Date
Greater Vancouver Rentals
Port Moody Based Agent
Lease Review Included
```

**Descriptions:**

```
This is a paid service ($1,500 + GST). Use the short form to start a rental search.
Tell me where you're moving from, your budget and move date. $1,500 + GST, paid by you.
Moving to the Tri-Cities, BC or Greater Vancouver? Share your budget, commute and date.
Paid help to line up a rental before you land. Licensed with Axford Real Estate.
```

### RSA 3 — Ontario / Alberta movers

**Headlines:**

```
Moving From Ontario?
Moving From Alberta?
Moving to Greater Vancouver
Help Before You Arrive
Rent in the Tri-Cities, BC
Axford Real Estate
$1,500 + GST Paid Service
Devin Desaulniers
Find a Rental Before You Move
Live Video Showings
Search, Showings, Lease
Tenant Relocation Service
Port Moody Based Agent
Tell Me Your Move Date
Paid Tenant-Side Help
```

**Descriptions:**

```
Devin Desaulniers helps people moving to Greater Vancouver rent before they arrive.
I search, do showings or live video, and review the lease with you. Axford Real Estate.
Line up a long-term rental before you land. Licensed, Axford Real Estate, Port Moody.
Moving to the Tri-Cities, BC or Greater Vancouver? Share your budget, commute and date.
```

### Sitelinks

| Title (≤25) | Description line 1 (≤35) | Description line 2 (≤35) | URL |
| ----------- | ------------------------ | ------------------------ | --- |
| Rental search form | Start a short rental search | $1,500 + GST, paid by you | `rental-before-you-arrive.html#intake` |
| How the service works | What's included, and the fee | Tenant-side help, two payments | `tenants.html` |
| Weekly rent report | Asking rents near the Tri-Cities, BC | Updated from the MLS® feed | `rent-report.html` |
| Relocating guide | Neighbourhoods and move timing | Greater Vancouver overview | `relocating-to-greater-vancouver.html` |

Add the same UTM parameters on sitelink URLs, with `utm_content=sitelink-form` (and so on).

### Callouts (≤25 characters each)

```
Axford Real Estate
$1,500 + GST tenant fee
Live video showings
Tri-Cities, BC coverage
Lease review included
Paid tenant-side help
```

### Optional call extension

Business name: Devin Desaulniers, Axford Real Estate
Phone: 604-809-1032
(Only if Devin wants paid-click-to-call during the test. It can use budget. Default: skip for week 1, add later if form volume is low and he wants the phone to ring.)

---

## 8. Check schedule

Use `docs/weekly-ad-metrics-template.csv` or a copy in Google Sheets. Dates below are offsets from the start date you set in Google Ads.

### Day 3 (first quality check)

- Confirm ads are approved (or fix policy flags — housing certification, brokerage name, fee wording).
- Spend should be on the order of ~$21 if it is delivering fully; less is fine if volume is thin.
- Open the Search terms report. Add negatives for junk. Pause any exact/phrase keyword that is clearly off-brief.
- Confirm clicks land on `rental-before-you-arrive.html#intake` and that the form works on a phone.
- Confirm FormSubmit email arrived for any real or test submit (if you submit a test, mark it “test” in the name).

### Day 7 (end of Maximize Clicks week)

- Log spend, clicks, average CPC, impressions, search impression share, conversions / form emails.
- If CPC is at the $4 cap and impression share is tiny, consider a $5 cap. If many clicks and zero forms, re-read the landing form on mobile and tighten keywords before raising bids.
- Decision: keep US targeting off, or add the US if Canadian volume is too thin.
- If the Google Ads conversion ID is now in `site.js` and live, and at least one conversion has recorded, you may switch to Maximize Conversions. Otherwise stay on Maximize Clicks.

### Day 14 (mid-trial)

- Same metrics. Cut leftover waste. Shift budget toward the ad group with cheaper, better-qualified leads if one is clearly ahead (you cannot raise the campaign budget without eating the $150 early — keep the daily cap).
- Count qualified leads from email, not only Google’s conversion column (in case the tag is not live yet).

### Day 21 (stop)

- The campaign end date should already stop spend. Also pause the campaign so nothing restarts.
- Fill the tracker: spend, clicks, CPC, leads, cost per lead, paid clients (likely zero or pending — a paid client can close after day 21).
- Decide: stop, run another small test with tighter keywords, or pause and wait. Do not raise spend without a new okay from Devin.

---

## 9. Step-by-step Google Ads setup checklist

A browser assistant can follow this with Devin signed in. **Devin enters the Amex card in Google Ads himself.** Do not collect, store, or type the card in chat, email, or a shared doc.

Account (likely): **devindrealty@gmail.com**. Confirm the login before creating the account. If a different Google account is the one he wants billed, use that instead — do not create a second ads account for the same business.

### A. Create the account (no ads on yet)

- [ ] Sign in at [ads.google.com](https://ads.google.com) with the chosen Google account.
- [ ] If Google tries to push a Smart campaign or Performance Max, leave the wizard and choose **+ New campaign** → **Create a campaign without a goal’s guidance** → **Search**.
- [ ] Business name: Devin Desaulniers / Axford Real Estate. Website: `https://devindesaulniers.ca`.
- [ ] Currency: **CAD**. Time zone: **(GMT-08:00) Pacific Time — Vancouver** (America/Vancouver). These cannot be changed later.
- [ ] Skip launching the first campaign until billing, conversions, and this plan’s settings are in place. It is fine to create the campaign in draft / paused.

### B. Billing (Devin only)

- [ ] Billing country: Canada. Add the Amex card in Google Ads billing. Set a payment threshold / auto-pay as Google requires.
- [ ] If a **new-advertiser promotional offer** appears at signup, read the terms on the offer before accepting. Official Canada terms: [Google Ads promotional credit terms](https://ads.google.com/intl/en_ca/home/terms-and-conditions/incentives/). Offers usually need a minimum spend within a set window, with credit applied later and expiring after it is applied. A $150 trial may not meet a large spend-to-unlock amount — do not raise the $150 budget just to chase a credit. Record whatever offer (if any) was shown.

### C. Housing certification and conversion action

- [ ] Complete the housing ads certification when Google presents it (Tools / Policy / personalized advertising).
- [ ] Goals → Conversions → New conversion action → Website → `devindesaulniers.ca`.
- [ ] Create one conversion named **Relocation rental form**. Count: One. Click-through window: 30 days is fine. Set it as a primary conversion for bidding once the tag is live.
- [ ] Copy the Conversion ID and label (`AW-xxxxxxxxxx/xxxxx`). Send that string back so it can be pasted into `GOOGLE_ADS_CONVERSION_ID` in `assets/js/site.js`, then deployed. Until that ships, Google Ads will not record form conversions automatically; rely on FormSubmit email + GoatCounter `form-tenant`.

### D. Build the campaign (paused)

- [ ] Campaign settings from section 4 (Search only, $7.14/day, 21-day end date, locations, Presence, English, Maximize Clicks with $4 CPC cap).
- [ ] Create ad groups A and B. Paste phrase + exact keywords. Paste the campaign negative list.
- [ ] Create the three RSAs. Add sitelinks and callouts. Paste the UTM final URL.
- [ ] Set the campaign to **Paused**. Double-check daily budget, end date, and that Display / Search partners are off.

### E. After the landing PR is live, then turn it on

- [ ] Confirm `https://devindesaulniers.ca/rental-before-you-arrive.html#intake` shows the short form, Axford Real Estate, and the $1,500 + GST disclosure.
- [ ] Submit a clearly labelled test form if Devin is comfortable (FormSubmit may need a one-time confirmation on a new form source).
- [ ] Enable the campaign. Note the start date in the tracker.
- [ ] Follow the Day 3 / 7 / 14 / 21 checks. Pause on day 21.

---

## 10. What this trial will not do

- It will not run Meta / Facebook / Instagram ads (Muse).
- It will not advertise buyer searches, general “realtor near me,” or listings.
- It will not spend more than $150 unless Devin later raises the budget himself.
- It does not guarantee five leads or a paid client.

---

## 11. Related files

- Landing previews (desktop 1280 and mobile 390) are saved outside the repo at `/workspace/ads-previews/` for review, and are also linked from the Page that accompanies this plan.
- Metrics sheet: `docs/weekly-ad-metrics-template.csv`
