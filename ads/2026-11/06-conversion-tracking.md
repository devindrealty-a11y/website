# Conversion tracking

No new code on the site, no pixel, no Google tag, no change to FormSubmit. The live pages do not record which ad was clicked. The tracking that works on November 1 is Ads Manager for clicks, the inbox and phone for leads, and a Monday sheet for the score.

Add a pixel only as a later project, with a privacy-page update. It is not part of this test.

## The number November 15 uses

**Cost per qualified inquiry** = spend on that ad ÷ qualified inquiries attributed to that ad.

An inquiry is qualified when all of these are true, decided on the first reply (email or a 10–15 minute call):

1. They are moving to Greater Vancouver, or they are buying from outside the region. They do not already live here and only want free links.
2. The timing is real. For a rental, about 4–6 weeks before move-in is the working window; further out is still qualified if the budget and the fee conversation are real.
3. The budget and the area can actually be searched.
4. They will hear the fee. For renters: **$1,500 + GST, paid by the tenant**, $750 + GST to start (non-refundable), $750 + GST when a rental is secured.

If they only want free listings, mark **unqualified** and stop spending conversation time as if they were a client. They still count as a raw email or call, so the sheet can show the gap between “filled a form” and “might hire.”

### Questions that make the mark obvious

- What is bringing you to Greater Vancouver?
- Where do you need to be for work or school?
- What monthly rent (or purchase range) is realistic?
- When do you need possession?
- Do you want someone local to manage this, knowing the tenant service is $1,500 + GST?
- Are you planning to rent, or do you think you will buy after you settle?

### Which ad they came from

The form email will not say `utm_content`. On the first reply, ask one question and write the answer down:

> Was it the video of me, or a photo — the skyline, the SkyTrain, or the trees and lake?

| They say | Log as |
| --- | --- |
| The video / “you talking” | `video` |
| Skyline, downtown, mountains | `still-skyline` |
| SkyTrain, the train, sunset tracks | `still-skytrain` |
| Trees, lake, Coquitlam photo | `still-coquitlam` |
| Not sure, or they will not say | `meta-unspecified` |
| Google / a search | `google` (should be zero in November) |
| A friend, a sign, the website with no ad | `other` |

`meta-unspecified` counts as a campaign inquiry. It does **not** count toward one ad’s cost per qualified inquiry. Guessing a variant would fake the winner.

Clicks and landing-page views still come from Ads Manager, per ad, whether or not anyone inquires. Those columns explain a zero. They do not replace the inquiry count.

## What to record for every contact

One row per person, the day they arrive.

| Field | Where it comes from |
| --- | --- |
| Date | Inbox or phone |
| Name, email, phone | The form or the call |
| Channel | Meta, phone, email, other |
| Creative code | The question above |
| Page they meant | Relocating guide, tenants form, buyers form, a rental listing |
| Moving from | Form field “Moving from,” or the call |
| Budget, beds, move date | Form or call |
| Qualified? | Yes / no, using the definition |
| Consultation booked? | Yes / no |
| Retainer collected (dollars) | Bank, not a verbal yes. $0 until then. |
| Second half collected (dollars) | $0 until a rental is secured and the fee is paid |
| Buyer fee collected (dollars) | $0 unless a purchase fee has been paid. No forecast. |
| Notes | Objection, in their words |

Raw form emails in November will mostly be “New relocation rental intake.” A “New rental inquiry” is a listing question from `rentals.html`. A “New buyer listings request” is Audience B. Keep those labels. Do not merge them into one lead type.

## Ads Manager columns to export each Monday

For each of the four ad sets:

- Amount spent
- Impressions
- Link clicks
- Landing page views
- The ad’s delivery status (approved, limited, or off)

Ignore cost per result if the “result” is a landing-page view. That number is useful as a diagnostic. The decision metric is cost per **qualified** inquiry, which only the sheet can calculate.

There is no Purchases or Leads column to trust. Optimizing the campaign for “leads” would require an instant form or a pixel. This test uses the website on purpose, so lead quality stays on the page that states the fee.

## Call and text

604-809-1032 will get some of the response, especially from people who will not fill in a form. Those contacts enter the same log. If they cannot name the video or a photo, use `meta-unspecified` or `other`. A phone lead with no creative code is still a real lead. It is a weak vote in the four-way test.

Reply the same day. The workbook’s funnel is form or call, then a short qualification, then the service. The ads do not close the $1,500 by themselves.

## What a later pixel would be for

Not for November. If tracking is added in a future site change, the events that match this sheet are:

- `page_view` on the three landing URLs
- A click on the tenants-page submit button that actually succeeds (the on-page “your request has been sent” message)
- The same for the buyers form and the rental inquiry form

Until those exist, do not paste a Meta or Google conversion number into the ROI sheet. Clicks from the ad account and qualified inquiries from the log stay in separate columns so they cannot be mistaken for each other.

## Privacy

The forms already ask for consent to be contacted. The attribution question is about which ad they saw, not a new use of their data. Do not upload customer lists to Meta for this test. Housing-category rules and the size of the test both argue against it.
