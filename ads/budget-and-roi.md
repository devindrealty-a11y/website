# Budget, caps, and the weekly ROI check

Parent: [README](README.md). Definitions and the cost-cap formula: [strategy.md](strategy.md).

All figures are CAD. The working band is **$200–$500 per month**. The hard ceiling is **$1,000 cash out the door in a calendar month** for Meta and Google combined, **including GST on the ad invoices**. The plan aims at about **$400 in November** and, only if the gate opens, about **$500 in December**. The ceiling is a stop, not a target.

## GST on the invoices

Meta and Google add 5% GST to ad charges billed in British Columbia. A $400 media month is about $420 on the card. Because the tenant fee is charged plus GST, the practice is operating as if it is GST-registered, and that 5% may be an input tax credit. Confirm with the bookkeeper.

- The 2:1 ratio uses media spend **before** GST when the GST is being recovered, and the fees **before** GST ($750 and $750, not $787.50).
- The **$1,000 ceiling uses cash**, tax included. If the card would cross $1,000, pause every campaign that day even if the pre-tax dashboards show less.

Set a Meta account spending limit of **$500** on November 1 (pre-tax limit, if that is how the account asks; if the field is tax-in, set $525). Set a Google account budget of **$200** only when phase 2 is built. The human cap still overrides both.

## November (phase 1, Meta only)

| Dates | Campaign | Daily | Month |
| --- | --- | --- | --- |
| Nov 1–30 | Tenant relocate, landing-page views | $10 | about $300 |
| Nov 1–21 | Buyers | $0 | $0 |
| Nov 22–30 | Buyers, landing-page views | $3 | about $27 |
|  | **Planned November media** |  | **about $327** |
|  | Room inside a $400 working month |  | about $70 |
|  | Room under the $500 account limit |  | use it only by a Monday decision |

The buyer campaign waits until November 22 so the first three weeks of a thin budget stay on the offer that can collect $750 inside the month. The buyer ads, URLs, and creative are built and paused on November 1, ready for the 22nd.

The ~$70 reserve is not scheduled. It is used only by a line in the Monday log, for example "T2 is producing intakes under $80, add $2/day for the rest of the month." Unused reserve is a success. It is not a miss.

T4 (the `rentals.html` ad) shares the tenant ad set. It does not get another daily budget on top of the $10.

## December, if the gate opens

Earliest start for Google: **Monday, December 7, 2026.** Meta keeps running.

| Campaign | Daily from Dec 7 | Rough December total |
| --- | --- | --- |
| Meta tenant | $8 | about $248 for a full month at $8, which assumes the cut happens Dec 1. If Meta stays at $10 until Dec 7 and then moves to $8, expect about $270. |
| Meta buyer | $3 | about $93 |
| Google tenant search | $4 | about $100 from Dec 7–31 |
| Google buyer search | $1.50 | about $37 from Dec 7–31 |
| **Combined** |  | **about $500** |

If you want a single number to type on December 1: set Meta tenant to **$8** and Meta buyer to **$3** that morning, and set the two Google campaigns to **$4** and **$1.50** on December 7. Check the sum of both dashboards the same day. Trim Meta tenant first if the month is tracking over $500.

### Phase 2 gate

Answer this in the log on **Monday, November 30**. Google turns on December 7 only if every line is yes.

1. FormSubmit is still delivering, and the three landing URLs still load on a phone.
2. At least one of these is true: a tenant client has paid the first **$750**, **or** there are at least **four** `New relocation rental intake` emails and the cost per those emails is **at or under $80** (recompute the cap first if 10 intakes have already replaced the default rates).
3. Month-to-date cash on the Meta invoice, tax included, is under $500, with room for about $150 of Google.
4. No ad is running a fee, a phone number, or a claim that the site no longer supports.

If the gate is no, December is Meta tenant only at **$10/day** (about $300) or a full pause. Write which one, and why. Buyer and Google stay off.

A full pause is the right December if tenant spend has passed **$200**, the cost per intake is over the cap, and no $750 has been collected.

## The $1,000 ceiling, any month

Pause Meta and Google the same day if any of these is true:

