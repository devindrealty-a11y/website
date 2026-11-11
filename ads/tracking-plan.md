# Tracking plan (do not install yet)

The site has no Meta Pixel and no GA4. This document is the plan for a **later** change. Do not add tags, do not edit `assets/js/site.js`, and do not edit `privacy.html` as part of the ad launch.

November can run without this. Until it ships, Ads Manager optimizes for landing page views, and the source of truth is Devin’s inbox plus the Monday sheet. He asks each lead what brought them in, because the forms do not save the UTM.

Install the tags and the privacy-page update in the **same** later change. Tags without a privacy update would collect data the current privacy page does not describe.

## What to measure

Three form successes, and nothing that merely looks like a success.

The submit handler is in `assets/js/site.js`. It posts JSON to FormSubmit. A real success is `res.ok && String(res.j.success) !== 'false'`. The honeypot (`_honey`) shows a thank-you and returns **without** sending. That path must not fire a conversion.

Read the fields **before** `form.reset()`. The current success branch resets the form first. A later edit has to capture `data-form-key`, name, email, and phone, then reset.

| Event name | When | Form key | Page |
| --- | --- | --- | --- |
| `tenant_intake` | Real FormSubmit success | `tenantIntake` | `tenants.html` |
| `buyer_listings` | Real FormSubmit success | `buyerListings` | `buyers.html` |
| `rental_inquiry` | Real FormSubmit success | `rentalInquiry` | `rentals.html` |

Do not pass a monetary value on these events. A form is not a $1,500 sale. Sending `value: 1500` would invent a ROAS number inside Ads Manager. Revenue stays on the Monday sheet until Devin chooses to upload offline conversions, which this plan does not set up.

Secondary events, not used for bidding:

| Event | When |
| --- | --- |
| `phone_click` | A click on a `tel:` link |
| `email_click` | A click on a `mailto:` link |

`phone_click` is easy to inflate with mis-taps. Keep it out of the optimization goal.

Do not fire events for `homeEvaluation`, `buyerOpinion`, or `listingInquiry` in this test. They can be added later if those pages ever get ads.

## Meta Pixel

One pixel for `devindesaulniers.ca`, created in Events Manager when someone is ready to edit the site. Name it `devindesaulniers.ca`.

- Base code on every public page, so landing-page views exist for the three ad URLs and for `tenants.html` (the intake sits there, one click past the guide).
- On each real form success, fire the standard event **Lead** with:
  - `content_name`: `tenant_intake`, `buyer_listings`, or `rental_inquiry`
  - `content_category`: `housing`
  - no `value` and no `currency`
- Also fire the custom event of the same name (`tenant_intake`, and so on) so each campaign can optimize to its own form.
- Advanced matching: email, phone, and name from the form, hashed by the pixel, taken from the fields before the reset. Do not put those values in the URL.
- `eventID`: a random id per submit, stored if a Conversions API is ever added. **Do not build a Conversions API for this launch.** The site is static and the form is handled by FormSubmit. A server just to relay leads is a new system this test does not need.
- Deduplicate nothing until a second pipe exists. Pixel-only is the whole install.

Campaign optimization after events have fired on at least a few real submits (test submits from Devin count only if FormSubmit actually accepted them):

| Campaign | Optimize for |
| --- | --- |
| Meta relocating renters | `tenant_intake` |
| Meta relocating buyers | `buyer_listings` |
| Google rental ad group | `rental_inquiry` |
| Google relocation ad group | `tenant_intake` |

Housing category stays on. Custom conversions in Events Manager can filter Lead where `content_name` equals the event, which is useful if the custom event is slow to appear.

Attribution inside Meta: **7-day click, view-through off.** The Monday sheet does not use view-through.

## GA4

One GA4 property and one web stream for `https://devindesaulniers.ca`.

- Enhanced measurement: page views and outbound clicks on. Scrolls can stay on; they are not conversions.
- The three events above, sent with `gtag('event', ...)` in the same success branch as the pixel, with parameters:
  - `form_key` (`tenantIntake`, `buyerListings`, `rentalInquiry`)
  - `page_path`
  - `utm_source`, `utm_campaign`, `utm_content` copied from session storage (see below)
- Mark `tenant_intake`, `buyer_listings`, and `rental_inquiry` as key events.
- Conversion window for the ads link: **30-day click**. No view-through.
- Link the Google Ads account when it exists. Import only those three key events. Set the rental campaign’s goal to `rental_inquiry` and the relocation ad group’s goal to `tenant_intake`. Until the import is receiving events, leave bidding on Maximize clicks.
- Consent Mode: the audience is Canada. A GDPR-style banner is a brokerage decision, not a requirement this plan invents. What is required is an accurate privacy page **before** the tags go live.

### UTMs have to survive the second click

Renter ads land on the relocating guide **with** UTMs. The intake form is on `tenants.html`, and those buttons are plain links (`tenants.html#intake`). The query string does not carry over.

`rentals.html` keeps the query string when a person opens a listing (the listing id is a hash). `buyers.html` may lose a `#listings` fragment; the query string on that URL stays.

A later code change should, on the first page view, save `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `gclid`, and `fbclid` in `sessionStorage`, and include them as hidden fields on the three forms. Then the FormSubmit email itself shows the source, which is the useful version for Devin even when he is not in GA4.

Do not add those hidden fields in the ad-launch change. They are part of the tracking change, and `privacy.html` has to mention them.

## Privacy page (same later change)

`privacy.html` currently describes the forms, FormSubmit, the DDF analytics call to `analytics.crea.ca`, the Elfsight chat, and YouTube thumbnails. It does not mention Meta or Google advertising tags.

The update should say, in the same plain style as the rest of that page:

- The site uses a Meta Pixel and Google Analytics (GA4) to see which ads and pages lead to a form being sent
- What is sent: page address, a cookie or similar id, and, on a successful form, the fact of the submit plus the form name
- Form fields (name, email, phone) may be sent to Meta in hashed form for matching
- Meta and Google may process that information outside Canada, which is the same kind of disclosure the page already makes for FormSubmit and Elfsight
- How to opt out: browser controls, and Meta’s and Google’s own ad settings
- The existing line that people can call or email instead of using the forms stays

Do not paste a tag until that copy is on the live privacy page.

## How to test the later install

Use the pixel helper and GA4 DebugView, on a page that is already deployed.

1. Load each of the three landing URLs with a test UTM. Confirm a page view, and confirm `sessionStorage` holds the UTM.
2. Submit a real form with a clearly fake-but-deliverable note Devin expects (“TRACKING TEST”). Confirm one Lead and one custom event, not two Leads from a double binding.
3. Submit with the honeypot filled (or call the honeypot path). Confirm **no** event.
4. Confirm the form email still arrives and the thank-you still shows.
5. In Ads Manager, confirm the Housing campaigns can select the new event. If they cannot, leave them on landing page views and try again the next day. Do not switch a campaign to a broken event.

Delete or ignore the test leads on the Monday sheet so they do not count as return.

## What this plan will not do

- No tag on 1 November
- No Google Tag Manager account required (the site can call `gtag` and `fbq` directly; a container is optional and not worth a second tool for three events)
- No Conversions API and no offline-conversion upload
- No retargeting audience. Housing ads restrict them, and the traffic will be too small to remarket usefully
- No change to the DDF view beacon on listing pages (`analytics.crea.ca`). That call stays as it is
