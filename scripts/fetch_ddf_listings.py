#!/usr/bin/env python3
"""Refresh listings/data.json and listings/rentals.json from the CREA DDF feed.

Tries the current DDF Web API (OData) at https://ddfapi.realtor.ca first.
The destination username and password are the OAuth client id and secret
(scope DDFApi_Read) at https://identity.crea.ca/connect/token. If that API
is not reachable, falls back to the legacy RETS feed at https://data.crea.ca.

Reads DDF_USERNAME and DDF_PASSWORD. If either is missing, exits 0 and
does not change either JSON file. A successful run replaces both files, so
listings that left the feed disappear. One pull feeds both files:

- listings/data.json: active residential for-sale listings
- listings/rentals.json: active residential for-lease or for-rent listings

Commercial listings are excluded from both. A listing is written to only one
file. Rent is stored as dollars per month (LeaseAmount preferred over
ListPrice, converted with the lease frequency). Sold and leased-completed
records are dropped, and sold prices are never written. Photos stay as
remote https URLs. Geography is Greater Vancouver and the Fraser Valley.

No third-party packages: the GitHub Action runs this with the stdlib.
"""
from __future__ import annotations

import base64
import json
import math
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from http.cookiejar import CookieJar

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUTPUT = os.path.join(ROOT, "listings", "data.json")
DEFAULT_RENTALS = os.path.join(ROOT, "listings", "rentals.json")

TOKEN_URL = "https://identity.crea.ca/connect/token"
ODATA_ROOT = "https://ddfapi.realtor.ca/odata/v1"
RETS_LOGIN = "https://data.crea.ca/Login.svc/Login"
RETS_SEARCH = "https://data.crea.ca/Search.svc/Search"
RETS_LOGOUT = "https://data.crea.ca/Logout.svc/Logout"
SCOPE = "DDFApi_Read"
PAGE_SIZE = 100
MAX_PHOTOS = 12
MAX_PAGES = 5000
UA = "DevinDesaulniersDDF/1.0"

# Municipalities and common board spellings for Greater Vancouver REALTORS
# and the Fraser Valley Real Estate Board. Matching is on the normalized city.
GV_FV_CITIES = {
    "vancouver", "burnaby", "new westminster", "richmond",
    "north vancouver", "west vancouver", "coquitlam", "port coquitlam",
    "port moody", "anmore", "belcarra", "pitt meadows", "maple ridge",
    "bowen island", "lions bay", "squamish", "whistler", "pemberton",
    "gibsons", "sechelt", "halfmoon bay", "roberts creek", "pender harbour",
    "delta", "north delta", "surrey", "white rock", "south surrey",
    "cloverdale", "langley", "city of langley", "township of langley",
    "fort langley", "walnut grove", "willoughby", "aldergrove",
    "abbotsford", "mission", "chilliwack", "hope", "harrison hot springs",
    "harrison mills", "cultus lake", "agassiz", "kent", "tsawwassen", "ladner",
    "greater vancouver", "fraser valley",
}
AOR_HINTS = ("greater vancouver", "fraser valley", "rebgv", "fvreb", "gvrealtors")
BC_NAMES = {"bc", "b.c", "british columbia"}
SOLD_WORDS = ("sold", "closed", "expired", "cancel", "withdraw", "terminated", "leased", "rented")
# Short words use boundaries so "land" does not hide inside another token.
COMMERCIAL_PHRASES = (
    "commercial", "industrial", "business opportunity", "warehouse", "hotel", "motel",
    "vacant land", "vacant",
)
EXCLUDE_PHRASES = COMMERCIAL_PHRASES + ("for rent", "rental", "lease")
EXCLUDE_WORDS = ("land", "office", "farm", "retail", "parking", "agricultural")
OPTIONAL_SELECT = ("PropertyType", "LeaseAmountFrequency")
TYPE_RULES = (
    (("half duplex", "half-duplex", "semi-detached", "semi detached", "duplex", "triplex", "fourplex"), "Half duplex / duplex"),
    (("townhouse", "townhome", "town house", "row house", "rowhouse"), "Townhouse"),
    (("condo", "condominium", "apartment", "high rise", "highrise", "loft"), "Condo / apartment"),
    (("detached", "single family", "single-family", "cottage", "house"), "Detached house"),
)
SELECT_FIELDS = [
    "ListingKey", "ListingId", "StandardStatus", "PropertyType", "PropertySubType",
    "StructureType", "ListPrice", "PublicRemarks", "UnparsedAddress", "City",
    "CityRegion", "StateOrProvince", "PostalCode", "StreetNumber", "StreetName",
    "StreetSuffix", "StreetDirPrefix", "UnitNumber", "BedroomsTotal",
    "BathroomsTotalInteger", "BathroomsPartial", "LivingArea", "LivingAreaUnits",
    "BuildingAreaTotal", "BuildingAreaUnits", "AboveGradeFinishedArea", "YearBuilt",
    "ListOfficeKey", "ListAgentKey", "ListOfficeName", "ListAgentFullName",
    "ListAOR", "OriginatingSystemName", "ListingURL", "InternetEntireListingDisplayYN",
    "InternetAddressDisplayYN", "ParkingTotal", "LeaseAmount", "LeaseAmountFrequency",
    "ModificationTimestamp",
]


