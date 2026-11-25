# Manual listings

**Only listings from Devin's own board (Greater Vancouver / Fraser Valley) may be added. Never add an out-of-board listing without written permission from the listing brokerage AND their full photo set.**

Okanagan, Penticton, and any other board outside Greater Vancouver and the Fraser Valley are out of board. Advertising one without that written permission is not allowed. Do not publish it on `listings.html`, in `listings/data.json`, or on its own page.

The homes-for-sale feed (`listings/data.json`) and the rentals feed (`listings/rentals.json`) come from the REALTOR.ca DDF pull for those two board areas. `data/manual-listings.json` is only for a listing the pull missed, or for an out-of-board listing that already has the written permission and the brokerage's own photos. The refresh merges this file back in after it rewrites the feed. It does not edit the file. `scripts/check_realtor_links.py` does not delete these rows.

## Add one

1. Confirm the listing is in Greater Vancouver or the Fraser Valley. If it is not, stop unless you have written permission from the listing brokerage and their full photo set. A Wikimedia stand-in is not that photo set.
2. Edit `data/manual-listings.json`. It is a JSON array. Add one object. Do not invent facts. Use the listing brokerage's photos when they supplied them.
3. Run:

```
python3 scripts/fetch_ddf_listings.py --merge-manual
```

4. Commit `data/manual-listings.json`, the `listings/` changes (feed, shard, page, `listings/manual-pages.json`), and any new photo under `assets/img/manual-listings/`. Do not commit the root `CNAME` file.

The shareable page is generated at `listings/<id>-<address-slug>.html`. The search opens the same home at `listings.html#<id>` (rentals use `rentals.html#<id>`). The HTML page is the link to send. The next DDF refresh merges this file again.

## Fields

Required: `id` (the REALTOR.ca property id, not the MLS number), `mls`, `price`, `address`, `city`, `brokerage`, `realtorUrl`.

`realtorUrl` must be a working `https://www.realtor.ca/real-estate/<id>/<slug>` URL. Open it and confirm the slug. An id with no slug is a 404, and the slug built from the address can be wrong. The checker keeps a URL that already has a slug.

Usual optional fields: `intent` (`sale` or `rent`), `province`, `postal`, `beds`, `baths`, `type` (use an existing search label such as `Condo / apartment`), `sqft`, `year`, `parking`, `remarks`, `facts` (list of `[label, value]`), `courtesy` (for example `Listing courtesy of the listing brokerage.`), `updated` (fixed ISO time; leave it stable so the refresh does not rewrite the feed just to bump a clock).

Photos: `photos` is a list of `https://` URLs or site-root paths such as `/assets/img/manual-listings/example.jpg`. For an out-of-board listing that has written permission, use the listing brokerage's full photo set. Do not hotlink another brokerage's listing photos, and do not substitute an area photo.

The page names Axford Real Estate as Devin's brokerage (site header and footer). The listing brokerage goes in `brokerage` and `courtesy`. Do not write "best", "top", or "expert". The page already includes the disclaimer that the information is believed accurate but not guaranteed and should be verified.

## Remove or expire

- Delete the object, set `"active": false`, or set `"expires": "YYYY-MM-DD"`. An empty file is `[]`.
- `expires` is the last day it is included, in Vancouver time. The next day it is gone.
- Run `--merge-manual`, or wait for the 12-hour workflow. That drops the card, the shard text, and the HTML page listed in `listings/manual-pages.json`.

Deleting only the HTML page does not work. The next refresh rebuilds the page from the JSON.
