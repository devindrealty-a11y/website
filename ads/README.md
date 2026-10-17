# Paid ads launch plan — Devin Desaulniers, Axford Real Estate

Internal plan for a small paid-ads test. Start date: **Sunday, November 1, 2026**. Currency: **CAD**. Nothing in this folder is wired to an ad account, a pixel, or the website. Publishing these files does not spend money and does not add tracking code.

The repository is public, and GitHub Pages may serve these Markdown files as static files. They are operating notes for the ad account. They are not linked from the site menu.

The person running the account is Devin Desaulniers, Real Estate Associate, Axford Real Estate, 2326 Clarke St, Port Moody, BC V3H 1Y8. Direct line: 604-809-1032. Leads already go to devin@axfordrealestate.ca through FormSubmit.

## What this test is selling

| Audience | Offer | Where the ad sends them | Where the lead is captured |
| --- | --- | --- | --- |
| People relocating to Greater Vancouver who need a rental | Tenant-side search. **$1,500 + GST**, paid by the tenant: **$750** at the start (non-refundable) and **$750** once a rental is secured. | [relocating-to-greater-vancouver.html](https://devindesaulniers.ca/relocating-to-greater-vancouver.html) and, as a controlled test, [rentals.html](https://devindesaulniers.ca/rentals.html) | Intake form on [tenants.html#intake](https://devindesaulniers.ca/tenants.html#intake). Email subject: `New relocation rental intake`. |
| Buyers in the Tri-Cities and Greater Vancouver | Buyer representation: neighbourhood context, listing alerts, showings, comparable sales, offer through keys. | [buyers.html#listings](https://devindesaulniers.ca/buyers.html#listings) | "Send me listings" form. Email subject: `New buyer listings request`. |

Both offers are already written on the site. Ads repeat that wording. They do not add a guarantee, a different fee, or a promise that a home will be secured.

## How the money is staged

Working budget **$200–$500 per month**. Hard ceiling **$1,000 cash in a calendar month** across Meta and Google, including GST on the ad invoices. The working target is the middle of the band, about **$400 in November**.

- **Phase 1, from November 1:** Facebook and Instagram only (one Meta ad account, Housing special ad category).
- **Phase 2, earliest Monday, December 7, 2026:** a small Google Search test, and only if the November 30 check says the tenant campaign is producing qualified intakes inside the cost cap. Google does not start automatically.

The return target is **at least 2:1**: fees actually collected (GST excluded) divided by media spend (GST excluded if that GST is being claimed back). A form fill is not revenue. The definitions, the November split, and the Monday checklist are in [budget-and-roi.md](budget-and-roi.md).

## Read this in order

| File | Use it to |
| --- | --- |
| [strategy.md](strategy.md) | See the offers, the 2:1 math, and the gates between phases. |
| [targeting.md](targeting.md) | Build the audiences inside Meta's housing rules and Google's location settings. |
| [meta-ads.md](meta-ads.md) | Paste the November campaigns, the four copy variants per audience, and the URLs. |
| [google-search.md](google-search.md) | Build the December search test if the gate opens. |
| [creative-briefs.md](creative-briefs.md) | Make the images and cut the video from assets the site already has. |
| [landing-pages.md](landing-pages.md) | Check message match on the three pages before spend starts. |
| [tracking.md](tracking.md) | Attribute leads with UTMs and the inbox from day one. Pixel and GA4 are specified for a later change. |
| [budget-and-roi.md](budget-and-roi.md) | Set the daily budgets, the caps, and the Monday ROI review. |

## Launch order

Do these before any campaign is switched on. The checkbox list with owners is in [budget-and-roi.md](budget-and-roi.md#before-november-1).

1. Confirm Axford is fine with this copy, the Housing category, and the fee appearing in the ads.
2. Confirm FormSubmit is activated and a real intake email arrives at devin@axfordrealestate.ca. The site notes say the first submission is held until that activation link is clicked.
3. Re-check the Google review counts if any ad or image will cite them. The site's figures (Devin 5.0 from 15 reviews as of October 3, 2026; Axford 148 five-star reviews as of October 2, 2026) will be stale by November.
4. Export the creative in [creative-briefs.md](creative-briefs.md). The 32-second relocation video already on the homepage is enough to launch. New cuts can follow.
5. In Meta, create the campaigns in [meta-ads.md](meta-ads.md) as **paused**. Set the account spending limit. Open each final URL on a phone.
6. Start the lead log in [budget-and-roi.md](budget-and-roi.md#lead-log). That spreadsheet is the source of truth for the 2:1 figure until a later change adds the pixel.
7. On November 1, turn on the two Meta campaigns. Leave Google off.
8. Monday, November 2: smoke check (ads approved, site up, lead log ready). Monday, November 9: first full ROI review.

## What this folder deliberately leaves alone

- No Meta pixel, no Google tag, and no GA4 snippet in the HTML or JavaScript.
- No change to `privacy.html`. That page has to be updated in the same change that eventually adds a pixel or GA4. See [tracking.md](tracking.md).
- No new landing page. The three URLs above are the ad destinations. The intake form stays on `tenants.html`, which the relocation guide already links to.
- No instant lead forms inside Facebook. The fee, the two payments, and the scope need to stay on the site, where they are already spelled out.
- Listing photos from the REALTOR.ca DDF feed stay out of the ads. Those homes belong to other brokerages.
