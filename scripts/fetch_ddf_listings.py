#!/usr/bin/env python3
"""Refresh listings/data.json from the CREA REALTOR.ca DDF feed.

Tries the current DDF Web API (OData) at https://ddfapi.realtor.ca first.
The destination username and password are the OAuth client id and secret
(scope DDFApi_Read) at https://identity.crea.ca/connect/token. If that API
is not reachable, falls back to the legacy RETS feed at https://data.crea.ca.

Reads DDF_USERNAME and DDF_PASSWORD. If either is missing, exits 0 and
does not change the JSON file. A successful run replaces the file, so
listings that left the feed disappear. Only active residential for-sale
listings in Greater Vancouver and the Fraser Valley are kept. Sold fields
are never written. Photos stay as remote https URLs.

No third-party packages: the GitHub Action runs this with the stdlib.
"""
from __future__ import annotations

import base64
import json
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
EXCLUDE_PHRASES = (
    "commercial", "industrial", "business opportunity", "warehouse", "hotel", "motel",
    "vacant land", "vacant", "for rent", "rental", "lease",
)
EXCLUDE_WORDS = ("land", "office", "farm", "retail", "parking", "agricultural")
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
    "InternetAddressDisplayYN", "ParkingTotal", "LeaseAmount", "ModificationTimestamp",
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
    output = os.environ.get("DDF_OUTPUT", "").strip() or DEFAULT_OUTPUT
    try:
        source, destination_id, records, stats = pull(user, password)
    except FetchError as exc:
        print(f"Listing refresh failed: {exc}", file=sys.stderr)
        return 1
    kept = dedupe(records)
    pulled = stats.get("pulled", 0)
    if pulled > 0 and not kept:
        print(
            f"Listing refresh failed: the feed returned {pulled} records but none were "
            "active residential listings in Greater Vancouver or the Fraser Valley. "
            "listings/data.json was not changed.",
            file=sys.stderr,
        )
        print("Summary: " + summary(stats), file=sys.stderr)
        return 1
    write_feed(output, source, destination_id, kept)
    print(f"Wrote {len(kept)} listings to {os.path.relpath(output, ROOT)} from {source}.")
    print("Summary: " + summary(stats))
    return 0


def summary(stats):
    return ", ".join(f"{key}={stats[key]}" for key in sorted(stats))


def pull(user, password):
    """Return (source, destination_id, compact records, stats)."""
    stats = Counter()
    try:
        token, destination_id = fetch_token(user, password)
    except ApiUnavailable as exc:
        print(f"DDF Web API is not available ({exc}). Trying the RETS feed.")
        records, destination_id = fetch_rets(user, password, stats)
        return "ddf-rets", destination_id, records, stats
    except FetchError as oauth_error:
        print(f"DDF Web API login failed ({oauth_error}). Trying the RETS feed.")
        try:
            records, destination_id = fetch_rets(user, password, stats)
        except FetchError as rets_error:
            raise FetchError(f"Web API: {oauth_error}. RETS: {rets_error}") from rets_error
        return "ddf-rets", destination_id, records, stats
    print("Signed in to the DDF Web API.")
    offices, members = fetch_lookups(token)
    records = fetch_odata(token, offices, members, stats)
    return "ddf-web-api", destination_id, records, stats


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
    kept = []
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
            if not started and (expand or status_filter or "PropertyType" in select):
                expand, status_filter, select = relax_query(expand, status_filter, select)
                url = None
                continue
            raise
        if status in (401, 403):
            raise FetchError(f"Property query returned {status}. The access token was not accepted.")
        if status == 400 and not started and (expand or status_filter or "PropertyType" in select):
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
            item = from_odata(rec, offices, members, stats)
            if item:
                kept.append(item)
        nxt = data.get("@odata.nextLink") or data.get("odata.nextLink")
        if nxt:
            url = nxt
        elif len(rows) < PAGE_SIZE:
            break
        else:
            raise FetchError("Property query page was full but did not include @odata.nextLink, so the pull is incomplete.")
        if pages >= MAX_PAGES:
            raise FetchError(f"Stopped after {MAX_PAGES} pages so a partial feed would not replace listings/data.json.")
    return kept


def relax_query(expand, status_filter, select):
    if expand:
        print("Property query rejected $expand=Media; retrying without it.")
        return False, status_filter, select
    if status_filter:
        print("Property query rejected the status filter; filtering after download.")
        return expand, False, select
    print("Property query rejected PropertyType; continuing without that field.")
    return expand, status_filter, [field for field in select if field != "PropertyType"]


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
    kept = []
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
                item = from_rets(rec, stats)
                if item:
                    kept.append(item)
            if code == "20201" or len(details) < PAGE_SIZE:
                break
            offset += len(details)
            if pages >= MAX_PAGES:
                raise FetchError(f"Stopped after {MAX_PAGES} RETS pages so a partial feed would not replace listings/data.json.")
    finally:
        try:
            open_url(logout)
        except FetchError:
            pass
    return kept, destination_id or None


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


def from_odata(rec, offices, members, stats):
    if flag_false(rec.get("InternetEntireListingDisplayYN")):
        stats["opted_out"] += 1
        return None
    status = first(rec, "StandardStatus", "MlsStatus", "ListingStatus")
    if not is_active(status):
        stats["not_active"] += 1
        return None
    city = first(rec, "City")
    province = first(rec, "StateOrProvince", "Province")
    aor = " ".join(p for p in (first(rec, "ListAOR"), first(rec, "OriginatingSystemName")) if p)
    if not in_target_area(city, province, aor):
        stats["outside_area"] += 1
        return None
    type_parts = [textify(rec.get(key)) for key in ("PropertyType", "PropertySubType", "StructureType")]
    transaction = textify(rec.get("LeaseAmount"))
    # A lease amount with no list price is a rental. A list price keeps it a sale.
    if rec.get("LeaseAmount") not in (None, "", 0, "0") and not rec.get("ListPrice"):
        stats["not_residential"] += 1
        return None
    label = residential_label(type_parts, "", stats)
    if not label:
        return None
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
    return compact(
        listing_id=listing_id,
        mls=first(rec, "ListingId", "ListingKey"),
        price=parse_number(rec.get("ListPrice")),
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
        transaction_note=transaction,
    )


def from_rets(rec, stats):
    status = first(rec, "StandardStatus", "MlsStatus", "ListingStatus", "Status")
    if not is_active(status):
        stats["not_active"] += 1
        return None
    address = rec.get("Address") if isinstance(rec.get("Address"), dict) else {}
    building = rec.get("Building") if isinstance(rec.get("Building"), dict) else {}
    city = first(address, "City") or first(rec, "City")
    province = first(address, "Province", "StateOrProvince") or first(rec, "StateOrProvince", "Province")
    aor = first(rec, "Board", "ListAOR", "OriginatingSystemName")
    if not in_target_area(city, province, aor):
        stats["outside_area"] += 1
        return None
    transaction = first(rec, "TransactionType")
    type_parts = [
        first(rec, "PropertyType", "PropertySubType"),
        first(building, "Type", "ConstructionStyleAttachment"),
        first(rec, "StructureType", "BuildingType"),
    ]
    if is_lease(transaction) and "sale" not in transaction.lower():
        stats["not_residential"] += 1
        return None
    label = residential_label(type_parts, transaction, stats)
    if not label:
        return None
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
        photos = []
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
    return compact(
        listing_id=listing_id,
        mls=first(rec, "ListingID", "ListingId", "ListingKey") or listing_id,
        price=parse_number(first(rec, "Price", "ListPrice")),
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
        transaction_note=transaction,
    )


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
