#!/usr/bin/env python3
"""Read-only look at how this DDF destination exposes leases.

Prints field names, enum names, and counts. It does not write listing files
and it does not print the client id, client secret, access token, or
destination id.
"""
import os
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_ddf_listings as ddf

INTERESTING_ENUMS = (
    "propertysubtype", "structuretype", "standardstatus", "feefrequency",
    "existingleasetype", "businesstype", "currentuse", "possibleuse",
    "propertytype", "transactiontype", "listingagreement",
)
EXTRA_FIELDS = (
    "TotalActualRent", "ExistingLeaseType", "BusinessType", "CurrentUse",
    "PossibleUse", "LeasePerUnit", "AvailabilityDate",
)


def local(tag):
    return tag.rsplit("}", 1)[-1]


def parse_metadata(xml_bytes):
    """Entity set names, Property field names, and enum members."""
    root = ET.fromstring(xml_bytes)
    entity_sets = []
    fields = {}
    enums = {}
    for node in root.iter():
        name = local(node.tag)
        if name == "EntitySet" and node.get("Name"):
            entity_sets.append(node.get("Name"))
        elif name == "EntityType" and node.get("Name"):
            props = []
            for child in list(node):
                if local(child.tag) == "Property" and child.get("Name"):
                    props.append((child.get("Name"), child.get("Type") or ""))
            fields[node.get("Name")] = props
        elif name == "EnumType" and node.get("Name"):
            members = []
            for child in list(node):
                if local(child.tag) == "Member" and child.get("Name"):
                    members.append(child.get("Name"))
            enums[node.get("Name")] = members
    return entity_sets, fields, enums


def interesting(enum_name):
    low = enum_name.lower()
    if low in INTERESTING_ENUMS:
        return True
    return any(word in low for word in ("lease", "rent", "transaction", "agreement"))


def scrub(text):
    if isinstance(text, bytes):
        text = text.decode("utf-8", "replace")
    text = ddf.re.sub(r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}", "[redacted]", text)
    text = ddf.re.sub(r"(client_secret|password|access_token)=[^&\s]+", r"\1=[redacted]", text, flags=ddf.re.I)
    return text.replace("\n", " ")[:300]


def get_json(token, url):
    status, payload = ddf.odata_request(token, url)
    if status != 200:
        print(f"GET {url.split('?', 1)[0]} status {status}: {scrub(payload)}")
        return status, payload, None
    return status, payload, ddf.json.loads(payload.decode("utf-8", "replace"))


def tally_line(counter, limit=30):
    return ", ".join(f"{name}={count}" for name, count in counter.most_common(limit)) or "(none)"


def price_bucket(value):
    number = ddf.parse_number(value)
    if number is None:
        return "blank"
    if number < 5000:
        return "under_5k"
    if number < 20000:
        return "under_20k"
    if number < 100000:
        return "under_100k"
    return "100k_plus"


def scan_property(token):
    select = [
        "ListingKey", "PropertySubType", "StructureType", "StandardStatus",
        "ListPrice", "LeaseAmount", "LeaseAmountFrequency",
    ] + [field for field in EXTRA_FIELDS]
    subtypes = ddf.Counter()
    structures = ddf.Counter()
    statuses = ddf.Counter()
    prices = ddf.Counter()
    extras = {field: ddf.Counter() for field in ("LeaseAmountFrequency",) + EXTRA_FIELDS}
    lease_amount_set = 0
    total_actual_rent_set = 0
    pulled = 0
    pages = 0
    url = None
    while True:
        if url is None:
            url = ddf.ODATA_ROOT + "/Property?" + ddf.urllib.parse.urlencode({
                "$select": ",".join(select),
                "$top": str(ddf.PAGE_SIZE),
            })
        status, payload, data = get_json(token, url)
        if data is None:
            missing = ddf.rejected_field(payload)
            if pages == 0 and missing in select:
                print(f"property scan dropped {missing}")
                select = [field for field in select if field != missing]
                extras.pop(missing, None)
                url = None
                continue
            return
        rows = data.get("value") or []
        pages += 1
        for rec in rows:
            pulled += 1
            subtypes[ddf.textify(rec.get("PropertySubType")) or "(blank)"] += 1
            structures[ddf.textify(rec.get("StructureType")) or "(blank)"] += 1
            statuses[ddf.textify(rec.get("StandardStatus")) or "(blank)"] += 1
            prices[price_bucket(rec.get("ListPrice"))] += 1
            if ddf.positive_amount(rec.get("LeaseAmount")):
                lease_amount_set += 1
            if ddf.positive_amount(rec.get("TotalActualRent")):
                total_actual_rent_set += 1
            for field in extras:
                text = ddf.textify(rec.get(field))
                if text:
                    extras[field][text] += 1
        nxt = data.get("@odata.nextLink") or data.get("odata.nextLink")
        url = nxt
        if not url and len(rows) >= ddf.PAGE_SIZE:
            print("Property scan stopped: a full page had no next link.")
            break
        if not url:
            break
        if pages >= ddf.MAX_PAGES:
            print("Property scan stopped at the page cap.")
            break
    print(f"property_scan pulled={pulled} pages={pages} lease_amount_set={lease_amount_set} total_actual_rent_set={total_actual_rent_set}")
    print("property_subtypes: " + tally_line(subtypes))
    print("structure_types: " + tally_line(structures))
    print("statuses: " + tally_line(statuses))
    print("list_price_buckets: " + tally_line(prices))
    for field, counter in extras.items():
        print(f"field {field}: " + tally_line(counter))