- Combined invoices for the calendar month would exceed **$1,000 including GST**.
- A campaign was switched on by accident (Google in November, or a third campaign).
- The landing page fee and the ad fee disagree.

Raising the working month from $500 toward $1,000 requires a 90-day collected-fee ratio of at least 2, and a sentence in the Monday log that names the new daily budgets. There is no automatic rule that scales spend because a week felt busy.

## Before November 1

- [ ] Axford has seen the primary texts in [meta-ads.md](meta-ads.md) and the Housing category note in [targeting.md](targeting.md).
- [ ] A real FormSubmit email has arrived for the intake and for "Send me listings". Those two log rows are marked `test`.
- [ ] Each final URL has been opened on a phone. `#listings` lands on the buyer form. The guide button reaches the intake.
- [ ] Review counts re-checked if any card uses them. The paste-ready copy in this folder does not use a number.
- [ ] Static A (fee card) exported, or a decision written that November 1 runs the existing 16:9 video only.
- [ ] Meta campaigns built **paused**, housing category on, creative enhancements off, account spending limit $500.
- [ ] Buyer campaign scheduled or calendar-reminded for November 22. Google campaigns not created yet, or created paused with a December 7 note.
- [ ] `buyer_net` blank or filled with your real typical net. No placeholder commission left in the ratio.
- [ ] Lead log created (copy the columns below into a sheet).
- [ ] Reply-time plan is real: two hours on weekday afternoons, next morning otherwise.

## Every Monday, 30 minutes

Start **November 2** with the smoke check only. Start the full review **November 9**, then every Monday (November 16, 23, 30, December 7, 14, 21, 28, and on).

### Smoke check (November 2, and any Monday a new campaign starts)

- Ads are approved, not rejected for housing or for a personal-attribute line.
- Spend so far is within the daily budget, not a decimal-point mistake.
- One final URL still loads.
- The lead log is the file you will actually open next Monday.

### Full review

1. **Spend.** Meta this week, Meta month-to-date, Google this week, Google month-to-date, and cash including GST. Write the numbers down. Compare with the $500 working cap and the $1,000 ceiling.
2. **Leads.** Count emails since the last review by subject line. Add phone leads. Mark each new row qualified or not, using [targeting.md](targeting.md).
3. **Cash.** Any $750 start, any $750 completion, any buyer net received. Dates, not promises.
4. **Ratio.** Month-to-date fees before GST, divided by month-to-date media before recoverable GST. Also the rough 90-day figure once December starts. A blank numerator is a ratio of 0. Write 0. Do not substitute "pipeline".
5. **Cost per tenant intake.** Tenant spend since November 1, divided by paid intake emails (exclude rows marked `test` or `source=organic`). Compare with **$80**, or with the recomputed cap once you have 10 intakes.
6. **Buyer quality.** Of the buyer emails, how many have a timeline inside 6 months. If every row is "12+ months / just exploring", pause the buyer campaign at the end of the review.
7. **Search terms,** once Google is on. Negatives added the same morning. List in [google-search.md](google-search.md).
8. **One decision.** Pause, hold, or move at most $2/day from the reserve or from the weaker platform. Record the sentence in the log. Change the ads that morning so the decision is not still theoretical next week.

### Decision rules

| What you see | What you do |
| --- | --- |
| Any week spends more than $150 and produces zero form emails and zero logged calls | Pause all campaigns for 48 hours. Check FormSubmit, the phone test, ad approval, and that the URLs still match. |
| Tenant cost per intake over the cap for two Mondays in a row, with at least $200 spent | Pause the ads with no intakes (start with T4, then the highest spend among T1–T3). Do not raise the daily budget. |
| A $750 payment clears | Hold the budget. Note the new ratio. Continue. |
| The November 30 gate is yes | Cut Meta tenant to $8 on December 1. Turn Google on December 7 at $4 and $1.50. |
| The November 30 gate is no, and no $750 has cleared, and spend is over $200 with the cap missed | Pause paid ads for December. Keep answering organic form mail. |
| Google cost per intake beats Meta for two Mondays | Move $2/day from Meta tenant to Google tenant. Write it down. |
| Buyer emails are all long-timeline browsers | Pause buyer Meta and leave Google buyer off. |
| Invoices would cross $1,000 including GST | Pause everything the same day. |
| Fee on the site changes | Pause tenant ads until the text and Static A match. |

