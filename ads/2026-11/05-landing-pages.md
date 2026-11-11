# Landing pages

The ads use pages that are already live. This package does not change them.

The click and the lead are different events. A landing-page view is not a qualified inquiry. The renter form that emails Devin sits on `tenants.html`. The ad URL below is the relocating guide, because that page states the fee, the service, and the path to the form in one place.

## Renter ads (Flight 1) — relocating guide

**URL (video).** Copy the whole line, including the hash.

```
https://devindesaulniers.ca/relocating-to-greater-vancouver.html?utm_source=meta&utm_medium=paid&utm_campaign=gv-reloc-2026-11&utm_content=video&utm_term=renters#rentals
```

Swap `utm_content` for the stills: `still-skyline`, `still-skytrain`, `still-coquitlam`.

| | |
| --- | --- |
| Page | https://devindesaulniers.ca/relocating-to-greater-vancouver.html |
| Section the ad opens | `#rentals` — “How I help relocating tenants” |
| What the visitor sees there | The fee in the first paragraph: **$1,500 total + GST, paid by the tenant**, $750 at the start (non-refundable) and $750 once a rental is secured. Then consultation, search, showings or live video, and lease review. |
| Button | “Start your rental search” goes to `tenants.html#intake` |
| Form that creates the email | `tenants.html`, subject “New relocation rental intake”, to devin@axfordrealestate.ca |
| Phone on the page | 604-809-1032 |

The form does not store the UTM. Attribution for the four ads is the question in the tracking plan, plus the click counts in Ads Manager. Do not expect the email to name the ad.

Check on a phone before launch: the `#rentals` block is on screen, the fee is in that block, and the button reaches the form. The guide above that block (areas, tenancy basics) is useful after they inquire. It is not the ad’s promise.

## Buyer ads (parked) — buyers page

```
https://devindesaulniers.ca/buyers.html?utm_source=meta&utm_medium=paid&utm_campaign=gv-reloc-2026-11&utm_content=buyer-remote&utm_term=buyers#listings
```

Swap `utm_content` to `buyer-tricities` or `buyer-newjob`. Variant B4 uses the **renter** URL with `utm_content=buyer-rent-first`, because B4 offers the tenant service.

| | |
| --- | --- |
| Page | https://devindesaulniers.ca/buyers.html |
| Section | `#listings` — “Send me listings” |
| What they can do | Leave name, email, areas, price range, timeline, and whether they are pre-approved |
| Email subject | “New buyer listings request” |
| What this lead is worth in the ROI sheet | Nothing, until a buyer fee is actually received. Do not enter $1,500 on a buyer form. |

The page is about buying in the Tri-Cities and Greater Vancouver: neighbourhood notes, a mortgage calculator link, and the listing form. It does not sell the tenant package. Renter ads stay on the relocating URL so the fee the ad states is the fee the page states.

## Later Google test — two pages

**Relocation keywords** use the same relocating URL as the renter ads, with:

```
utm_source=google&utm_medium=cpc&utm_campaign=gv-search-later&utm_content=relocation-realtor
```

**“Coquitlam rentals” and the other listing keywords** use:

```
https://devindesaulniers.ca/rentals.html?utm_source=google&utm_medium=cpc&utm_campaign=gv-search-later&utm_content=coquitlam-rentals
```

| | |
| --- | --- |
| Page | https://devindesaulniers.ca/rentals.html |
| What it is | A search of active residential rentals in Greater Vancouver and the Fraser Valley. Rent is per month. |
| Inquiry | On a listing, “Ask Devin about this rental.” Email subject “New rental inquiry.” That message is about one home. It is not the Tenant Relocation Service. |
| City in the URL | The search box does not read a city from the link. Someone who clicks still has to type Coquitlam. The ad copy should say they can search it there, not that the list will already be filtered. |

Count rental-listing emails in their own column. They are not the numerator of the 2:1 return.

## Promise check

| Ad says | Page must show | Match |
| --- | --- | --- |
| Moving to Greater Vancouver, rental before you arrive | Relocating hero and the `#rentals` section | Yes |
| $1,500 + GST, paid by the tenant | First paragraph of `#rentals`, and the tenants page | Yes |
| $750 to start, non-refundable, and $750 when a rental is secured | Same paragraph. Leave this detail on the page. | Yes |
| Tenant side, not the landlord’s list | “I represent your search on the tenant side” | Yes |
| Buying from out of province | Buyers page, “How I help buyers,” and the relocating page’s buying section | Yes, on buyer ads only |
| Coquitlam rentals for browsing | Rentals search | Yes, and it is a different offer |

If a sentence is not on the page it links to, cut the sentence. Do not edit the page to catch up to an ad during this test.

## UTM names (keep them stable)

| Parameter | Values in this test |
| --- | --- |
| utm_source | `meta` or, later, `google` |
| utm_medium | `paid` or, later, `cpc` |
| utm_campaign | `gv-reloc-2026-11` (Meta) or `gv-search-later` |
| utm_content | `video`, `still-skyline`, `still-skytrain`, `still-coquitlam`, or a buyer code |
| utm_term | `renters` or `buyers` |

The hash (`#rentals` or `#listings`) goes last.