class FetchError(Exception):
    pass


class ApiUnavailable(FetchError):
    pass


def main(argv=None):
    user = os.environ.get("DDF_USERNAME", "").strip()
    password = os.environ.get("DDF_PASSWORD", "").strip()
    if not user or not password:
        print("DDF_USERNAME or DDF_PASSWORD is not set. Skipping listing refresh.")
        return 0
    output, rentals_output = output_paths()
    try:
        source, destination_id, sales, rentals, stats = pull(user, password)
    except FetchError as exc:
        print(f"Listing refresh failed: {exc}", file=sys.stderr)
        return 1
    sales = dedupe(sales)
    rentals = dedupe(rentals)
    pulled = stats.get("pulled", 0)
    if pulled > 0 and not sales and not rentals:
        print(
            f"Listing refresh failed: the feed returned {pulled} records but none were "
            "active residential for-sale listings or for-lease rentals in Greater Vancouver "
            "or the Fraser Valley. listings/data.json and listings/rentals.json were not changed.",
            file=sys.stderr,
        )
        print("Summary: " + summary(stats), file=sys.stderr)
        return 1
    write_feed(output, source, destination_id, sales)
    write_feed(rentals_output, source, destination_id, rentals)
    print(
        f"Wrote {len(sales)} listings to {os.path.relpath(output, ROOT)} and "
        f"{len(rentals)} rentals to {os.path.relpath(rentals_output, ROOT)} from {source}."
    )
    print("Summary: " + summary(stats))
    return 0


def output_paths():
    """Sale file, then rentals file. An explicit DDF_OUTPUT keeps rentals beside it."""
    output = os.environ.get("DDF_OUTPUT", "").strip() or DEFAULT_OUTPUT
    rentals = os.environ.get("DDF_RENTALS_OUTPUT", "").strip()
    if not rentals:
        if os.environ.get("DDF_OUTPUT", "").strip():
            rentals = os.path.join(os.path.dirname(os.path.abspath(output)), "rentals.json")
        else:
            rentals = DEFAULT_RENTALS
    return output, rentals


def summary(stats):
    return ", ".join(f"{key}={stats[key]}" for key in sorted(stats))


def pull(user, password):
    """Return (source, destination_id, sale records, rental records, stats)."""
    stats = Counter()
    try:
        token, destination_id = fetch_token(user, password)
    except ApiUnavailable as exc:
        print(f"DDF Web API is not available ({exc}). Trying the RETS feed.")
        sales, rentals, destination_id = fetch_rets(user, password, stats)
        return "ddf-rets", destination_id, sales, rentals, stats
    except FetchError as oauth_error:
        print(f"DDF Web API login failed ({oauth_error}). Trying the RETS feed.")
        try:
            sales, rentals, destination_id = fetch_rets(user, password, stats)
        except FetchError as rets_error:
            raise FetchError(f"Web API: {oauth_error}. RETS: {rets_error}") from rets_error
        return "ddf-rets", destination_id, sales, rentals, stats
    print("Signed in to the DDF Web API.")
    offices, members = fetch_lookups(token)
    sales, rentals = fetch_odata(token, offices, members, stats)
    return "ddf-web-api", destination_id, sales, rentals, stats


def fetch_token(user, password):
    body = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": user,
        "client_secret": password,
        "scope": SCOPE,
    }).encode()
    req = urllib.request.Request(
        TOKEN_URL,
        data=body,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json", "User-Agent": UA},
    )
    try:
        status, payload, _headers = read_response(req)
    except urllib.error.URLError as exc:
        raise ApiUnavailable(f"could not reach {TOKEN_URL}: {exc.reason}") from exc
    if status == 404:
        raise ApiUnavailable(f"{TOKEN_URL} returned 404")
    if status != 200:
        raise FetchError(f"token endpoint returned {status}: {snip(payload)}")
    try:
        data = json.loads(payload.decode("utf-8", "replace"))
    except json.JSONDecodeError as exc:
        raise FetchError(f"token endpoint did not return JSON: {exc}") from exc
    token = data.get("access_token")
    if not token:
        raise FetchError("token endpoint did not return an access_token")
    return token, destination_from_token(token)


def destination_from_token(token):
    try:
        part = token.split(".")[1]
        padded = part + "=" * (-len(part) % 4)
        claims = json.loads(base64.urlsafe_b64decode(padded))
    except (IndexError, ValueError, json.JSONDecodeError):
        return None
    for key in ("destinationid", "destinationId", "DestinationId"):
        if claims.get(key):
            return str(claims[key])
    return None


