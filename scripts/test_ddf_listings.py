#!/usr/bin/env python3
"""Offline checks for the DDF normalizer. No network, no form submission."""
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import fetch_ddf_listings as ddf

STATS = ddf.Counter


def odata(**extra):
    intent = extra.pop("intent", "sale")
    rec = {
        "ListingKey": "100",
        "ListingId": "R100",
        "StandardStatus": "Active",
        "PropertyType": "Residential",
        "PropertySubType": "Townhouse",
        "ListPrice": 899000,
        "ClosePrice": 850000,
        "PublicRemarks": "A bright townhouse.",
        "City": "Coquitlam",
        "CityRegion": "Maillardville",
        "StateOrProvince": "BC",
        "StreetNumber": "100",
        "StreetName": "Sample",
        "StreetSuffix": "Crescent",
        "BedroomsTotal": 3,
        "BathroomsTotalInteger": 2,
        "ListOfficeName": "Sample Harbour Realty",
        "ListAgentFullName": "Alex Sample",
        "ListingURL": "https://www.realtor.ca/real-estate/1/example?utm_source=ddf&utm_medium=web",
        "InternetEntireListingDisplayYN": True,
        "InternetAddressDisplayYN": True,
        "Media": [
            {"MediaURL": "https://cdn.example/2.jpg", "Order": 2, "MediaCategory": "Photo"},
            {"MediaURL": "http://cdn.example/insecure.jpg", "Order": 0, "MediaCategory": "Photo"},
            {"MediaURL": "https://cdn.example/1.jpg", "Order": 0, "PreferredPhotoYN": True, "MediaCategory": "Photo"},
            {"MediaURL": "https://cdn.example/doc.pdf", "Order": 1, "MediaCategory": "Document"},
        ],
    }
    rec.update(extra)
    return ddf.from_odata(rec, {}, {}, STATS(), intent=intent)


def test_keeps_active_gv_townhouse_and_drops_sold_price():
    item = odata()
    assert item["city"] == "Coquitlam"
    assert item["type"] == "Townhouse"
    assert item["price"] == 899000
    assert item["address"] == "100 Sample Crescent"
    assert item["brokerage"] == "Sample Harbour Realty"
    assert item["photos"] == ["https://cdn.example/1.jpg", "https://cdn.example/2.jpg"]
    assert "utm_source" not in item["realtorUrl"]
    assert "ClosePrice" not in item
    blob = json.dumps(item)
    assert "850000" not in blob


def test_rejects_sold_commercial_lease_and_outside_area():
    assert odata(StandardStatus="Closed") is None
    assert odata(StandardStatus="Sold") is None
    assert odata(PropertyType="Commercial", PropertySubType="Office") is None
    assert odata(PropertyType="Residential Lease", PropertySubType="", ListPrice=2500) is None
    assert odata(City="Toronto", StateOrProvince="ON") is None
    assert odata(City="Richmond", StateOrProvince="Ontario") is None
    assert odata(City="Richmond", StateOrProvince="BC") is not None
    assert odata(InternetEntireListingDisplayYN=False) is None


def test_hides_address_when_seller_opts_out():
    item = odata(InternetAddressDisplayYN=False)
    assert item["address"] is None
    assert item["city"] == "Coquitlam"


def test_aor_and_city_aliases():
    assert ddf.in_target_area("District of North Vancouver", "British Columbia", "")
    assert ddf.in_target_area("Township of Langley", "BC", "")
    assert ddf.in_target_area("Cultus Lake", "BC", "Fraser Valley Real Estate Board")
    assert not ddf.in_target_area("Victoria", "BC", "Victoria Real Estate Board")
    assert ddf.residential_label(["Residential", "Semi-detached"], "For sale", STATS()) == "Half duplex / duplex"


