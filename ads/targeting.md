# Targeting

Two Meta campaigns and one Google Search campaign. All of them use the landing URLs in [landing-pages.md](landing-pages.md) and the words in [copy.md](copy.md).

Housing ads cannot be narrowed the way a normal Meta campaign can. Set the category first, then use only the controls that are still available. The copy does the qualifying: “moving to Greater Vancouver”, the $1,500 fee, and tenant-side versus buying.

## Meta — both campaigns

Create both campaigns in the same ad account, currency **CAD**, tied to the Facebook page [Devin Desaulniers Realtor](https://www.facebook.com/DevinDesaulniersRealtor/) and Instagram [@devindesaulniers](https://www.instagram.com/devindesaulniers/). If Axford requires ads to run from the brokerage’s Business Manager, use that account and still use Devin’s page as the identity people see.

### Campaign settings (same for renters and buyers)

| Setting | Value |
| --- | --- |
| Special ad category | **Housing** |
| Objective, until a pixel exists | **Traffic** |
| Optimization | Landing page views |
| Attribution | 7-day click. Turn view-through off if the control is there. |
| Budget | Daily, plus the November spending limit in [budget-and-return.md](budget-and-return.md) |
| Schedule | 1–30 November 2026, then extend only after a Monday check |
| Placements | Facebook Feed, Instagram Feed, Instagram Stories, Instagram Reels, Facebook Stories |
| Brand safety | Exclude Audience Network if the placement list allows it |

A Housing campaign will lock age at 18–65+ and gender at all. Leave those locks. Postal-code targeting, lookalike audiences, and customer-list audiences should be unavailable; do not look for a way around that.

Detailed targeting (interests, job titles, “recently moved”, life events) is often removed or heavily limited once Housing is selected. If those boxes are gone, do not add interests. If a few neutral interests are still offered, leave them empty anyway. “People who like moving” and “expats” are a poor substitute for a real intent signal, and some of them drift into segments a housing ad should not use.

**Do not upload** a client list, a pixel custom audience, or a lookalike. The pixel is not on the site yet, and Housing ads restrict those audiences even after it is.

### Locations — people who live in these cities

The people who need this service are not already in Greater Vancouver. Target **people living in** these cities:

- Calgary, Alberta
- Edmonton, Alberta
- Toronto, Ontario
- Ottawa, Ontario
- Winnipeg, Manitoba
- Montreal, Quebec

If Ads Manager offers the census metropolitan area for a city, choose the metro area so the suburbs are included (Mississauga with Toronto, Gatineau’s Ontario side with Ottawa, and so on). If it only offers a pin and a radius, the radius has to be **at least 25 km** (Meta’s housing minimum is 15 miles). Do not draw a tight ring around a downtown.

One ad set per campaign, with all six cities in that ad set. A $6/day renter budget split into six ad sets will not learn anything.

Montreal will see English ads. If the week-2 placement or region report shows Montreal taking a large share of spend with almost no landing-page views, remove Montreal and leave the other five.

**Leave these places out of the location list** (do not add them and then exclude them): Vancouver, Burnaby, Richmond, Surrey, Coquitlam, Port Coquitlam, Port Moody, New Westminster, North Vancouver, West Vancouver, Delta, Langley, Maple Ridge, Pitt Meadows, White Rock, Anmore, and Belcarra. People already there are a different campaign, and this budget cannot buy the local realtor auction.

Also leave out the US, the UK, Australia, and other countries for this test. The newcomer page on the site can support a later international test after a Canadian retainer has been invoiced.

Language: **English**.

### Renter campaign

| | |
| --- | --- |
| Campaign name | `META \| Housing \| Relocating renters \| 2026-11` |
| Ad set name | `Origin cities \| English \| Nov 2026` |
| Daily / limit | $6 / $180 in November |
| Ads | R1, R2, R3, R4 from [copy.md](copy.md), each with its own UTM |
| Final URL | Relocating guide |

### Buyer campaign

| | |
| --- | --- |
| Campaign name | `META \| Housing \| Relocating buyers \| 2026-11` |
| Ad set name | `Origin cities \| English \| Nov 2026` |
| Daily / limit | $2 / $60 in November |
| Ads | B1, B2, B3, B4 |
| Final URL | Buyers page |

Same cities as the renter campaign. The difference is the copy and the URL, not the map.

### After a pixel exists

[tracking-plan.md](tracking-plan.md) is a later change to the site. When that change is live and the events are firing on real form submits:

- Duplicate nothing. Edit these campaigns.
- Switch the renter campaign’s optimization event to the tenant-intake lead.
- Switch the buyer campaign’s optimization event to the buyer-listings lead.
- Keep the Housing category.
- Expect the delivery status to say “learning limited”. At this budget that label is normal. Judge the Monday sheet, not the learning badge.

Until then, optimize for landing page views. Ads Manager’s “results” are clicks, not clients.

## Google Search

One campaign, two ad groups, shared budget. Search only. No Display, no YouTube, no Performance Max, no remarketing. Those networks either need more budget or a conversion tag this site does not have yet, and housing rules restrict personalized audiences.

| Setting | Value |
| --- | --- |
| Campaign name | `GOOG \| Search \| Relocation and rentals \| 2026-11` |
| Type | Search |
| Networks | Google Search only. Uncheck Search Partners if that box is separate and the first week shows weak clicks from partners. |
| Locations | Canada |
| Location option | Presence: people in or regularly in the targeted locations |
| Language | English |
| Bidding | Maximize clicks, with a **maximum CPC of $4** |
| Daily budget | $2 |
| Campaign total / spending limit for November | $60 |
| Start / end | 1–30 November 2026 |
| Final URL suffix | The UTMs in [landing-pages.md](landing-pages.md). Turn on auto-tagging as well, so a later GA4 link can use the `gclid`. |
| Call asset | 604-809-1032, counted as a click, not as a conversion |
| Sitelinks | Optional, after the two ads are approved. Text in [copy.md](copy.md). |

The $4 CPC cap keeps one click from spending the day. If Google will not save the campaign without a higher cap, use $6 and watch the search-terms report on 9 November.

### Ad group A — local rental searches

Name: `Rentals \| Tri-Cities`

Final URL: `https://devindesaulniers.ca/rentals.html` plus the rental-search UTMs.

Phrase match and exact match only. No broad match.

| Phrase | Exact |
| --- | --- |
| "coquitlam rentals" | [coquitlam rentals] |
| "coquitlam houses for rent" | [coquitlam houses for rent] |
| "coquitlam apartments for rent" | [coquitlam apartments for rent] |
| "homes for rent coquitlam" | [homes for rent coquitlam] |
| "port coquitlam rentals" | [port coquitlam rentals] |
| "port moody rentals" | [port moody rentals] |
| "tri cities rentals" | [tri cities rentals] |
| "tricities rentals" | [tricities rentals] |

One responsive search ad, using the rental headlines and the four descriptions in [copy.md](copy.md). Four separate ads would starve a $2/day campaign.

### Ad group B — relocation realtor

Name: `Relocation realtor`

Final URL: `https://devindesaulniers.ca/relocating-to-greater-vancouver.html` plus the relocation UTMs.

| Phrase | Exact |
| --- | --- |
| "relocation realtor vancouver" | [relocation realtor vancouver] |
| "relocation agent vancouver" | [relocation agent vancouver] |
| "moving to vancouver realtor" | [moving to vancouver realtor] |
| "realtor for relocating to vancouver" | [realtor for relocating to vancouver] |
| "tenant agent vancouver" | [tenant agent vancouver] |
| "rental agent for tenants vancouver" | [rental agent for tenants vancouver] |

Ads: one responsive search ad from the relocation headlines in [copy.md](copy.md).

### Negatives (campaign level)

Add these as phrase negatives before the first click:

```
jobs
job
salary
hiring
career
property management
airbnb
short term
short-term
sublet
room for rent
roommate
roommates
basement wanted
free
cheap
scam
login
mls login
course
exam
license
licence
template
"for rent by owner wanted"
storage
commercial
office
warehouse
```

Also negative-match the other service inside each ad group, so the budgets do not steal from each other:

- On the rentals ad group, phrase-negative: `realtor`, `agent`, `relocation`, `relocating`, `buy`, `buying`, `homes for sale`
- On the relocation ad group, phrase-negative: `apartments for rent`, `houses for rent`, `for rent`, `rentals`

Check the search-terms report every Monday and add anything that is clearly the wrong job (careers, one-night stays, rooms in a shared house).

### What this Google test will not do

People searching “coquitlam rentals” are often already in the region, or about to be. That is a different person from the Meta origin-city audience. Their conversion is a **rental inquiry** on a listing, or a call. Do not book that inquiry as a $1,500 placement unless the conversation becomes one (they are moving from out of town and they agree to the fee).

“Relocation realtor Vancouver” is the closer match to the paid service. It will get fewer searches. That is why it shares the $2 day with the rental ad group instead of having a budget of its own that Google might refuse.

## Audience summary

| Audience | Where | Who | They land on |
| --- | --- | --- | --- |
| Relocating renters | Meta, 60% of November | People living in the six origin cities | Relocating guide |
| Relocating buyers | Meta, 20% | Same cities | Buyers page |
| Rental searchers | Google ad group A | Anyone in Canada searching those rental queries | Rentals page |
| Relocation searchers | Google ad group B | Anyone in Canada searching those realtor queries | Relocating guide |