def scan_rets(user, password):
    """Tally RETS TransactionType and PropertyType without storing listings."""
    jar = ddf.CookieJar()
    password_mgr = ddf.urllib.request.HTTPPasswordMgrWithDefaultRealm()
    for base in ("https://data.crea.ca/", "https://data.crea.ca/Login.svc/Login"):
        password_mgr.add_password(None, base, user, password)
        password_mgr.add_password("CREA.Distribution", base, user, password)
    opener = ddf.urllib.request.build_opener(
        ddf.urllib.request.HTTPDigestAuthHandler(password_mgr),
        ddf.urllib.request.HTTPCookieProcessor(jar),
    )
    session_id = {}

    def open_url(url):
        headers = {"User-Agent": ddf.UA, "RETS-Version": "RETS/1.7.2", "Accept": "*/*"}
        if session_id.get("id"):
            headers["Cookie"] = f"X-SESSIONID={session_id['id']}"
        req = ddf.urllib.request.Request(url, headers=headers)
        try:
            resp = opener.open(req, timeout=90)
        except ddf.urllib.error.HTTPError as exc:
            return exc.code, exc.read(), exc.headers
        body = resp.read()
        ddf.capture_session(resp.headers, session_id)
        return resp.status, body, resp.headers

    status, body, headers = open_url(ddf.RETS_LOGIN)
    ddf.capture_session(headers, session_id)
    if status != 200:
        print(f"RETS login status {status}")
        return
    text = body.decode("utf-8", "replace")
    code = ddf.rets_code(text)
    if code not in (None, "0"):
        print(f"RETS login ReplyCode {code}")
        return
    search = ddf.rets_url(text, "Search") or ddf.RETS_SEARCH
    logout = ddf.rets_url(text, "Logout") or ddf.RETS_LOGOUT
    columns = (
        "TransactionType", "PropertyType", "PropertySubType", "Lease",
        "LeasePerTime", "Price", "MlsStatus", "Status",
    )
    transactions = ddf.Counter()
    property_types = ddf.Counter()
    leases = 0
    pulled = 0
    offset = 1
    pages = 0
    fmt = "COMPACT-DECODED"
    try:
        while pages < ddf.MAX_PAGES:
            params = {
                "SearchType": "Property",
                "Class": "Property",
                "QueryType": "DMQL2",
                "Query": "(LastUpdated=2000-01-01T00:00:00Z)",
                "Format": fmt,
                "Select": ",".join(columns),
                "Limit": str(ddf.PAGE_SIZE),
                "Offset": str(offset),
                "Count": "1",
            }
            status, body, headers = open_url(search + "?" + ddf.urllib.parse.urlencode(params))
            ddf.capture_session(headers, session_id)
            page = body.decode("utf-8", "replace")
            code = ddf.rets_code(page)
            if code not in (None, "0", "20201"):
                print(f"RETS {fmt} ReplyCode {code}: {scrub(page)}")
                if fmt == "COMPACT-DECODED":
                    fmt = "STANDARD-XML"
                    print("Retrying RETS as STANDARD-XML and tallying TransactionType elements.")
                    continue
                break
            if fmt == "STANDARD-XML":
                rows = ddf.parse_property_details(page)
                if not rows and pages == 0:
                    print("RETS standard XML returned no PropertyDetails on the first page.")
                    break
                for rec in rows:
                    pulled += 1
                    transactions[ddf.first(rec, "TransactionType") or "(blank)"] += 1
                    property_types[ddf.first(rec, "PropertyType") or "(blank)"] += 1
                    if ddf.positive_amount(ddf.first(rec, "Lease", "LeaseAmount")):
                        leases += 1
                pages += 1
                if len(rows) < ddf.PAGE_SIZE:
                    break
                offset += len(rows)
                continue
            names, records = compact_rows(page)
            if pages == 0:
                print("RETS compact columns: " + ", ".join(names))
            if not records and code == "20201":
                break
            for rec in records:
                pulled += 1
                transactions[rec.get("TransactionType") or "(blank)"] += 1
                property_types[rec.get("PropertyType") or rec.get("PropertySubType") or "(blank)"] += 1
                if ddf.positive_amount(rec.get("Lease") or rec.get("LeaseAmount")):
                    leases += 1
            pages += 1
            if len(records) < ddf.PAGE_SIZE:
                break
            offset += len(records)
    finally:
        open_url(logout)
    print(f"rets_scan format={fmt} pulled={pulled} pages={pages} lease_set={leases}")
    print("rets_transaction: " + tally_line(transactions))
    print("rets_property_type: " + tally_line(property_types))


