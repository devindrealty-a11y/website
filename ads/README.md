# Paid ads — ready to launch 1 November 2026

Launch package for **Devin Desaulniers, REALTOR®**, Real Estate Associate, **Axford Real Estate** (Port Moody). The test starts **Sunday 1 November 2026**.

This folder is the plan. It does not create ad accounts, add a payment method, or spend money. It does not add a Meta Pixel, GA4, or any other tracking code, and it does not change the live pages.

## What the test is for

Reach people who are **relocating to Greater Vancouver**:

1. **Renters** for the tenant-side placement service: **$1,500 + GST**, paid by the tenant in two parts ($750 at the start, non-refundable, and $750 once a rental is secured).
2. **Buyers** who want a local REALTOR® before they arrive.

Meta (Facebook and Instagram) is the main channel. Google Search is a small test on queries such as “Coquitlam rentals” and “relocation realtor Vancouver”.

Default pace is **$300 in November** (inside the $200–$500 a month range). The hard stop is **$1,000** of platform spend. The target is **at least 2:1**: invoiced tenant fees (before GST) plus buyer commission Devin has actually received, divided by platform spend.

## Read in this order

| Doc | Use it to |
| --- | --- |
| [budget-and-return.md](budget-and-return.md) | Set the dollars, the cap, and the 2:1 math |
| [targeting.md](targeting.md) | Build the Housing-category audiences and the keyword lists |
| [copy.md](copy.md) | Paste the ads (4 variants for each audience) |
| [creative-briefs.md](creative-briefs.md) | Make the images and the video cuts |
| [landing-pages.md](landing-pages.md) | Point each ad at the right live URL |
| [tracking-plan.md](tracking-plan.md) | Install Meta Pixel and GA4 later, on the forms that already exist |
| [weekly-roi-check.md](weekly-roi-check.md) | Run the Monday check and decide whether to continue |
| [launch-checklist.md](launch-checklist.md) | Broker sign-off, then the clicks in Ads Manager |

## Defaults a media buyer can follow without a meeting

- **Currency:** CAD. If an ad account is in USD, do not launch until it is CAD. The cap is meaningless in another currency.
- **Month 1 spending limits:** Meta renters $180, Meta buyers $60, Google Search $60. **$300 total.**
- **Cap:** pause everything when Ads Manager plus Google Ads reach **$1,000** of media spend. Sales tax on the card, if any, is outside that number.
- **Final URLs** (details and UTMs in [landing-pages.md](landing-pages.md)):
  - Relocating renters → `https://devindesaulniers.ca/relocating-to-greater-vancouver.html`
  - Buyers → `https://devindesaulniers.ca/buyers.html`
  - “Coquitlam rentals” and the other rental-search ads → `https://devindesaulniers.ca/rentals.html`
- **Special ad category:** Housing, on every Meta campaign, before the audience is built.
- **Do not publish** until Axford’s managing broker has approved the copy. Advertising compliance sits with the brokerage.

## What a lead actually is

The site already emails Devin through FormSubmit. Until the tracking plan is built, the inbox is the record.

| Email subject | Form | Counts toward |
| --- | --- | --- |
| New relocation rental intake | `tenants.html` (`tenantIntake`) | Renter ads. The relocating guide sends people here. |
| New buyer listings request | `buyers.html` (`buyerListings`) | Buyer ads |
| New rental inquiry | `rentals.html` (`rentalInquiry`) | Google rental-search ads |

A rental inquiry is someone asking about a listed home. It is not, by itself, a $1,500 placement. The Monday sheet keeps those separate so the ratio stays honest.

## Accounts this package does not open

- Meta Business Manager, Ads Manager, or a payment method
- Google Ads or a payment method
- A Meta Pixel, a GA4 property, or Google Tag Manager
- Changes to `privacy.html`, the forms, or any live HTML

When Devin is ready to spend, he uses his own login and his own card, after the [launch checklist](launch-checklist.md).
