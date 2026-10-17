# Landing pages

Three live pages. The ads use the production domain `https://devindesaulniers.ca/`. Do not send traffic to a `github.io` URL, to `relocatingtovancouver.ca` (that domain is not in use), or to a preview query (`?preview=1` shows sample listings).

No page changes in this package. Where a page is a weak fit for an ad, the fix is which URL the ad uses, not an edit.

## Which ad goes where

| Ads | Final URL | What the person can do on that page |
| --- | --- | --- |
| Meta R1–R4, Google relocation ad | [relocating-to-greater-vancouver.html](https://devindesaulniers.ca/relocating-to-greater-vancouver.html) | Read the move guide. Hero button goes to the rental intake. A later section links buyers to the listings form. |
| Meta B1–B4 | [buyers.html](https://devindesaulniers.ca/buyers.html) | Buyer services, Tri-Cities guides, and the “Send me listings” form (`#listings`). |
| Google rental-search ad | [rentals.html](https://devindesaulniers.ca/rentals.html) | Search active homes for rent. Open a home and send “Ask Devin about this rental”. |

The $1,500 intake is **not** on `rentals.html`. It is on `tenants.html` (`#intake`, form key `tenantIntake`). The relocating guide already links there twice (“Need a rental? Start here” and “Start your rental search”). Renter ads land on the guide so the fee and the “how it works” story are on the same URL as the click. The form is one more click, on a page that states the fee in the hero.

`rentals.html` is the right page for “Coquitlam rentals” because that query is about the list, and the page is the list. Those ads do not mention the $1,500 fee.

## Full URLs to paste

Meta sometimes drops the `#listings` fragment. Buyers still land on `buyers.html`, and the hero button says “Send me listings”. The fragment is included anyway.

### Relocating renters (Meta)

```
https://devindesaulniers.ca/relocating-to-greater-vancouver.html?utm_source=meta&utm_medium=paid&utm_campaign=relocating-renters&utm_content=r1
```

Swap `r1` for `r2`, `r3`, or `r4`. The video ad uses `r1-video`.

### Relocating buyers (Meta)

```
https://devindesaulniers.ca/buyers.html?utm_source=meta&utm_medium=paid&utm_campaign=relocating-buyers&utm_content=b1#listings
```

Swap `b1` for `b2`, `b3`, or `b4`.

### Google — rental searches

Campaign final URL suffix (applies to every keyword in that ad group):

```
utm_source=google&utm_medium=paid&utm_campaign=search-rentals&utm_content=rsa
```

Final URL:

```
https://devindesaulniers.ca/rentals.html
```

### Google — relocation realtor

Final URL suffix:

```
utm_source=google&utm_medium=paid&utm_campaign=search-relocation&utm_content=rsa
```

Final URL:

```
https://devindesaulniers.ca/relocating-to-greater-vancouver.html
```

Turn on auto-tagging as well. UTMs are there so a person can read the source in the browser even before GA4 exists. The forms do not currently store the UTM. [tracking-plan.md](tracking-plan.md) covers that gap. Until then, Devin asks every new lead what brought them in and writes Meta, Google, or other on the Monday sheet.

## What each page already contains

### relocating-to-greater-vancouver.html

- Hero: “Relocating to Greater Vancouver?” and a button to `tenants.html#intake`
- Areas, commute, and B.C. renting basics (deposits, rent increase, condition inspection)
- The tenant offer: **$1,500 total + GST**, the two amounts, search, showings, lease review
- A buyer section that points at `buyers.html#listings` and the mortgage calculator
- Phone 604-809-1032 and devin@axfordrealestate.ca
- **No form on this page.** A conversion is either a later submit on `tenants.html` or on `buyers.html`, or a call.

The fee is in the section “How I help relocating tenants”, below the hero. Ads that quote $1,500 are still pointing at a page that states that fee. The hero itself leads with the rental button, not the price. That is acceptable for this test because the fee is on the same URL. A later page edit could repeat the price in the hero. This package does not make that edit.

The guide’s hero is rental-first. Buyer ads therefore use `buyers.html`, not this guide. The Google relocation ad may attract both, which matches the page (it covers both).

### buyers.html

- Hero: buying in the Tri-Cities and Greater Vancouver, button “Send me listings”
- How Devin helps buyers, neighbourhood notes, video tours
- Form `#listings`, key `buyerListings`, subject line **New buyer listings request**
- Fields include name, email, phone, property type, areas, price range, beds, baths, timeline, pre-approval, notes, and a consent checkbox
- The mortgage calculator link is labelled as an estimate on the site. Ads do not mention it, so nobody expects a payment quote.

### rentals.html

- Search of active residential rentals in Greater Vancouver and the Fraser Valley. Rent is per month.
- Opening a home shows “Ask Devin about this rental”, form key `rentalInquiry`, subject **New rental inquiry**
- The inquiry is emailed to Devin. It is not sent to the listing brokerage. The page says so.
- The city box does **not** read a city from the URL. A click from a “Coquitlam rentals” ad opens the full regional list. The person types Coquitlam. Do not add `?q=` and expect it to filter; the script only uses `id` and `preview`. Leaving the page as it is means the first screen is a search box with the placeholder “Vancouver, Surrey, Coquitlam…”, which is enough for a $40–$60 test. Pre-filling the city would be a later code change.

Footer and nav on all three pages include the phone, the brokerage address, and a link to the tenant service.

## UTM names (keep these stable)

| Parameter | Values |
| --- | --- |
| utm_source | `meta` or `google` |
| utm_medium | `paid` |
| utm_campaign | `relocating-renters`, `relocating-buyers`, `search-rentals`, `search-relocation` |
| utm_content | `r1` `r2` `r3` `r4` `r1-video` `b1` `b2` `b3` `b4` `rsa` |

Do not invent a second spelling (`fb` vs `meta`) or the Monday sheet will split one campaign in two once tracking exists.

## Click path Devin should try before spending

On a phone, signed out of any admin session:

1. Open the R1 URL. The guide loads on `devindesaulniers.ca` with a valid certificate. Tap “Need a rental? Start here”. The intake form is on screen. Do not submit a test unless he is ready for FormSubmit’s activation email (see the checklist).
2. Open the B1 URL. “Send me listings” is visible without hunting.
3. Open the rentals URL. The search box is usable, a real listing opens, and “Ask Devin about this rental” is on that listing. If the feed fails to load, do not launch the Google rental ad group until it loads.

## Forms this test cares about

From `assets/js/config.js`. All of them post to FormSubmit and email devin@axfordrealestate.ca.

| Key | Page | Subject |
| --- | --- | --- |
| `tenantIntake` | `tenants.html` | New relocation rental intake |
| `buyerListings` | `buyers.html` | New buyer listings request |
| `rentalInquiry` | `rentals.html` | New rental inquiry |

Home evaluation, expert opinion, and sale-listing inquiries can still arrive. They are not the goal of this test. If someone mentions an ad, log them as extra on the Monday sheet and leave the budgets where they are.
