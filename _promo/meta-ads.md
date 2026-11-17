# Meta ads: Facebook and Instagram

Budget: **$5–$10 a day** (treat this as Canadian dollars, the same currency as the $1,500 fee). Recommended working point inside that band: **$8 a day, $56 a week**.

Account: a Facebook Page and Instagram account for Devin Desaulniers, REALTOR®. The public Facebook page already linked from the site is https://www.facebook.com/DevinDesaulniersRealtor/ and Instagram is https://www.instagram.com/devindesaulniers/. Run the ads from the Page, with the Instagram account connected, so the brokerage relationship is visible on the profile people land on.

All three campaigns are housing ads. In Ads Manager, set the special ad category to **Housing** and the country to **Canada** before you build an audience. Meta has required that category for housing ads reaching Canada since December 3, 2020. If the category is wrong, Meta can pause the campaign. A business admin also has to accept Meta's non-discrimination policy (Ads Manager will block delivery until that is done).

Source for the targeting limits below: Meta's developer document "Special Ad Categories," updated May 21, 2026 (https://developers.facebook.com/documentation/ads-commerce/marketing-api/audiences/special-ad-category). The audience help page is https://www.facebook.com/business/help/2220749868045706.

## What Housing category will not let you target

The people this plan is written for are real: someone moving to Vancouver or B.C. from another province or another country, a newcomer, a student or worker relocating, and a buyer looking at the Tri-Cities, BC. Meta will not let a housing ad select those people directly.

For ads reaching Canada, Housing category locks the audience like this:

- **Age** is fixed at 18–65+. You cannot narrow it to students.
- **Gender** must be all genders.
- **Postal codes, neighbourhoods, and "metro area" targeting** are not available. You cannot target only Port Moody, only Coquitlam, or only a campus.
- **A city, address, or pin** must cover at least a **15 mile / 25 kilometre** radius. Meta rejects a smaller radius.
- **Location exclusions** are not available. You cannot target Canada and then remove people who already live in B.C.
- **Behaviour and demographic targeting** are not available. That removes "recently moved," job title, life events, and anything that stands in for national origin, family status, or income.
- **Interest exclusions** are not available. Interests that remain have to be on Meta's approved list. If the interest box rejects "Vancouver" or "relocation," delete it. Do not hunt for a workaround.
- **Lookalike audiences and saved audiences** are not available.

So the audience is a wide geography, and the ad text does the qualifying. Someone who is not moving will scroll past a first line that says "Moving to Greater Vancouver?"

Do not build an ad set for one nationality, one language community, or "newcomers" as a demographic. People moving from another country are reached in two lawful ways: the copy says so, and they see it once they are in Canada (or they find the organic posts, the blog, and YouTube). Spending this budget on a housing ad aimed at a single country overseas is a poor use of $8 a day and is easy to misread as national-origin targeting. Keep every location inside Canada.

## Campaign setup that fits this budget

Use three campaigns, one ad set each, three ads in each ad set. Do not split a campaign into an ad set per city. At a few dollars a day, seven city ad sets would each starve.

| | Campaign 1 | Campaign 2 | Campaign 3 |
| --- | --- | --- | --- |
| Name | `relocation-rentals` | `relocating` | `tri-cities-buyers` |
| Job | Tenant-paid rental service | Relocation guide | Buyer search in the Tri-Cities, BC |
| Landing page | `tenants.html` | `relocating-to-greater-vancouver.html` | `buyers.html` |
| Objective | Traffic | Traffic | Traffic |
| Optimization | Link clicks | Link clicks | Link clicks |
| Destination | `tenants.html#intake` | the guide | `buyers.html#listings` |

There is no Meta pixel on the site, so Landing Page Views and Leads are not available as optimization events until a pixel is installed. Link clicks are the honest setting on day one. A lead, for the decision rules at the bottom, is a completed intake or listings form in the inbox, or a call or text that mentions the ad. The forms post to email through FormSubmit and do not currently attach the UTM, so the inbox will not label the source for you. Count forms and calls for that week against that week's spend.

Do not use an instant form. The site forms already ask for the rental or buyer details, and the pages explain the fee.

