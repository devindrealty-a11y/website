"""Weekly Greater Vancouver asking-rent report.

Reads listings/rentals.json, writes rent-report.html, a newsletter HTML file
and a plain-text twin, and a Monday snapshot under rent-report/history/.
The next run compares medians and listing ids with the previous snapshot.
"""
import argparse
import html
import json
import os
import re
import sys
from datetime import datetime, time, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
from urllib.parse import quote
from zoneinfo import ZoneInfo

from partials import (
    BROKERAGE,
    BROKERAGE_ADDR,
    CTA_TEXT,
    EMAIL,
    PHONE,
    SITE,
    TEL,
    foot,
    head,
    tenant_cta_attrs,
    tenant_cta_href,
)

TZ = ZoneInfo("America/Vancouver")
PAGE = "rent-report.html"
HISTORY_DIR = os.path.join("rent-report", "history")
MIN_PRICE = 800
MAX_PRICE = 40000
MIN_SQFT_HARD = 200
MIN_SQFT_VALUE = 400
MIN_PPSF = 1.25
MAX_PPSF = 10.0
MIN_DISCOUNT = 0.12
RELAXED_DISCOUNT = 0.08
PEER_CITY_MIN = 5
PEER_BAND_MIN = 8
WOW_MIN = 5
MOVER_MIN = 8
EXTRA_CITY_MIN = 5
BEST_LIMIT = 8
NEW_SHOW = 8
NAMED_CITIES = [
    "Coquitlam",
    "Port Moody",
    "Port Coquitlam",
    "Burnaby",
    "Vancouver",
    "Surrey",
    "Langley",
    "Richmond",
    "New Westminster",
    "Maple Ridge",
]
BED_ORDER = ["0", "1", "2", "3", "4", "5+"]
BED_LABELS = {
    "0": "Studio",
    "1": "1 bedroom",
    "2": "2 bedrooms",
    "3": "3 bedrooms",
    "4": "4 bedrooms",
    "5+": "5+ bedrooms",
}
DROP_CITIES = {"bc", "n/a", "na", "none", "null", "unknown"}
CITY_ALIASES = {
    "coquitlam": "Coquitlam",
    "port moody": "Port Moody",
    "port coquitlam": "Port Coquitlam",
    "poco": "Port Coquitlam",
    "burnaby": "Burnaby",
    "vancouver": "Vancouver",
    "surrey": "Surrey",
    "langley": "Langley",
    "langley city": "Langley",
    "city of langley": "Langley",
    "township of langley": "Langley",
    "langley township": "Langley",
    "richmond": "Richmond",
    "new westminster": "New Westminster",
    "new west": "New Westminster",
    "maple ridge": "Maple Ridge",
    "north vancouver": "North Vancouver",
    "north van": "North Vancouver",
    "west vancouver": "West Vancouver",
    "west van": "West Vancouver",
    "delta": "Delta",
    "white rock": "White Rock",
    "pitt meadows": "Pitt Meadows",
    "tsawwassen": "Tsawwassen",
    "anmore": "Anmore",
    "abbotsford": "Abbotsford",
    "mission": "Mission",
    "squamish": "Squamish",
    "bowen island": "Bowen Island",
    "lions bay": "Lions Bay",
    "gibsons": "Gibsons",
    "langdale": "Langdale",
}
BADGE = "https://www.realtor.ca/images/en-ca/powered_by_realtor.svg"
EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)
e = lambda value: html.escape(str(value), quote=True)


class ReportError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_dt(value):
    if not value:
        return None
    text = str(value).strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def parse_now(value):
    if not value:
        return datetime.now(TZ)
    parsed = parse_dt(value)
    if parsed is None:
        raise ReportError("could not read --now " + str(value), 1)
    return parsed.astimezone(TZ)


def week_bounds(now):
    local = now.astimezone(TZ)
    monday = local.date() - timedelta(days=local.weekday())
    sunday = monday + timedelta(days=6)
    start = datetime.combine(monday, time.min, tzinfo=TZ)
    return monday, sunday, start


def as_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if isinstance(value, float) and (value != value or value in (float("inf"), float("-inf"))):
        return None
    return float(value)


def as_int(value):
    number = as_number(value)
    if number is None or not number.is_integer():
        return None
    return int(number)


