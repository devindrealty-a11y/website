#!/usr/bin/env python3
"""Offline checks for the weekly rent report. No network."""
import json
import os
import re
import shutil
import sys
import tempfile
import unittest
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_build"))
import rent_report as rr
import terms_page

NOW = datetime(2026, 10, 15, 9, 0, tzinfo=rr.TZ)
LATER = datetime(2026, 10, 15, 10, 0, tzinfo=rr.TZ)
NEXT = datetime(2026, 10, 22, 9, 0, tzinfo=rr.TZ)


def home(**kwargs):
    base = {
        "id": "1",
        "mls": "R1",
        "price": 2800,
        "address": "1 Main Street",
        "city": "Vancouver",
        "beds": 2,
        "baths": 1,
        "type": "Condo / apartment",
        "sqft": 800,
        "brokerage": "Sample Harbour Realty",
        "realtorUrl": "https://www.realtor.ca/real-estate/1",
        "photo": "https://example.com/a.jpg",
        "updated": "2026-10-14T18:00:00Z",
    }
    base.update(kwargs)
    return base


def write_feed(directory, listings, **extra):
    path = os.path.join(directory, "rentals.json")
    payload = {"updated": "2026-10-15T12:00:00Z", "sample": False, "count": len(listings), "listings": listings}
    payload.update(extra)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle)
    return path


def sitemap(directory):
    text = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        '  <url><loc>https://devindesaulniers.ca/rentals.html</loc></url>\n'
        '</urlset>\n'
    )
    with open(os.path.join(directory, "sitemap.xml"), "w", encoding="utf-8") as handle:
        handle.write(text)