def test_rets_xml_round_trip():
    xml = """<?xml version="1.0"?>
<RETS ReplyCode="0">
  <Property ID="55">
    <PropertyDetails ID="55">
      <ListingID>FV55</ListingID>
      <Price>1,125,000</Price>
      <PropertyType ID="1">Residential</PropertyType>
      <TransactionType>For sale</TransactionType>
      <PublicRemarks>Detached home.</PublicRemarks>
      <MoreInformationLink>https://www.realtor.ca/real-estate/55/example</MoreInformationLink>
      <Address>
        <StreetAddress>500 Imaginary Drive</StreetAddress>
        <City>Abbotsford</City>
        <Province>British Columbia</Province>
        <Neighbourhood>East Abbotsford</Neighbourhood>
      </Address>
      <Building>
        <BathroomTotal>3</BathroomTotal>
        <BedroomsTotal>5</BedroomsTotal>
        <SizeInterior>2800 sqft</SizeInterior>
        <Type>House</Type>
        <ConstructedDate>1998</ConstructedDate>
      </Building>
      <AgentDetails ID="9">
        <Name>Riley Preview</Name>
        <Office><Name>Preview Valley Realty</Name></Office>
      </AgentDetails>
      <Photo>
        <PropertyPhoto SequenceID="1"><PhotoURL>https://cdn.example/b.jpg</PhotoURL></PropertyPhoto>
        <PropertyPhoto SequenceID="0"><LargePhotoURL>https://cdn.example/a.jpg</LargePhotoURL></PropertyPhoto>
      </Photo>
    </PropertyDetails>
  </Property>
</RETS>"""
    rows = ddf.parse_property_details(xml)
    assert len(rows) == 1
    item = ddf.from_rets(rows[0], STATS())
    assert item["id"] == "55"
    assert item["mls"] == "FV55"
    assert item["price"] == 1125000
    assert item["city"] == "Abbotsford"
    assert item["type"] == "Detached house"
    assert item["beds"] == 5
    assert item["baths"] == 3
    assert item["sqft"] == 2800
    assert item["year"] == 1998
    assert item["brokerage"] == "Preview Valley Realty"
    assert item["photos"][0] == "https://cdn.example/a.jpg"
    assert item["analyticsId"] == "55"


def test_replace_drops_removed_ids():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "data.json")
        ddf.write_feed(path, "ddf-web-api", "9", [{"id": "1", "city": "Surrey"}, {"id": "2", "city": "Langley"}])
        ddf.write_feed(path, "ddf-web-api", "9", [{"id": "2", "city": "Langley"}])
        data = json.loads(open(path, encoding="utf-8").read())
        assert [row["id"] for row in data["listings"]] == ["2"]
        assert data["sample"] is False
        assert "ClosePrice" not in open(path, encoding="utf-8").read()


def test_write_feed_keeps_search_cards_light():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "data.json")
        ddf.write_feed(path, "ddf-web-api", "9", [{
            "id": "55",
            "city": "Surrey",
            "price": 900000,
            "brokerage": "Sample Harbour Realty",
            "photos": ["https://cdn.example/a.jpg", "https://cdn.example/b.jpg"],
            "remarks": "A bright home.",
        }])
        card = json.loads(open(path, encoding="utf-8").read())["listings"][0]
        assert card["photo"] == "https://cdn.example/a.jpg"
        assert card["photoCount"] == 2
        assert "remarks" not in card
        assert "photos" not in card
        shard = json.loads(open(os.path.join(tmp, "sale", f"{55 % ddf.SHARD_COUNT}.json"), encoding="utf-8").read())
        assert shard["55"]["remarks"] == "A bright home."
        assert shard["55"]["photos"] == ["https://cdn.example/a.jpg", "https://cdn.example/b.jpg"]
        rentals = os.path.join(tmp, "rentals.json")
        ddf.write_feed(rentals, "ddf-web-api", "9", [{"id": "10", "city": "Delta", "price": 2400, "remarks": "Monthly."}])
        assert os.path.isdir(os.path.join(tmp, "rent"))


def test_missing_secrets_exit_clean():
    env = os.environ.copy()
    env.pop("DDF_USERNAME", None)
    env.pop("DDF_PASSWORD", None)
    env["DDF_OUTPUT"] = os.path.join(tempfile.gettempdir(), "ddf-should-not-write.json")
    env["DDF_RENTALS_OUTPUT"] = os.path.join(tempfile.gettempdir(), "ddf-rentals-should-not-write.json")
    for path in (env["DDF_OUTPUT"], env["DDF_RENTALS_OUTPUT"]):
        if os.path.exists(path):
            os.remove(path)
    proc = subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "fetch_ddf_listings.py")],
        env=env, capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "Skipping" in proc.stdout
    assert not os.path.exists(env["DDF_OUTPUT"])
    assert not os.path.exists(env["DDF_RENTALS_OUTPUT"])
    env["DDF_USERNAME"] = "someone"
    proc = subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "fetch_ddf_listings.py")],
        env=env, capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0
    assert not os.path.exists(env["DDF_OUTPUT"])
    assert not os.path.exists(env["DDF_RENTALS_OUTPUT"])


