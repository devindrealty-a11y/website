# Meta campaigns (phase 1)

Parent: [README](README.md). Audiences: [targeting.md](targeting.md). Daily dollars: [budget-and-roi.md](budget-and-roi.md).

Build both campaigns **paused** before November 1. Switch the tenant campaign on November 1. Switch the buyer campaign on November 22. Currency CAD. Facebook Page: [Devin Desaulniers Realtor](https://www.facebook.com/DevinDesaulniersRealtor/). Instagram account: [@devindesaulniers](https://www.instagram.com/devindesaulniers/).

## Account settings

- Business country Canada. Time zone Pacific.
- Special ad category on **each** campaign: **Housing**.
- Objective, until a pixel exists and has recorded real form submits: **Traffic**, optimized for **Landing page views**. A Leads or Sales objective with no event will optimize on an empty signal. Switching to website leads is a step in [tracking.md](tracking.md), after the pixel work is actually shipped and a test submit shows up in Events Manager.
- Budget: campaign budget, Advantage campaign budget off (one ad set per campaign, so the campaign budget and the ad set budget are the same). Daily budgets, not lifetime, so a Monday pause takes effect the same day.
- Account spending limit: **$500** for November. That is above the ~$400 plan and under the $1,000 cash ceiling. Lower it if invoices are about to cross the ceiling. See the GST note in the budget doc.
- Attribution setting: leave the default. Do not judge 2:1 from Meta's reported ROAS. The lead log is the source of truth.

## Campaign 1 — tenant relocation

| Field | Value |
| --- | --- |
| Campaign name | `2026-11 \| Meta \| Housing \| Tenant relocate` |
| Ad set name | `Origin cities \| EN \| relocating guide` |
| Daily budget | $10 from November 1 through November 30 (about $300) |
| Schedule | November 1, 2026, 06:00 Pacific, ongoing. No end date inside the campaign. The Monday review is the off switch. |
| Optimization | Landing page views |
| Bid | Highest volume. No cost cap inside Meta. The $80 intake cap is applied by a human at the Monday review, because a platform cost cap on landing-page views would throttle delivery of a $10 day. |
| Placements | Facebook and Instagram feeds, Stories, Reels. Audience Network off if available. |
| Creative enhancements | Off |

Four ads in this one ad set. Meta will weight them. Do not also split the $10 across two ad sets on day one.

| Ad name | `utm_content` | Final URL |
| --- | --- | --- |
| `T1 fee` | `t1` | `https://devindesaulniers.ca/relocating-to-greater-vancouver.html?utm_source=meta&utm_medium=paid-social&utm_campaign=tenant-relocate&utm_content=t1` |
| `T2 see it first` | `t2` | same URL with `utm_content=t2` |
| `T3 local` | `t3` | same URL with `utm_content=t3` |
| `T4 window` | `t4` | `https://devindesaulniers.ca/rentals.html?utm_source=meta&utm_medium=paid-social&utm_campaign=tenant-relocate&utm_content=t4` |

T4 is the rentals-search variant. It stays in the ad set from November 1 so the auction can try it, pointed at `rentals.html`. If by Monday, November 16 it has spent about $40 or more and produced no `New rental inquiry` and no intake that the person says came from the rentals page, pause T4 and leave T1–T3 running. Do not give T4 its own ad set unless the November 16 review shows it earning intakes under the $80 cap. Details of why this page is a test, not the main destination, are in [landing-pages.md](landing-pages.md).

Call to action on every tenant ad: **Learn more**.

Identity line on every ad, already worked into the primary text: Devin Desaulniers, Real Estate Associate, Axford Real Estate.

### T1 — fee up front

Above the fold (first 125 characters): "Moving to Greater Vancouver and need the rental lined up first?"

Primary text:

```
Moving to Greater Vancouver and need the rental lined up first?

I'm Devin Desaulniers, Real Estate Associate with Axford Real Estate in Port Moody. I work for you, the tenant: a consultation, a search in the areas we agree on, showings in person or on live video, and a lease review before you sign.

The fee is $1,500 + GST, paid by the tenant in two parts: $750 at the start (non-refundable) and $750 once you secure the rental.
```

| Field | Text | Characters |
| --- | --- | --- |
| Headline | Line up your rental first | 25 |
| Description | $1,500 + GST, paid in two parts | 31 |

### T2 — see the place before you pay

Above the fold: "Searching Vancouver rentals from another province?"

Primary text:

```
Searching Vancouver rentals from another province? I live here. I attend the showing, or I walk you through on a live video with floor plans, and we go through the lease before you sign.

I'm Devin Desaulniers, Real Estate Associate with Axford Real Estate in Port Moody. Tenant-side help for a move to Greater Vancouver. Fee $1,500 + GST, in two parts.
```

| Field | Text | Characters |
| --- | --- | --- |
| Headline | See the rental before you pay | 29 |
| Description | Live video walkthroughs | 23 |

### T3 — local, Tri-Cities depth without pretending the search stops there

Above the fold: "I've lived in Greater Vancouver for 28 years."

Primary text:

```
I've lived in Greater Vancouver for 28 years, and I work in Port Moody. If you're moving here, tell me where you'll work or study and I'll help you compare areas, including the Tri-Cities, Burnaby, and New Westminster.

Then I search and show rentals on your side of the lease. Devin Desaulniers, Real Estate Associate, Axford Real Estate. Fee $1,500 + GST, paid in two parts.
```

| Field | Text | Characters |
| --- | --- | --- |
| Headline | A local on your side of the lease | 33 |
| Description | Port Moody · Axford Real Estate | 31 |

The "28 years" line is the same claim as the relocation guide. Keep it only while that sentence remains on the site.

### T4 — browse rentals, for the rentals.html URL only

Above the fold: "Active rentals across Greater Vancouver and the Fraser Valley."

Primary text:

```
Active rentals across Greater Vancouver and the Fraser Valley, with rent shown per month. Search by city, budget, and bedrooms.

Moving from out of province and want someone on the tenant side? I'm Devin Desaulniers, Real Estate Associate with Axford Real Estate. Representation is $1,500 + GST, paid in two parts. The guide on my site explains how that works.
```

| Field | Text | Characters |
| --- | --- | --- |
| Headline | Homes for rent, listed now | 26 |
| Description | Greater Vancouver and Fraser Valley | 35 |

T4 does not promise that every home in the search is available through the paid service. The page is a DDF search of other brokerages' listings, plus a way to ask Devin about one of them.

## Campaign 2 — buyers

| Field | Value |
| --- | --- |
| Campaign name | `2026-11 \| Meta \| Housing \| Buyers Tri-Cities` |
| Ad set name | `Metro Van cities \| EN \| buyers page` |
| Daily budget | $3 from November 22 through November 30 (about $27). December continues at $3 only if the phase 2 gate opens and buyer emails are not all "just exploring". |
| Schedule | November 22, 2026, 06:00 Pacific. |
| Optimization, bid, placements | Same as the tenant campaign. |
| Page | Same Facebook page and Instagram account. |

This daily budget will not exit Meta's learning phase. It is a message test on `buyers.html`, not a scale campaign. Read it from the lead log, not from a cost-per-result goal inside Ads Manager.

Call to action: **Learn more**. (The button "Sign up" over-promises. The form is a request for listings.)

| Ad name | `utm_content` | Final URL |
| --- | --- | --- |
| `B1 tri-cities` | `b1` | `https://devindesaulniers.ca/buyers.html?utm_source=meta&utm_medium=paid-social&utm_campaign=buyer-tricities&utm_content=b1#listings` |
| `B2 first home` | `b2` | same pattern, `utm_content=b2`, hash `#listings` last |
| `B3 from away` | `b3` | same pattern, `utm_content=b3` |
| `B4 send listings` | `b4` | same pattern, `utm_content=b4` |

The hash must stay at the end of the URL so the browser opens the form. Put the UTMs in the query string, not after the hash.

### B1 — Tri-Cities buyer

Above the fold: "Buying in Coquitlam, Port Coquitlam, or Port Moody?"

Primary text:

```
Buying in Coquitlam, Port Coquitlam, or Port Moody? I'll learn your budget and must-haves, set up listing alerts, go to showings with you, and walk through comparable sales before you write.

Devin Desaulniers, Real Estate Associate, Axford Real Estate, Port Moody.
```

| Field | Text | Characters |
| --- | --- | --- |
| Headline | Buying in the Tri-Cities, BC | 28 |
| Description | Showings, comps, and the offer | 30 |

### B2 — first home, plain steps

Above the fold: "Buying a first home is a lot of tabs and not enough sequence."

Primary text:

```
Buying a first home is a lot of tabs and not enough sequence. I keep the steps in order: budget, neighbourhoods, showings, offer, subjects, keys.

I'm based in Port Moody with Axford Real Estate, and I work with buyers across the Tri-Cities and Greater Vancouver. Devin Desaulniers, Real Estate Associate.
```

| Field | Text | Characters |
| --- | --- | --- |
| Headline | A clear plan for a first home | 29 |
| Description | Tri-Cities and Greater Vancouver | 32 |

Avoid "perfect for young families" or any line about who should live in a home. Housing ads and the page both stay with the work, not with family status.

### B3 — already here, bought from a distance

Above the fold: "Moved to Greater Vancouver and ready to buy?"

Primary text:

```
Moved to Greater Vancouver and ready to buy, or still comparing a few areas? I can shortlist around your commute, send notes from showings, and shape an offer timeline that fits the move.

Devin Desaulniers, Real Estate Associate, Axford Real Estate, Port Moody. Start with the listings form and your price range.
```

| Field | Text | Characters |
| --- | --- | --- |
| Headline | Buying after a move to Vancouver | 32 |
| Description | Tell me your timeline and budget | 32 |

### B4 — matches the button on the page

Above the fold: "Tell me the areas, the price range, and the timeline."

Primary text:

```
Tell me the areas, the price range, and the timeline. I'll send listings that match. There's a free mortgage calculator on the page if you want a feel for the payment before you talk to a lender.

Devin Desaulniers, Real Estate Associate, Axford Real Estate. The calculator is an estimate, not a pre-approval.
```

| Field | Text | Characters |
| --- | --- | --- |
| Headline | Send me the listings you want | 29 |
| Description | Coquitlam, PoCo, and Port Moody | 31 |

The calculator line has to stay tied to "estimate, not a pre-approval", because that is what the site's disclaimer says. The calculator itself is on a different host (`devindrealty-a11y.github.io/mortgage-calculator`). The ad still lands on `buyers.html`, which links out to it. Do not send ad traffic straight to the calculator. That page does not capture a lead.

## Files to attach

Use the specs in [creative-briefs.md](creative-briefs.md).

- T1, T2, T3: the existing 16:9 relocation video, plus the 4:5 fee card once it is exported. If the card is not ready on November 1, launch video-only and add the card the day it is exported.
- T4: the 4:5 "search rentals" card. No DDF photos.
- B1–B4: the 4:5 Tri-Cities buyer card, and the headshot card. Same images may run on more than one buyer ad. The primary text is what differs. Meta needs a distinct image or video per ad if the texts are the only change it will accept; in that case crop the same card with the headline of that variant baked in, as the brief describes.

## Before the switch is flipped

- Each final URL opens on a phone, query string intact, and the `#listings` bookmark lands on the form.
- Primary text includes the name and "Axford Real Estate".
- Tenant ads that mention the fee use **$1,500 + GST** and the two $750 parts, matching the site.
- No ad says a rental or a purchase is guaranteed, "easy", or available at a specific monthly rent or sale price.
- Housing category is on. Age and gender are untouched.
- Advantage creative enhancements are off.
- The lead log has today's date and a blank row ready.