A quiet week inside the cap, with the page healthy and replies going out on time, is a hold. It is not a reason to rewrite the campaigns.

## Lead log

Copy this header into a sheet. One row per person, not per email thread.

| Column | What to enter |
| --- | --- |
| `date_pt` | When the email or call arrived |
| `test` | `yes` for the pre-launch tests, otherwise blank |
| `source` | `meta`, `google`, `organic`, `paid-unknown`, `phone` |
| `utm_content` | `t1`–`t4`, `b1`–`b4`, `rsa1`, or blank |
| `form` | `tenant_intake`, `buyer_listings`, `rental_inquiry`, `phone` |
| `name` | As written |
| `from_or_area` | Moving-from city, or buyer areas |
| `timeline` | Move-in date, or the buyer timeline field |
| `qualified` | `yes` or `no` |
| `why_not` | One short reason if no |
| `fee_start_date` | Date the first $750 cleared, else blank |
| `fee_start` | `750` or blank. Before GST. |
| `fee_second_date` | Date the second $750 cleared |
| `fee_second` | `750` or blank |
| `buyer_net_date` | Date you were paid on a purchase |
| `buyer_net` | Dollars you actually received, before income tax |
| `notes` | How they said they found you, and the Monday decision if this row triggered one |

### Weekly strip

Copy one row per Monday.

| Monday | Media spend MTD (before GST) | Cash on card MTD (incl. GST) | Intake emails (paid) | Qualified intakes | $ collected MTD | Ratio | Cost per intake | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-11-02 |  |  |  |  |  |  |  | Smoke check only |
| 2026-11-09 |  |  |  |  |  |  |  |  |
| 2026-11-16 |  |  |  |  |  |  |  | T4 keep or pause |
| 2026-11-23 |  |  |  |  |  |  |  | Buyer campaign is on |
| 2026-11-30 |  |  |  |  |  |  |  | Phase 2 gate yes/no |
| 2026-12-07 |  |  |  |  |  |  |  | Google on or stays off |
| 2026-12-14 |  |  |  |  |  |  |  |  |
| 2026-12-21 |  |  |  |  |  |  |  |  |
| 2026-12-28 |  |  |  |  |  |  |  |  |
| 2027-01-04 |  |  |  |  |  |  |  |  |
| 2027-01-25 |  |  |  |  |  |  |  | 90-day ratio. Stay, trim, or stop. |

## A worked month, so the ratio is easy to read

These numbers are an illustration of the arithmetic, not a forecast.

Suppose November spends $327 before GST. One tenant pays the first $750. No second payment yet. No buyer closes.

```
ratio = 750 ÷ 327 = 2.3
```

That month has cleared 2:1 on cash timing that may still reverse if you later refund nothing (the first half is non-refundable) — so 2.3 stands. It has **not** proved the second half will arrive. The log still tracks `fee_second`. You hold the budget. You do not double it, because one file is not a 90-day pattern, and the phase 2 gate also wants the intake cost in line if you are going to add Google.

Suppose instead the month spends $327 and produces six intakes, none of whom hire.

```
cost per intake = 327 ÷ 6 = $54.50
ratio = 0
```

$54 is under the $80 cap, so the campaign is allowed to continue into a second month at the same daily budget. It is not allowed to scale. The ratio is honestly 0 until a payment clears.

Suppose the month spends $327 and produces one intake.

```
cost per intake = $327
ratio = 0
```

That is over the cap. December pauses unless a $750 arrives in the last days and you write a specific reason to keep a smaller January test.

## What you can ignore inside the ad platforms

- "Purchase ROAS" and any recommended budget increase.
- A result that counts link clicks as leads.
- Frequency under 2. At this budget, fatigue is unlikely in month one. If frequency on a single origin city climbs past 3 and the click-through rate falls for two weeks, refresh the primary text of that ad. Do not answer fatigue by raising the budget.
- Cost per landing-page view by itself. It matters only as a clue when intakes are missing: a very cheap landing-page view with no emails means the page or the form is the problem; an expensive one with no clicks means the creative or the geo is the problem.
