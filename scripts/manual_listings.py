#!/usr/bin/env python3
"""Listings the DDF refresh must not wipe.

Only Greater Vancouver and Fraser Valley listings may be added. An
out-of-board listing needs written permission from the listing brokerage
and their full photo set. See _build/MANUAL-LISTINGS.md.

Source file: data/manual-listings.json (override with MANUAL_LISTINGS_PATH).
The 12-hour workflow rewrites listings/data.json and listings/rentals.json
from Greater Vancouver and the Fraser Valley, then merges the active rows
from this file back in. The source file itself sits outside listings/, so
`git add -A listings` never edits it.

Remove a row by deleting it, setting "active" to false, or setting
"expires" to the last day it should appear (YYYY-MM-DD, Vancouver time).
The next refresh, or `python3 scripts/fetch_ddf_listings.py --merge-manual`,
drops it from the feed and deletes its generated page.

See _build/MANUAL-LISTINGS.md.
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
from datetime import datetime
from urllib.parse import quote
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_ddf_listings as ddf

MANIFEST = os.path.join("listings", "manual-pages.json")
DISCLAIMER = (
    "This information is believed to be accurate but is not guaranteed and should be verified."
)
CREA_DISCLAIMER = (
    "The listing information is deemed reliable but is not guaranteed. "
    "The information contained on this site is based in whole or in part on information "
    "that is provided by members of The Canadian Real Estate Association (CREA), who are "
    "responsible for its accuracy. REALTOR.ca Canada Inc. reproduces and distributes this "
    "information as a service for its members and neither CREA nor REALTOR.ca Canada Inc. "
    "assumes responsibility for its accuracy."
)
CARD_EXTRAS = (
    "photoCaption", "photoCredit", "photoCreditUrl",
    "photoLicense", "photoLicenseUrl", "photoChange",
    "page", "manual",
)


class ManualListingsError(Exception):
    pass


def source_path():
    override = os.environ.get("MANUAL_LISTINGS_PATH", "").strip()
    return override or os.path.join(ddf.ROOT, "data", "manual-listings.json")


def vancouver_today():
    return datetime.now(ZoneInfo("America/Vancouver")).date().isoformat()


def load_rows():
    """Rows from the manual file. Missing file means there are none."""
    path = source_path()
    if not os.path.isfile(path):
        return []
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as exc:
        raise ManualListingsError(f"{path} is not valid JSON: {exc}") from exc
    if isinstance(data, list):
        rows = data
    elif isinstance(data, dict):
        rows = data.get("listings") or []
    else:
        raise ManualListingsError(f"{path} must be a list or an object with a listings array")
    if not isinstance(rows, list):
        raise ManualListingsError(f"{path} listings must be an array")
    return rows


def row_intent(row):
    value = str((row or {}).get("intent") or (row or {}).get("mode") or "sale").strip().lower()
    if value in {"rent", "rental", "lease"}:
        return "rent"
    return "sale"


def is_active(row, today=None):
    """True when the row should be published today.

    expires is the last Vancouver date the row is included. The next day it drops.
    """
    if not isinstance(row, dict):
        return False
    active = row.get("active")
    if active is False:
        return False
    if isinstance(active, str) and active.strip().lower() in {"false", "no", "0", "off"}:
        return False
    expires = str(row.get("expires") or "").strip()
    if not expires:
        return True
    day = expires[:10]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
        raise ManualListingsError(f"expires must be YYYY-MM-DD, got {expires!r}")
    return day >= (today or vancouver_today())


def active_ids(rows=None, today=None):
    rows = load_rows() if rows is None else rows
    today = today or vancouver_today()
    ids = set()
    for row in rows:
        if is_active(row, today) and str(row.get("id") or "").strip():
            ids.add(str(row["id"]).strip())
    return ids


def page_relpath(listing_id, address, city, override=None):
    text = str(override or "").strip().lstrip("/")
    if text:
        return _safe_page(text)
    slug = ddf.address_slug(address, city) or "home"
    return _safe_page(f"listings/{listing_id}-{slug}.html")


def _safe_page(rel):
    rel = str(rel or "").replace("\\", "/").lstrip("/")
    parts = [part for part in rel.split("/") if part]
    if any(part == ".." for part in parts):
        raise ManualListingsError(f"page path cannot contain ..: {rel}")
    rel = "/".join(parts)
    if not rel.startswith("listings/") or not rel.endswith(".html"):
        raise ManualListingsError(f"page must be listings/<file>.html, got {rel}")
    if rel.startswith("listings/sale/") or rel.startswith("listings/rent/"):
        raise ManualListingsError(f"page must not sit in a shard folder: {rel}")
    return rel


def _photos(row):
    raw = row.get("photos")
    if not raw and isinstance(row.get("photo"), str):
        raw = [row["photo"]]
    photos = []
    for photo in raw or []:
        if isinstance(photo, str) and (photo.startswith("https://") or photo.startswith("/")):
            photos.append(photo)
    return photos[: ddf.MAX_PHOTOS]


def to_item(row):
    """Full feed record. Remarks and photos stay on the item for the shard."""
    if not isinstance(row, dict):
        raise ManualListingsError("each manual listing must be an object")
    listing_id = str(row.get("id") or "").strip()
    if not listing_id:
        raise ManualListingsError("a manual listing is missing id")
    address = str(row.get("address") or "").strip()
    city = str(row.get("city") or "").strip()
    mls = str(row.get("mls") or listing_id).strip()
    price = row.get("price")
    if isinstance(price, str):
        price = ddf.parse_number(price)
    if isinstance(price, float) and price.is_integer():
        price = int(price)
    item = {
        "id": listing_id,
        "mls": mls,
        "price": price,
        "address": address or None,
        "city": city,
        "area": str(row.get("area") or ""),
        "postal": str(row.get("postal") or ""),
        "beds": row.get("beds"),
        "baths": row.get("baths"),
        "type": str(row.get("type") or ""),
        "sqft": row.get("sqft"),
        "year": row.get("year"),
        "parking": row.get("parking") if row.get("parking") not in ("", None) else None,
        "remarks": str(row.get("remarks") or ""),
        "brokerage": str(row.get("brokerage") or ""),
        "agent": str(row.get("agent") or ""),
        "photos": _photos(row),
        "realtorUrl": ddf.realtor_link(row.get("realtorUrl") or "", listing_id, address, city, mls),
        "updated": str(row.get("updated") or ""),
        "manual": True,
        "page": page_relpath(listing_id, address, city, row.get("page")),
    }
    for key in CARD_EXTRAS:
        if key in {"page", "manual"}:
            continue
        value = row.get(key)
        if value not in (None, "", []):
            item[key] = value
    return item


def merge_into(listings, intent, rows=None, today=None):
    """Return listings plus active manual rows for this intent. Manual ids win."""
    rows = load_rows() if rows is None else rows
    today = today or vancouver_today()
    extras = []
    for row in rows:
        if row_intent(row) != intent or not is_active(row, today):
            continue
        extras.append(to_item(row))
    if not extras:
        return list(listings)
    return ddf.dedupe(list(listings) + extras)


def _write_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write("\n")
    os.replace(tmp, path)


def _shard_detail(item):
    detail = {}
    photos = item.get("photos") or []
    remarks = item.get("remarks") or ""
    if photos:
        detail["photos"] = photos
    if remarks:
        detail["remarks"] = remarks
    return detail


def _update_shard(feed_path, listing_id, detail):
    directory = ddf.shard_directory(feed_path)
    os.makedirs(directory, exist_ok=True)
    dest = os.path.join(directory, f"{ddf.shard_index(listing_id)}.json")
    payload = {}
    if os.path.isfile(dest):
        with open(dest, encoding="utf-8") as fh:
            loaded = json.load(fh)
        if isinstance(loaded, dict):
            payload = loaded
    key = str(listing_id)
    if detail:
        if payload.get(key) == detail:
            return False
        payload[key] = detail
        _write_json(dest, payload)
        return True
    if key not in payload:
        return False
    del payload[key]
    if payload:
        _write_json(dest, payload)
    else:
        os.remove(dest)
    return True


def patch_feed_file(path, intent, rows=None, today=None):
    """Insert, replace, or remove manual cards in an existing feed file.

    Does not rewrite the other listings. Returns how many manual rows are active.
    """
    if not os.path.isfile(path):
        raise ManualListingsError(f"Missing feed file: {path}")
    rows = load_rows() if rows is None else rows
    today = today or vancouver_today()
    relevant = [row for row in rows if isinstance(row, dict) and row_intent(row) == intent and str(row.get("id") or "").strip()]
    ids = {str(row["id"]).strip() for row in relevant}
    active = [to_item(row) for row in relevant if is_active(row, today)]
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict) or not isinstance(data.get("listings"), list):
        raise ManualListingsError(f"{path} has no listings array")
    kept = []
    orphaned = []
    for row in data["listings"]:
        row_id = str(row.get("id") or "")
        if row_id in ids:
            continue
        # A manual card whose id was deleted from the source file must leave the feed.
        if row.get("manual") is True:
            orphaned.append(row_id)
            continue
        kept.append(row)
    cards = [ddf.card_record(item) for item in active]
    new_listings = kept + cards
    changed = new_listings != data["listings"]
    if changed:
        data["listings"] = new_listings
        data["count"] = len(new_listings)
        _write_json(path, data)
    for listing_id in orphaned:
        _update_shard(path, listing_id, None)
    for row in relevant:
        listing_id = str(row["id"]).strip()
        item = next((entry for entry in active if entry["id"] == listing_id), None)
        _update_shard(path, listing_id, _shard_detail(item) if item else None)
    return len(active)


def apply_published():
    """Merge the manual file into the published feeds and rewrite its pages."""
    rows = load_rows()
    sale_path, rent_path = ddf.output_paths()
    sale_count = patch_feed_file(sale_path, "sale", rows)
    rent_count = patch_feed_file(rent_path, "rent", rows)
    pages = write_pages(rows)
    print(
        f"Manual listings: {sale_count} for sale, {rent_count} for rent, "
        f"{len(pages)} page(s). Source: {os.path.relpath(source_path(), ddf.ROOT)}."
    )
    return sale_count, rent_count, pages


def _esc(value):
    return html.escape("" if value is None else str(value), quote=True)


def _money(value):
    if value is None or value == "":
        return "Price on request"
    number = value if isinstance(value, (int, float)) else ddf.parse_number(value)
    if number is None:
        return _esc(value)
    if isinstance(number, float) and number.is_integer():
        number = int(number)
    if isinstance(number, int):
        return f"${number:,}"
    return f"${number:,.2f}"


def _root_prefix(rel):
    return "../" * rel.count("/")


def _photo_src(photo, root):
    if photo.startswith("/"):
        return root + photo.lstrip("/")
    return photo


def _fact_rows(row, item):
    rows = [
        ("City", item.get("city")),
        ("Province", row.get("province")),
        ("Postal code", item.get("postal")),
        ("Property type", item.get("type")),
        ("Bedrooms", item.get("beds")),
        ("Bathrooms", item.get("baths")),
        ("Interior", f"{int(item['sqft']):,} sq ft" if isinstance(item.get("sqft"), (int, float)) else None),
        ("Year built", item.get("year")),
        ("Parking", item.get("parking")),
        ("MLS® number", item.get("mls")),
    ]
    for pair in row.get("facts") or []:
        if isinstance(pair, (list, tuple)) and len(pair) >= 2:
            rows.append((pair[0], pair[1]))
    return [(label, value) for label, value in rows if value not in (None, "")]


def _load_partials():
    build = os.path.join(ddf.ROOT, "_build")
    if build not in sys.path:
        sys.path.insert(0, build)
    import partials
    return partials


def render_page(row, item):
    partials = _load_partials()
    rel = item["page"]
    root = _root_prefix(rel)
    address = item.get("address") or "Home"
    city = item.get("city") or ""
    place = address + (", " + city if city else "")
    province = str(row.get("province") or "").strip()
    titled = place + (", " + province if province else "")
    brokerage = item.get("brokerage") or ""
    courtesy = str(row.get("courtesy") or "").strip()
    if not courtesy and brokerage:
        courtesy = f"Listing courtesy of {brokerage}."
    price = _money(item.get("price"))
    title = f"{titled} | Devin Desaulniers, Axford Real Estate"
    desc = (
        f"{titled}. {price}. "
        + (courtesy + " " if courtesy else "")
        + "Devin Desaulniers is a Real Estate Associate at Axford Real Estate."
    )
    if len(desc) > 300:
        desc = desc[:297].rstrip() + "..."
    photo = (item.get("photos") or [None])[0]
    og = "assets/img/og-default.png"
    if isinstance(photo, str) and photo.startswith("/assets/"):
        og = photo.lstrip("/")
    elif isinstance(row.get("photoFile"), str) and row["photoFile"].startswith("assets/"):
        og = row["photoFile"]
    bits = []
    if item.get("beds") not in (None, ""):
        bits.append(f"{item['beds']} bed")
    if item.get("baths") not in (None, ""):
        bits.append(f"{item['baths']} bath")
    if item.get("sqft"):
        bits.append(f"{int(item['sqft']):,} sq ft" if isinstance(item["sqft"], (int, float)) else str(item["sqft"]))
    lead = " · ".join([price] + bits)
    facts = "".join(
        f"<div><span>{_esc(label)}</span><strong>{_esc(value)}</strong></div>"
        for label, value in _fact_rows(row, item)
    )
    photo_html = ""
    if photo:
        width = row.get("photoWidth") or ""
        height = row.get("photoHeight") or ""
        size = ""
        if width and height:
            size = f' width="{_esc(width)}" height="{_esc(height)}"'
        caption = str(row.get("photoCaption") or item.get("photoCaption") or "")
        credit = str(row.get("photoCredit") or "")
        credit_url = str(row.get("photoCreditUrl") or "")
        license_name = str(row.get("photoLicense") or "")
        license_url = str(row.get("photoLicenseUrl") or "")
        change = str(row.get("photoChange") or "")
        credit_html = ""
        if credit and credit_url.startswith("https://"):
            credit_html += f'<a href="{_esc(credit_url)}">{_esc(credit)}</a>'
        elif credit:
            credit_html += _esc(credit)
        if license_name and license_url.startswith("https://"):
            credit_html += f' (<a href="{_esc(license_url)}">{_esc(license_name)}</a>)'
        elif license_name:
            credit_html += f" ({_esc(license_name)})"
        if change:
            credit_html += f"{'. ' if credit_html else ''}{_esc(change)}"
        note = _esc(caption)
        if credit_html:
            note = (note + " " if note else "") + credit_html
        photo_html = (
            f'<figure class="ls-area-photo">'
            f'<img src="{_esc(_photo_src(photo, root))}" alt="{_esc(caption or place)}"{size}>'
            f'<figcaption class="ls-photo-note">{note}</figcaption>'
            f"</figure>"
        )
    realtor = item.get("realtorUrl") or ""
    realtor_html = ""
    if realtor.startswith("https://"):
        realtor_html = (
            f'<p class="ls-source" id="ls-realtor-link"><span class="ls-source-links">'
            f'<a class="ls-source-link" href="{_esc(realtor)}" target="_blank" rel="noopener">Listing data via REALTOR.ca</a>'
            f"</span>"
            f'<a class="powered-by" href="{_esc(realtor)}" target="_blank" rel="noopener">'
            f'<img src="https://www.realtor.ca/images/en-ca/powered_by_realtor.svg" alt="Powered by REALTOR.ca" width="88" height="28" onerror="this.remove()">'
            f"</a></p>"
        )
    renting = row_intent(row) == "rent"
    ask_label = "Ask Devin about this rental" if renting else "Ask Devin about this home"
    contact_href = f"{root}contact.html?intent={'renting' if renting else 'buying'}&listing={quote(place, safe='')}"
    mls = str(item.get("mls") or "").strip()
    if mls:
        contact_href += "&mls=" + quote(mls, safe="")
    contact_href += "#qualify"
    remarks = str(row.get("remarks") or item.get("remarks") or "").strip()
    remarks_html = ""
    if remarks:
        remarks_html = f'<div class="ls-remarks"><h2>Description</h2><p>{_esc(remarks)}</p></div>'
    search_href = f"{root}listings.html#{_esc(item['id'])}" if row_intent(row) == "sale" else f"{root}rentals.html#{_esc(item['id'])}"
    phone = partials.PHONE
    tel = partials.TEL
    brokerage_name = partials.BROKERAGE
    page = partials.head(
        _esc(title),
        _esc(desc),
        "listings" if row_intent(row) == "sale" else "rentals",
        og_image=og,
        page_url=rel,
        root=root,
        show_tenant_bar=True,
    )
    page += f"""
