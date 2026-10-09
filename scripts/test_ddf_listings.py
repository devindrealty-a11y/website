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
    return ddf.from_odata(rec, {}, {}, STATS())


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


def test_missing_secrets_exit_clean():
    env = os.environ.copy()
    env.pop("DDF_USERNAME", None)
    env.pop("DDF_PASSWORD", None)
    env["DDF_OUTPUT"] = os.path.join(tempfile.gettempdir(), "ddf-should-not-write.json")
    if os.path.exists(env["DDF_OUTPUT"]):
        os.remove(env["DDF_OUTPUT"])
    proc = subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "fetch_ddf_listings.py")],
        env=env, capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "Skipping" in proc.stdout
    assert not os.path.exists(env["DDF_OUTPUT"])
    env["DDF_USERNAME"] = "someone"
    proc = subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "fetch_ddf_listings.py")],
        env=env, capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0
    assert not os.path.exists(env["DDF_OUTPUT"])


def test_hidden_until_switch_on():
    sys.path.insert(0, os.path.join(ROOT, "_build"))
    import partials
    assert partials.LISTINGS_LIVE is False
    sample = json.loads(open(os.path.join(ROOT, "_fixtures", "listings-sample.json"), encoding="utf-8").read())
    live = json.loads(open(os.path.join(ROOT, "listings", "data.json"), encoding="utf-8").read())
    assert sample["sample"] is True
    assert live["sample"] is False
    assert live["listings"] == []
    assert "FICTIONAL" in sample["listings"][0]["remarks"]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
    print("all tests passed")