def test_listings_are_published():
    sys.path.insert(0, os.path.join(ROOT, "_build"))
    import partials
    assert partials.LISTINGS_LIVE is True
    sample = json.loads(open(os.path.join(ROOT, "_fixtures", "listings-sample.json"), encoding="utf-8").read())
    live = json.loads(open(os.path.join(ROOT, "listings", "data.json"), encoding="utf-8").read())
    rent_sample = json.loads(open(os.path.join(ROOT, "_fixtures", "rentals-sample.json"), encoding="utf-8").read())
    rent_live = json.loads(open(os.path.join(ROOT, "listings", "rentals.json"), encoding="utf-8").read())
    assert sample["sample"] is True
    assert live["sample"] is False
    assert "FICTIONAL" in sample["listings"][0]["remarks"]
    assert all("remarks" not in row and "photos" not in row for row in live["listings"])
    assert live["count"] == len(live["listings"])
    pictured = next(row for row in live["listings"] if row.get("photo") and str(row.get("id", "")).isdigit())
    shard_no = int(pictured["id"]) % ddf.SHARD_COUNT
    shard = json.loads(open(os.path.join(ROOT, "listings", "sale", f"{shard_no}.json"), encoding="utf-8").read())
    assert shard[pictured["id"]]["photos"][0] == pictured["photo"]
    assert "FICTIONAL" not in (shard[pictured["id"]].get("remarks") or "")
    assert rent_sample["sample"] is True
    assert rent_live["sample"] is False
    assert "FICTIONAL" in rent_sample["listings"][0]["remarks"]
    assert all("remarks" not in row and "photos" not in row for row in rent_live["listings"])
    assert all(row["price"] < 20000 for row in rent_sample["listings"])
    assert rent_live["count"] == len(rent_live["listings"])
    assert rent_live["count"] > 0
    rent_row = next(row for row in rent_live["listings"] if row.get("photo") and str(row.get("id", "")).isdigit())
    rent_shard_no = int(rent_row["id"]) % ddf.SHARD_COUNT
    rent_shard = json.loads(open(os.path.join(ROOT, "listings", "rent", f"{rent_shard_no}.json"), encoding="utf-8").read())
    assert rent_shard[rent_row["id"]]["photos"][0] == rent_row["photo"]
    assert all(isinstance(row.get("price"), int) and row["price"] > 0 for row in rent_live["listings"])
    sale_ids = {row["id"] for row in live["listings"]}
    assert not sale_ids.intersection(row["id"] for row in rent_live["listings"])
    js = open(os.path.join(ROOT, "assets", "js", "listings.js"), encoding="utf-8").read()
    assert "https://analytics.crea.ca/LogEvents.svc/LogEvents" in js
    assert "EventType=view" in js
    assert "ReferralURL" in js
    assert 'listings/" + (mode === "rent" ? "rent" : "sale")' in js
    assert "photoCount" in js
    assert "ls-lightbox" in js
    assert "is-listing-open" in js
    css = open(os.path.join(ROOT, "assets", "css", "styles.css"), encoding="utf-8").read()
    assert ".ls-frame img{position:absolute" in css
    assert "object-fit:contain" in css
    assert "min-width:0" in css
    for name in ("listings.html", "rentals.html"):
        page = open(os.path.join(ROOT, name), encoding="utf-8").read()
        assert "ls-gallery" in page
        assert "ls-lead" in page
        assert "ls-summary" in page
        assert 'aria-label="Enlarge photo"' in page
    sitemap = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    assert "<loc>https://devindesaulniers.ca/listings.html</loc>" in sitemap
    assert "<loc>https://devindesaulniers.ca/rentals.html</loc>" in sitemap
    index = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    assert 'href="listings.html"' in index
    assert 'href="rentals.html"' in index
    for name in ("listings.html", "rentals.html"):
        html = open(os.path.join(ROOT, name), encoding="utf-8").read()
        assert 'name="robots" content="noindex, nofollow"' not in html
        assert "Trademarks are owned or controlled by The Canadian Real Estate Association (CREA)" in html
        assert "Axford Real Estate" in html
        assert "Powered by REALTOR.ca" in html or "listings.js" in html
        assert "listings.js" in html
        low = html.lower()
        assert "best " not in low
        assert "top " not in low