<section class="page-hero page-hero--search page-hero--listing">
  <div class="container">
    <span class="eyebrow">{_esc(brokerage_name)}</span>
    <h1>{_esc(titled)}</h1>
    <p class="lead">{_esc(lead)}</p>
  </div>
</section>
<section class="section section--listings">
  <div class="container">
    <p class="ls-operator"><img src="{root}assets/img/axford-logo.png" alt="" width="108" height="23"><span><strong>Devin Desaulniers</strong>, Real Estate Associate, {_esc(brokerage_name)}. <a href="{tel}">{_esc(phone)}</a></span></p>
    <p class="ls-back"><a href="{search_href}">This home in the search</a></p>
    <div class="ls-detail-grid">
      <div class="ls-gallery">{photo_html}</div>
      <div class="ls-lead">
        <p class="ls-price">{_esc(price)}</p>
        <h2 class="ls-address">{_esc(place)}</h2>
        <p class="ls-meta">{_esc(" · ".join(bits))}</p>
        <div class="ls-cta"><div class="ls-cta-row">
          <a class="btn btn-primary" href="{_esc(contact_href)}">{_esc(ask_label)}</a>
          <a class="btn btn-outline" href="{tel}">Book a showing · {_esc(phone)}</a>
        </div></div>
      </div>
      <div class="ls-summary">
        <p class="ls-broker">{_esc(courtesy)}</p>
        <div class="ls-facts">{facts}</div>
        {realtor_html}
      </div>
    </div>
    {remarks_html}
    <div class="ls-inquiry" id="ls-inquiry">
      <h2>{_esc(ask_label)}</h2>
      <p class="lead">Contact Devin Desaulniers at {_esc(brokerage_name)} to book a showing or ask a question. Call or text <a href="{tel}">{_esc(phone)}</a>, or use the contact form. The form is filled in with this address and MLS® number. This message comes to Devin. It is not sent to the listing brokerage.</p>
      <div class="ls-cta-row">
        <a class="btn btn-primary" href="{_esc(contact_href)}">{_esc(ask_label)}</a>
        <a class="btn btn-outline" href="{tel}">Book a showing · {_esc(phone)}</a>
      </div>
    </div>
  </div>
