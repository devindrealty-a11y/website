# Out-of-area listings

The homes-for-sale feed (`listings/data.json`) and the rentals feed (`listings/rentals.json`) come from the REALTOR.ca DDF pull. That pull keeps Greater Vancouver and the Fraser Valley only. A Penticton listing, or any other listing outside that area, will not survive the 12-hour refresh unless it is in the manual file.

The manual file is the source of truth. The refresh merges it back in after rewriting the feed. It does not edit the file. `scripts/check_realtor_links.py` does not delete these rows, even when REALTOR.ca answers 404.

## Add one

1. Edit `data/manual-listings.json`. Add an object to `listings`. Copy the Penticton entry and replace the facts. Do not invent facts, and do not copy listing photos unless the licence is explicit.
2. Run:

```
python3 scripts/fetch_ddf_listings.py --merge-manual
```

3. Commit `data/manual-listings.json`, the `listings/` changes (feed, shard, page, `listings/manual-pages.json`), and any new photo under `assets/img/manual-listings/`. Do not commit the root `CNAME` file.

The shareable page is generated at `listings/<id>-<address-slug>.html`. For `#204-3589 Skaha Lake Road` in Penticton that is:

`https://devindesaulniers.ca/listings/30357378-204-3589-skaha-lake-road-penticton.html`

The search also opens it at `https://devindesaulniers.ca/listings.html#<id>` (rentals use `rentals.html#<id>`). The HTML page is the link to send. It does not wait on the large feed file. Both have to keep working.

The next DDF refresh merges this file again, so the listing stays after `listings/data.json` is replaced.

## Fields

Required: `id` (the REALTOR.ca property id, not the MLS number), `mls`, `price`, `address`, `city`, `brokerage`, `realtorUrl`.

`realtorUrl` must be a working `https://www.realtor.ca/real-estate/<id>/<slug>` URL. Open it and confirm the slug. An id with no slug is a 404, and the slug built from the address can be wrong. The checker keeps a URL that already has a slug.

Usual optional fields: `intent` (`sale` or `rent`), `province`, `postal`, `beds`, `baths`, `type` (use an existing search label such as `Condo / apartment`), `sqft`, `year`, `parking`, `remarks`, `facts` (list of `[label, value]`), `courtesy` (for example `Listing courtesy of Summerland Realty Ltd.`), `updated` (fixed ISO time; leave it stable so the refresh does not rewrite the feed just to bump a clock).

Photos: `photos` is a list of `https://` URLs or site-root paths such as `/assets/img/manual-listings/example.jpg`. Set `photoCaption` so the picture is labelled as an area photo when it is not the unit. Set `photoCredit`, `photoCreditUrl`, `photoLicense`, `photoLicenseUrl`, and `photoChange` when the file was resized. Prefer a Wikimedia Commons photo under CC BY, CC BY-SA, or CC0. Do not hotlink another brokerage's listing photos.

The page names Axford Real Estate as Devin's brokerage (site header and footer). The listing brokerage goes in `brokerage` and `courtesy`. Do not write "best", "top", or "expert". The page already includes the disclaimer that the information is believed accurate but not guaranteed and should be verified.

## Remove or expire

- Delete the object, or set `"active": false`, or set `"expires": "YYYY-MM-DD"`.
- `expires` is the last day it is included, in Vancouver time. The next day it is gone.
- Run `--merge-manual`, or wait for the 12-hour workflow. That drops the card, the shard text, and the HTML page listed in `listings/manual-pages.json`.

Leaving the JSON in place and only deleting the HTML page does not work. The next refresh rebuilds the page from the JSON.