def test_photo_urls_keep_the_highres_copy():
    media = [
        {"MediaURL": "https://cdn.example/listing/thumb/1/R1_1.jpg", "Order": 0, "MediaCategory": "Photo", "PreferredPhotoYN": True},
        {"MediaURL": "https://cdn.example/listing/highres/1/R1_1.jpg", "Order": 1, "MediaCategory": "Photo"},
        {"MediaURL": "https://cdn.example/listing/lowres/1/R1_2.jpg", "Order": 2, "MediaCategory": "Photo"},
        {"MediaURL": "https://cdn.example/listing/highres/1/R1_2.jpg", "Order": 2, "MediaCategory": "Photo"},
        {"MediaURL": "https://cdn.example/listing/doc.pdf", "Order": 3, "MediaCategory": "Document"},
    ]
    assert ddf.photo_urls(media) == [
        "https://cdn.example/listing/highres/1/R1_1.jpg",
        "https://cdn.example/listing/highres/1/R1_2.jpg",
    ]


def test_photo_urls_keeps_up_to_fifty():
    media = [
        {
            "MediaURL": f"https://cdn.example/listing/highres/{i}/R1_{i}.jpg",
            "Order": i,
            "MediaCategory": "Photo",
        }
        for i in range(60)
    ]
    urls = ddf.photo_urls(media)
    assert ddf.MAX_PHOTOS == 50
    assert len(urls) == 50
    assert urls[0] == "https://cdn.example/listing/highres/0/R1_0.jpg"
    assert urls[-1] == "https://cdn.example/listing/highres/49/R1_49.jpg"


def test_builds_realtor_url_when_feed_omits_it():
    item = odata(ListingURL=None, ListingKey="12345678")
    assert item["realtorUrl"] == "https://www.realtor.ca/real-estate/12345678/100-sample-crescent-coquitlam"
    kept = odata()
    assert kept["realtorUrl"] == "https://www.realtor.ca/real-estate/1/example"
    assert "utm_source" not in kept["realtorUrl"]


def test_realtor_slug_uses_property_id_not_mls_number():
    assert ddf.address_slug("1307-595 AUSTIN AVE", "Coquitlam") == "1307-595-austin-ave-coquitlam"
    assert ddf.address_slug("6531 NO. 2 Road", "Richmond") == "6531-no-2-road-richmond"
    assert ddf.address_slug("2652 O'HARA Lane", "Surrey") == "2652-ohara-lane-surrey"
    assert ddf.address_slug("74 East 37TH Avenue", "Vancouver") == "74-e-37th-avenue-vancouver"
    assert ddf.address_slug("107-809 West 16TH Street", "North Vancouver") == "107-809-w-16th-street-north-vancouver"
    assert ddf.address_slug("3303-488 Southwest MARINE Drive", "Vancouver") == "3303-488-sw-marine-drive-vancouver"
    assert ddf.address_slug("9304 STELLER'S Way", "Whistler") == "9304-stellers-way-whistler"
    item = odata(
        ListingURL=None, ListingKey="30453805", ListingId="R3179251",
        UnitNumber="1307", StreetNumber="595", StreetName="AUSTIN", StreetSuffix="AVE", City="Coquitlam",
    )
    assert item["address"] == "1307-595 AUSTIN AVE"
    assert item["realtorUrl"] == "https://www.realtor.ca/real-estate/30453805/1307-595-austin-ave-coquitlam"
    assert "R3179251" not in item["realtorUrl"]
    exact = odata(
        MoreInformationLink="https://www.realtor.ca/real-estate/100/from-the-feed?utm_source=ddf",
        ListingURL="https://www.realtor.ca/real-estate/1/example",
    )
    assert exact["realtorUrl"] == "https://www.realtor.ca/real-estate/100/from-the-feed"
    bare = odata(ListingURL="https://www.realtor.ca/real-estate/12345678")
    assert bare["realtorUrl"] == "https://www.realtor.ca/real-estate/12345678/100-sample-crescent-coquitlam"
    hidden = odata(ListingURL=None, InternetAddressDisplayYN=False)
    assert hidden["address"] is None
    assert hidden["realtorUrl"] == "https://www.realtor.ca/real-estate/100/coquitlam"
    search = odata(ListingURL=None, ListingKey="not-numeric")
    assert search["realtorUrl"].startswith("https://www.realtor.ca/map#")
    assert "Keywords=R100" in search["realtorUrl"]
    legacy = ddf.realtor_link(
        "https://www.realtor.ca/PropertyDetails.aspx?PropertyId=30453805",
        "999", "1307-595 AUSTIN AVE", "Coquitlam", "R3179251",
    )
    assert legacy == "https://www.realtor.ca/real-estate/30453805/1307-595-austin-ave-coquitlam"


