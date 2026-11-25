#!/usr/bin/env python3
"""Repair REALTOR.ca links on the listing files, then drop pages that 404.

The detail route is https://www.realtor.ca/real-estate/<PropertyId>/<slug>.
A URL with only the id is the "Oh No! The page you are looking for does not
exist." page. This rewrites those to a slugged detail URL (or a map search
when the property id is unknown).

It then requests each detail URL with a browser User-Agent. A Cloudflare
block, a 403, or a challenge is not a dead listing and is left alone. A real
404, including the Oh No page, removes that listing from the feed. When the
live page names its canonical detail URL, that exact URL is stored.

No third-party packages. The listing refresh workflow runs this after the
DDF pull. Exit 0 when REALTOR.ca blocks the checker: the repaired URLs are
still written, and nothing is removed on a guess.

Rows in data/manual-listings.json are kept even when REALTOR.ca returns a
404. Removing one is done in that file, not by this checker.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_ddf_listings as ddf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
PROBE = 16
WORKERS = 6
TIMEOUT = 20
MAX_BODY = 250_000

_CANONICAL = re.compile(
    r"https://www\.realtor\.ca/(?:real-estate|immobilier)/(\d+)/([a-z0-9-]+)",
    re.I,
)


def classify(status, body):
    """Tell a REALTOR.ca 404 apart from a bot block.

    status 0 means the request failed before an HTTP status (timeout, DNS).
    """
    text = (body or "").lower()
    blocked = status in (401, 403, 429, 503) or any(marker in text for marker in (
        "you have been blocked",
        "vous avez été bloqué",
        "cf-browser-verification",
        "just a moment",
        "/cdn-cgi/challenge-platform",
    ))
    if blocked:
        return "blocked"
    if status == 404 or ("oh no" in text and "does not exist" in text):
        return "dead"
    if status == 0 or status >= 500:
        return "error"
    if 200 <= status < 400:
        return "ok"
    return "error"


def canonical_url(body, property_id):
    """Exact detail URL published on a live REALTOR.ca page, if it names this id."""
    if not body or not property_id:
        return ""
    for match in _CANONICAL.finditer(body):
        if match.group(1) == str(property_id):
            return f"https://www.realtor.ca/real-estate/{match.group(1)}/{match.group(2).lower()}"
    return ""


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": BROWSER_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-CA,en;q=0.9",
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read(MAX_BODY).decode("utf-8", "replace")
            return resp.status, body
    except urllib.error.HTTPError as exc:
        raw = exc.read(MAX_BODY) if exc.fp else b""
        return exc.code, raw.decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError, OSError):
        return 0, ""


def repair_listings(listings):
    """Point every listing at a slugged detail URL or an MLS search. Returns how many changed."""
    changed = 0
    for item in listings:
        url = ddf.listing_realtor_url(item)
        if url and url != item.get("realtorUrl"):
            item["realtorUrl"] = url
            changed += 1
    return changed


def detail_targets(listings, limit):
    rows = []
    for item in listings:
        url = item.get("realtorUrl") or ""
        property_id = ddf.realtor_property_id(url)
        if property_id and ddf.realtor_detail_slug(url):
            rows.append(item)
    if limit is not None:
        return rows[:limit]
    return rows


def check_one(item):
    url = item.get("realtorUrl") or ""
    status, body = fetch(url)
    kind = classify(status, body)
    canonical = canonical_url(body, ddf.realtor_property_id(url)) if kind == "ok" else ""
    return item, kind, canonical


def apply_results(listings, results, protected=None):
    """Drop dead listings and adopt canonical URLs. Returns (kept, removed, retargeted).

    protected is a set of manual listing ids. Those rows are kept when the
    detail page 404s. A block or a transport error never removes anything.
    """
    protected = {str(value) for value in (protected or set())}
    dead_ids = set()
    retargeted = 0
    for item, kind, canonical in results:
        listing_id = str(item.get("id") or "")
        kept_manual = item.get("manual") is True or listing_id in protected
        if kind == "dead" and listing_id and kept_manual:
            print(
                f"Keeping manual listing {listing_id}. REALTOR.ca did not serve that detail page.",
                file=sys.stderr,
            )
            continue
        if kind == "dead" and listing_id:
            dead_ids.add(listing_id)
            continue
        if kind == "ok" and canonical and canonical != item.get("realtorUrl"):
            item["realtorUrl"] = canonical
            retargeted += 1
    if not dead_ids and not retargeted:
        return listings, [], 0
    kept = []
    removed = []
    for item in listings:
        if str(item.get("id") or "") in dead_ids:
            removed.append(item)
        else:
            kept.append(item)
    return kept, removed, retargeted


def outcome_counts(results):
    counts = {"ok": 0, "dead": 0, "blocked": 0, "error": 0}
    for _item, kind, _canonical in results:
        counts[kind] = counts.get(kind, 0) + 1
    return counts


def probe_blocked(results):
    """True when every probe was a block or a transport error, so the rest must not be judged."""
    if not results:
        return False
    counts = outcome_counts(results)
    return counts["ok"] == 0 and counts["dead"] == 0


def check_urls(listings, limit):
    """Return (results, skipped). skipped is how many detail URLs were not requested."""
    targets = detail_targets(listings, limit)
    if not targets:
        return [], 0
    if limit is not None:
        results = _run_checks(targets)
        return results, 0
    probe = targets[:PROBE]
    probed = _run_checks(probe)
    if probe_blocked(probed):
        return probed, max(0, len(targets) - len(probe))
    rest = targets[PROBE:]
    return probed + _run_checks(rest), 0


def _run_checks(items):
    if not items:
        return []
    results = []
    workers = min(WORKERS, len(items))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(check_one, item) for item in items]
        for future in as_completed(futures):
            results.append(future.result())
    return results


def load_feed(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def write_feed_file(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write("\n")
    os.replace(tmp, path)


def drop_shard_ids(path, ids):
    if not ids:
        return 0
    directory = ddf.shard_directory(path)
    if not os.path.isdir(directory):
        return 0
    removed = 0
    wanted = {str(value) for value in ids}
    for name in os.listdir(directory):
        if not name.endswith(".json"):
            continue
        dest = os.path.join(directory, name)
        with open(dest, encoding="utf-8") as fh:
            payload = json.load(fh)
        if not isinstance(payload, dict):
            continue
        hit = [key for key in list(payload) if key in wanted]
        if not hit:
            continue
        for key in hit:
            del payload[key]
            removed += 1
        if payload:
            write_feed_file(dest, payload)
        else:
            os.remove(dest)
    return removed


def process(path, http, limit):
    import manual_listings
    protected = manual_listings.active_ids()
    data = load_feed(path)
    listings = data.get("listings") or []
    repaired = repair_listings(listings)
    if repaired:
        data["count"] = len(listings)
        write_feed_file(path, data)
    removed = []
    retargeted = 0
    counts = {"ok": 0, "dead": 0, "blocked": 0, "error": 0}
    skipped = 0
    if http:
        results, skipped = check_urls(listings, limit)
        counts = outcome_counts(results)
        if not probe_blocked(results):
            kept, removed, retargeted = apply_results(listings, results, protected)
            if removed or retargeted:
                data["listings"] = kept
                data["count"] = len(kept)
                write_feed_file(path, data)
                drop_shard_ids(path, [item.get("id") for item in removed])
    return {
        "path": path,
        "repaired": repaired,
        "removed": len(removed),
        "retargeted": retargeted,
        "skipped": skipped,
        **counts,
    }


def default_paths():
    return [
        os.path.join(ROOT, "listings", "data.json"),
        os.path.join(ROOT, "listings", "rentals.json"),
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Repair and verify REALTOR.ca listing links.")
    parser.add_argument("paths", nargs="*", help="Feed JSON files. Defaults to the sale and rental feeds.")
    parser.add_argument("--no-http", action="store_true", help="Rewrite URLs and do not request REALTOR.ca.")
    parser.add_argument("--limit", type=int, default=None, help="Request at most this many detail URLs per file.")
    args = parser.parse_args(argv)
    paths = args.paths or default_paths()
    exit_code = 0
    for path in paths:
        if not os.path.isfile(path):
            print(f"Missing listing file: {path}", file=sys.stderr)
            exit_code = 1
            continue
        summary = process(path, http=not args.no_http, limit=args.limit)
        name = os.path.relpath(summary["path"], ROOT)
        print(
            f"{name}: repaired={summary['repaired']} removed={summary['removed']} "
            f"canonical={summary['retargeted']} ok={summary['ok']} dead={summary['dead']} "
            f"blocked={summary['blocked']} error={summary['error']} skipped={summary['skipped']}"
        )
        if summary["blocked"] and summary["ok"] == 0 and summary["dead"] == 0 and not args.no_http:
            print(
                f"{name}: REALTOR.ca blocked the checker, so no listing was removed. "
                "A block page is not a 404."
            )
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
