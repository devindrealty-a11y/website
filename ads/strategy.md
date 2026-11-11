# Strategy

Parent: [README](README.md). Budget mechanics and the Monday checklist live in [budget-and-roi.md](budget-and-roi.md).

## Goal

Spend a small, capped amount to find whether paid ads can produce tenant clients and buyer conversations at a **2:1 return** on fees actually collected. November is a learning month with a dollar ceiling. It is a success if the cost of a real intake stays inside the cap below, or if at least one tenant client pays the first $750. It is a failure if spend runs ahead of qualified leads. In that case the campaigns pause. They do not get a bigger budget.

## The two offers, as the site already states them

### Tenant relocation (the offer that can prove 2:1 inside a month)

Devin represents the tenant, not a landlord's inventory. Axford has a separate property-management business. This service is a different engagement, and the ads say so by describing tenant representation only.

Scope, from `tenants.html` and the relocation guide:

- Personalized consultation on budget, commute, lifestyle, and red flags.
- A rental search in the areas agreed up front, including Axford's own rental opportunities, Facebook Marketplace, Craigslist, and other rental sources.
- Showings with the client, or a live video walkthrough and floor plans while they are still out of province.
- Lease review and negotiation before they sign.

Price: **$1,500 + GST**, paid by the tenant. **$750 + GST** at the start, non-refundable. **$750 + GST** only once a rental is secured. If no rental is secured, the second half is not owed.

Timing the site already tells people: settle preferences early, and expect the active search about **4–6 weeks** before move-in, because most Greater Vancouver rentals are listed close to the date they are available.

GST is 5%. A client who completes both halves pays $1,575. The figure used in the return math is the **$1,500 before GST**, because the GST is collected and remitted.

### Buyers (a longer cycle, a smaller test)

Buyer help on `buyers.html`: goals and budget, listing alerts, showings, comparable sales, the offer (including financing and inspection subjects), subject removal, deposits, and completion. Neighbourhood depth is strongest in Coquitlam, Port Coquitlam, and Port Moody, with the form also covering Burnaby, New Westminster, Pitt Meadows, Maple Ridge, Anmore, and Belcarra.

The buyer does not pay Devin's fee directly. Compensation on a purchase is arranged through the listing side and the brokerage, then split. This plan does not assume a dollar amount for that net. Before November 1, write your typical net-to-you on a completed Tri-Cities purchase into the lead log and label it `buyer_net`. Until a deal completes, buyer ad spend counts as cost and buyer leads count as **zero revenue**.

## Why Facebook and Instagram lead, and why Search is phase 2

The relocating tenant is the better first campaign for a $400 month:

- The price is published, fixed, and short. One completed file is $1,500 before GST. One start payment is $750 before GST.
- The client can hire Devin weeks before they arrive. The sales cycle is measured in weeks, so November spend can be compared with November cash.
- The homepage already has a 32-second relocation video, and the relocation guide already explains the fee.

Meta is the phase 1 channel because the brief leads with it, and because a short video plus a clear fee can be shown to people in the cities Canadians actually move from. Meta's housing rules block the tight "people who are about to move" filters a media buyer would normally want. The ad copy does that qualifying. People who are not moving scroll past "Moving to Greater Vancouver?"