def test_link_checker_repairs_urls_and_drops_only_real_404s():
    import check_realtor_links as links
    assert links.classify(403, "Sorry, you have been blocked / Désolé, vous avez été bloqué") == "blocked"
    assert links.classify(404, "Oh No! The page you are looking for does not exist.") == "dead"
    assert links.classify(200, "<title>1307 595 AUSTIN AVE</title>") == "ok"
    assert links.classify(0, "") == "error"
    assert links.canonical_url(
        '{"url": "https://www.realtor.ca/real-estate/30453805/1307-595-austin-ave-coquitlam"}',
        "30453805",
    ) == "https://www.realtor.ca/real-estate/30453805/1307-595-austin-ave-coquitlam"
    assert links.canonical_url(
        '{"url": "https://www.realtor.ca/real-estate/999/other"}',
        "30453805",
    ) == ""

    def fake_fetch(url):
        if url.endswith("/1307-595-austin-ave-coquitlam"):
            return 404, "Oh No! The page you are looking for does not exist."
        if "/10/" in url:
            return 200, '{"url": "https://www.realtor.ca/real-estate/10/10-main-street-surrey"}'
        return 403, "Sorry, you have been blocked"

    original = links.fetch
    links.fetch = fake_fetch
    try:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "rentals.json")
            austin_id = "30453805"
            shard_dir = os.path.join(tmp, "rent")
            os.makedirs(shard_dir)
            shard_no = int(austin_id) % ddf.SHARD_COUNT
            with open(os.path.join(shard_dir, f"{shard_no}.json"), "w", encoding="utf-8") as fh:
                json.dump({austin_id: {"remarks": "Austin"}, "10": {"remarks": "Main"}}, fh)
            with open(path, "w", encoding="utf-8") as fh:
                json.dump({
                    "count": 2,
                    "listings": [
                        {
                            "id": austin_id, "mls": "R3179251",
                            "address": "1307-595 AUSTIN AVE", "city": "Coquitlam",
                            "realtorUrl": "https://www.realtor.ca/real-estate/30453805",
                        },
                        {
                            "id": "10", "mls": "R10",
                            "address": "10 Main Street", "city": "Surrey",
                            "realtorUrl": "https://www.realtor.ca/real-estate/10",
                        },
                    ],
                }, fh)
            summary = links.process(path, http=True, limit=None)
            assert summary["repaired"] == 2
            assert summary["removed"] == 1
            assert summary["dead"] == 1
            assert summary["ok"] == 1
            saved = json.loads(open(path, encoding="utf-8").read())
            assert saved["count"] == 1
            assert saved["listings"][0]["id"] == "10"
            assert saved["listings"][0]["realtorUrl"] == "https://www.realtor.ca/real-estate/10/10-main-street-surrey"
            shard = json.loads(open(os.path.join(shard_dir, f"{shard_no}.json"), encoding="utf-8").read())
            assert austin_id not in shard
            assert shard["10"]["remarks"] == "Main"

            blocked_path = os.path.join(tmp, "data.json")
            with open(blocked_path, "w", encoding="utf-8") as fh:
                json.dump({
                    "count": 1,
                    "listings": [{
                        "id": "55", "mls": "R55", "address": "55 Block Road", "city": "Burnaby",
                        "realtorUrl": "https://www.realtor.ca/real-estate/55",
                    }],
                }, fh)
            links.fetch = lambda url: (403, "<title>Sorry, you have been blocked</title>")
            blocked = links.process(blocked_path, http=True, limit=None)
            assert blocked["removed"] == 0
            assert blocked["blocked"] == 1
            kept = json.loads(open(blocked_path, encoding="utf-8").read())
            assert kept["listings"][0]["realtorUrl"] == "https://www.realtor.ca/real-estate/55/55-block-road-burnaby"
    finally:
        links.fetch = original