</section>
<section class="section section--paper ls-legal">
  <div class="container narrow-wide">
    <h2>Listing data</h2>
    <p><strong>{_esc(brokerage_name)}</strong> operates this website. Devin Desaulniers is a Real Estate Associate with {_esc(brokerage_name)}, {_esc(partials.BROKERAGE_ADDR)}, and a member of The Canadian Real Estate Association.</p>
    <p>{_esc(DISCLAIMER)}</p>
    <p>Trademarks are owned or controlled by The Canadian Real Estate Association (CREA) and identify real estate professionals who are members of CREA (REALTOR®) and/or the quality of services they provide (MLS®).</p>
    <p>{_esc(CREA_DISCLAIMER)}</p>
    <p>The listing content on this website is protected by copyright and other laws, and is intended solely for the private, non-commercial use by individuals.</p>
  </div>
</section>
"""
    page += partials.foot(root)
    return str(page)


def _read_manifest(root):
    path = os.path.join(root, MANIFEST)
    if not os.path.isfile(path):
        return []
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return []
    pages = data.get("pages") if isinstance(data, dict) else None
    if not isinstance(pages, list):
        return []
    return [str(page) for page in pages]


def write_pages(rows=None, root=None):
    """Write one HTML file per active manual listing and delete retired ones."""
    rows = load_rows() if rows is None else rows
    root = root or ddf.ROOT
    today = vancouver_today()
    desired = {}
    for row in rows:
        if not is_active(row, today):
            continue
        if not str(row.get("id") or "").strip():
            continue
        item = to_item(row)
        desired[item["page"]] = render_page(row, item)
    previous = _read_manifest(root)
    removed = []
    for rel in previous:
        if rel in desired:
            continue
        try:
            safe = _safe_page(rel)
        except ManualListingsError:
            continue
        dest = os.path.join(root, safe)
        if os.path.isfile(dest):
            os.remove(dest)
            removed.append(safe)
    written = []
    for rel, html_text in desired.items():
        dest = os.path.join(root, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        current = ""
        if os.path.isfile(dest):
            with open(dest, encoding="utf-8") as fh:
                current = fh.read()
        if current != html_text:
            tmp = dest + ".tmp"
            with open(tmp, "w", encoding="utf-8") as fh:
                fh.write(html_text)
            os.replace(tmp, dest)
        written.append(rel)
    manifest = {"pages": written}
    manifest_path = os.path.join(root, MANIFEST)
    os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
    current_manifest = _read_manifest(root)
    if current_manifest != written or not os.path.isfile(manifest_path):
        _write_json(manifest_path, manifest)
    return written