Placements, until a vertical cut exists: **Facebook Feed and Instagram Feed only**. Turn off Reels, Stories, Audience Network, and right-column. The relocation video is 1280×720 (16:9, about 32 seconds) and the blog images are 1200×630. A 9:16 placement crops off the Axford Real Estate footer on the blog cards. Check every preview before you publish. If the brokerage name is cropped out of the image, the primary text still has to show "Axford Real Estate" before "See more."

## Audiences

### Campaigns 1 and 2 — people who may be moving

One ad set per campaign. Location: **people living in** these cities, which is where a lot of moves to B.C. start:

- Calgary
- Edmonton
- Toronto
- Ottawa
- Montréal
- Winnipeg
- Halifax

If Ads Manager will not accept the city on its own, drop a pin on the city centre and set the radius to **25 km**, the Canada minimum. Do not go smaller. Do not exclude B.C., and do not add a second ad set of "people already in Vancouver." Campaign 3 covers people in the region.

Leave age at 18–65+ and gender at all. Leave detailed targeting empty unless an approved interest is still offered and is plainly about the place (for example an interest Meta still lists for Vancouver). The copy speaks to a new job, a study term, and a move from another province or country. That is the student and worker message. It is not a targeting filter.

### Campaign 3 — Tri-Cities, BC buyers

One ad set. Pin **2326 Clarke St, Port Moody, BC**, radius **25 km**. That is the smallest circle Meta allows. It covers Port Moody, Coquitlam, Port Coquitlam, Anmore, Belcarra, Burnaby, New Westminster, and much of Vancouver, and it reaches into Surrey, the North Shore, Pitt Meadows, and Maple Ridge. You cannot buy "Tri-Cities only." The ad text and the landing page do that job: neighbourhoods on `buyers.html` are Coquitlam, Port Coquitlam, Port Moody, and Anmore and Belcarra.

Same age and gender locks. No detailed targeting.

## Weekly budget split

Meta will not learn much at this spend. A learning phase that wants on the order of 50 results a week will not finish on link clicks from $8 a day, and it will never finish if the result is a lead. Judge the test with the stop and scale rules below, not with "learning" status.

Run all three campaigns only at **$8 or $10 a day**. At **$5 a day**, run campaign 1 alone. Splitting $35 a week three ways will not produce a CPC you can trust.

| Daily total | Week | Campaign 1 rentals | Campaign 2 guide | Campaign 3 buyers |
| --- | ---: | ---: | ---: | ---: |
| $5 | $35 | $35 (only campaign on) | off | off |
| $8 | $56 | $28 | $10.50 | $17.50 |
| $10 | $70 | $35 | $14 | $21 |

Daily equivalents at $8: about **$4 / $1.50 / $2.50**. At $10: **$5 / $2 / $3**.

Why rentals get half: the page has a price, a form, and a service a relocating tenant can buy. The guide is the assist. Buyers are the second priority because the Tri-Cities, BC search is the other paid service, and September's sales post gives the ad a real number to talk about. Selling does not have its own campaign. There is no seller form. Someone selling calls or texts 604-809-1032. The Google post in week 8 of the business-profile series is the seller piece.

If you turn a campaign off, move its dollars to campaign 1. Do not bank them.

## UTM links

Use these as the final URL. The `#` anchor stays at the end so the page opens on the form.

**Campaign 1**

- v1: `https://devindesaulniers.ca/tenants.html?utm_source=meta&utm_medium=paid-social&utm_campaign=relocation-rentals&utm_content=c1-v1#intake`
- v2: `https://devindesaulniers.ca/tenants.html?utm_source=meta&utm_medium=paid-social&utm_campaign=relocation-rentals&utm_content=c1-v2#intake`
- v3: `https://devindesaulniers.ca/tenants.html?utm_source=meta&utm_medium=paid-social&utm_campaign=relocation-rentals&utm_content=c1-v3#intake`

**Campaign 2**