def nearest_dollar(value):
    if value is None:
        return None
    return int(Decimal(str(value)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def median_dollars(prices):
    if not prices:
        return None
    vals = sorted(Decimal(str(p)) for p in prices)
    n = len(vals)
    mid = n // 2
    raw = vals[mid] if n % 2 else (vals[mid - 1] + vals[mid]) / 2
    return int(raw.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def average_dollars(prices):
    if not prices:
        return None
    total = sum(Decimal(str(p)) for p in prices)
    return int((total / len(prices)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def summarize(prices):
    return {
        "count": len(prices),
        "median": median_dollars(prices),
        "average": average_dollars(prices),
    }


def wow_parts(current, previous):
    if current is None or previous is None or previous == 0:
        return None
    dollars = int(current) - int(previous)
    pct = round(dollars / float(previous) * 100, 1)
    return {"dollars": dollars, "pct": pct}


def clean_city(name):
    if name is None:
        return None
    raw = " ".join(str(name).split())
    if not raw:
        return None
    key = raw.lower()
    if key in DROP_CITIES:
        return None
    return CITY_ALIASES.get(key, raw)


def bed_band(beds):
    if beds <= 0:
        return "0"
    if beds >= 5:
        return "5+"
    return str(beds)


def https_url(value):
    if isinstance(value, str) and value.startswith("https://"):
        return value
    return ""


def as_comparable(raw, listing_id):
    price = as_number(raw.get("price"))
    if price is None or price < MIN_PRICE or price > MAX_PRICE:
        return None
    city = clean_city(raw.get("city"))
    if not city:
        return None
    beds = as_int(raw.get("beds"))
    if beds is None or beds < 0 or beds > 30:
        return None
    address = " ".join(str(raw.get("address") or "").split())
    if "garage" in address.lower():
        return None
    sqft = as_int(raw.get("sqft"))
    if sqft is not None and sqft <= 0:
        sqft = None
    if sqft is not None and sqft < MIN_SQFT_HARD:
        return None
    updated = parse_dt(raw.get("updated"))
    return {
        "id": listing_id,
        "mls": str(raw.get("mls") or "").strip(),
        "price": int(price) if float(price).is_integer() else float(price),
        "city": city,
        "address": address or "Address not published",
        "beds": beds,
        "band": bed_band(beds),
        "baths": as_number(raw.get("baths")),
        "type": str(raw.get("type") or "").strip(),
        "sqft": sqft,
        "brokerage": str(raw.get("brokerage") or "").strip(),
        "realtor_url": https_url(raw.get("realtorUrl")),
        "photo": https_url(raw.get("photo")),
        "updated": updated,
    }


def prepare_listings(raw_listings):
    by_id = {}
    seen = set()
    skipped = 0
    for raw in raw_listings:
        if not isinstance(raw, dict):
            skipped += 1
            continue
        listing_id = str(raw.get("id") or "").strip()
        if not listing_id:
            skipped += 1
            continue
        item = as_comparable(raw, listing_id)
        seen.add(listing_id)
        if item is None or listing_id in by_id:
            skipped += 1
            continue
        by_id[listing_id] = item
    comparable = list(by_id.values())
    return {
        "ids": sorted(seen),
        "comparable": comparable,
        "feed_count": len(raw_listings),
        "excluded": skipped,
    }


def format_long(day):
    return f"{day.strftime('%B')} {day.day}, {day.year}"


def _as_date(value):
    if isinstance(value, datetime):
        return value.date()
    if hasattr(value, "year") and hasattr(value, "month") and hasattr(value, "day"):
        return value
    return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()


def format_span(start_iso, end_iso):
    start = _as_date(start_iso)
    end = _as_date(end_iso)
    if start.year == end.year and start.month == end.month:
        return f"{start.strftime('%B')} {start.day}–{end.day}, {start.year}"
    if start.year == end.year:
        return f"{start.strftime('%B')} {start.day} – {end.strftime('%B')} {end.day}, {start.year}"
    return f"{format_long(start)} – {format_long(end)}"


def short_week(iso):
    day = datetime.strptime(iso, "%Y-%m-%d").date()
    return f"{day.strftime('%b')} {day.day}"


def format_rent(value):
    if value is None:
        return "—"
    amount = int(value) if isinstance(value, int) or (isinstance(value, float) and value.is_integer()) else nearest_dollar(value)
    if amount < 0:
        return "-$" + f"{abs(amount):,}"
    return "$" + f"{amount:,}"


def format_wow(wow):
    if not wow:
        return "—"
    dollars = wow["dollars"]
    if dollars == 0:
        return "No change"
    word = "Up" if dollars > 0 else "Down"
    pct = f"{abs(wow['pct']):.1f}".rstrip("0").rstrip(".")
    return f"{word} {format_rent(abs(dollars))} ({pct}%)"


def format_beds(beds):
    if beds == 0:
        return "Studio"
    if beds == 1:
        return "1 bedroom"
    return f"{beds} bedrooms"


def format_baths(value):
    if value is None:
        return ""
    if float(value).is_integer():
        n = int(value)
        return "1 bath" if n == 1 else f"{n} baths"
    text = f"{value:g}"
    return text + " baths"


def format_ppsf(value):
    return f"${value:,.2f}/sq ft"


def group_prices(comparable):
    by_city = {}
    by_band = {}
    for item in comparable:
        by_city.setdefault(item["city"], []).append(item["price"])
        by_band.setdefault(item["band"], []).append(item["price"])
    return by_city, by_band


def stats_map(groups):
    return {key: summarize(prices) for key, prices in groups.items()}


def city_rows(by_city, previous):
    prev = previous or {}
    extras = sorted(city for city, prices in by_city.items() if city not in NAMED_CITIES and len(prices) >= EXTRA_CITY_MIN)
    thin = sorted(
        ({"city": city, "count": len(prices)} for city, prices in by_city.items() if city not in NAMED_CITIES and len(prices) < EXTRA_CITY_MIN),
        key=lambda row: row["city"],
    )
    rows = []
    for city in NAMED_CITIES + extras:
        stats = summarize(by_city.get(city) or [])
        wow = None
        before = prev.get(city) or {}
        if stats["count"] >= WOW_MIN and before.get("count", 0) >= WOW_MIN:
            wow = wow_parts(stats["median"], before.get("median"))
        rows.append({
            "city": city,
            "count": stats["count"],
            "median": stats["median"],
            "average": stats["average"],
            "wow": wow,
        })
    return rows, thin


def bed_rows(by_band, previous):
    prev = previous or {}
    rows = []
    for band in BED_ORDER:
        stats = summarize(by_band.get(band) or [])
        before = prev.get(band) or {}
        wow = None
        if stats["count"] >= WOW_MIN and before.get("count", 0) >= WOW_MIN:
            wow = wow_parts(stats["median"], before.get("median"))
        rows.append({
            "band": band,
            "label": BED_LABELS[band],
            "count": stats["count"],
            "median": stats["median"],
            "average": stats["average"],
            "wow": wow,
        })
    return rows


def movers(rows):
    eligible = [row for row in rows if row["wow"] and row["count"] >= MOVER_MIN and row["wow"]["dollars"] != 0]
    ups = sorted((row for row in eligible if row["wow"]["dollars"] > 0), key=lambda row: (-row["wow"]["pct"], row["city"]))[:3]
    downs = sorted((row for row in eligible if row["wow"]["dollars"] < 0), key=lambda row: (row["wow"]["pct"], row["city"]))[:3]
    return ups, downs


def _peer_maps(eligible):
    city_groups = {}
    band_groups = {}
    for item in eligible:
        ratio = item["price"] / item["sqft"]
        city_groups.setdefault((item["city"], item["band"]), []).append(ratio)
        band_groups.setdefault(item["band"], []).append(ratio)
    city_med = {}
    band_med = {}
    for key, ratios in city_groups.items():
        if len(ratios) >= PEER_CITY_MIN:
            city_med[key] = _median_raw(ratios)
    for key, ratios in band_groups.items():
        if len(ratios) >= PEER_BAND_MIN:
            band_med[key] = _median_raw(ratios)
    return city_groups, band_groups, city_med, band_med


def _median_raw(values):
    vals = sorted(values)
    n = len(vals)
    mid = n // 2
    if n % 2:
        return float(vals[mid])
    return float(vals[mid - 1] + vals[mid]) / 2


def _eligible_value(comparable):
    eligible = []
    for item in comparable:
        sqft = item.get("sqft")
        if not sqft or sqft < MIN_SQFT_VALUE:
            continue
        ratio = item["price"] / sqft
        if ratio < MIN_PPSF or ratio > MAX_PPSF:
            continue
        eligible.append(item)
    return eligible


def _score_value(eligible, min_discount):
    city_groups, band_groups, city_med, band_med = _peer_maps(eligible)
    scored = []
    for item in eligible:
        band = item["band"]
        key = (item["city"], band)
        if key in city_med:
            peer = city_med[key]
            peer_n = len(city_groups[key])
            peer_label = item["city"] + " " + BED_LABELS[band].lower()
        elif band in band_med:
            peer = band_med[band]
            peer_n = len(band_groups[band])
            peer_label = "Greater Vancouver " + BED_LABELS[band].lower()
        else:
            continue
        if peer <= 0:
            continue
        ratio = item["price"] / item["sqft"]
        discount = (peer - ratio) / peer
        if discount < min_discount:
            continue
        card = dict(item)
        card["updated"] = item["updated"].isoformat() if item["updated"] else ""
        card["ppsf"] = ratio
        card["discount"] = discount
        card["peer_ppsf"] = peer
        card["peer_n"] = peer_n
        card["peer_label"] = peer_label
        scored.append(card)
    scored.sort(key=lambda row: (-row["discount"], row["price"], row["id"]))
    return scored


def _take_cities(scored, limit, per_city):
    picked = []
    counts = {}
    for row in scored:
        if counts.get(row["city"], 0) >= per_city:
            continue
        picked.append(row)
        counts[row["city"]] = counts.get(row["city"], 0) + 1
        if len(picked) >= limit:
            break
    return picked


def best_value(comparable, limit=BEST_LIMIT):
    eligible = _eligible_value(comparable)
    picked = _take_cities(_score_value(eligible, MIN_DISCOUNT), limit, 2)
    if len(picked) < 5:
        picked = _take_cities(_score_value(eligible, RELAXED_DISCOUNT), limit, 3)
    return picked


def select_new(prepared, prev_ids, week_start):
    comparable = prepared["comparable"]
    if prev_ids is not None:
        fresh_ids = [listing_id for listing_id in prepared["ids"] if listing_id not in prev_ids]
        by_id = {item["id"]: item for item in comparable}
        rows = [by_id[listing_id] for listing_id in fresh_ids if listing_id in by_id]
        method = "snapshot"
        count = len(fresh_ids)
    else:
        rows = [item for item in comparable if item["updated"] and item["updated"] >= week_start]
        method = "updated"
        count = len(rows)
    rows.sort(key=lambda item: (item["updated"] or EPOCH, item["id"]), reverse=True)
    cards = []
    for item in rows[:NEW_SHOW]:
        card = dict(item)
        card["updated"] = item["updated"].isoformat() if item["updated"] else ""
        cards.append(card)
    return {
        "new_method": method,
        "new_count": count,
        "new_comparable": len(rows),
        "new_listings": cards,
    }


def public_stats(stats):
    return {"count": stats["count"], "median": stats["median"], "average": stats["average"]}


def build_record(prepared, by_city, by_band, monday, sunday, now, feed_updated):
    overall = summarize([item["price"] for item in prepared["comparable"]])
    return {
        "week": monday.isoformat(),
        "week_end": sunday.isoformat(),
        "prepared": now.astimezone(TZ).date().isoformat(),
        "generated_at": now.astimezone(TZ).isoformat(timespec="seconds"),
        "feed_updated": feed_updated,
        "feed_count": prepared["feed_count"],
        "counted": len(prepared["comparable"]),
        "excluded": prepared["excluded"],
        "overall": public_stats(overall),
        "by_city": {city: public_stats(summarize(prices)) for city, prices in sorted(by_city.items())},
        "by_beds": {band: public_stats(summarize(by_band.get(band) or [])) for band in BED_ORDER},
        "ids": prepared["ids"],
    }


def series_point(record):
    point = dict(record)
    point.pop("ids", None)
    point.pop("generated_at", None)
    point["median"] = record["overall"]["median"]
    point["average"] = record["overall"]["average"]
    point["count"] = record["overall"]["count"]
    return point


def assemble(prepared, previous, prev_ids, now, feed_updated):
    monday, sunday, week_start = week_bounds(now)
    by_city, by_band = group_prices(prepared["comparable"])
    record = build_record(prepared, by_city, by_band, monday, sunday, now, feed_updated)
    prev_cities = (previous or {}).get("by_city") or {}
    prev_beds = (previous or {}).get("by_beds") or {}
    cities, thin = city_rows(by_city, prev_cities)
    beds = bed_rows(by_band, prev_beds)
    ups, downs = movers(cities)
    fresh = select_new(prepared, prev_ids, week_start)
    prev_overall = (previous or {}).get("overall") or {}
    overall = record["overall"]
    count_delta = None
    if previous and prev_overall.get("count") is not None:
        count_delta = overall["count"] - int(prev_overall["count"])
    report = {
        "week": record["week"],
        "week_end": record["week_end"],
        "prepared": record["prepared"],
        "feed_updated": feed_updated,
        "feed_count": record["feed_count"],
        "counted": record["counted"],
        "excluded": record["excluded"],
        "previous_week": previous.get("week") if previous else None,
        "overall": overall,
        "overall_wow": wow_parts(overall["median"], prev_overall.get("median")) if previous else None,
        "average_wow": wow_parts(overall["average"], prev_overall.get("average")) if previous else None,
        "count_delta": count_delta,
        "cities": cities,
        "thin_cities": thin,
        "beds": beds,
        "movers_up": ups,
        "movers_down": downs,
        "best": best_value(prepared["comparable"]),
        "record": record,
    }
    report.update(fresh)
    return report


def load_json(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def write_text(path, text):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as handle:
            if handle.read() == text:
                return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    return True


def dumps(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def signature(record):
    body = dict(record)
    body.pop("generated_at", None)
    return json.dumps(body, sort_keys=True, ensure_ascii=False)


def load_series(path):
    if not os.path.exists(path):
        return []
    data = load_json(path)
    weeks = data.get("weeks") if isinstance(data, dict) else None
    if not isinstance(weeks, list):
        raise ReportError("rent-report history series is not a list of weeks", 1)
    return weeks


def load_week_file(path):
    if not os.path.exists(path):
        return None
    data = load_json(path)
    if not isinstance(data, dict):
        return None
    return data


def previous_point(weeks, week):
    older = [point for point in weeks if isinstance(point, dict) and str(point.get("week") or "") < week]
    return older[-1] if older else None


def upsert_series(weeks, point):
    kept = [item for item in weeks if item.get("week") != point["week"]]
    kept.append(point)
    kept.sort(key=lambda item: item.get("week") or "")
    return kept


def published_lastmod(root):
    path = os.path.join(root, HISTORY_DIR, "series.json")
    if not os.path.exists(path):
        return None
    try:
        weeks = load_series(path)
    except (OSError, json.JSONDecodeError, ReportError):
        return None
    if not weeks:
        return None
    prepared = weeks[-1].get("prepared")
    if isinstance(prepared, str) and len(prepared) >= 10:
        return prepared[:10]
    return None


def patch_sitemap(root, lastmod):
    path = os.path.join(root, "sitemap.xml")
    if not os.path.exists(path) or not lastmod:
        return False
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    loc = SITE + PAGE
    line = f"  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod></url>"
    pattern = re.compile(
        r"  <url><loc>" + re.escape(loc) + r"</loc>(?:<lastmod>[^<]*</lastmod>)?</url>\n?"
    )
    if pattern.search(text):
        updated = pattern.sub(line + "\n", text, count=1)
    else:
        needle = "  <url><loc>" + SITE + "rentals.html</loc></url>\n"
        if needle in text:
            updated = text.replace(needle, needle + line + "\n", 1)
        elif "</urlset>" in text:
            updated = text.replace("</urlset>", line + "\n</urlset>", 1)
        else:
            return False
    return write_text(path, updated)


def rental_href(listing_id, absolute=False):
    href = "rentals.html?id=" + quote(str(listing_id), safe="")
    return (SITE + href) if absolute else href


def format_updated(value):
    parsed = parse_dt(value) if isinstance(value, str) else value
    if not parsed:
        return ""
    return format_long(parsed.astimezone(TZ).date())


def meta_line(card):
    parts = [format_beds(card["beds"])]
    baths = format_baths(card.get("baths"))
    if baths:
        parts.append(baths)
    if card.get("type"):
        parts.append(card["type"])
    if card.get("sqft"):
        parts.append(f"{card['sqft']:,} sq ft")
    return " · ".join(parts)


def card_html(card, value=False):
    href = rental_href(card["id"])
    title = card["address"]
    if card.get("photo"):
        media = (
            f'<a class="rr-card-media" href="{e(href)}">'
            f'<img src="{e(card["photo"])}" alt="{e("Photo of " + card["address"] + ", " + card["city"])}" loading="lazy" decoding="async">'
            f"</a>"
        )
    else:
        media = f'<a class="rr-card-media" href="{e(href)}"><span class="rr-card-ph">{e(card["city"])}</span></a>'
    extra = ""
    if value:
        pct = int(Decimal(str(card["discount"] * 100)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        extra = (
            f'<p class="rr-value">{pct}% under the median {e(format_ppsf(card["peer_ppsf"]))} '
            f'for {e(card["peer_label"])} homes ({card["peer_n"]} on the feed). '
            f'This one is {e(format_ppsf(card["ppsf"]))}.</p>'
        )
    elif card.get("updated"):
        extra = f'<p class="rr-value">Record updated {e(format_updated(card["updated"]))}.</p>'
    broker = f'<p class="rr-broker">Listing brokerage: {e(card["brokerage"])}</p>' if card.get("brokerage") else ""
    mls = f'<p class="rr-broker">MLS® {e(card["mls"])}</p>' if card.get("mls") else ""
    badge = ""
    if card.get("realtor_url"):
        badge = (
            f'<a href="{e(card["realtor_url"])}" target="_blank" rel="noopener">'
            f'<img src="{BADGE}" alt="Powered by REALTOR.ca" width="120" height="24"></a>'
        )
    return f'''<article class="rr-card">
  {media}
  <div class="rr-card-body">
    <h3><a href="{e(href)}">{e(title)}</a></h3>
    <p class="rr-meta">{e(card["city"])} · {e(meta_line(card))}</p>
    <p class="rr-rent">{e(format_rent(card["price"]))} <span class="rr-meta">/ month</span></p>
    {extra}
    {broker}
    {mls}
    <div class="rr-actions">
      <a class="btn btn-outline btn-sm" href="{e(href)}">See this rental</a>
      {badge}
    </div>
  </div>
</article>'''


def wow_sub(wow):
    if wow is None:
        return "First saved week"
    return format_wow(wow)


def count_sub(delta):
    if delta is None:
        return "Homes in this week's medians"
    if delta == 0:
        return "Same count as last week"
    if delta > 0:
        noun = "home" if delta == 1 else "homes"
        return f"{delta} more {noun} than last week"
    noun = "home" if delta == -1 else "homes"
    return f"{abs(delta)} fewer {noun} than last week"


def new_intro(report):
    count = report["new_count"]
    shown = len(report["new_listings"])
    if report["new_method"] == "updated":
        start = format_long(datetime.strptime(report["week"], "%Y-%m-%d").date())
        if count == 0:
            body = "No comparable listing was updated this week."
        elif count == 1:
            body = "1 listing was updated this week."
        else:
            body = f"{count} listings were updated this week."
        if shown and shown < count:
            body += f" Showing {shown}."
        return (
            "This is the first snapshot, so new means the REALTOR.ca record was updated on or after "
            + start
            + ". Next Monday, a listing counts as new only when its id was not in the saved file. "
            + body
        )
    prev = format_long(datetime.strptime(report["previous_week"], "%Y-%m-%d").date()) if report.get("previous_week") else "the previous snapshot"
    if count == 0:
        return f"No listing id in this week's feed was missing from the {prev} snapshot."
    noun = "listing id is" if count == 1 else "listing ids are"
    verb = "was" if count == 1 else "were"
    sentence = f"{count} {noun} in this week's feed and {verb} not in the {prev} snapshot."
    if report["new_comparable"] != count:
        sentence += f" {report['new_comparable']} have a city and a rent I can show."
    if shown and shown < report["new_comparable"]:
        sentence += f" Here are {shown} of the newest."
    return sentence


def city_change_note(report):
    if not report.get("previous_week"):
        return "Week-over-week change shows up once two Mondays are saved, and only when both weeks have at least five homes in that row. This is the first saved week."
    prev = format_long(datetime.strptime(report["previous_week"], "%Y-%m-%d").date())
    return f"Change compares this median with the {prev} snapshot. A dash means one of the two weeks has fewer than five homes, so one listing could swing it."


def thin_sentence(thin):
    if not thin:
        return ""
    bits = ", ".join(f"{row['city']} ({row['count']})" for row in thin)
    return f'<p class="rr-note">Also on the feed, with too few homes for a row of their own: {e(bits)}.</p>'


def bars_html(rows):
    ranked = [row for row in rows if row.get("median")]
    ranked.sort(key=lambda row: (-row["median"], row["city"]))
    if not ranked:
        return ""
    top = max(row["median"] for row in ranked) or 1
    lines = ['<div class="rr-bars" aria-hidden="true">']
    for row in ranked:
        width = max(2, round(row["median"] / top * 100, 1))
        lines.append(
            '<div class="rr-bar-row"><span class="rr-bar-name">' + e(row["city"]) + "</span>"
            + f'<span class="rr-bar-track"><span class="rr-bar-fill" style="width:{width}%"></span></span>'
            + '<span class="rr-bar-val">' + e(format_rent(row["median"])) + "</span></div>"
        )
    lines.append("</div>")
    return "".join(lines)


def sparkline(values):
    nums = [value for value in values if isinstance(value, (int, float))]
    if len(nums) < 2:
        return ""
    width, height, pad = 88, 28, 3
    lo, hi = min(nums), max(nums)
    if lo == hi:
        lo -= 1
        hi += 1
    def x(index):
        return pad + (width - 2 * pad) * index / (len(nums) - 1)
    def y(value):
        return pad + (hi - value) / (hi - lo) * (height - 2 * pad)
    poly = " ".join(f"{x(index):.1f},{y(value):.1f}" for index, value in enumerate(nums))
    return (
        f'<svg class="rr-spark" viewBox="0 0 {width} {height}" aria-hidden="true" focusable="false">'
        f'<polyline fill="none" stroke="#24578c" stroke-width="2" points="{poly}"/></svg>'
    )


def city_medians(series, city):
    values = []
    for point in series:
        cell = (point.get("by_city") or {}).get(city) or {}
        if cell.get("median") is not None:
            values.append(cell["median"])
    return values


def table_html(caption, headers, body):
    head_cells = "".join(f'<th scope="col"{cls}>{label}</th>' for label, cls in headers)
    return (
        '<div class="table-wrap"><table class="price-table rr-table"><caption>'
        + e(caption)
        + "</caption><thead><tr>"
        + head_cells
        + "</tr></thead><tbody>"
        + body
        + "</tbody></table></div>"
    )


def money_cell(value):
    return f'<td class="num">{e(format_rent(value) if value is not None else "—")}</td>'


def trend_svg(series):
    points = [(point["week"], point["median"]) for point in series if point.get("median") is not None]
    if not points:
        return ""
    width, height = 720, 260
    pad_l, pad_r, pad_t, pad_b = 78, 16, 16, 36
    vals = [value for _, value in points]
    lo, hi = min(vals), max(vals)
    if lo == hi:
        lo = max(0, lo - 100)
        hi = hi + 100
    else:
        span = hi - lo
        lo -= span * 0.18
        hi += span * 0.18
    inner_w = width - pad_l - pad_r
    inner_h = height - pad_t - pad_b
    def x(index):
        if len(points) == 1:
            return pad_l + inner_w / 2
        return pad_l + inner_w * index / (len(points) - 1)
    def y(value):
        return pad_t + (hi - value) / (hi - lo) * inner_h
    parts = [f'<svg viewBox="0 0 {width} {height}" aria-hidden="true" focusable="false">']
    labels = [min(vals)] if min(vals) == max(vals) else [min(vals), max(vals)]
    for value in labels:
        yy = y(value)
        parts.append(f'<line x1="{pad_l}" y1="{yy:.1f}" x2="{width - pad_r}" y2="{yy:.1f}" stroke="#e1e6eb"/>')
        parts.append(
            f'<text x="{pad_l - 8}" y="{yy + 4:.1f}" text-anchor="end" font-family="Montserrat,sans-serif" font-size="12" fill="#56616d">{e(format_rent(value))}</text>'
        )
    if len(points) >= 2:
        poly = " ".join(f"{x(index):.1f},{y(value):.1f}" for index, (_, value) in enumerate(points))
        parts.append(f'<polyline fill="none" stroke="#24578c" stroke-width="2.5" points="{poly}"/>')
    for index, (_, value) in enumerate(points):
        parts.append(f'<circle cx="{x(index):.1f}" cy="{y(value):.1f}" r="4.5" fill="#173a5e"/>')
    indexes = list(range(len(points)))
    if len(points) > 8:
        step = max(1, len(points) // 6)
        indexes = list(range(0, len(points), step))
        if indexes[-1] != len(points) - 1:
            indexes.append(len(points) - 1)
    for index in indexes:
        parts.append(
            f'<text x="{x(index):.1f}" y="{height - 12}" text-anchor="middle" font-family="Montserrat,sans-serif" font-size="12" fill="#56616d">{e(short_week(points[index][0]))}</text>'
        )
    parts.append("</svg>")
    return "".join(parts)


def faq_items(report):
    span = format_span(report["week"], report["week_end"])
    return [
        (
            "Is this the rent tenants are paying?",
            "No. These are asking rents on active residential listings in the REALTOR.ca feed for the week of "
            + span
            + ", not rents on signed leases. A home can lease for less or more than the asking rent, and some listings leave the feed during the week.",
        ),
        (
            "Which homes are counted?",
            "I count active residential rentals with a city, a bedroom count, and an asking rent from $800 to $40,000 a month. I leave out listings with no city, a garage, or a size under 200 square feet. Medians and averages are rounded to the nearest dollar.",
        ),
        (
            "What does best value mean on this page?",
            "It means the asking rent per square foot is at least 12% under the median for the same city and bedroom count, or for that bedroom count across Greater Vancouver when that city has fewer than five homes with a usable size. The home also needs at least 400 square feet and a rent per square foot between $1.25 and $10. It is a screen, not a promise that the home is in good condition or that the rent figure is correct.",
        ),
        (
            "When does this report update?",
            "A scheduled job rebuilds this page every Monday morning from the rental feed and saves that week's medians. Week-over-week change compares the latest snapshot with the one saved the Monday before.",
        ),
    ]


def json_script(data):
    return '<script type="application/ld+json">\n' + json.dumps(data, indent=2, ensure_ascii=False) + "\n</script>"


# Google's Dataset rich result accepts creator only as Person or Organization.
# The sitewide RealEstateAgent node is a different type, so the creator is inlined.
DATASET_CREATOR = {
    "@type": "Person",
    "name": "Devin Desaulniers",
    "url": "https://devindesaulniers.ca",
    "worksFor": {"@type": "Organization", "name": "Axford Real Estate"},
}
TERMS_PAGE = "terms.html"
DATASET_LICENSE = SITE + TERMS_PAGE


def schema_blocks(report, title, description):
    url = SITE + PAGE
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": url + "#webpage",
                "url": url,
                "name": title,
                "description": description,
                "dateModified": report["prepared"],
                "inLanguage": "en-CA",
                "isPartOf": {"@type": "WebSite", "name": "Devin Desaulniers", "url": SITE},
                "about": {"@id": url + "#dataset"},
                "author": {"@id": SITE + "#devin-desaulniers"},
            },
            {
                "@type": "Dataset",
                "@id": url + "#dataset",
                "name": "Moving to Greater Vancouver: Weekly Rent Report",
                "description": description,
                "url": url,
                "creator": DATASET_CREATOR,
                "license": DATASET_LICENSE,
                "dateModified": report["prepared"],
                "temporalCoverage": report["week"] + "/" + report["week_end"],
                "spatialCoverage": {"@type": "Place", "name": "Greater Vancouver, British Columbia, Canada"},
                "keywords": ["asking rent", "Greater Vancouver", "rental market", "bedroom"],
                "isAccessibleForFree": True,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
                    {"@type": "ListItem", "position": 2, "name": "Weekly rent report", "item": url},
                ],
            },
        ],
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer}}
            for question, answer in faq_items(report)
        ],
    }
    return json_script(graph) + "\n" + json_script(faq)


def meta_description(report):
    median = format_rent(report["overall"]["median"])
    span = format_span(report["week"], report["week_end"])
    return (
        f"Median asking rent on the Greater Vancouver feed is {median}/month "
        f"for the week of {span}, with city and bedroom breakdowns."
    )


def sec_head(eyebrow, heading, aside=""):
    aside_html = f'<div class="sec-head-aside">{aside}</div>' if aside else ""
    return (
        '<div class="sec-head"><div><span class="eyebrow">' + eyebrow + "</span><h2>"
        + heading
        + "</h2></div>"
        + aside_html
        + "</div>"
    )


def render_page(report, series):
    title = "Moving to Greater Vancouver: Weekly Rent Report | Devin Desaulniers, Axford Real Estate"
    description = meta_description(report)
    span = format_span(report["week"], report["week_end"])
    prepared = format_long(datetime.strptime(report["prepared"], "%Y-%m-%d").date())
    feed_bit = ""
    if report.get("feed_updated"):
        parsed = parse_dt(report["feed_updated"])
        if parsed:
            feed_bit = " Feed updated " + format_long(parsed.astimezone(TZ).date()) + "."
    show_spark = any(len(city_medians(series, row["city"])) >= 2 for row in report["cities"])
    city_headers = [("City", ""), ("Listings", ' class="num"'), ("Median", ' class="num"'), ("Average", ' class="num"'), ("Vs last week", "")]
    if show_spark:
        city_headers.append(("Trend", ""))
    city_body = []
    for row in report["cities"]:
        cells = (
            f'<th scope="row" class="rr-city">{e(row["city"])}</th>'
            + f'<td class="num">{row["count"]}</td>'
            + money_cell(row["median"])
            + money_cell(row["average"])
            + f'<td>{e(format_wow(row["wow"]))}</td>'
        )
        if show_spark:
            cells += "<td>" + sparkline(city_medians(series, row["city"])) + "</td>"
        city_body.append("<tr>" + cells + "</tr>")
    bed_body = []
    for row in report["beds"]:
        bed_body.append(
            "<tr>"
            + f'<th scope="row">{e(row["label"])}</th>'
            + f'<td class="num">{row["count"]}</td>'
            + money_cell(row["median"])
            + money_cell(row["average"])
            + f'<td>{e(format_wow(row["wow"]))}</td>'
            + "</tr>"
        )
    trend_rows = []
    for point in series:
        trend_rows.append(
            "<tr><th scope=\"row\">"
            + e(format_span(point["week"], point["week_end"]))
            + "</th>"
            + money_cell(point.get("median"))
            + money_cell(point.get("average"))
            + f'<td class="num">{int(point.get("count") or 0)}</td></tr>'
        )
    trend_note = "Each Monday adds a point. One saved week is a dot, and the line starts on the second Monday."
    if len([point for point in series if point.get("median") is not None]) >= 2:
        trend_note = "Median asking rent for the homes counted each Monday."
    mover_html = ""
    if report["movers_up"] or report["movers_down"]:
        def mover_list(title, rows):
            if not rows:
                return ""
            items = "".join(
                f'<li><strong>{e(row["city"])}</strong> — {e(format_wow(row["wow"]))} to a median of {e(format_rent(row["median"]))} ({row["count"]} homes)</li>'
                for row in rows
            )
            return f'<div class="rr-mover"><h3>{title}</h3><ul class="guide-list">{items}</ul></div>'
        mover_html = '<div class="rr-movers">' + mover_list("Medians that rose", report["movers_up"]) + mover_list("Medians that fell", report["movers_down"]) + "</div>"
    new_cards = "".join(card_html(card) for card in report["new_listings"]) or "<p>Nothing new to show from this feed.</p>"
    if report["best"]:
        best_cards = "".join(card_html(card, value=True) for card in report["best"])
        best_intro = (
            "These are the homes whose asking rent per square foot sits furthest under the median for the same city and bedroom count. "
            "I kept at most two per city. A low figure can be an older home, a data error, or a real opening. I can tell those apart."
        )
    else:
        best_cards = ""
        best_intro = "No home cleared the screen this week. The full rental search is on the homes for rent page."
    faq_html = "".join(
        f'<div class="faq-item"><h3>{e(question)}</h3><div class="ans"><p>{e(answer)}</p></div></div>'
        for question, answer in faq_items(report)
    )
    legal = [
        f"{BROKERAGE} operates this website. Devin Desaulniers is a Real Estate Associate with {BROKERAGE}, {BROKERAGE_ADDR}, and a member of The Canadian Real Estate Association.",
        "Trademarks are owned or controlled by The Canadian Real Estate Association (CREA) and identify real estate professionals who are members of CREA (REALTOR®) and/or the quality of services they provide (MLS®).",
        "The listing information is deemed reliable but is not guaranteed. The information contained on this site is based in whole or in part on information that is provided by members of The Canadian Real Estate Association (CREA), who are responsible for its accuracy. REALTOR.ca Canada Inc. reproduces and distributes this information as a service for its members and neither CREA nor REALTOR.ca Canada Inc. assumes responsibility for its accuracy.",
        "The listing content on this website is protected by copyright and other laws, and is intended solely for the private, non-commercial use by individuals. Any other reproduction, distribution or use of the content, in whole or in part, is specifically forbidden. The prohibited uses include commercial use, “screen scraping”, “database scraping”, and any other activity intended to collect, store, reorganize or manipulate data on the pages produced by or displayed on this website.",
        "Each best-value and new-listing card shows the listing brokerage and a “Powered by REALTOR.ca” mark that links to that listing on REALTOR.ca. Leased, rented, and sold listings are not shown. Opening a listing on the homes for rent page sends a view event to the CREA DDF® Analytics Web Service.",
    ]
    legal_html = "".join(f"<p>{e(paragraph)}</p>" for paragraph in legal)
    legal_html += (
        '<p>How this report may be used is set out in the <a href="' + TERMS_PAGE + '">terms of use</a>. '
        "Listing data is provided through the CREA DDF® and is owned by the respective real estate boards.</p>"
    )
    cta_attrs = tenant_cta_attrs(PAGE)
    cta_href = tenant_cta_href()
    nav = (
        '<nav class="page-nav" aria-label="On this page"><div class="container"><span class="pn-label">On this page</span>'
        '<a href="#cities">By city</a><a href="#bedrooms">By bedroom</a><a href="#trend">Week by week</a>'
        '<a href="#new">New this week</a><a href="#value">Best value</a><a href="#methodology">How this is counted</a>'
        "</div></nav>"
    )
    page = head(
        title,
        description,
        "rent-report",
        page_url=PAGE,
        body_class="rr-page",
        extra_head=schema_blocks(report, title, description),
    )
    page += f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Weekly rent report</span>
    <h1>Moving to Greater Vancouver: Weekly Rent Report</h1>
    <p class="lead">Asking rents for the week of {e(span)}, from active residential listings on the REALTOR.ca feed. The median is the middle rent. The average sits higher when a few expensive houses are listed. Prepared {e(prepared)}.</p>
    <dl class="rr-stats">
      <div class="rr-stat"><dt>Median asking rent</dt><dd>{e(format_rent(report["overall"]["median"]))}</dd><dd class="rr-sub">{e(wow_sub(report["overall_wow"]))}</dd></div>
      <div class="rr-stat"><dt>Average asking rent</dt><dd>{e(format_rent(report["overall"]["average"]))}</dd><dd class="rr-sub">{e(wow_sub(report["average_wow"]))}</dd></div>
      <div class="rr-stat"><dt>Listings counted</dt><dd>{report["counted"]}</dd><dd class="rr-sub">{e(count_sub(report["count_delta"]))}</dd></div>
      <div class="rr-stat"><dt>New this week</dt><dd>{report["new_count"]}</dd><dd class="rr-sub">{e("Updated records" if report["new_method"] == "updated" else "Not in last week's file")}</dd></div>
    </dl>
    <div class="btn-row">
      <a class="btn btn-light" href="{cta_href}" {cta_attrs}>Start a rental search</a>
      <a class="btn btn-ghost-light" href="rentals.html">Browse homes for rent</a>
    </div>
    <p class="hero-note"><a href="{cta_href}" {cta_attrs}>{e(CTA_TEXT)}</a></p>
    <p class="hero-note">These are asking rents, not signed leases.{e(feed_bit)}</p>
  </div>
</section>
{nav}
<section class="section" id="cities">
  <div class="container">
    {sec_head("By city", "Median asking rent", '<p class="lead">Coquitlam, Port Moody, Port Coquitlam, Burnaby, Vancouver, Surrey, Langley, Richmond, New Westminster, Maple Ridge, and every other city with at least five counted homes.</p>')}
    {bars_html(report["cities"])}
    {table_html("Median and average monthly asking rent by city for the week of " + span, city_headers, "".join(city_body))}
    <p class="rr-note">{e(city_change_note(report))}</p>
    {thin_sentence(report["thin_cities"])}
  </div>
</section>
<section class="section section--paper" id="bedrooms">
  <div class="container">
    {sec_head("By bedroom", "What size costs what", "<p class=\"lead\">Studio through four bedrooms are counted on their own. Five bedrooms and up are one row, because those houses are rare on the rental feed.</p>")}
    {table_html("Median and average monthly asking rent by bedroom count for the week of " + span, [("Bedrooms", ""), ("Listings", ' class="num"'), ("Median", ' class="num"'), ("Average", ' class="num"'), ("Vs last week", "")], "".join(bed_body))}
    <p class="rr-note">{e(city_change_note(report))}</p>
  </div>
</section>
<section class="section section--tint" id="trend">
  <div class="container">
    {sec_head("Week by week", "Median asking rent over time", "<p class=\"lead\">" + e(trend_note) + "</p>")}
    <figure class="rr-chart">
      <figcaption>Median monthly asking rent, saved each week</figcaption>
      {trend_svg(series)}
    </figure>
    {table_html("Saved weekly medians", [("Week", ""), ("Median", ' class="num"'), ("Average", ' class="num"'), ("Listings", ' class="num"')], "".join(trend_rows))}
    {mover_html}
  </div>
</section>
<section class="section" id="new">
  <div class="container">
    {sec_head("New this week", "Listings that just showed up", "<p class=\"lead\">" + e(new_intro(report)) + "</p>")}
    <div class="rr-cards">{new_cards}</div>
  </div>
</section>
<section class="section section--paper" id="value">
  <div class="container">
    {sec_head("Best value", "Lower rent for the size", "<p class=\"lead\">" + e(best_intro) + "</p>")}
    <div class="rr-cards">{best_cards}</div>
    <p class="rr-note"><a href="rentals.html">See every home for rent</a> to filter by city, budget, and bedrooms.</p>
  </div>
</section>
<section class="section" id="methodology">
  <div class="container narrow-wide">
    {sec_head("How this is counted", "What the numbers leave out")}
    <p>This week the feed had {report["feed_count"]} active rentals. I used {report["counted"]} in the medians and left out {report["excluded"]}.</p>
    <div class="faq-list rr-faq">{faq_html}</div>
    <h2 class="sub-h">Listing data</h2>
    {legal_html}
  </div>
</section>
<section class="section section--night cta-band">
  <div class="container center">
    <span class="eyebrow">Tenant relocation</span>
    <h2>Want me to find yours?</h2>
    <p class="lead">Tenant Relocation Service $1,500 + GST. I search the cities you care about, walk the home or do a live video tour, and review the lease with you before you send a deposit.</p>
    <div class="btn-row">
      <a class="btn btn-light" href="{cta_href}" {cta_attrs}>Start a rental search</a>
      <a class="btn btn-ghost-light" href="{TEL}">Call or text {PHONE}</a>
    </div>
  </div>
</section>
'''
    page += foot()
    return page


def wrap_text(text, width=72):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        if line and len(line) + 1 + len(word) > width:
            lines.append(line)
            line = word
        else:
            line = word if not line else line + " " + word
    if line:
        lines.append(line)
    return "\n".join(lines)


def render_newsletter_text(report):
    span = format_span(report["week"], report["week_end"])
    prepared = format_long(datetime.strptime(report["prepared"], "%Y-%m-%d").date())
    lines = [
        "MOVING TO GREATER VANCOUVER: WEEKLY RENT REPORT",
        f"Week of {span}",
        f"Prepared {prepared}",
        "",
        CTA_TEXT,
        SITE + "tenants.html#intake",
        "",
        wrap_text(
            f"Median asking rent: {format_rent(report['overall']['median'])} a month ({wow_sub(report['overall_wow'])}). "
            f"Average: {format_rent(report['overall']['average'])} ({wow_sub(report['average_wow'])}). "
            f"Listings counted: {report['counted']}. New this week: {report['new_count']}."
        ),
        "",
        wrap_text(new_intro(report)),
        "",
        "BY CITY",
        wrap_text(city_change_note(report)),
    ]
    for row in report["cities"]:
        if not row["count"]:
            continue
        lines.append(
            f"{row['city']} — median {format_rent(row['median'])}, average {format_rent(row['average'])}, "
            f"{row['count']} homes, {format_wow(row['wow'])}"
        )
    lines += ["", "BY BEDROOM"]
    for row in report["beds"]:
        if not row["count"]:
            continue
        lines.append(
            f"{row['label']} — median {format_rent(row['median'])}, average {format_rent(row['average'])}, "
            f"{row['count']} homes, {format_wow(row['wow'])}"
        )
    lines += ["", "NEW LISTINGS"]
    if not report["new_listings"]:
        lines.append("None to show.")
    for card in report["new_listings"]:
        lines.append(
            f"- {card['address']}, {card['city']} — {format_beds(card['beds'])}, {format_rent(card['price'])}/month"
        )
        lines.append("  " + rental_href(card["id"], absolute=True))
    lines += ["", "BEST-VALUE RENTALS"]
    if not report["best"]:
        lines.append("None cleared the screen this week.")
    for index, card in enumerate(report["best"], start=1):
        pct = int(Decimal(str(card["discount"] * 100)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        lines.append(
            f"{index}. {card['address']}, {card['city']} — {format_beds(card['beds'])}, "
            f"{format_rent(card['price'])}/month, {card['sqft']:,} sq ft, {pct}% under the {card['peer_label']} median"
        )
        if card.get("brokerage"):
            lines.append(f"   Listing brokerage: {card['brokerage']}")
        lines.append("   " + rental_href(card["id"], absolute=True))
    lines += [
        "",
        wrap_text(
            "Figures are asking rents on active REALTOR.ca listings, not signed leases. "
            f"Full report: {SITE}{PAGE}"
        ),
        "",
        CTA_TEXT,
        SITE + "tenants.html#intake",
        "",
        "Devin Desaulniers",
        f"Real Estate Associate, {BROKERAGE}",
        PHONE,
        EMAIL,
        SITE,
    ]
    return "\n".join(lines) + "\n"


def render_newsletter_html(report):
    span = format_span(report["week"], report["week_end"])
    prepared = format_long(datetime.strptime(report["prepared"], "%Y-%m-%d").date())
    font = "font-family:Verdana,Geneva,sans-serif;"
    ink = font + "color:#27333f;"
    muted = font + "color:#56616d;"

    def city_rows_html():
        rows = []
        for row in report["cities"]:
            if not row["count"]:
                continue
            rows.append(
                "<tr>"
                f'<td style="{ink}padding:8px 8px 8px 0;border-bottom:1px solid #e1e6eb;">{e(row["city"])}</td>'
                f'<td style="{ink}padding:8px;border-bottom:1px solid #e1e6eb;text-align:right;">{e(format_rent(row["median"]))}</td>'
                f'<td style="{ink}padding:8px;border-bottom:1px solid #e1e6eb;text-align:right;">{e(format_rent(row["average"]))}</td>'
                f'<td style="{ink}padding:8px;border-bottom:1px solid #e1e6eb;text-align:right;">{row["count"]}</td>'
                f'<td style="{ink}padding:8px 0 8px 8px;border-bottom:1px solid #e1e6eb;">{e(format_wow(row["wow"]))}</td>'
                "</tr>"
            )
        return "".join(rows)

    def bed_rows_html():
        rows = []
        for row in report["beds"]:
            if not row["count"]:
                continue
            rows.append(
                "<tr>"
                f'<td style="{ink}padding:8px 8px 8px 0;border-bottom:1px solid #e1e6eb;">{e(row["label"])}</td>'
                f'<td style="{ink}padding:8px;border-bottom:1px solid #e1e6eb;text-align:right;">{e(format_rent(row["median"]))}</td>'
                f'<td style="{ink}padding:8px 0 8px 8px;border-bottom:1px solid #e1e6eb;">{e(format_wow(row["wow"]))}</td>'
                "</tr>"
            )
        return "".join(rows)

    best_bits = []
    for card in report["best"]:
        pct = int(Decimal(str(card["discount"] * 100)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        href = rental_href(card["id"], absolute=True)
        broker = f" Listing brokerage: {e(card['brokerage'])}." if card.get("brokerage") else ""
        best_bits.append(
            f'<p style="{ink}font-size:15px;line-height:1.5;margin:0 0 12px;">'
            f'<a href="{e(href)}" style="{font}color:#24578c;">{e(card["address"])}, {e(card["city"])}</a>'
            f' — {e(format_beds(card["beds"]))}, {e(format_rent(card["price"]))}/month, {card["sqft"]:,} sq ft, '
            f'{pct}% under the {e(card["peer_label"])} median.{broker}</p>'
        )
    best_html = "".join(best_bits) or f'<p style="{ink}font-size:15px;">None cleared the screen this week.</p>'
    new_bits = []
    for card in report["new_listings"]:
        href = rental_href(card["id"], absolute=True)
        new_bits.append(
            f'<p style="{ink}font-size:15px;line-height:1.5;margin:0 0 8px;">'
            f'<a href="{e(href)}" style="{font}color:#24578c;">{e(card["address"])}, {e(card["city"])}</a>'
            f' — {e(format_beds(card["beds"]))}, {e(format_rent(card["price"]))}/month</p>'
        )
    new_html = "".join(new_bits) or f'<p style="{ink}font-size:15px;">None to show.</p>'
    cta = (
        f'<a href="{SITE}tenants.html#intake" style="{font}display:inline-block;padding:14px 22px;'
        f'background-color:#24578c;color:#ffffff;text-decoration:none;border-radius:6px;font-size:15px;font-weight:bold;">'
        f'{e(CTA_TEXT)}</a>'
    )
    preheader = e(CTA_TEXT + " Median asking rent " + format_rent(report["overall"]["median"]) + " for the week of " + span + ".")
    return f'''<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moving to Greater Vancouver: Weekly Rent Report — week of {e(span)}</title>
<link rel="canonical" href="{SITE}{PAGE}">
<meta name="robots" content="noindex, nofollow">
</head>
<body style="margin:0;padding:0;background-color:#f4f6f8;{font}color:#27333f;">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">{preheader}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f4f6f8;{font}color:#27333f;">
  <tr>
    <td align="center" style="padding:24px 12px;">
      <table role="presentation" width="640" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:640px;background-color:#ffffff;border:1px solid #e1e6eb;">
        <tr>
          <td style="padding:28px 28px 8px;background-color:#0d1b2a;{font}color:#ffffff;">
            <p style="{font}margin:0 0 8px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#93bde6;">Weekly rent report</p>
            <h1 style="{font}margin:0 0 8px;font-size:26px;line-height:1.25;color:#ffffff;font-weight:bold;">Moving to Greater Vancouver: Weekly Rent Report</h1>
            <p style="{font}margin:0;font-size:15px;line-height:1.5;color:#c9d5e1;">Week of {e(span)}. Prepared {e(prepared)}.</p>
          </td>
        </tr>
        <tr>
          <td style="padding:22px 28px;background-color:#173a5e;">
            {cta}
          </td>
        </tr>
        <tr>
          <td style="padding:24px 28px 8px;">
            <p style="{ink}font-size:16px;line-height:1.5;margin:0 0 8px;">Median asking rent: <strong>{e(format_rent(report["overall"]["median"]))}</strong> a month ({e(wow_sub(report["overall_wow"]))})</p>
            <p style="{ink}font-size:16px;line-height:1.5;margin:0 0 8px;">Average asking rent: <strong>{e(format_rent(report["overall"]["average"]))}</strong> ({e(wow_sub(report["average_wow"]))})</p>
            <p style="{ink}font-size:16px;line-height:1.5;margin:0 0 8px;">Listings counted: <strong>{report["counted"]}</strong>. New this week: <strong>{report["new_count"]}</strong>.</p>
            <p style="{muted}font-size:14px;line-height:1.5;margin:0 0 16px;">{e(new_intro(report))}</p>
            <p style="{ink}font-size:14px;margin:0 0 18px;"><a href="{SITE}{PAGE}" style="{font}color:#24578c;">Open the full report</a></p>
            <h2 style="{font}margin:8px 0 10px;font-size:18px;color:#132639;">By city</h2>
            <p style="{muted}font-size:14px;line-height:1.5;margin:0 0 12px;">{e(city_change_note(report))}</p>
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="{font}font-size:14px;">
              <tr>
                <th align="left" style="{muted}padding:0 8px 8px 0;font-size:12px;font-weight:bold;">City</th>
                <th align="right" style="{muted}padding:0 8px 8px;font-size:12px;font-weight:bold;">Median</th>
                <th align="right" style="{muted}padding:0 8px 8px;font-size:12px;font-weight:bold;">Average</th>
                <th align="right" style="{muted}padding:0 8px 8px;font-size:12px;font-weight:bold;">Homes</th>
                <th align="left" style="{muted}padding:0 0 8px 8px;font-size:12px;font-weight:bold;">Vs last week</th>
              </tr>
              {city_rows_html()}
            </table>
            <h2 style="{font}margin:22px 0 10px;font-size:18px;color:#132639;">By bedroom</h2>
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="{font}font-size:14px;">
              {bed_rows_html()}
            </table>
            <h2 style="{font}margin:22px 0 10px;font-size:18px;color:#132639;">New listings</h2>
            {new_html}
            <h2 style="{font}margin:22px 0 10px;font-size:18px;color:#132639;">Best-value rentals</h2>
            {best_html}
          </td>
        </tr>
        <tr>
          <td style="padding:8px 28px 28px;">
            <p style="{muted}font-size:13px;line-height:1.5;margin:0 0 16px;">Figures are asking rents on active REALTOR.ca listings, not signed leases. {e(BROKERAGE)} · Devin Desaulniers, Real Estate Associate.</p>
            {cta}
            <p style="{muted}font-size:13px;line-height:1.5;margin:14px 0 0;">Call or text {PHONE} · <a href="mailto:{EMAIL}" style="{font}color:#24578c;">{EMAIL}</a></p>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</body>
</html>
'''


def save_history(root, record, weeks):
    history = os.path.join(root, HISTORY_DIR)
    os.makedirs(history, exist_ok=True)
    week_path = os.path.join(history, record["week"] + ".json")
    if os.path.exists(week_path):
        try:
            old = load_json(week_path)
        except (OSError, json.JSONDecodeError):
            old = None
        if isinstance(old, dict) and signature(old) == signature(record):
            record = dict(record)
            record["generated_at"] = old.get("generated_at", record["generated_at"])
    write_text(week_path, dumps(record))
    point = series_point(record)
    series = upsert_series(weeks, point)
    write_text(os.path.join(history, "series.json"), dumps({"weeks": series}))
    return series, record


def build_site(root, rentals_path, now=None):
    now = now or datetime.now(TZ)
    if not os.path.exists(rentals_path):
        raise ReportError("rentals file not found: " + rentals_path, 1)
    try:
        data = load_json(rentals_path)
    except (OSError, json.JSONDecodeError) as exc:
        raise ReportError("could not read rentals file: " + str(exc), 1) from exc
    if not isinstance(data, dict) or not isinstance(data.get("listings"), list):
        raise ReportError("rentals file has no listings array", 1)
    if data.get("sample"):
        raise ReportError("rentals file is sample data; refusing to publish the rent report", 2)
    prepared = prepare_listings(data["listings"])
    if not prepared["comparable"]:
        raise ReportError("no comparable rentals; leaving the published report unchanged", 1)
    monday, _, _ = week_bounds(now)
    history = os.path.join(root, HISTORY_DIR)
    series_path = os.path.join(history, "series.json")
    weeks = load_series(series_path) if os.path.exists(series_path) else []
    previous = previous_point(weeks, monday.isoformat())
    prev_ids = None
    if previous:
        prev_file = load_week_file(os.path.join(history, str(previous.get("week")) + ".json"))
        if prev_file and isinstance(prev_file.get("ids"), list):
            prev_ids = {str(listing_id) for listing_id in prev_file["ids"]}
    feed_updated = data.get("updated") if isinstance(data.get("updated"), str) else ""
    report = assemble(prepared, previous, prev_ids, now, feed_updated)
    series, record = save_history(root, report.pop("record"), weeks)
    report["series"] = series
    page = render_page(report, series)
    write_text(os.path.join(root, PAGE), page)
    news_dir = os.path.join(root, "rent-report")
    os.makedirs(news_dir, exist_ok=True)
    write_text(os.path.join(news_dir, "newsletter.html"), render_newsletter_html(report))
    write_text(os.path.join(news_dir, "newsletter.txt"), render_newsletter_text(report))
    patch_sitemap(root, record["prepared"])
    median = format_rent(report["overall"]["median"])
    print(
        f"rent report: week of {report['week']} — {report['counted']} comparable of {report['feed_count']}, "
        f"median {median}, new {report['new_count']} ({report['new_method']})"
    )
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build the weekly Greater Vancouver rent report from listings/rentals.json.")
    parser.add_argument("--root", default=None, help="Repository root. Default: parent of _build.")
    parser.add_argument("--rentals", default=None, help="Path to rentals.json.")
    parser.add_argument("--now", default=None, help="ISO timestamp used as today. Default: now in America/Vancouver.")
    args = parser.parse_args(argv)
    root = args.root or repo_root()
    rentals = args.rentals or os.path.join(root, "listings", "rentals.json")
    try:
        build_site(root, rentals, parse_now(args.now))
    except ReportError as exc:
        print(str(exc), file=sys.stderr)
        return exc.code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
