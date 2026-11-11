# Google Search (phase 2)

Parent: [README](README.md). This campaign stays **paused** through November. Build it in the last week of November so December 7 is a switch, not a setup day. Turn it on only when the [phase 2 gate](budget-and-roi.md#phase-2-gate) is a yes in the November 30 log.

Search is the smaller test. It does not replace the Meta campaigns in the first month they run together.

## Account settings

- Currency CAD. Time zone Pacific.
- A **Search** campaign. Display network off. Search partners off for the first 14 days.
- Location option: **Presence: people in or regularly in your targeted locations.**
- Language: English.
- Bidding: **Maximize clicks** with a maximum CPC of **$2.50** on the tenant campaign and **$3.50** on the buyer campaign. There are no site conversions to feed Maximize conversions until the tracking change in [tracking.md](tracking.md) is live. Do not turn on smart bidding against a pixel that does not exist.
- Budget: daily, amounts in [budget-and-roi.md](budget-and-roi.md). Account budget for Google in December: **$200**, which is above the planned ~$155 and still leaves the combined Meta + Google month inside $500.
- Final URL suffix (tenant campaign):

```
utm_source=google&utm_medium=cpc&utm_campaign=tenant-relocate&utm_term={keyword}&utm_content={creative}
```

- Buyer ads: leave the suffix **empty** and put UTMs in the final URL itself, with `#listings` at the very end. A suffix appended by Google can land after the hash and never reach Analytics or the future hidden fields.

Networks and inventory that stay off: Display, Demand Gen, Performance Max, YouTube in-stream, and any remarketing list. Housing ads plus a dollar-a-day budget do not need them, and Performance Max will spend outside the keywords below.

## Campaign G-T — tenant relocation

| Field | Value |
| --- | --- |
| Name | `2026-12 \| Google \| Search \| Tenant relocate` |
| Daily budget | $4 (about $124 in a 31-day December, less if it starts December 7: about $100) |
| Locations | Calgary, Edmonton, Toronto, Ottawa, Winnipeg, Montreal, Halifax |
| Ad group | `Relocate rental` |
| Final URL | `https://devindesaulniers.ca/relocating-to-greater-vancouver.html` |
| Start | December 7, 2026, if the gate is open. Otherwise leave paused and write the reason in the log. |

### Keywords

Phrase and exact only. No broad match.

| Keyword | Match |
| --- | --- |
| moving to vancouver rental | Exact, phrase |
| relocating to vancouver rental | Exact, phrase |
| moving to greater vancouver rental | Exact, phrase |
| tenant agent vancouver | Exact, phrase |
| realtor to find a rental vancouver | Exact, phrase |
| help finding a rental in vancouver | Phrase |
| moving to coquitlam rental | Exact, phrase |
| moving to port moody rental | Exact, phrase |
| moving to port coquitlam rental | Exact, phrase |
| moving to burnaby rental | Phrase |
| relocating to vancouver from calgary | Phrase |
| relocating to vancouver from toronto | Phrase |
| relocating to vancouver from edmonton | Phrase |
| corporate relocation vancouver rental | Phrase |

### Negatives (campaign level)

`movers, moving company, moving companies, uhaul, u-haul, "u haul", pods, "moving truck", job, jobs, hiring, salary, career, careers, course, courses, exam, school, roommate, room, sublet, airbnb, "short term", hotel, motel, "property management", "property manager", landlord, "for rent by owner", cheap, free, "section 8", shelter`

Add search terms from the first Monday after launch. Anything that is a moving company, a job, or a one-night stay gets negated that morning.

### Responsive search ad

Path fields: `relocating` / `rentals` (the path is cosmetic; the final URL is still the relocation guide).

Headlines (each 30 characters or fewer):

| Headline | Chars |
| --- | --- |
| Moving to Vancouver? | 20 |
| Line up a rental first | 22 |
| Tenant-side rental help | 23 |
| See it before you pay | 21 |
| Live video walkthroughs | 23 |
| $1,500 + GST, two parts | 23 |
| Devin Desaulniers | 17 |
| Axford Real Estate | 18 |
| Start 4-6 weeks before | 22 |
| Lease review included | 21 |
| Help before you arrive | 22 |
| Port Moody based | 16 |
| Out-of-province moves | 21 |
| A local on your side | 20 |
| Greater Vancouver rentals | 25 |

Pin headline "Devin Desaulniers" to position 2 or leave unpinned if Google rejects a pin. Pin "$1,500 + GST, two parts" nowhere. Let it rotate. Do not pin three headlines or the ad stops testing.

Descriptions (each 90 characters or fewer):

| Description | Chars |
| --- | --- |
| I search, show, and review the lease before you move to Greater Vancouver. | 74 |
| Fee is $1,500 + GST: $750 to start, $750 when the rental is secured. | 68 |
| Consultation, search, showings in person or on video, and lease review. | 71 |
| Devin Desaulniers, Real Estate Associate at Axford Real Estate. | 63 |

## Campaign G-B — buyers

| Field | Value |
| --- | --- |
| Name | `2026-12 \| Google \| Search \| Buyers Tri-Cities` |
| Daily budget | $1.50 (about $37 from December 7 through December 31) |
| Locations | Metro Vancouver (presence only) |
| Ad group | `Buyer agent Tri-Cities` |
| Start | Same day as G-T, same gate. If buyer Meta emails in late November are all "12+ months / just exploring", leave G-B paused even if G-T starts. |

Final URLs, one per ad if you duplicate the RSA, otherwise this single URL:

```
https://devindesaulniers.ca/buyers.html?utm_source=google&utm_medium=cpc&utm_campaign=buyer-tricities&utm_content=rsa1#listings
```

### Keywords

| Keyword | Match |
| --- | --- |
| coquitlam realtor | Exact, phrase |
| port moody realtor | Exact, phrase |
| port coquitlam realtor | Exact, phrase |
| tri-cities realtor | Exact, phrase |
| tri cities realtor bc | Exact, phrase |
| buyers agent coquitlam | Exact, phrase |
| buyer's agent port moody | Exact, phrase |
| first time home buyer coquitlam | Phrase |
| realtor port moody bc | Exact |

Skipped on purpose at this budget: `homes for sale`, `coquitlam homes`, `mls`, and brokerage-only names. They are real queries and they are too broad for $1.50 a day.

### Negatives (campaign level)

`rent, rental, rentals, lease, leasing, apartment, roommate, job, jobs, salary, hiring, course, exam, school, "how to become", review, reviews, complaint, complaints, recruiting`

"Apartment" is a negative here so the buyer campaign does not pay for rental queries. The tenant campaign carries rental language.

### Responsive search ad

Path: `buyers` / `tri-cities`

Headlines:

| Headline | Chars |
| --- | --- |
| Buying in the Tri-Cities | 24 |
| Coquitlam, PoCo, Moody | 22 |
| Buyer representation | 20 |
| Listings that fit you | 21 |
| First home, clear steps | 23 |
| Showings with a local | 21 |
| Devin Desaulniers | 17 |
| Axford Real Estate | 18 |
| Free mortgage calculator | 24 |
| From offer through keys | 23 |
| Port Moody based | 16 |
| Tell me your timeline | 21 |
| Greater Vancouver buyers | 24 |
| Comparable sales, explained | 27 |
| Local buyer representation | 26 |

Descriptions:

| Description | Chars |
| --- | --- |
| Neighbourhood guides, listing alerts, showings, and offers in the Tri-Cities. | 77 |
| Tell me your areas, budget, and timeline. I'll send listings that match. | 72 |
| Devin Desaulniers, Real Estate Associate at Axford Real Estate. | 63 |
| The mortgage calculator is free, and it is an estimate, not a pre-approval. | 75 |

## What to do with the search terms report

Every Monday that a Google campaign is live, export the search terms for the past 7 days.

- A query that matches the offer and produced a click under the max CPC: leave it.
- A moving company, a job, a roommate, or another city: add it as a negative that morning.
- A query with 30 or more impressions and zero clicks after two weeks: pause that keyword. The ad is not answering it.
- Do not add new keywords in the first two weeks unless a search term is clearly the same service and has already earned a click.

## How this stays the smaller test

December's planned Google total is about **$4 tenant + $1.50 buyer per day**, against Meta at about **$8 tenant + $3 buyer**. If Google's cost per tenant intake is lower than Meta's for two Mondays in a row, move **$2 a day** from Meta tenant to Google tenant. Write the move in the log. Do not invert the whole account on one week, and do not cross the monthly cash ceiling.