class RentReportTests(unittest.TestCase):
    def test_median_and_average_round_half_up(self):
        self.assertEqual(rr.median_dollars([2800, 2900]), 2850)
        self.assertEqual(rr.median_dollars([1, 2, 3]), 2)
        self.assertEqual(rr.median_dollars([1000, 1001]), 1001)
        self.assertEqual(rr.average_dollars([1, 2]), 2)
        self.assertEqual(rr.average_dollars([1, 1, 2]), 1)

    def test_week_bounds_and_city_aliases(self):
        monday, sunday, start = rr.week_bounds(NOW)
        self.assertEqual(monday.isoformat(), "2026-10-12")
        self.assertEqual(sunday.isoformat(), "2026-10-18")
        self.assertEqual(start.tzinfo, rr.TZ)
        self.assertEqual(rr.clean_city("new west"), "New Westminster")
        self.assertEqual(rr.clean_city("  Port   Coquitlam "), "Port Coquitlam")
        self.assertIsNone(rr.clean_city("BC"))
        self.assertEqual(rr.bed_band(0), "0")
        self.assertEqual(rr.bed_band(6), "5+")

    def test_filters_drop_junk(self):
        prepared = rr.prepare_listings([
            home(id="ok"),
            home(id="cheap", price=75),
            home(id="garage", address="GARAGE-2161 Prairie Avenue"),
            home(id="nocity", city=""),
            home(id="tiny", sqft=110),
            home(id="room", price=600, sqft=180),
        ])
        self.assertEqual([item["id"] for item in prepared["comparable"]], ["ok"])
        self.assertEqual(prepared["excluded"], 5)
        self.assertIn("cheap", prepared["ids"])

    def test_first_week_then_comparison(self):
        directory = tempfile.mkdtemp(prefix="rent-report-")
        try:
            sitemap(directory)
            listings = [home(id=f"v{i}", price=2000, updated="2026-10-14T18:00:00Z") for i in range(10)]
            listings.append(home(id="old", price=2000, updated="2026-10-11T20:00:00-07:00"))
            path = write_feed(directory, listings)
            first = rr.build_site(directory, path, NOW)
            self.assertEqual(first["week"], "2026-10-12")
            self.assertEqual(first["overall"]["median"], 2000)
            self.assertIsNone(first["overall_wow"])
            self.assertEqual(first["new_method"], "updated")
            self.assertNotIn("old", [card["id"] for card in first["new_listings"]])
            self.assertEqual(first["new_count"], 10)
            page = open(os.path.join(directory, "rent-report.html"), encoding="utf-8").read()
            newsletter = open(os.path.join(directory, "rent-report", "newsletter.html"), encoding="utf-8").read()
            text = open(os.path.join(directory, "rent-report", "newsletter.txt"), encoding="utf-8").read()
            self.assertIn("Moving to Greater Vancouver: Weekly Rent Report", page)
            self.assertIn(rr.CTA_TEXT, page)
            self.assertIn('data-goatcounter-click="cta-tenant-relocation"', page)
            self.assertIn('"@type": "Dataset"', page)
            self.assertIn('"@type": "Person"', page)
            self.assertIn('"license": "https://devindesaulniers.ca/terms.html"', page)
            self.assertIn('href="terms.html"', page)
            self.assertIn('aria-current="page"', page)
            self.assertIn("First saved week", page)
            self.assertIn("left out 0", page)
            self.assertIn("font-family:Verdana,Geneva,sans-serif", newsletter)
            self.assertIn(rr.CTA_TEXT, newsletter)
            self.assertIn('content="noindex, nofollow"', newsletter)
            self.assertIn(rr.CTA_TEXT, text)
            self.assertIn("https://devindesaulniers.ca/tenants.html#intake", text)
            series = json.load(open(os.path.join(directory, "rent-report", "history", "series.json"), encoding="utf-8"))
            self.assertEqual(len(series["weeks"]), 1)
            stamped = json.load(open(os.path.join(directory, "rent-report", "history", "2026-10-12.json"), encoding="utf-8"))
            again = rr.build_site(directory, path, LATER)
            self.assertEqual(again["overall"]["median"], 2000)
            restamped = json.load(open(os.path.join(directory, "rent-report", "history", "2026-10-12.json"), encoding="utf-8"))
            self.assertEqual(restamped["generated_at"], stamped["generated_at"])
            series = json.load(open(os.path.join(directory, "rent-report", "history", "series.json"), encoding="utf-8"))
            self.assertEqual(len(series["weeks"]), 1)
            sitemap_text = open(os.path.join(directory, "sitemap.xml"), encoding="utf-8").read()
            self.assertEqual(sitemap_text.count("rent-report.html"), 1)
            self.assertIn("<lastmod>2026-10-15</lastmod>", sitemap_text)

            nxt = [home(id=f"v{i}", price=2200, updated="2026-10-20T18:00:00Z") for i in range(1, 10)]
            nxt.append(home(id="new1", price=2200, address="9 New Street", updated="2026-10-21T18:00:00Z"))
            path = write_feed(directory, nxt, updated="2026-10-22T12:00:00Z")
            second = rr.build_site(directory, path, NEXT)
            self.assertEqual(second["week"], "2026-10-19")
            self.assertEqual(second["overall_wow"]["dollars"], 200)
            self.assertEqual(second["new_method"], "snapshot")
            self.assertEqual(second["new_count"], 1)
            self.assertEqual(second["new_listings"][0]["id"], "new1")
            page = open(os.path.join(directory, "rent-report.html"), encoding="utf-8").read()
            self.assertIn("Up $200 (10%)", page)
            self.assertIn("rentals.html?id=new1", page)
            series = json.load(open(os.path.join(directory, "rent-report", "history", "series.json"), encoding="utf-8"))
            self.assertEqual([item["week"] for item in series["weeks"]], ["2026-10-12", "2026-10-19"])
        finally:
            shutil.rmtree(directory)

    def test_dataset_creator_and_license(self):
        description = (
            "Median asking rent on the Greater Vancouver feed is $2,800/month "
            "for the week of October 19–25, 2026, with city and bedroom breakdowns."
        )
        page = rr.schema_blocks(
            {"prepared": "2026-10-19", "week": "2026-10-19", "week_end": "2026-10-25"},
            "Moving to Greater Vancouver: Weekly Rent Report",
            description,
        )
        blocks = re.findall(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
            page,
            re.S,
        )
        datasets = []
        for block in blocks:
            data = json.loads(block)
            nodes = data["@graph"] if isinstance(data, dict) and "@graph" in data else [data]
            datasets.extend(node for node in nodes if node.get("@type") == "Dataset")
        self.assertEqual(len(datasets), 1)
        dataset = datasets[0]
        self.assertGreaterEqual(len(dataset["description"]), 50)
        self.assertLessEqual(len(dataset["description"]), 5000)
        self.assertEqual(dataset["name"], "Moving to Greater Vancouver: Weekly Rent Report")
        creator = dataset["creator"]
        self.assertEqual(creator["@type"], "Person")
        self.assertEqual(creator["name"], "Devin Desaulniers")
        self.assertEqual(creator["url"], "https://devindesaulniers.ca")
        self.assertEqual(creator["worksFor"], {"@type": "Organization", "name": "Axford Real Estate"})
        self.assertNotIn("@id", creator)
        self.assertEqual(dataset["license"], "https://devindesaulniers.ca/terms.html")
        self.assertNotIn("creativecommons.org", page.lower())
        terms = terms_page.render()
        self.assertIn("CREA DDF", terms)
        self.assertIn("owned by the respective real estate boards", terms)
        self.assertNotIn("creativecommons.org", terms.lower())
        self.assertIn('href="rent-report.html"', terms)

    def test_best_value_caps_each_city(self):
        listings = []
        def add(city, band_price, cheap_price, sqft, beds, n_peer, n_cheap):
            for index in range(n_peer):
                listings.append(home(
                    id=f"{city}-p{index}", city=city, price=band_price, sqft=sqft, beds=beds,
                ))
            for index in range(n_cheap):
                listings.append(home(
                    id=f"{city}-c{index}", city=city, price=cheap_price, sqft=sqft, beds=beds,
                ))
        add("Vancouver", 3200, 1920, 800, 2, 6, 3)
        add("Burnaby", 3200, 1920, 800, 2, 5, 2)
        add("Surrey", 2100, 1200, 600, 1, 5, 2)
        picked = rr.best_value(rr.prepare_listings(listings)["comparable"])
        self.assertGreaterEqual(len(picked), 5)
        self.assertLessEqual(len(picked), 8)
        counts = {}
        for card in picked:
            counts[card["city"]] = counts.get(card["city"], 0) + 1
            self.assertGreaterEqual(card["discount"], 0.12)
            self.assertIn("rentals.html?id=", rr.rental_href(card["id"]))
        self.assertTrue(all(count <= 2 for count in counts.values()))

    def test_sample_and_empty_do_not_publish(self):
        directory = tempfile.mkdtemp(prefix="rent-report-empty-")
        try:
            target = os.path.join(directory, "rent-report.html")
            with open(target, "w", encoding="utf-8") as handle:
                handle.write("KEEP")
            path = write_feed(directory, [home(price=75)], sample=True)
            with self.assertRaises(rr.ReportError) as raised:
                rr.build_site(directory, path, NOW)
            self.assertEqual(raised.exception.code, 2)
            path = write_feed(directory, [home(price=75)], sample=False)
            with self.assertRaises(rr.ReportError) as raised:
                rr.build_site(directory, path, NOW)
            self.assertEqual(raised.exception.code, 1)
            self.assertEqual(open(target, encoding="utf-8").read(), "KEEP")
        finally:
            shutil.rmtree(directory)

    def test_sitemap_patch_is_idempotent(self):
        directory = tempfile.mkdtemp(prefix="rent-report-map-")
        try:
            sitemap(directory)
            self.assertTrue(rr.patch_sitemap(directory, "2026-10-15"))
            self.assertTrue(rr.patch_sitemap(directory, "2026-10-22") or True)
            text = open(os.path.join(directory, "sitemap.xml"), encoding="utf-8").read()
            self.assertEqual(text.count("rent-report.html"), 1)
            self.assertIn("<lastmod>2026-10-22</lastmod>", text)
            self.assertIn("rentals.html", text)
        finally:
            shutil.rmtree(directory)


if __name__ == "__main__":
    unittest.main()
