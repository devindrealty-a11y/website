# Targeting

Parent: [README](README.md). Paste-ready campaigns are in [meta-ads.md](meta-ads.md) and [google-search.md](google-search.md).

Both campaigns advertise housing. On Meta they run under the **Housing** special ad category. On Google they run as Search only. Display, Demand Gen, and remarketing stay off. Housing-ad rules in both platforms limit who can be selected. The form and the first line of copy do the rest of the qualifying.

Confirm the switches in Ads Manager on build day. Meta's housing rules are updated often. The constraints below match Meta's special-ad help as described in August 2026: age fixed at 18–65+, all genders, no postal code, no location exclusions, a city or pin expanded by a minimum radius (15 miles / 25 km in the United States and other listed countries; some countries use 10 miles), many detailed-targeting options removed, and Advantage+ lookalikes unavailable. Canada is in the special-ad country set. If Ads Manager shows a different minimum radius for Canada, use the radius it enforces.

## Audience A — relocating tenants

**Who the copy is for.** An adult planning a move to Greater Vancouver from another part of Canada, who will need a long-term rental lined up before they arrive, and who is close enough to a move date (about 4–8 weeks out, sometimes a little earlier for planning) that a paid search is useful. They may be moving for work, school, or family. The intake form already asks where they are moving from, the target move-in date, rent budget, bedrooms, areas, pets, and work or school location.

**Who the copy is not written for.** Someone already housed in Metro Vancouver who wants a cheaper apartment this weekend. A landlord looking for a tenant. A person wanting a roommate, a sublet, or a short stay. Those clicks are expensive relative to a $1,500 file, and `rentals.html` will attract some of them anyway. They are logged as not qualified.

### Meta (November 1)

| Setting | Value |
| --- | --- |
| Special ad category | Housing |
| Locations included | Calgary; Edmonton; Toronto; Ottawa; Winnipeg; Montreal; Halifax. City-level. Let Meta apply the required radius. |
| Locations excluded | None. Housing campaigns do not allow location exclusions. British Columbia is simply not in the include list, which keeps the budget on origin cities. |
| Age and gender | Leave the housing defaults (18–65+, all genders). |
| Language | English. |
| Detailed targeting | None on day one. If Ads Manager still offers a neutral interest such as moving or relocation, add it only as a second ad set after the first $150, and only if the broad ad set is over the $80 intake cap. Do not exclude interests. |
| Lookalikes | Off. Unavailable for this category, and a client-list lookalike would be the wrong first test at this budget. |
| Custom audiences | None for launch. A list of past clients can be revisited later with Axford's privacy sign-off. |

Selecting a city expands past the city centre. Selecting Toronto already pulls in nearby suburbs inside the radius. Do not also add Mississauga, Brampton, North Vancouver, or the rest of each metro. Overlap makes the small budget bid against itself.

Montreal is included with the language set to English, so the ad is aimed at people there who use English in Meta. If Montreal takes spend for a week and sends no intakes, remove that city at the next Monday review.

Victoria, Saskatoon, and Regina are a second wave, not launch. Add one of them only after an origin city has produced an intake under the cap.

**Why this is broad on purpose.** Under housing rules the account cannot target "likely to move", an age band, a household income, or "everyone in Canada except Vancouver". A headline that starts with "Moving to Greater Vancouver" is the filter. The form's "Moving from" and "Target move-in date" fields are the second filter. The Monday log is the third.

### Google Search (phase 2 only)

| Setting | Value |
| --- | --- |
| Campaign type | Search. Display network off. Search partners off for the first two weeks, then on only if search-partner spend is under 10% of the campaign. |
| Locations | The same origin cities: Calgary, Edmonton, Toronto, Ottawa, Winnipeg, Montreal, Halifax. |
| Location option | **Presence: people in or regularly in** your targeted locations. The "presence or interest" option spends on anyone reading about those cities. Leave it off. |
| Language | English. |
| Keywords | Relocation intent only. The list is in [google-search.md](google-search.md). There is no ad group for generic "apartments for rent". |
| Audiences | Observation only, if used at all. No targeting layer that narrows by affinity. Bids stay manual or Maximize Clicks with a ceiling until there are conversions to feed a smart-bidding strategy. |

