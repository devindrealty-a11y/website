# Monthly Tri-Cities, BC market report

The pages at `market-report/` are generated. Edit a JSON file, then rebuild. Do not hand-edit the HTML or the PDF.

## Add next month

1. Copy the latest file in `_build/market_data/` to `_build/market_data/YYYY-MM.json`.
   The file name is the edition (the month you publish it). `2026-10.json` is the October 2026 edition and it covers September 2026, because that was the month Greater Vancouver REALTORS had released.
2. Replace the figures with the new statistics package. Use only numbers printed in:
   - the Greater Vancouver REALTORS monthly release (Coquitlam, Port Coquitlam, Port Moody benchmarks; Coquitlam, Port Coquitlam, and Port Moody/Belcarra sales and new listings)
   - the Fraser Valley Real Estate Board release, and only as Fraser Valley context. Those cities are not the Tri-Cities, BC.
3. Keep the area order: Coquitlam, Port Coquitlam, Port Moody.
   Benchmarks: All residential, Detached, Townhouse, Apartment.
   Activity: Detached, Attached, Apartment.
   Leave `median` as `null` when the board does not publish one (fewer than 20 sales).
4. Rebuild:

```bash
cd /workspace/_build && python3 build.py
```

`python3 market_report.py` alone rewrites `market-report/` (HTML and PDF). `build.py` does that and also refreshes the shared footer, buyers page, blog index, privacy page, and `sitemap.xml`.

## What the script checks

- Month-over-month percents match the sales and new-listing counts (half-up, one decimal).
- The printed sales-to-listings percent matches sales divided by new listings.
- Every dollar amount and percent on the page is one of those figures, or a sum or year-over-year percent calculated from them.
- The page says Tri-Cities, BC, names Axford Real Estate, and does not say best, top, or guaranteed.

Buyer, seller, and FAQ wording is generated from the JSON. You do not write that copy by hand. If a sentence is wrong for the new month, change the generator in `_build/market_report.py` rather than the HTML.

## PDF and the download form

The PDF is `market-report/tri-cities-bc-market-report-YYYY-MM.pdf`. Chrome headless writes it. The page does not show the file until the form succeeds.

The form posts with `fetch` to `marketReport` in `assets/js/config.js` (`https://formsubmit.co/ajax/devin@axfordrealestate.ca`). The subject is `Market report download: <name>`. Do not test-submit it. The first real submission is the one that asks Devin to activate FormSubmit.

After a successful response, `assets/js/market-report.js` sends the GoatCounter event `report-download` and reveals the PDF link. The event does not include the name or email.

## Sources to cite

Put each release in `sources` with the publisher, the release date, and the public URL. The page links those. Do not add a number you cannot point at in one of those files.