- v1: `https://devindesaulniers.ca/relocating-to-greater-vancouver.html?utm_source=meta&utm_medium=paid-social&utm_campaign=relocating&utm_content=c2-v1`
- v2: `https://devindesaulniers.ca/relocating-to-greater-vancouver.html?utm_source=meta&utm_medium=paid-social&utm_campaign=relocating&utm_content=c2-v2`
- v3: `https://devindesaulniers.ca/relocating-to-greater-vancouver.html?utm_source=meta&utm_medium=paid-social&utm_campaign=relocating&utm_content=c2-v3`

**Campaign 3**

- v1: `https://devindesaulniers.ca/buyers.html?utm_source=meta&utm_medium=paid-social&utm_campaign=tri-cities-buyers&utm_content=c3-v1#listings`
- v2: `https://devindesaulniers.ca/buyers.html?utm_source=meta&utm_medium=paid-social&utm_campaign=tri-cities-buyers&utm_content=c3-v2#listings`
- v3: `https://devindesaulniers.ca/buyers.html?utm_source=meta&utm_medium=paid-social&utm_campaign=tri-cities-buyers&utm_content=c3-v3#listings`

## Creative that already exists

Use these files. Do not pull stills from the luxury YouTube tours into the rental campaign. A $8 million condo thumbnail next to a $1,500 tenant service reads as the product. The site is explicit that those tours are not listings.