Search can do something Meta housing campaigns cannot: show the ad to a person in Calgary at the moment they type a Vancouver rental query. That is why a passing November is allowed to fund a small December search test, not a larger one.

## Audience B — Tri-Cities and Greater Vancouver buyers

**Who the copy is for.** A person who wants to buy in Coquitlam, Port Coquitlam, Port Moody, or elsewhere in Greater Vancouver, including first-time buyers and people relocating who already know they want to purchase. The form asks property type, areas, price range, bedrooms, bathrooms, timeline, and whether a mortgage pre-approval is in place.

**Qualified, for the log.** Timeline "as soon as possible", "within 3 months", or "3–6 months", and a price range that is filled in. "6–12 months" is a nurture lead: reply, do not count it as qualified. "12+ months / just exploring" is not qualified.

### Meta (buyer ads start November 22)

| Setting | Value |
| --- | --- |
| Special ad category | Housing |
| Locations included | Port Moody, Coquitlam, Port Coquitlam, Burnaby, New Westminster, Vancouver, Surrey, Pitt Meadows, Maple Ridge. City-level, radius left at Meta's minimum. Anmore and Belcarra fall inside the Port Moody radius if Meta has no city for them. |
| Locations excluded | None. |
| Age, gender, language | Housing defaults. English. |
| Detailed targeting, lookalikes, custom audiences | None at launch. |

These cities plus the required radius cover Greater Vancouver. The ad text names the Tri-Cities so a Surrey renter who is not buying is less likely to click, and the people who do click land on a buyer page. Do not try to draw a polygon around a single neighbourhood. Housing rules will widen it, and the budget is too small for neighbourhood splits.

People relocating from Calgary who intend to **buy** will see the tenant ads, because those ads run in the origin cities. Variant B3 in the buyer campaign speaks to out-of-province buyers, and it runs in the Greater Vancouver location set above (people who have already arrived, or who Meta places in that radius). Origin-city buyer ads are a later test, after tenant intake costs are known. Running a second buyer geo in November would split about $3 a day into nothing readable.

### Google Search (phase 2, smaller than the tenant search campaign)

| Setting | Value |
| --- | --- |
| Locations | Metro Vancouver, with the presence option (people in or regularly in the locations). |
| Keywords | Realtor and buyer-agent queries for Coquitlam, Port Coquitlam, Port Moody, and the Tri-Cities. The list is in [google-search.md](google-search.md). |
| Left out on purpose | Broad "homes for sale" and city-only queries. At roughly a dollar a day they produce clicks from researchers and from people comparing a dozen agents. |

## Placements and inventory

**Meta.** Facebook and Instagram feeds, Stories, and Reels. Turn **Audience Network** off if the housing campaign still shows that toggle. Leave Advantage+ placements on for the Facebook and Instagram surfaces so $10 a day is not hand-split across six placements.

**Meta creative enhancements.** Off. Automatic text changes, image expansion, and music can rewrite the fee or imply a result the page does not promise.

**Google.** Search results only.

## What the platforms will not do in this test

- Age, gender, income, family status, or postal-code targeting.
- A lookalike of past clients.
- "Everyone interested in Vancouver" worldwide.
- Retargeting website visitors. There is no pixel in this launch, and housing remarketing is a poor fit for a first $400.
- A Facebook instant form. The lead stays on the site so the fee and the two-part payment are read before the email is sent.

## How a click becomes a qualified lead

1. The ad's first line matches one audience (moving and renting, or buying in the Tri-Cities).
2. The landing page repeats that promise. Mapping is in [landing-pages.md](landing-pages.md).
3. The form records move date, origin, budget, and areas (tenant) or timeline, areas, and price (buyer).
4. The Monday log marks qualified or not, using the definitions above. Only qualified tenant intakes and collected fees move the budget.