def fetch_lookups(token):
    offices = {}
    members = {}
    try:
        for rec in odata_values(token, "Office", "OfficeKey,OfficeName"):
            key = first(rec, "OfficeKey", "OfficeMlsId")
            name = first(rec, "OfficeName", "OfficeFullName", "Name")
            if key and name:
                offices[str(key)] = str(name)
    except FetchError as exc:
        print(f"Office lookup skipped: {exc}")
    try:
        for rec in odata_values(token, "Member", "MemberKey,MemberFullName,MemberFirstName,MemberLastName"):
            key = first(rec, "MemberKey", "MemberMlsId")
            name = first(rec, "MemberFullName", "MemberName")
            if not name:
                name = " ".join(p for p in (first(rec, "MemberFirstName"), first(rec, "MemberLastName")) if p)
            if key and name:
                members[str(key)] = str(name)
    except FetchError as exc:
        print(f"Member lookup skipped: {exc}")
    return offices, members


def fetch_odata(token, offices, members, stats):
    sales = []
    rentals = []
    select = list(SELECT_FIELDS)
    expand = True
    status_filter = True
    url = None
    pages = 0
    started = False
    while True:
        if url is None:
            url = property_url(select, expand, status_filter, skip=0)
        try:
            status, payload = odata_request(token, url)
        except FetchError:
            if not started and can_relax(expand, status_filter, select):
                expand, status_filter, select = relax_query(expand, status_filter, select)
                url = None
                continue
            raise
        if status in (401, 403):
            raise FetchError(f"Property query returned {status}. The access token was not accepted.")
        if status == 400 and not started and can_relax(expand, status_filter, select):
            expand, status_filter, select = relax_query(expand, status_filter, select)
            url = None
            continue
        if status != 200:
            raise FetchError(f"Property query returned {status}: {snip(payload)}")
        try:
            data = json.loads(payload.decode("utf-8", "replace"))
        except json.JSONDecodeError as exc:
            raise FetchError(f"Property query did not return JSON: {exc}") from exc
        rows = data.get("value") or []
        started = True
        pages += 1
        for rec in rows:
            stats["pulled"] += 1
            channel, item = from_odata(rec, offices, members, stats, intent=None)
            if item and channel == "sale":
                sales.append(item)
            elif item and channel == "rent":
                rentals.append(item)
        nxt = data.get("@odata.nextLink") or data.get("odata.nextLink")
        if nxt:
            url = nxt
        elif len(rows) < PAGE_SIZE:
            break
        else:
            raise FetchError("Property query page was full but did not include @odata.nextLink, so the pull is incomplete.")
        if pages >= MAX_PAGES:
            raise FetchError(f"Stopped after {MAX_PAGES} pages so a partial feed would not replace the listing files.")
    return sales, rentals


def can_relax(expand, status_filter, select):
    if expand or status_filter:
        return True
    return any(field in select for field in OPTIONAL_SELECT)


def relax_query(expand, status_filter, select):
    if expand:
        print("Property query rejected $expand=Media; retrying without it.")
        return False, status_filter, select
    if status_filter:
        print("Property query rejected the status filter; filtering after download.")
        return expand, False, select
    for field in OPTIONAL_SELECT:
        if field in select:
            print(f"Property query rejected {field}; continuing without that field.")
            return expand, status_filter, [item for item in select if item != field]
    return expand, status_filter, select


def property_url(select, expand, status_filter, skip):
    params = {"$top": str(PAGE_SIZE), "$select": ",".join(select)}
    if expand:
        params["$expand"] = "Media($select=MediaURL,MediaCategory,Order,PreferredPhotoYN)"
    if status_filter:
        params["$filter"] = "StandardStatus eq 'Active'"
    if skip:
        params["$skip"] = str(skip)
    return ODATA_ROOT + "/Property?" + urllib.parse.urlencode(params)


def odata_values(token, collection, select):
    url = ODATA_ROOT + f"/{collection}?" + urllib.parse.urlencode({"$select": select, "$top": str(PAGE_SIZE)})
    pages = 0
    while url:
        status, payload = odata_request(token, url)
        if status == 400 and "$select" in url:
            url = ODATA_ROOT + f"/{collection}?" + urllib.parse.urlencode({"$top": str(PAGE_SIZE)})
            continue
        if status != 200:
            raise FetchError(f"{collection} query returned {status}: {snip(payload)}")
        data = json.loads(payload.decode("utf-8", "replace"))
        for rec in data.get("value") or []:
            yield rec
        url = data.get("@odata.nextLink") or data.get("odata.nextLink")
        pages += 1
        if pages >= MAX_PAGES:
            break


def odata_request(token, url):
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": UA,
    })
    try:
        status, payload, _headers = read_response(req)
    except urllib.error.URLError as exc:
        raise FetchError(f"could not reach the DDF Web API: {exc.reason}") from exc
    return status, payload