| Asset | Use |
| --- | --- |
| `assets/video/greater-vancouver-relocation-ad.mp4` and `assets/video/greater-vancouver-relocation-ad-poster.jpg` | Campaigns 1 and 2. 1280×720, about 32 seconds, poster is the title frame at 4 seconds. Confirm "Axford Real Estate" is still readable after Meta's crop. The poster is a title frame, not a 4:5 ad. |
| `assets/img/blog/2026-10-10-how-to-rent-in-vancouver-before-you-move.jpg` | Campaign 1 static. Branded card, stat "1/2", footer includes Axford Real Estate. The stat is the provincial cap on a security deposit (half of one month's rent). |
| `assets/img/blog/2026-10-08-vancouver-september-asking-rents.jpg` | Campaign 1 or 2 static. Stat "+1.4%" for Vancouver apartment and condo asking rents, September versus August 2026. |
| `assets/img/blog/2026-10-09-what-190k-leaves-you-after-tax-and-rent.jpg` | Campaign 2 static. Map of what $190,000 leaves after tax and a year of average one-bedroom asking rent. Label it as his calculation, which the blog already does. |
| `assets/img/blog/2026-10-06-metro-vancouver-september-2026-home-sales.jpg` | Campaign 3 static. Stat "−8.4%", Greater Vancouver REALTORS® September 2026 sales versus September 2025. |
| `assets/img/og-tenants.png` | Fallback link image for campaign 1 if a blog card's footer is cropped. It is a designed tenants graphic. Still check that Axford Real Estate survives the crop. |
| `assets/img/devin-headshot-800.jpg` | Campaign 3, beside a text overlay you add in Ads Manager: "Buying in the Tri-Cities, BC" and "Axford Real Estate". The headshot file itself has no brokerage line. |

Do **not** run `assets/img/blog/2026-10-07-canadas-best-cities-for-work-2026.jpg` as an ad. The graphic is a ranking titled around a superlative. B.C. advertising should not carry "best," even when the word is about cities. The underlying post can still feed a Google Business Profile post if the post itself avoids that word. See `google-business-posts.md`.

YouTube, only as a last creative for campaign 3, and only with an overlay: thumbnail `https://i.ytimg.com/vi/gyg2-U7o-6E/hqdefault.jpg` or `https://i.ytimg.com/vi/TA6-pO-hDfQ/hqdefault.jpg`, plus on-image text "Video tour, not a listing I'm offering" and "Axford Real Estate". If you will not add both lines, skip it and use the September sales card. Do not use `daQ3Q4ZCmf4`, `mR_HYgiJClc`, `INd7HTnfDLs`, or `TptjgpShZYM` as the ad image. The first three read as trophy homes. The fourth is a street-address tour and should not be implied to be for sale.

Public URLs if you upload from a link rather than a file:

- https://devindesaulniers.ca/assets/video/greater-vancouver-relocation-ad.mp4
- https://devindesaulniers.ca/assets/video/greater-vancouver-relocation-ad-poster.jpg
- https://devindesaulniers.ca/assets/img/blog/2026-10-10-how-to-rent-in-vancouver-before-you-move.jpg
- https://devindesaulniers.ca/assets/img/blog/2026-10-08-vancouver-september-asking-rents.jpg
- https://devindesaulniers.ca/assets/img/blog/2026-10-09-what-190k-leaves-you-after-tax-and-rent.jpg
- https://devindesaulniers.ca/assets/img/blog/2026-10-06-metro-vancouver-september-2026-home-sales.jpg
- https://devindesaulniers.ca/assets/img/og-tenants.png
- https://devindesaulniers.ca/assets/img/devin-headshot-800.jpg

## British Columbia advertising rules on every ad

BC Financial Services Authority: the brokerage name must be displayed prominently and in an easily readable way in all real estate advertising. The full name is **Axford Real Estate**. A short form is not sufficient. If the ad names Devin, use the name on his licence (Devin Desaulniers). Section 41 of the Real Estate Services Rules prohibits advertising he knows or ought to know is false or misleading.

Checked against:

- https://www.bcfsa.ca/industry-resources/real-estate-professional-resources/knowledge-base/information/advertising-information
- https://www.bcfsa.ca/industry-resources/real-estate-professional-resources/knowledge-base/practice-resources/advertising-checklist-and-sample-advertising
- Real Estate Services Rules, s. 40 and s. 41: https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/209_2021

House rules for this account, in addition:

- "Axford Real Estate" appears in the first 125 characters of every primary text.
- No "best," "top," "#1," "guaranteed," or a promise that he will secure a rental or a purchase.
- No star ratings in the ad. The counts on the site (his Google reviews, Axford's five-star count) go stale, and a rating in an ad needs a source and a date in the ad itself. Leave them on the website.
- The $1,500 figure always includes "+ GST" and "paid by the tenant."
- Do not describe a YouTube tour as for sale, sold, or "my listing."
- Have the managing broker approve the copy before the first dollar.

Meta's on-screen limits: headline about 40 characters, description about 30, before they truncate. The lines below are inside those counts. Primary text can be longer. The first 125 characters are the part that matters.

CTA button names below are Meta's own labels.

---

## Campaign 1 — relocation rentals

Special ad category: Housing. Audience: the seven origin cities. Optimization: link clicks. Daily budget: $4 at the $8 plan.

### Ad c1-v1

- **Creative:** `greater-vancouver-relocation-ad.mp4`, poster as the thumbnail. Feed only.
- **Primary text:** Moving to Greater Vancouver? I help tenants line up a rental before they arrive. Axford Real Estate. Devin Desaulniers, REALTOR®. Search, showings (in person or by live video), and a lease review. $1,500 + GST, paid by the tenant: $750 at the start, $750 once a rental is secured. Reach out 4 to 6 weeks before the move.
- **Headline:** Line up a rental before you land
- **Description:** $1,500 + GST, tenant-paid
- **CTA:** Sign Up
- **URL:** the c1-v1 link above

### Ad c1-v2

- **Creative:** `2026-10-10-how-to-rent-in-vancouver-before-you-move.jpg`. Confirm the footer is visible.
- **Primary text:** Starting a job or a term in B.C.? You can rent before you land. Axford Real Estate. I'm Devin Desaulniers, REALTOR®, in Port Moody. A security deposit here is capped at half a month's rent. I search on the tenant side across Greater Vancouver, including the Tri-Cities, BC. $1,500 + GST, paid by you, in two parts.
- **Headline:** Tenant-side help before you arrive
- **Description:** Showings, search, lease review
- **CTA:** Learn More
- **URL:** the c1-v2 link above

### Ad c1-v3

- **Creative:** `2026-10-08-vancouver-september-asking-rents.jpg`.
- **Primary text:** Vancouver asking rents are still high if you're moving from away. Axford Real Estate. Devin Desaulniers, REALTOR®. September apartment and condo asking rents were $2,741, up 1.4% on the month and still 1.3% under last year (Rentals.ca and Urbanation). I help tenants compare areas and view places before they arrive. $1,500 + GST, paid by the tenant.
- **Headline:** Rent in Greater Vancouver remotely
- **Description:** Axford Real Estate
- **CTA:** Learn More
- **URL:** the c1-v3 link above

The $2,741, +1.4%, and −1.3% figures are from the October 8, 2026 blog post, which cites the Rentals.ca and Urbanation report released October 7, 2026. If that post is later corrected, correct the ad the same day.

---

## Campaign 2 — relocating guide

Special ad category: Housing. Same origin-city audience as campaign 1. That overlap is acceptable: the ads ask for different things (a paid service versus a guide), and the budget is too small for a third geography. If campaign 1's CPC is clearly better after the first $40, pause campaign 2 and follow the budget rule above.

Daily budget: $1.50 at the $8 plan. This campaign is the first one to turn off.

### Ad c2-v1

- **Creative:** the same relocation video as c1-v1. Different text, different URL.
- **Primary text:** Moving to Greater Vancouver from another province? Start with areas and commute. Axford Real Estate. I'm Devin Desaulniers, REALTOR®. I've lived here 28 years. The guide covers Vancouver, Burnaby, New Westminster, the Tri-Cities, BC, and how renting works before you buy. Call or text 604-809-1032.
- **Headline:** Moving to Greater Vancouver
- **Description:** Areas, commute, rent or buy
- **CTA:** Learn More
- **URL:** the c2-v1 link above

"28 years" is the figure on `relocating-to-greater-vancouver.html`.

### Ad c2-v2

- **Creative:** `2026-10-09-what-190k-leaves-you-after-tax-and-rent.jpg`.
- **Primary text:** A $190,000 salary does not all clear rent in Vancouver. Axford Real Estate. Devin Desaulniers, REALTOR®, ran 2026 tax and a year of average one-bedroom asking rent: about $102,376 left, close to Ottawa on the same math. Read the notes, then the relocation guide, before you pick a city. Not tax advice.
- **Headline:** What pay leaves after rent
- **Description:** A guide for people moving
- **CTA:** Learn More
- **URL:** the c2-v2 link above

The dollar figure is his calculation in the October 9, 2026 post, for a single filer with basic credits only. The ad says so by sending people to the guide and by the "not tax advice" line. Do not shorten this ad in a way that drops "Not tax advice."

### Ad c2-v3

- **Creative:** `2026-10-08-vancouver-september-asking-rents.jpg` if it is not already the only winner in campaign 1. If campaign 1 is using it and winning, use `og-tenants.png` here instead so the two campaigns don't look identical in the feed.
- **Primary text:** Most Greater Vancouver rentals show up a few weeks before they're free. Axford Real Estate. Devin Desaulniers, REALTOR®. For a rental, start the active search about 4 to 6 weeks out. The relocation guide covers deposits, areas, and when to rent first. Tenant-side help is $1,500 + GST if you want someone at the showings.
- **Headline:** Start the search 4 to 6 weeks out
- **Description:** Neighbourhoods and commute
- **CTA:** Learn More
- **URL:** the c2-v3 link above

---

## Campaign 3 — Tri-Cities, BC buyers

Special ad category: Housing. Audience: 25 km around the Port Moody office. Daily budget: $2.50 at the $8 plan.

The landing page is for buyers (goals, listing alerts, showings, comparable sales, offers). It also explains Coquitlam, Port Coquitlam, Port Moody, and Anmore and Belcarra. He works with sellers too. This campaign does not send sellers to the buyer form. Seller calls go to 604-809-1032.

### Ad c3-v1

- **Creative:** `2026-10-06-metro-vancouver-september-2026-home-sales.jpg`.
- **Primary text:** Looking at homes in the Tri-Cities, BC? September sales were slower than last year. Axford Real Estate. Devin Desaulniers, REALTOR®. Greater Vancouver REALTORS® reported 1,717 sales, down 8.4%, mostly apartments. I'll send listings that match what you want and walk through comparable sales with you. No promise on where prices go.
- **Headline:** Buying in the Tri-Cities, BC
- **Description:** Coquitlam, PoCo, Port Moody
- **CTA:** Sign Up
- **URL:** the c3-v1 link above

Figures from the October 6, 2026 post, citing Greater Vancouver REALTORS®, October 2, 2026.

### Ad c3-v2

- **Creative:** `devin-headshot-800.jpg` with an Ads Manager overlay: "Buying in the Tri-Cities, BC" and "Axford Real Estate". If you cannot add the overlay, do not run the bare headshot.
- **Primary text:** Buying in Coquitlam, Port Coquitlam, or Port Moody? Tell me what you want. Axford Real Estate. I'm Devin Desaulniers, REALTOR®. Listing alerts, showings, and an offer built from recent sales, with subjects like financing and inspection left in place. Greater Vancouver too, if that's the search.
- **Headline:** Get listings for your search
- **Description:** Alerts as homes are listed
- **CTA:** Sign Up
- **URL:** the c3-v2 link above

### Ad c3-v3

- **Creative:** the September sales card if c3-v1 is paused, or the headshot treatment from c3-v2 with the line "Video tours, not listings" if you would rather show a face. Optional and secondary: a YouTube thumbnail from the table above, only with both overlay lines. Default is the sales card, so this ad can run even if the overlay never gets made. Use a different crop or the headshot so it is not a duplicate of c3-v1 in the same ad set.
- **Primary text:** More homes were listed than a typical September, and condo sales were the slow part. Axford Real Estate. Devin Desaulniers, REALTOR®. Benchmarks in the Tri-Cities, BC were lower than a year earlier. A benchmark is not the price of your house. I use recent sales on the street you're considering. Start with the buyer page.
- **Headline:** A plain read of September sales
- **Description:** Listings for your buyer search
- **CTA:** Learn More
- **URL:** the c3-v3 link above

Benchmarks in that post, if you need them in a later edit and not in this short text: Coquitlam $971,700 (−6.3%), Port Coquitlam $835,500 (−8.2%), Port Moody $1,011,500 (−5.8%), all property types, September 2026 versus September 2025. Greater Vancouver REALTORS®. Do not add them unless the whole sentence, including "benchmark," fits.

---

## What to watch, when to stop, when to scale

Check twice a week. Monday: spend, CPC, link clicks. Friday: inbox forms and any call or text that mentioned an ad. Write the four numbers in a note: spend, link clicks, average CPC, leads.

CPC means cost per link click, from Ads Manager, not cost per impression.

### Stop an ad

- It has spent **$20** and has **fewer than 5** link clicks. Pause that ad. Leave the other ads in the campaign running.
- It has spent **$15**, and its CPC is **more than double** the CPC of another ad in the same campaign that has at least 5 clicks. Pause the expensive one.
- The preview crops "Axford Real Estate" off the image and the primary text no longer shows the brokerage name before "See more." Pause until the text is fixed.
- A comment points out a wrong number. Pause, fix the blog and the ad together, then turn it back on.

### Stop a campaign

- Campaign 1 spends **$50 in a week** with **zero** intakes, calls, or emails. Pause it for the next week and put that money into campaign 3 as a one-week test. If campaign 3 also produces no conversations in that week, stop paid spend.
- Campaign 2 is the first cut. If after **$25** its CPC is higher than campaign 1's, turn campaign 2 off and move the $1.50 a day to campaign 1.
- The whole account passes **$150** with **zero** real conversations (form, call, or email from a person who is actually moving, buying, or selling). Stop. Do not refresh creative past that point on this budget. The offer or the page needs a broker conversation before more money goes in.

### Scale

Scale means moving toward the **$10-a-day ceiling of this band**, not jumping to $20.

- Do it only for a campaign that produced **at least 2 real intakes or listing requests in 14 days**, at a cost per one of those of **under $40**.
- Add **$1 a day**, then leave it for **4 days**. Do not double a budget.
- Do not scale on a good CPC alone. Clicks without a form or a call are not the result.
- Stay at $10 unless you make a new decision in writing. This plan's ceiling is the ceiling you asked for.

### What "good" cannot mean here

A week at $56 might be 15 to 40 link clicks if CPC lands between about $1.50 and $3.50, or fewer if CPC is higher. It might be zero leads. That is a normal outcome at this spend, not a sign the pixel is broken. There is no pixel. Do not install one in a hurry on day three and reset the reading. If you add one later, start a new note and do not mix the two periods.