Google Search is the better intent tool for the same person ("moving to Vancouver rental", "tenant agent Vancouver"). It is phase 2 because the budget cannot support two platforms until Meta has shown that the page and the inbox can turn clicks into qualified intakes. Turning both on at $200–$400 would leave each campaign too thin to read. Search starts only through the gate in [budget-and-roi.md](budget-and-roi.md#phase-2-gate).

Buyers stay in the account from November 22 (a short end-of-month test) and, if the gate opens, as a small December slice. A purchase will not complete inside the first week, so buyer ads are judged on qualified "Send me listings" emails, not on a weekly return ratio.

## What 2:1 means

```
return ratio = collected fees before GST ÷ media spend before recoverable GST
```

Collected fees:

- Tenant: $750 when the start payment clears, plus $750 when the second payment clears.
- Buyer: `buyer_net` when the brokerage actually pays it.
- A rental-listing inquiry from `rentals.html` (email subject `New rental inquiry`) is logged and answered. It is **$0** in this ratio unless that person later hires the tenant service or a purchase completes.

Media spend is the amount in Ads Manager and Google Ads before GST, if that GST is claimed as an input tax credit. Devin charges GST on the tenant fee, so he is treating the practice as GST-registered. Confirm with the bookkeeper. If the GST on the ad invoices is not being recovered, put the tax in the denominator too.

The ratio is reviewed **every Monday** and judged on two windows:

| Window | What it decides |
| --- | --- |
| That week, and month-to-date | Whether to pause, hold, or move the unspent reserve. A single quiet week does not kill a campaign that is still inside the cost cap. |
| Rolling 90 days, starting November 1 | Whether the test is actually at 2:1. One $750 start against the scheduled ~$327 of November media is about 2.3. The same payment against a full $400 month is about 1.9. Either result continues. Neither one earns a budget increase on its own. |

Ads Manager "results" and a future pixel `Lead` event are lead counts. They are never added into the numerator.

### The cost cap that protects the ratio

Until there are 10 real tenant intakes to replace these defaults, plan with:

- **15%** of intake emails pay the first $750 (`r = 0.15`).
- **70%** of those also pay the second $750 (`c = 0.70`).

Expected fees from one intake email:

```
0.15 × 750 × (1 + 0.70) = $191
```

Maximum cost per intake email at a 2:1 return:

```
191 ÷ 2 = $96
```

**Working cap: $80 per tenant intake email** (subject line `New relocation rental intake`). The cap sits under the $96 figure so a slightly weaker close rate still clears 2:1. After 10 intakes, replace `r` and `c` with the real rates and recompute. If the real `r` is 8% and `c` stays 70%, the cap falls to **$51** (`0.08 × 750 × 1.70 ÷ 2`). The Monday review uses whichever number the log supports.

Buyer cap, once `buyer_net`, the share of form emails that are qualified (`q`), and the share of qualified buyers who complete (`close`) are filled in:

```
max cost per buyer form email = (q × close × buyer_net) ÷ 2
```

Leave this blank rather than inventing a commission. A worked example for the shape of it, not a forecast: net $8,000, 40% of emails qualified, 15% of those complete, gives an expected $480 per email and a cap of $240. At a few dollars a day, one qualified buyer email every month or two can still sit on a 2:1 path **if that buyer later completes**. The weekly review does not score that path as won when the email arrives.

## Phase gates

| Phase | Dates | Channels | Working spend | Opens when |
| --- | --- | --- | --- | --- |
| 1 | November 1–30, 2026 | Meta only | About $400, inside $200–$500 | Launch checklist is done. |
| 2 | From December 7, 2026 | Meta, plus a smaller Google Search test | Up to $500 combined | November 30 review: at least one $750 collected, **or** tenant cost per intake ≤ $80 with at least four intake emails. Also: no unresolved FormSubmit or page outage. |
| Hold | Any month the gate fails | Meta tenant only, or full pause | $0–$300 | Cost per intake over the cap after $200 of tenant spend, and no $750 collected. Google stays off. Buyer stays off. |
| Scale conversation | After a 90-day ratio ≥ 2, and only by a line in the Monday log | Same channels | Still ≤ $1,000 cash that month | Never automatic. $500 remains the working ceiling until that written note. |

## 30, 60, and 90 days

**November 30.** Meta has run the tenant ads all month and the buyer ads from November 22. The log shows spend, intake emails, qualified yes/no, and any $750. The phase 2 gate is answered in writing in the log. Google is still off.

**December 31.** If phase 2 opened, Search has about three weeks of data. Compare cost per qualified tenant intake on Meta versus Google. Keep the cheaper source. Pause the other rather than feeding both out of habit. Buyer spend is still a lead-quality read, not a return read.

**January 31, 2027 (day 90).** Compute the rolling ratio from collected fees. At or above 2:1, the test has earned a conversation about staying near $500 or, with a written note, moving toward the $1,000 ceiling. Under 2:1, with the cost cap also missed, pause paid ads and keep answering the organic forms. The site, the fee, and the service do not depend on this test.

## Reply speed is part of the return

A paid lead that sits for days will not hit 2:1 at any bid. Target:

- Weekdays 9:00–18:00 Pacific: first reply within two hours.
- Evenings and weekends: first reply by 10:00 the next morning, Pacific.

The first reply states the fee again ($1,500 + GST, two parts) and the 4–6 week search window, then asks for anything the form missed. People who only wanted a free list of rentals are declined quickly and politely. They stay in the log as not qualified, so the cost cap stays honest.