def fetch_rets(user, password, stats):
    jar = CookieJar()
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    for base in ("https://data.crea.ca/", "https://data.crea.ca/Login.svc/Login"):
        password_mgr.add_password(None, base, user, password)
        password_mgr.add_password("CREA.Distribution", base, user, password)
    opener = urllib.request.build_opener(
        urllib.request.HTTPDigestAuthHandler(password_mgr),
        urllib.request.HTTPCookieProcessor(jar),
    )
    session_id = {}

    def open_url(url):
        headers = {"User-Agent": UA, "RETS-Version": "RETS/1.7.2", "Accept": "*/*"}
        if session_id.get("id"):
            headers["Cookie"] = f"X-SESSIONID={session_id['id']}"
        req = urllib.request.Request(url, headers=headers)
        try:
            resp = opener.open(req, timeout=90)
        except urllib.error.HTTPError as exc:
            body = exc.read()
            return exc.code, body, exc.headers
        except urllib.error.URLError as exc:
            raise FetchError(f"could not reach the RETS feed: {exc.reason}") from exc
        body = resp.read()
        capture_session(resp.headers, session_id)
        return resp.status, body, resp.headers

    status, body, headers = open_url(RETS_LOGIN)
    capture_session(headers, session_id)
    if status != 200:
        raise FetchError(f"RETS login returned {status}: {snip(body)}")
    text = body.decode("utf-8", "replace")
    code = rets_code(text)
    if code not in (None, "0"):
        raise FetchError(f"RETS login ReplyCode {code}: {snip(body)}")
    search = rets_url(text, "Search") or RETS_SEARCH
    logout = rets_url(text, "Logout") or RETS_LOGOUT
    destination_id = rets_value(text, "Broker") or rets_value(text, "User")
    if destination_id and "," in destination_id:
        destination_id = destination_id.split(",")[0].strip()
    sales = []
    rentals = []
    offset = 1
    pages = 0
    fmt = "STANDARD-XML-Encoded"
    try:
        while True:
            params = {
                "SearchType": "Property",
                "Class": "Property",
                "QueryType": "DMQL2",
                "Query": "(LastUpdated=2000-01-01T00:00:00Z)",
                "Format": fmt,
                "Limit": str(PAGE_SIZE),
                "Offset": str(offset),
                "Count": "1",
            }
            status, body, headers = open_url(search + "?" + urllib.parse.urlencode(params))
            capture_session(headers, session_id)
            if status != 200:
                raise FetchError(f"RETS search returned {status}: {snip(body)}")
            page_text = body.decode("utf-8", "replace")
            code = rets_code(page_text)
            if code not in (None, "0", "20201"):
                if fmt == "STANDARD-XML-Encoded":
                    fmt = "STANDARD-XML"
                    print(f"RETS search ReplyCode {code} for encoded XML; retrying STANDARD-XML.")
                    continue
                raise FetchError(f"RETS search ReplyCode {code}: {snip(body)}")
            details = parse_property_details(page_text)
            pages += 1
            for rec in details:
                stats["pulled"] += 1
                channel, item = from_rets(rec, stats, intent=None)
                if item and channel == "sale":
                    sales.append(item)
                elif item and channel == "rent":
                    rentals.append(item)
            if code == "20201" or len(details) < PAGE_SIZE:
                break
            offset += len(details)
            if pages >= MAX_PAGES:
                raise FetchError(f"Stopped after {MAX_PAGES} RETS pages so a partial feed would not replace the listing files.")
    finally:
        try:
            open_url(logout)
        except FetchError:
            pass
    return sales, rentals, destination_id or None


def capture_session(headers, session_id):
    if headers is None:
        return
    raw = headers.get("Set-Cookie") or ""
    match = re.search(r"X-SESSIONID=([^;,\s]+)", raw, re.I)
    if match:
        session_id["id"] = match.group(1)
    elif headers.get("X-SESSIONID"):
        session_id["id"] = headers.get("X-SESSIONID")


def rets_code(text):
    match = re.search(r"ReplyCode=\"(\d+)\"", text)
    return match.group(1) if match else None


def rets_url(text, key):
    match = re.search(rf"^{re.escape(key)}=(https://\S+)", text, re.M)
    return match.group(1).strip() if match else None


def rets_value(text, key):
    match = re.search(rf"^{re.escape(key)}=(.+)$", text, re.M)
    return match.group(1).strip() if match else None