def test_property_select_uses_live_schema():
    url = ddf.property_url(ddf.SELECT_FIELDS, False, True, 0)
    assert "ListOfficeName" not in url
    assert "ListAgentFullName" not in url
    assert "PropertyType=" not in url and "PropertyType%2C" not in url and "PropertyType," not in url
    assert "TransactionType" not in url
    assert "PropertySubType" in url
    assert "LeaseAmount" in url
    assert "TotalActualRent" in url
    assert "Media" in url
    assert "StandardStatus" in url
    assert ddf.rejected_field(b'{"error":{"details":"Could not find a property named \'ListOfficeName\' on type \'DDF.Core.Entities.Property\'."}}') == "ListOfficeName"


def test_monthly_rent_conversions():
    assert ddf.monthly_rent(500, "Weekly") == 2167
    assert ddf.monthly_rent(24000, "Annually") == 2000
    assert ddf.monthly_rent(2400, "Monthly") == 2400
    assert ddf.monthly_rent(2400, "") == 2400
    assert ddf.monthly_rent(2000, "Bi-Monthly") == 1000
    assert ddf.monthly_rent(1200, "Semi-Monthly") == 2400
    assert ddf.monthly_rent(500, "Bi-Weekly") == 1083
    assert ddf.monthly_rent(5000, "One Time") is None
    assert ddf.monthly_rent(3000, "Quarterly") is None


def test_lease_goes_to_rentals_and_sales_stay_sales():
    assert odata(PropertyType="Residential Lease", PropertySubType="", ListPrice=2500) is None
    leased = odata(intent="rent", PropertyType="Residential Lease", PropertySubType="Townhouse", ListPrice=2500)
    assert leased["price"] == 2500
    assert leased["type"] == "Townhouse"
    assert "ClosePrice" not in leased
    weekly = odata(
        intent="rent", PropertyType="Residential", PropertySubType="Apartment",
        ListPrice=None, LeaseAmount=500, LeaseAmountFrequency="Weekly",
    )
    assert weekly["price"] == 2167
    assert weekly["type"] == "Condo / apartment"
    assert odata(intent="rent", PropertyType="Commercial", PropertySubType="Office", LeaseAmount=4000, LeaseAmountFrequency="Monthly", ListPrice=None) is None
    both = odata(LeaseAmount=2800, ListPrice=899000)
    assert both["price"] == 899000
    assert odata(intent="rent", LeaseAmount=2800, ListPrice=899000) is None
    assert odata(LeaseAmount=2800, LeaseAmountFrequency="Monthly", ListPrice=899000) is None
    priced = odata(intent="rent", LeaseAmount=2800, LeaseAmountFrequency="Monthly", ListPrice=899000)
    assert priced["price"] == 2800
    assert odata(TransactionType="For sale or lease", LeaseAmount=2600, LeaseAmountFrequency="Monthly", ListPrice=900000) is None
    dual = odata(intent="rent", TransactionType="For sale or lease", LeaseAmount=2600, LeaseAmountFrequency="Monthly", ListPrice=900000)
    assert dual["price"] == 2600
    assert odata(intent="rent", LeaseAmount=9000, LeaseAmountFrequency="One Time", PropertyType="Residential Lease", ListPrice=None) is None
    channel, item = odata(intent=None)
    assert channel == "sale" and item["price"] == 899000
    # Asking rent on this feed: blank list price, empty LeaseAmount, monthly TotalActualRent.
    assert odata(ListPrice=None, LeaseAmount=None, LeaseAmountFrequency="Monthly", TotalActualRent=2850) is None
    rented = odata(
        intent="rent", ListPrice=None, LeaseAmount=None,
        LeaseAmountFrequency="Monthly", TotalActualRent=2850,
        PropertySubType="Apartment",
    )
    assert rented["price"] == 2850
    assert rented["type"] == "Condo / apartment"
    held = odata(ListPrice=None, LeaseAmount=None, TotalActualRent=2850, LeaseAmountFrequency=None)
    assert held["price"] is None
    income = odata(ListPrice=1250000, TotalActualRent=3200, LeaseAmountFrequency="Monthly")
    assert income["price"] == 1250000
    assert odata(intent="rent", ListPrice=1250000, TotalActualRent=3200, LeaseAmountFrequency="Monthly") is None


