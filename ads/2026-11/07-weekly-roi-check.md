# Weekly ROI check

Fifteen minutes every Monday, starting November 2, 2026. The blank file is [weekly-roi-log.csv](weekly-roi-log.csv). Copy it into a spreadsheet so the formulas can run. The CSV itself is the column list.

The test has two different questions. Do not mix them up.

| Question | When | Number |
| --- | --- | --- |
| Which ad wins? | November 15 | Lowest **cost per qualified inquiry** |
| Has the service proved out? | Any later raise above $200 / month | **Collected fees ÷ ad spend ≥ 2** |

## Fee math

Confirm GST with Axford before a contract. The ads say “+ GST.”

| | Before tax | At 5% GST |
| --- | --- | --- |
| To start (non-refundable) | $750 | $787.50 |
| When a rental is secured | $750 | $787.50 |
| Full Tenant Relocation Service | $1,500 | $1,575 |

Enter **cash collected**, not a verbal yes and not the second $750 before it is paid.

Buyer fees go in their own column and only after they are received. A buyer lead with no fee adds $0. A forecast commission does not belong on this sheet.

## Columns

One row per week, campaign total. Add a note per ad on November 7 and November 14 so the winner math is visible. After November 15, one row for the winner is enough.

| Column | Meaning |
| --- | --- |
| week_ending | Saturday date |
| flight | `test` (Nov 1–14) or `winner` |
| spend | Dollars from Ads Manager for that week |
| link_clicks | Link clicks |
| landing_page_views | Landing page views |
| raw_contacts | Emails + calls + texts, all types |
| qualified_inquiries | Definition in the tracking plan |
| of_which_attributed | Qualified inquiries tied to a specific ad. Excludes “not sure.” |
| consultations | Qualification calls held |
| retainer_collected | Dollars |
| completion_fee_collected | Dollars |
| buyer_fee_collected | Dollars |
| fees_collected | Sum of the three money columns |
| cumulative_spend | Running total from November 1 |
| cumulative_fees | Running total of fees_collected |
| return_ratio | cumulative_fees ÷ cumulative_spend. Blank if spend is 0. |
| cpqi | Week’s spend ÷ week’s qualified inquiries. Blank if inquiries are 0. |
| decision | `hold`, `winner`, `pause`, or `stop` |
| notes | Objections, disapprovals, which ad got the inquiry |

### November 15 score (do this in the notes, or on four extra rows)

For each ad:

**CPQI = that ad’s spend ÷ qualified inquiries attributed to that ad**

- The lowest CPQI wins, if it has at least one attributed qualified inquiry.
- An ad with zero qualified inquiries has no CPQI. It loses to any ad with one.
- Tie: more qualified inquiries, then lower cost per link click (spend ÷ link clicks).
- All four at zero: there is no winner. Keep the lowest cost-per-link-click ad at $100 / month through November 30. `decision` = `hold`. Do not go to $200.
- `meta-unspecified` inquiries do not break a tie. Mention them in notes so a quiet ad is not punished for a lead who forgot the picture.

Illustration, not a prediction: video spent $25 and was named by one qualified inquiry (CPQI $25). Each still spent $25 and was named by nobody. The video wins. Two stills with zero inquiries are not “infinite CPQI”; they are simply out.

## The 2:1 rule

**Return = cumulative fees collected ÷ cumulative ad spend.** Target **2.0 or better** before the monthly budget goes above $200.

| Collected (5% GST) | Most you can have spent and still be at 2:1 |
| --- | --- |
| One retainer, $787.50 | $393 |
| One full fee, $1,575 | $787 |
| Two full fees, $3,150 | $1,575 |

Examples, so the sheet has a feel for the scale of this test:

- $100 spent, one retainer in ($787.50): return about **7.9**.
- $200 spent, one full fee in ($1,575): return about **7.9**.
- $787 spent, one full fee in: return **2.0**.
- $787 spent, nothing collected: **stop**.

A planning cross-check, not a quota: if about one in five qualified inquiries becomes a full fee, cost per qualified inquiry needs to stay near **$150 or lower** for the path to 2:1 to be intact (0.2 × $1,575 = $315 of expected fee per inquiry; $315 ÷ $150 = 2.1). The real ratio on the sheet overrides this. If close rate is worse than one in five, the inquiry cap has to be lower. Do not treat $150 as a target to spend toward.

## Monday decisions

| What you see | What you do |
| --- | --- |
| November 2–14, ads approved, spend roughly even | `hold`. Do not edit. |
| One ad has spent about $40 before November 10 | Pause it until the others catch up, then turn it back on. |
| November 15, one ad has the best CPQI | That ad is the winner. Pause the other three. $100 / month. `winner`. |
| November 15, nobody qualified | No winner. Cheapest click only, $100 / month, until November 30. |
| Winner has at least one qualified inquiry | You may use up to $200 / month. You may not go past $200. |
| Qualified inquiries exist, no cash yet, spend under $787 | Stay at $100–$200. `hold`. |
| Cumulative spend reaches $787 and fees are $0 | Pause everything. `stop`. |
| Return ratio is 2.0 or better and a retainer is in the bank | The test has proved out. A higher budget is a separate decision. This sheet does not raise it. |
| November ends with zero qualified inquiries | Pause December 1 unless the notes record a specific reason to buy one more month, and the broker agrees. Default `pause`. |
| Tempted to “add Google to see” | Google stays off, or it is paid by cutting the Meta daily budget so the month is still ≤ $200. |

## What not to optimize

Clicks, likes, video views, and cheap form fills. A $4 click that becomes a retainer is a better week than forty clicks from people who wanted a free list. Cost per paid client — cash in, divided by spend — is the number the workbook asked for. On a $100 test that number will often be blank. Blank means “no fee yet,” which is an acceptable week. It is not a reason to change the ads before November 15.