def parse_property_details(xml_text):
    """Yield dicts from STANDARD-XML PropertyDetails, or compact DATA rows."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return list(parse_compact(xml_text))
    details = [el for el in root.iter() if local(el.tag) == "PropertyDetails"]
    if details:
        return [rets_detail_dict(el) for el in details]
    compact = list(parse_compact(xml_text))
    if compact:
        return compact
    return []


def parse_compact(xml_text):
    columns = None
    for line in xml_text.splitlines():
        if "<COLUMNS>" in line:
            inner = re.sub(r"</?COLUMNS>", "", line)
            columns = [c for c in inner.split("\t") if c]
        elif "<DATA>" in line and columns:
            inner = re.sub(r"</?DATA>", "", line)
            values = inner.split("\t")
            if values and values[0] == "":
                values = values[1:]
            if values and values[-1] == "":
                values = values[:-1]
            yield dict(zip(columns, values))


def rets_detail_dict(el):
    """Flatten the fields the normalizer needs. Nested agent/office stay named."""
    out = {"_id": el.get("ID") or ""}
    for child in list(el):
        name = local(child.tag)
        if name == "Address":
            out["Address"] = {local(c.tag): elem_text(c) for c in list(child)}
        elif name == "Building":
            out["Building"] = {local(c.tag): elem_text(c) for c in list(child)}
        elif name == "Photo":
            out["Photos"] = [photo_dict(p) for p in child.iter() if local(p.tag) == "PropertyPhoto"]
        elif name == "AgentDetails":
            out.setdefault("Agents", []).append(agent_dict(child))
        else:
            out[name] = elem_text(child)
    return out


def photo_dict(el):
    data = {local(c.tag): elem_text(c) for c in list(el)}
    data["SequenceID"] = data.get("SequenceID") or el.get("SequenceID") or ""
    return data


def agent_dict(el):
    data = {"Name": "", "OfficeName": ""}
    for child in list(el):
        name = local(child.tag)
        if name == "Name":
            data["Name"] = elem_text(child)
        elif name in ("Office", "OfficeDetails"):
            for office_child in child.iter():
                if local(office_child.tag) == "Name" and elem_text(office_child):
                    data["OfficeName"] = elem_text(office_child)
                    break
    return data


def local(tag):
    return tag.rsplit("}", 1)[-1]


def elem_text(el):
    if el is None:
        return ""
    text = (el.text or "").strip()
    if text:
        return text
    for attr in ("DisplayName", "Value", "Name", "Text"):
        if el.get(attr):
            return el.get(attr).strip()
    return "".join(el.itertext()).strip()


def from_odata(rec, offices, members, stats, intent="sale"):
    """Normalize one OData property.

    intent "sale" or "rent" returns that record or None.
    intent None returns (channel, record) after a single pass.
    """
    channel, item = build_odata(rec, offices, members, stats)
    return finish_intent(channel, item, intent, stats)


def from_rets(rec, stats, intent="sale"):
    """Normalize one RETS property. Same intent contract as from_odata."""
    channel, item = build_rets(rec, stats)
    return finish_intent(channel, item, intent, stats)


def finish_intent(channel, item, intent, stats):
    if intent is None:
        return channel, item
    if channel != intent:
        if item:
            stats["kept"] = max(0, stats["kept"] - 1)
        return None
    return item


def build_odata(rec, offices, members, stats):
    if flag_false(rec.get("InternetEntireListingDisplayYN")):
        stats["opted_out"] += 1
        return None, None
    status = first(rec, "StandardStatus", "MlsStatus", "ListingStatus")
    if not is_active(status):
        stats["not_active"] += 1
        return None, None
    city = first(rec, "City")
    province = first(rec, "StateOrProvince", "Province")
    aor = " ".join(p for p in (first(rec, "ListAOR"), first(rec, "OriginatingSystemName")) if p)
    if not in_target_area(city, province, aor):
        stats["outside_area"] += 1
        return None, None
    type_parts = [textify(rec.get(key)) for key in ("PropertyType", "PropertySubType", "StructureType")]
    transaction = textify(rec.get("TransactionType"))
    frequency = textify(rec.get("LeaseAmountFrequency"))
    channel = listing_channel(transaction, type_parts, rec.get("LeaseAmount"), rec.get("ListPrice"), frequency)
    if channel == "rent":
        label = rental_label(type_parts, transaction, stats)
        amount, freq = rent_source(rec.get("LeaseAmount"), rec.get("ListPrice"), frequency)
        price = monthly_rent(amount, freq)
        if label and price is None:
            stats["rent_unusable"] += 1
            return None, None
    else:
        label = residential_label(type_parts, transaction, stats)
        price = parse_number(rec.get("ListPrice"))
    if not label:
        return None, None
    brokerage = first(rec, "ListOfficeName", "ListingOfficeName", "OfficeName")
    office = rec.get("ListOffice") or rec.get("Office")
    if not brokerage and isinstance(office, dict):
        brokerage = first(office, "OfficeName", "Name")
    if not brokerage:
        brokerage = offices.get(str(rec.get("ListOfficeKey") or ""))
    agent = first(rec, "ListAgentFullName", "ListAgentName")
    member = rec.get("ListAgent") or rec.get("Member")
    if not agent and isinstance(member, dict):
        agent = first(member, "MemberFullName", "MemberName", "Name")
    if not agent:
        agent = members.get(str(rec.get("ListAgentKey") or ""))
    photos = photo_urls(rec.get("Media"))
    show_address = not flag_false(rec.get("InternetAddressDisplayYN"))
    listing_id = first(rec, "ListingKey", "ListingId")
    item = compact(
        listing_id=listing_id,
        mls=first(rec, "ListingId", "ListingKey"),
        price=price,
        address=street_line(rec) if show_address else "",
        city=city,
        area=first(rec, "CityRegion", "SubdivisionName"),
        postal=first(rec, "PostalCode") if show_address else "",
        beds=parse_int(rec.get("BedroomsTotal")),
        baths=parse_baths(rec.get("BathroomsTotalInteger"), rec.get("BathroomsPartial")),
        type_label=label,
        sqft=parse_area(rec.get("LivingArea") or rec.get("BuildingAreaTotal") or rec.get("AboveGradeFinishedArea"),
                        rec.get("LivingAreaUnits") or rec.get("BuildingAreaUnits") or ""),
        year=parse_year(rec.get("YearBuilt")),
        parking=parse_int(rec.get("ParkingTotal")),
        remarks=first(rec, "PublicRemarks"),
        brokerage=brokerage or "",
        agent=agent or "",
        photos=photos,
        realtor_url=clean_url(first(rec, "ListingURL", "MoreInformationLink")),
        updated=first(rec, "ModificationTimestamp"),
        analytics_id=listing_id if digits(listing_id) else "",
        stats=stats,
    )
    return channel, item


def build_rets(rec, stats):
    status = first(rec, "StandardStatus", "MlsStatus", "ListingStatus", "Status")
    if not is_active(status):
        stats["not_active"] += 1
        return None, None
    address = rec.get("Address") if isinstance(rec.get("Address"), dict) else {}
    building = rec.get("Building") if isinstance(rec.get("Building"), dict) else {}
    city = first(address, "City") or first(rec, "City")
    province = first(address, "Province", "StateOrProvince") or first(rec, "StateOrProvince", "Province")
    aor = first(rec, "Board", "ListAOR", "OriginatingSystemName")
    if not in_target_area(city, province, aor):
        stats["outside_area"] += 1
        return None, None
    transaction = first(rec, "TransactionType")
    type_parts = [
        first(rec, "PropertyType", "PropertySubType"),
        first(building, "Type", "ConstructionStyleAttachment"),
        first(rec, "StructureType", "BuildingType"),
    ]
    lease_amount = first(rec, "Lease", "LeaseAmount")
    list_price = first(rec, "Price", "ListPrice")
    frequency = first(rec, "LeasePerTime", "PricePerTime", "LeaseAmountFrequency", "LeaseTermRemainingFreq")
    channel = listing_channel(transaction, type_parts, lease_amount, list_price, frequency)
    if channel == "rent":
        label = rental_label(type_parts, transaction, stats)
        amount, freq = rent_source(lease_amount, list_price, frequency)
        price = monthly_rent(amount, freq)
        if label and price is None:
            stats["rent_unusable"] += 1
            return None, None
    else:
        label = residential_label(type_parts, transaction, stats)
        price = parse_number(list_price)
    if not label:
        return None, None
    agents = rec.get("Agents") or []
    agent_name = ""
    brokerage = ""
    if agents:
        agent_name = agents[0].get("Name") or ""
        brokerage = agents[0].get("OfficeName") or ""
    brokerage = brokerage or first(rec, "ListOfficeName", "OfficeName")
    # Sequence 0 is the default photo in the RETS feed. Stable order by SequenceID.
    photos = []
    if rec.get("Photos"):
        ordered = sorted(rec["Photos"], key=lambda p: parse_int(p.get("SequenceID")) or 0)
        for photo in ordered:
            url = photo.get("LargePhotoURL") or photo.get("PhotoURL") or ""
            if str(url).startswith("https://") and url not in photos:
                photos.append(url)
            if len(photos) >= MAX_PHOTOS:
                break
    street = first(address, "StreetAddress") or street_line({
        "UnitNumber": first(address, "UnitNumber"),
        "StreetNumber": first(address, "StreetNumber"),
        "StreetDirPrefix": first(address, "StreetDirectionPrefix"),
        "StreetName": first(address, "StreetName"),
        "StreetSuffix": first(address, "StreetSuffix"),
    })
    street = street.replace("|", ", ")
    listing_id = first(rec, "_id", "ListingID", "ListingId", "ListingKey")
    item = compact(
        listing_id=listing_id,
        mls=first(rec, "ListingID", "ListingId", "ListingKey") or listing_id,
        price=price,
        address=street,
        city=city,
        area=first(address, "Neighbourhood", "CommunityName", "Subdivision") or first(rec, "CityRegion"),
        postal=first(address, "PostalCode") or first(rec, "PostalCode"),
        beds=parse_int(first(building, "BedroomsTotal") or first(rec, "BedroomsTotal")),
        baths=parse_baths(first(building, "BathroomTotal") or first(rec, "BathroomsTotalInteger"), None),
        type_label=label,
        sqft=parse_area(first(building, "SizeInterior", "SizeTotal") or first(rec, "LivingArea", "BuildingAreaTotal"), ""),
        year=parse_year(first(building, "ConstructedDate") or first(rec, "YearBuilt")),
        parking=parse_int(first(rec, "ParkingSpaceTotal", "ParkingTotal")),
        remarks=first(rec, "PublicRemarks"),
        brokerage=brokerage,
        agent=agent_name or first(rec, "ListAgentFullName"),
        photos=photos,
        realtor_url=clean_url(first(rec, "MoreInformationLink", "ListingURL")),
        updated=first(rec, "LastUpdated", "ModificationTimestamp"),
        analytics_id=listing_id if digits(listing_id) else "",
        stats=stats,
    )
    return channel, item


def listing_channel(transaction, type_parts, lease_amount, list_price, frequency):
    """Pick sale or rent. A listing is never both.

    Explicit sale language with no lease language stays a sale, even if a
    lease amount is also filled in. Lease/rent language, a lease amount with
    no list price, or a lease amount plus a frequency goes to rentals.
    """
    trans = textify(transaction).lower()
    blob = " ".join(p for p in (textify(p) for p in type_parts) if p).lower()
    lease_words = is_lease(trans) or is_lease(blob)
    sale_words = "sale" in trans
    has_lease = positive_amount(lease_amount)
    has_list = positive_amount(list_price)
    has_freq = bool(textify(frequency))
    if sale_words and not lease_words:
        return "sale"
    if lease_words:
        return "rent"
    if has_lease and (not has_list or has_freq):
        return "rent"
    return "sale"


def rent_source(lease_amount, list_price, frequency):
    """Prefer LeaseAmount. Fall back to ListPrice/Price when the row is a lease."""
    if positive_amount(lease_amount):
        return lease_amount, frequency
    return list_price, frequency


def monthly_rent(amount, frequency):
    """Dollars per month. Blank frequency is treated as monthly.

    RESO-style frequencies:
    Weekly * 52/12, Bi-Weekly * 26/12, Semi-Monthly * 2,
    Bi-Monthly (every two months) / 2, Annually / 12.
    One Time and any unrecognized frequency return None.
    """
    number = parse_number(amount)
    if number is None or number <= 0:
        return None
    freq = re.sub(r"[^a-z]", "", textify(frequency).lower())
    factors = {
        "": (1, 1),
        "monthly": (1, 1),
        "month": (1, 1),
        "permonth": (1, 1),
        "weekly": (52, 12),
        "week": (52, 12),
        "perweek": (52, 12),
        "biweekly": (26, 12),
        "semimonthly": (2, 1),
        "bimonthly": (1, 2),
        "annually": (1, 12),
        "annual": (1, 12),
        "yearly": (1, 12),
        "year": (1, 12),
        "peryear": (1, 12),
        "daily": (365, 12),
        "onetime": None,
    }
    if freq not in factors or factors[freq] is None:
        return None
    num, den = factors[freq]
    monthly = number * num / den
    return int(math.floor(monthly + 0.5))


def positive_amount(value):
    number = parse_number(value)
    return number is not None and number > 0


def compact(listing_id, mls, price, address, city, area, postal, beds, baths, type_label,
            sqft, year, parking, remarks, brokerage, agent, photos, realtor_url, updated,
            analytics_id, stats, transaction_note=""):
    if not listing_id:
        stats["missing_id"] += 1
        return None
    # Never carry sold-price fields. `price` is the list price only.
    item = {
        "id": str(listing_id),
        "mls": str(mls or listing_id),
        "price": int(price) if isinstance(price, float) and price.is_integer() else price,
        "address": address or None,
        "city": city or "",
        "area": area or "",
        "postal": postal or "",
        "beds": beds,
        "baths": baths,
        "type": type_label,
        "sqft": sqft,
        "year": year,
        "parking": parking,
        "remarks": remarks or "",
        "brokerage": brokerage or "",
        "agent": agent or "",
        "photos": photos[:MAX_PHOTOS],
        "realtorUrl": realtor_url or "",
        "updated": updated or "",
    }
    if analytics_id:
        item["analyticsId"] = str(analytics_id)
    if not item["brokerage"]:
        stats["missing_brokerage"] += 1
    stats["kept"] += 1
    return item


def residential_label(parts, transaction, stats):
    texts = [p for p in (textify(p) for p in parts) if p]
    trans = textify(transaction)
    if is_lease(trans) and "sale" not in trans.lower():
        stats["not_residential"] += 1
        return None
    blob = " ".join(texts).lower()
    if blob or trans:
        if any(phrase in blob or phrase in trans.lower() for phrase in EXCLUDE_PHRASES):
            stats["not_residential"] += 1
            return None
        if any(has_word(blob, word) or has_word(trans.lower(), word) for word in EXCLUDE_WORDS):
            stats["not_residential"] += 1
            return None
        for keys, label in TYPE_RULES:
            if any(key in blob for key in keys):
                return label
        if "residential" in blob:
            return "Other residential"
        stats["not_residential"] += 1
        return None
    stats["type_unknown"] += 1
    return "Other residential"


def rental_label(parts, transaction, stats):
    """Residential for-lease label. Commercial types are excluded; lease words are not."""
    texts = [p for p in (textify(p) for p in parts) if p]
    blob = " ".join(texts).lower()
    trans = textify(transaction).lower()
    hay = f"{blob} {trans}".strip()
    if any(phrase in hay for phrase in COMMERCIAL_PHRASES):
        stats["not_residential"] += 1
        return None
    if any(has_word(hay, word) for word in EXCLUDE_WORDS):
        stats["not_residential"] += 1
        return None
    for keys, label in TYPE_RULES:
        if any(key in blob for key in keys):
            return label
    if "residential" in blob or is_lease(hay) or not blob:
        return "Other residential"
    stats["not_residential"] += 1
    return None


def is_lease(text):
    low = (text or "").lower()
    return any(word in low for word in ("lease", "rent", "rental"))


def is_active(status):
    text = textify(status).lower()
    if not text:
        return True
    if any(word in text for word in SOLD_WORDS):
        return False
    return "active" in text or text in {"a", "new"}


def in_target_area(city, province, aor):
    prov = (province or "").strip().lower().rstrip(".")
    if prov and prov not in BC_NAMES:
        return False
    if norm_city(city) in GV_FV_CITIES:
        return True
    low = (aor or "").lower()
    return any(hint in low for hint in AOR_HINTS)


def norm_city(city):
    text = re.sub(r"\s+", " ", (city or "").strip().lower())
    text = re.sub(r"^(city|district|township|village|municipality) of ", "", text)
    return text


def has_word(blob, word):
    return re.search(r"(?:^|[^a-z])" + re.escape(word) + r"(?:$|[^a-z])", blob or "") is not None


def textify(value):
    if value is None or isinstance(value, bool):
        return ""
    if isinstance(value, (int, float)):
        return ""
    if isinstance(value, list):
        return " ".join(p for p in (textify(v) for v in value) if p)
    if isinstance(value, dict):
        return " ".join(p for p in (textify(v) for v in value.values()) if p)
    return str(value).strip()


def first(rec, *keys):
    if not isinstance(rec, dict):
        return ""
    for key in keys:
        value = rec.get(key)
        if value is None or value == "":
            continue
        if isinstance(value, str):
            text = value.strip()
            if text:
                return text
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            return str(value)
    return ""


def flag_false(value):
    if value is False or value == 0:
        return True
    if isinstance(value, str) and value.strip().lower() in {"false", "n", "no", "0"}:
        return True
    return False


def street_line(rec):
    parts = [first(rec, key) for key in ("StreetNumber", "StreetDirPrefix", "StreetName", "StreetSuffix")]
    line = " ".join(p for p in parts if p)
    unit = first(rec, "UnitNumber")
    if unit and line:
        return f"{unit}-{line}"
    return line or unit


def photo_urls(media):
    rows = media or []
    if isinstance(rows, dict):
        rows = rows.get("value") or []
    picked = []
    for media_row in rows:
        if not isinstance(media_row, dict):
            continue
        category = textify(media_row.get("MediaCategory")).lower()
        if category and "photo" not in category and "image" not in category:
            continue
        url = media_row.get("MediaURL") or media_row.get("LargePhotoURL") or media_row.get("PhotoURL") or ""
        if not str(url).startswith("https://"):
            continue
        try:
            order = int(media_row.get("Order"))
        except (TypeError, ValueError):
            order = 999
        preferred = 0 if media_row.get("PreferredPhotoYN") else 1
        picked.append((preferred, order, str(url)))
    picked.sort()
    out = []
    for _preferred, _order, url in picked:
        if url not in out:
            out.append(url)
        if len(out) >= MAX_PHOTOS:
            break
    return out


def clean_url(url):
    if not url or not str(url).startswith("https://"):
        return ""
    parts = urllib.parse.urlsplit(url)
    query = urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
    query = [(k, v) for k, v in query if not k.lower().startswith("utm_")]
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, parts.path, urllib.parse.urlencode(query), ""))


def parse_number(value):
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"\d[\d,]*\.?\d*", str(value))
    if not match:
        return None
    return float(match.group(0).replace(",", ""))


def parse_int(value):
    number = parse_number(value)
    if number is None:
        return None
    return int(number)


def parse_baths(total, partial):
    number = parse_number(total)
    if number is None:
        return None
    if isinstance(total, str) and "." in total:
        return number
    return int(number) if number.is_integer() else number


def parse_year(value):
    match = re.search(r"\b(18|19|20)\d{2}\b", str(value or ""))
    return int(match.group(0)) if match else None


def parse_area(value, units):
    number = parse_number(value)
    if number is None or number <= 0:
        return None
    blob = f"{units} {value}".lower()
    if any(mark in blob for mark in ("meter", "metre", "sqm", "m2", "m²")):
        number *= 10.76391041671
    return int(round(number))


def digits(value):
    return bool(value) and str(value).isdigit()


def dedupe(records):
    by_id = {}
    for rec in records:
        by_id[rec["id"]] = rec
    return [by_id[key] for key in sorted(by_id)]


def write_feed(path, source, destination_id, listings):
    payload = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": source,
        "sample": False,
        "destinationId": destination_id,
        "area": "Greater Vancouver and Fraser Valley",
        "count": len(listings),
        "listings": listings,
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write("\n")
    os.replace(tmp, path)


def read_response(req):
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            return resp.status, resp.read(), resp.headers
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(), exc.headers


def snip(payload):
    if isinstance(payload, bytes):
        text = payload.decode("utf-8", "replace")
    else:
        text = str(payload)
    text = re.sub(r"(client_secret|password)=[^&\s]+", r"\1=***", text, flags=re.I)
    return text[:400].replace("\n", " ")


if __name__ == "__main__":
    sys.exit(main())
