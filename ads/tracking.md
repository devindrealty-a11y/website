# Conversion tracking plan

Parent: [README](README.md). This file is the specification. It does not add a pixel, a tag, or a script to the site. November launches on UTMs plus the inbox. The pixel and GA4 are a later, separate change, coordinated so they share one consent choice and one form-success trigger.

## Source of truth

| Question | Answered by | From |
| --- | --- | --- |
| Did we spend inside the cap? | Meta Ads Manager and Google Ads, invoices included | November 1 |
| Did a lead arrive, and did cash clear? | The lead log in [budget-and-roi.md](budget-and-roi.md#lead-log), filled from FormSubmit emails and the bank or e-transfer record | November 1 |
| Which ad was clicked? | UTMs on the final URL, plus Meta's ad-level clicks. Joined by hand until hidden fields exist | November 1 |
| Which page path did they take after the click? | GA4, once it is installed | Later change |
| Can Meta optimize for the form? | Meta pixel `Lead` event, once it fires on a real success | Later change |

Ads Manager revenue, a pixel value, and GA4 revenue are **not** added into the 2:1 ratio. The ratio uses fees collected and media spend, as defined in [strategy.md](strategy.md).

## Day-one tracking (no site code)

### UTM scheme

| Parameter | Tenant Meta | Buyer Meta | Tenant Google | Buyer Google |
| --- | --- | --- | --- | --- |
| `utm_source` | `meta` | `meta` | `google` | `google` |
| `utm_medium` | `paid-social` | `paid-social` | `cpc` | `cpc` |
| `utm_campaign` | `tenant-relocate` | `buyer-tricities` | `tenant-relocate` | `buyer-tricities` |
| `utm_content` | `t1` `t2` `t3` `t4` | `b1` `b2` `b3` `b4` | `{creative}` via the suffix | `rsa1` |
| `utm_term` | (omit) | (omit) | `{keyword}` via the suffix | (omit; hash must stay last) |

Full URLs are written out in [meta-ads.md](meta-ads.md) and [google-search.md](google-search.md).

### What the inbox can already tell apart

FormSubmit subjects, from the live forms:

| Subject | Form | Audience |
| --- | --- | --- |
| New relocation rental intake | `tenants.html` intake | Tenant service |
| New buyer listings request | `buyers.html` | Buyer |
| New rental inquiry | `rentals.html` detail | Browse lead, $0 unless they hire |
| New free home evaluation | `home-evaluation.html` | Not an ad destination. If one arrives, log it as organic unless the person names an ad. |
| New expert opinion request | `buyer-opinion.html` | Same. |

Phone calls and texts to 604-809-1032 that mention an ad get a log row with form = `phone`. Ask which ad or page. If they cannot say, `utm_content` stays blank and the row still counts as a lead for the channel only when you are sure it was paid.

### The gap this leaves open

`assets/js/site.js` posts the form fields to FormSubmit. It does not copy `utm_*` or the landing URL into the email. The relocation guide's links to `tenants.html#intake` also drop the query string.

So in November:

- Clicks are counted by Meta, per ad name.
- Leads are counted by emails received.
- The join is approximate: same day, origin city that matches the geo, and the person's answer about how they found the page.
- Cost per intake uses **all** intake emails in the week divided into tenant spend, unless a row is clearly organic (they say a friend, Google organic, or the blog sent them). Mark those `source=organic` and leave them out of the paid cost-per-intake. When you are unsure, mark `source=paid-unknown` and **include** them in the paid count. That bias makes the cost look a bit worse, which is the safer direction for a 2:1 gate.

## Later change: one consent gate, two free tools

Do this as its own site change, after November is underway or before it if someone has time. Do not block November 1 on it. The working ROI review does not need it. Optimization inside Meta's auction does.

### Tools

- **GA4**, the free Google Analytics property, as the on-site record: which landing page, which UTM, whether they reached the form, whether the success message showed.
- **Meta pixel**, standard events only, so a future Leads objective has something to optimize. Browser pixel only. This site is static GitHub Pages. A Conversions API would need a server or a worker. At $10 a day that extra pipe is not part of the plan.
- **Google Ads conversions**, imported from the GA4 `generate_lead` event, and only after phase 2 exists. One conversion definition per form key. Do not also paste a separate Google Ads tag that fires the same submit. That double-counts inside Google.

Both tags stay unloaded until the visitor accepts analytics. One banner, one choice, both tags. Refusing leaves the page working and the form working. The form email does not depend on the pixel.

### Privacy page, in the same change

`privacy.html` currently describes FormSubmit, the Elfsight chat widget, and the required DDF view beacon to `analytics.crea.ca`. It does not mention Meta or Google Analytics. The change that adds either tag updates that page in the same commit: what is collected (page address, UTMs, a lead event with no extra description of their budget or notes), that Meta and Google may process it outside Canada, and that the form still works if they decline. The existing DDF beacon stays as it is. It is a listing-view requirement, not part of this ads stack, and it should not be folded into the marketing consent banner.

BC PIPA is the privacy law that applies to this Port Moody practice. The banner is how the marketing tags stay optional. CASL is already handled on the forms: the consent checkbox is for contact about that request, not a standing newsletter. Paid leads are not added to a bulk marketing list on the back of that checkbox.

### Where the events fire

All form posts already funnel through one success branch in `assets/js/site.js`: the request returns ok, `success` is not the string `"false"`, the form resets, and the success message is shown. That is the only place a lead event fires.

Fire once per successful response. Do not fire on the "Next" button of the two-step intake. Do not fire when the honeypot path pretends success for a bot. Do not fire on the error message.

| `data-form-key` | Meta standard event | GA4 event | Parameters |
| --- | --- | --- | --- |
| `tenantIntake` | `Lead` | `generate_lead` | `lead_type=tenant_intake`, `form_id=tenantIntake` |
| `buyerListings` | `Lead` | `generate_lead` | `lead_type=buyer_listings`, `form_id=buyerListings` |
| `rentalInquiry` | `Lead` | `generate_lead` | `lead_type=rental_inquiry`, `form_id=rentalInquiry` |
| `listingInquiry`, `homeEvaluation`, `buyerOpinion` | (none for this ad account) | `generate_lead` with the matching `lead_type` | Logged so organic forms are visible. Not used as the Meta optimization event. |

No value parameter on the pixel, and no `value` on the GA4 event for these leads. Sending `1500` or `750` would make Ads Manager show fictional revenue every time someone hits Submit. Cash stays in the spreadsheet.

Optional, and easy to inflate: a `Contact` event on `tel:` clicks. If it is added, keep it out of the optimization goal. Calls are counted in the lead log when a conversation happens.

Page views: GA4's default page_view, plus the UTMs it stores automatically if the tag is on the first page. Meta `PageView` from the base pixel.

### Hidden fields, same change

On each `form[data-form-key]`, before the FormSubmit POST, set hidden inputs from the current query string and from `sessionStorage`:

- `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`
- `landing_url` (the first page URL of the visit, stored in `sessionStorage` when the query string contains `utm_source`)

On the relocation guide, when someone clicks through to `tenants.html`, the stored UTMs travel with the session even though the link itself has no query string. The intake email then contains `utm_content`, and the Monday log stops being a best guess.

### Deduping

A single submit will create one email, one GA4 `generate_lead`, and one Meta `Lead`. The weekly review counts **emails and cash**, not the sum of the three. When comparing channels, use GA4 for path and UTMs, and use Meta only for delivery metrics (spend, clicks, landing-page views). If the pixel count and the email count diverge by more than about 20% in a week, the pixel is wrong (fires missing, double fires, or consent opt-outs). Trust the inbox until they line up.

### Test procedure for that later change

1. Accept the banner in a private window. Confirm GA4 DebugView shows `page_view` with the test UTMs.
2. Decline in a second private window. Confirm no request to `facebook.com/tr` or `google-analytics.com`.
3. Submit the intake with a test name and the honeypot empty. Confirm exactly one `Lead` / `generate_lead`, and an email whose hidden fields match the URL.
4. Submit with the honeypot filled. Confirm no lead event.
5. Click "Next" on step one of the intake and abandon. Confirm no lead event.
6. Load the guide with UTMs, click through to the intake, submit. Confirm the email still has `utm_content`.
7. Update `privacy.html` and read it against what the network panel actually sends.

Until those seven pass, the Meta objective stays **Traffic / Landing page views**. After they pass, and after about a week of real `Lead` events, the tenant campaign may switch to website leads optimized on `Lead` where `lead_type=tenant_intake`. At $10 a day the campaign will still not collect Meta's usual 50 events a week. The switch is still worth it only if the event is clean. If lead volume is too low for delivery, switch back to landing-page views and keep using the log.

## What not to install

- A second pixel "just for the buyer campaign". One pixel, distinguished by `lead_type`.
- Hotjar, a session recorder, or a chat analytics add-on. Elfsight is already disclosed. Another recorder is a new privacy review.
- Google Tag Manager plus a raw GA4 tag plus a Google Ads tag all firing the same submit.
- Server-side CAPI, enhanced matching that uploads email addresses to Meta, or a customer list built from form emails. The form consent does not cover uploading their address to an ad platform.

## Coordination checklist

| Piece | November 1 | Later change |
| --- | --- | --- |
| UTM on every ad URL | Yes | Keep the same names |
| Lead log from email and cash | Yes | Keep it; it remains the 2:1 source |
| Hidden UTM fields + sessionStorage | No | Yes |
| Consent banner | No | Yes, one banner for both tags |
| `privacy.html` updated | No | Yes, same commit as the tags |
| GA4 | No | Yes |
| Meta pixel on the form success branch | No | Yes |
| Pixel value / predicted revenue | No | No |
| Google Ads import of GA4 leads | No | Yes, when Search is live and GA4 is live |
| Meta objective | Landing page views | Leads, only after the test procedure passes |