def compact_rows(page):
    names = []
    records = []
    for line in page.splitlines():
        if "COLUMNS" in line and "<" in line:
            inner = ddf.re.sub(r"</?COLUMNS>", "", line)
            names = [part.strip() for part in inner.split("\t") if part.strip()]
        elif "<DATA>" in line:
            inner = ddf.re.sub(r"</?DATA>", "", line)
            parts = inner.split("\t")
            # Compact rows are tab-wrapped, so the first cell is often empty.
            if parts and parts[0] == "":
                parts = parts[1:]
            if names:
                records.append({names[i]: parts[i].strip() for i in range(min(len(names), len(parts)))})
    return names, records


def main():
    user = os.environ.get("DDF_USERNAME", "").strip()
    password = os.environ.get("DDF_PASSWORD", "").strip()
    if not user or not password:
        print("DDF_USERNAME or DDF_PASSWORD is not set. Skipping rental probe.")
        return 0
    token, _destination = ddf.fetch_token(user, password)
    print("Signed in to the DDF Web API.")
    status, payload = ddf.odata_request(token, ddf.ODATA_ROOT + "/$metadata")
    if status != 200:
        print(f"metadata status {status}: {scrub(payload)}")
        return 1
    entity_sets, fields, enums = parse_metadata(payload)
    print("entity_sets: " + ", ".join(entity_sets))
    prop_fields = fields.get("Property") or []
    print(f"property_field_count {len(prop_fields)}")
    print("property_fields: " + ", ".join(name for name, _typ in prop_fields))
    lease_named = [name for name, _typ in prop_fields if any(word in name.lower() for word in ("lease", "rent", "transaction", "agreement"))]
    print("property_lease_named_fields: " + (", ".join(lease_named) or "(none)"))
    for enum_name in sorted(enums):
        if not interesting(enum_name):
            continue
        members = enums[enum_name]
        shown = ", ".join(members[:80])
        if len(members) > 80:
            shown += f", … ({len(members)} total)"
        print(f"enum {enum_name}: {shown or '(no members)'}")
    dest_status, _payload, dest = get_json(token, ddf.ODATA_ROOT + "/Destination?" + ddf.urllib.parse.urlencode({
        "$select": "DestinationName,DestinationUrl,DestinationType,DestinationStatus,FullNSP",
        "$top": "5",
    }))
    if dest:
        rows = dest.get("value") or []
        print(f"destination_rows {len(rows)}")
        for row in rows:
            bits = []
            for key in ("DestinationName", "DestinationUrl", "DestinationType", "DestinationStatus", "FullNSP"):
                if key in row:
                    bits.append(f"{key}={row.get(key)}")
            print("destination " + " ".join(bits))
    for path in ("/Property", "/Property/PropertyReplication()"):
        _count_status, _payload, counted = get_json(token, ddf.ODATA_ROOT + path + "?" + ddf.urllib.parse.urlencode({
            "$count": "true",
            "$top": "1",
            "$select": "ListingKey",
        }))
        if counted is not None:
            keys = sorted((counted.get("value") or [{}])[0].keys()) if counted.get("value") else []
            print(f"count {path} odata_count={counted.get('@odata.count')} sample_keys={','.join(keys)}")
    if os.environ.get("DDF_PROBE_SCAN", "1") != "0":
        scan_property(token)
    if os.environ.get("DDF_PROBE_RETS", "1") != "0":
        scan_rets(user, password)
    return 0 if dest_status in (200, None) else 0


if __name__ == "__main__":
    sys.exit(main())
