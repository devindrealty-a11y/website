# Landing pages

Parent: [README](README.md). The ads use three pages that are already live. This plan does not add a page and does not edit these files.

| Ad | URL | Job of the page |
| --- | --- | --- |
| T1, T2, T3 | https://devindesaulniers.ca/relocating-to-greater-vancouver.html | Tell a relocating reader how Greater Vancouver is laid out, what renting in B.C. involves, and what the $1,500 + GST tenant service includes. The button goes to the intake form. |
| T4 | https://devindesaulniers.ca/rentals.html | Let someone search active residential rentals. Rent is per month. This is inventory, not the service contract. |
| B1–B4, and the Google buyer ad | https://devindesaulniers.ca/buyers.html#listings | Open the buyers page on the "Send me listings" form. |

The page that actually takes the tenant payment conversation is https://devindesaulniers.ca/tenants.html#intake. The relocation guide already links there ("Need a rental? Start here" and "Start your rental search"). It is the downstream conversion page. It is not a fourth ad URL in this test, because the brief lands traffic on the guide, the search, and the buyers page. If the November 16 review shows clicks on the guide and almost no intake emails, the next test is allowed to point T1 at `tenants.html#intake` directly. Write that change in the log before you edit the ad URL. The fee and the form on `tenants.html` already match the ads.

## Message match

### Relocation guide (T1–T3)

What the visitor just read in the ad: a move to Greater Vancouver, tenant-side help, $1,500 + GST in two parts, video or in-person showings, Devin Desaulniers at Axford in Port Moody.

What the page already says, in the same words:

- H1: "Relocating to Greater Vancouver? Here's how a local agent can help."
- The $1,500 total + GST, $750 at the start (non-refundable), $750 once a rental is secured.
- The 4–6 week search window.
- 28 years in Greater Vancouver, licensed since 2020, office at 2326 Clarke St, Port Moody.
- A button to `tenants.html#intake`.

The page also covers buying. That is fine. The hero button is the rental path, which matches T1–T3. Do not send these ads to `#buying`.

### Rentals search (T4)

What the ad says: active rentals, rent per month, and a separate sentence that out-of-province representation is $1,500 + GST.

What the page is: a search of the REALTOR.ca DDF feed (961 active residential rentals on the October 14, 2026 refresh; the count changes every 12 hours). Filters for city, rent, beds, baths, and type. A detail view with an inquiry form, email subject `New rental inquiry`.

Match is looser here, on purpose. Someone who only wants to browse should be able to browse. Someone who wants to hire Devin has to find the Tenants link in the nav. That is a weaker path than the guide, which is why T4 is one ad in the set and not the whole campaign. A `New rental inquiry` is logged at **$0** toward the 2:1 ratio unless the person later books the tenant service.

If most T4 clicks become "is this suite still available?" from people already in Metro Vancouver, pause T4. The origin-city targeting reduces that, and it will not eliminate it, because friends and family forward links.

### Buyers page (B1–B4)

What the ad says: Tri-Cities buying, a clear sequence, listings that match a price range, an estimate-only mortgage calculator.

What the page already says:

- H1: "Buying in the Tri-Cities, BC & Greater Vancouver."
- Services: goals and budget, listing alerts, showings, comparable sales, the offer, subjects, completion.
- Neighbourhood notes for Coquitlam, Port Coquitlam, and Port Moody.
- The form at `#listings`: name, email, phone, property type, areas, price range, beds, baths, timeline, pre-approval, notes, and a consent checkbox.
- The calculator link, with the site-wide line that results are estimates and not a mortgage approval.

The URL's `#listings` hash is there so the ad opens on the form rather than on the top of a long guide. The guides above the form are a bonus for anyone who scrolls up. They are not required before the form will submit.

## The two forms that count

| Form | Where | `data-form-key` | Email subject | Counts as |
| --- | --- | --- | --- | --- |
| Relocation rental intake | `tenants.html#intake` | `tenantIntake` | New relocation rental intake | The tenant lead. Qualified or not in the log. Revenue only when $750 clears. |
| Send me listings | `buyers.html#listings` | `buyerListings` | New buyer listings request | The buyer lead. Qualified when the timeline is inside 6 months and a price range is filled in. Revenue only when a purchase pays. |

Both forms post through FormSubmit to devin@axfordrealestate.ca, via `assets/js/config.js`. Both require a consent checkbox for contact about that request. Both have a honeypot field. The site's own notes say the first real submission is held until Devin clicks the FormSubmit activation email. **Confirm a test message has arrived before November 1.** Do not spend against a form that is still waiting on that click.

The intake is two steps (contact details, then rental needs). Count a lead only when the email arrives, not when someone taps "Next".

## A tracking gap to know about before launch

The relocation guide's buttons point at `tenants.html#intake` **without** copying the ad's query string. A person who clicks T1, reads the guide, and then submits the intake will not carry `utm_content=t1` onto the form, and the form does not yet store UTMs in the email.

Until the tracking change in [tracking.md](tracking.md) is built:

- Meta still records the click on T1, T2, T3, or T4.
- The inbox records that an intake arrived, and the time.
- The lead log joins them by time and by the answer to "where are you moving from?"
- The first reply can include one line: "If you came in from a page or an ad, which one was it?" Write the answer in the log. It will be incomplete. It is still enough to pause a silent ad.

Do not "fix" this by editing the HTML in the ads launch. The tracking doc describes the later, separate change: keep UTMs in `sessionStorage` and add hidden fields on the forms. That change also updates `privacy.html`. It is out of scope here.

`buyers.html#listings` is a same-page form, so the query string is still in the address bar when they submit. The email will not contain it until those hidden fields exist. The log note for buyer leads is the same: time, timeline, and which buyer ad was spending.

## Pre-launch checks (phone, not a desktop screenshot)

Do this once, on a phone, for each final URL in [meta-ads.md](meta-ads.md), including the query string.

1. The page loads on cellular data in a few seconds. Hero text is the relocation promise, the rentals search, or the buyers form, matching the ad.
2. The phone number in the header is tap-to-call: 604-809-1032.
3. On the guide, "Need a rental? Start here" reaches the intake form.
4. On the buyers URL, the listings form is on screen without hunting. Required fields block an empty submit.
5. Submit one real intake and one real buyer request from a personal address. Confirm both emails arrive with the subjects above. Then mark those two rows in the lead log as `test` so they never enter the cost-per-lead math.
6. Submit nothing on `rentals.html` unless you open a sample listing in local preview. A public test inquiry about a real listing emails Devin and names a real address. Skip that test, or send it only if you are prepared to disregard it and you say so in the log.
7. Privacy page still describes the forms and does not mention a Meta pixel or GA4. That remains true at launch.

## When a page and an ad drift

If the fee, the two-part split, the phone number, or the "I work for the tenant" description changes on the site, pause T1–T4 the same day and update the primary text and Static A before they run again. The buyers ads pause if the form fields or the Tri-Cities focus change enough that the headline is no longer true.