def test_rets_lease_is_monthly_and_not_a_sale():
    xml = """<?xml version="1.0"?>
<RETS ReplyCode="0">
  <Property ID="77">
    <PropertyDetails ID="77">
      <ListingID>FV77</ListingID>
      <Price>500</Price>
      <PricePerTime>Weekly</PricePerTime>
      <PropertyType ID="1">Residential</PropertyType>
      <TransactionType>For lease</TransactionType>
      <PublicRemarks>Apartment for rent.</PublicRemarks>
      <MoreInformationLink>https://www.realtor.ca/real-estate/77/example</MoreInformationLink>
      <Address>
        <StreetAddress>77 Rental Road</StreetAddress>
        <City>Surrey</City>
        <Province>British Columbia</Province>
      </Address>
      <Building>
        <BathroomTotal>1</BathroomTotal>
        <BedroomsTotal>1</BedroomsTotal>
        <Type>Apartment</Type>
      </Building>
      <AgentDetails ID="3">
        <Name>Riley Preview</Name>
        <Office><Name>Preview Valley Realty</Name></Office>
      </AgentDetails>
    </PropertyDetails>
  </Property>
</RETS>"""
    rows = ddf.parse_property_details(xml)
    assert ddf.from_rets(rows[0], STATS()) is None
    item = ddf.from_rets(rows[0], STATS(), intent="rent")
    assert item["price"] == 2167
    assert item["city"] == "Surrey"
    assert item["type"] == "Condo / apartment"
    assert item["brokerage"] == "Preview Valley Realty"
    assert item["analyticsId"] == "77"
    commercial = dict(rows[0])
    commercial["PropertyType"] = "Commercial"
    commercial["TransactionType"] = "For lease"
    assert ddf.from_rets(commercial, STATS(), intent="rent") is None
    assert ddf.from_rets(commercial, STATS()) is None


def test_rental_probe_reads_metadata_and_compact_rows():
    import probe_ddf_rentals as probe
    xml = """<?xml version="1.0"?>
<edmx:Edmx xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx" Version="4.0">
  <edmx:DataServices>
    <Schema xmlns="http://docs.oasis-open.org/odata/ns/edm" Namespace="DDF.Core.Entities">
      <EntityType Name="Property">
        <Property Name="ListingKey" Type="Edm.String"/>
        <Property Name="LeaseAmount" Type="Edm.Double"/>
      </EntityType>
      <EnumType Name="PropertySubType">
        <Member Name="Single Family"/>
        <Member Name="Residential Lease"/>
      </EnumType>
    </Schema>
    <Schema xmlns="http://docs.oasis-open.org/odata/ns/edm" Namespace="Default">
      <EntityContainer Name="Container">
        <EntitySet Name="Property" EntityType="DDF.Core.Entities.Property"/>
        <EntitySet Name="Destination" EntityType="DDF.Core.Entities.Destination"/>
      </EntityContainer>
    </Schema>
  </edmx:DataServices>
</edmx:Edmx>
""".encode()
    sets, fields, enums = probe.parse_metadata(xml)
    assert sets == ["Property", "Destination"]
    assert [name for name, _typ in fields["Property"]] == ["ListingKey", "LeaseAmount"]
    assert enums["PropertySubType"] == ["Single Family", "Residential Lease"]
    names, rows = probe.compact_rows(
        "<COLUMNS>\tTransactionType\tPropertyType\t</COLUMNS>\n"
        "<DATA>\tFor lease\tResidential Lease\t</DATA>\n"
    )
    assert names == ["TransactionType", "PropertyType"]
    assert rows == [{"TransactionType": "For lease", "PropertyType": "Residential Lease"}]
    packed = (
        "<RETS><COLUMNS>\tTransactionType\tPrice\t</COLUMNS>"
        "<DATA>\tFor rent\t2500\t</DATA><DATA>\tFor sale\t900000\t</DATA></RETS>"
    )
    names, rows = probe.compact_rows(packed)
    assert names == ["TransactionType", "Price"]
    assert rows[0]["TransactionType"] == "For rent"
    assert rows[1]["Price"] == "900000"
    assert probe.amount_bucket(2400) == "1500_3000"
    assert probe.amount_bucket(2400000) == "100000_plus"
    assert "for_rent_or_lease" in probe.remark_flags("Bright condo for rent.")
    assert probe.remark_flags(2400) == ("empty",)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
    print("all tests passed")
