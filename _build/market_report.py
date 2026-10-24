#!/usr/bin/env python3
"""Build the monthly Tri-Cities, BC market report pages and PDF from JSON.

    cd _build && python3 market_report.py

Reads every file in _build/market_data/*.json. Writes:

    market-report/index.html
    market-report/<id>.html
    market-report/tri-cities-bc-market-report-<id>.pdf

`python3 build.py` calls write_reports() as well, so the shared header, footer
and sitemap stay in step. How to add next month: _build/MARKET_REPORT.md.

Numbers on the page are formatted from the JSON. The script checks that
month-over-month percents and sales-to-listings ratios match the counts, and
that every dollar amount and percent in the page is one of those figures.
It does not fetch or invent statistics.
"""
import datetime
import decimal
import glob
import html
import json
import os
import re
import shutil
import subprocess
import tempfile

from partials import BROKERAGE, BROKERAGE_ADDR, EMAIL, PHONE, SITE, TEL, foot, head

METRO_PLACES = {
    "sales_yoy": 1, "sales_vs_10yr": 0, "new_listings_yoy": 1, "new_listings_vs_10yr": 1,
    "active_listings_yoy": 0, "active_vs_10yr": 1, "sales_to_active": 1,
    "sales_to_active_detached": 1, "sales_to_active_attached": 1, "sales_to_active_apartment": 1,
    "composite_yoy": 1, "composite_mom": 1, "detached_sales_yoy": 1, "detached_yoy": 1,
    "detached_mom": 1, "apartment_sales_yoy": 1, "apartment_yoy": 1, "apartment_mom": 1,
    "attached_sales_yoy": 1, "townhouse_yoy": 1, "townhouse_mom": 1,
    "pressure_below": 0, "pressure_above": 0,
}

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(HERE, "market_data")
OUT_DIR = os.path.join(ROOT, "market-report")
MINUS = "\u2212"
DISCLAIMER = (
    "This report is general information, not legal, tax, or financial advice, and not a mortgage approval. "
    "A benchmark is the board's estimate for a typical property. A median is the middle sale among homes that sold. "
    "Neither figure is a price for a particular home, and nothing here is a promise about a future sale price."
)
FOOTNOTES = [
    "Benchmark prices and their one-month and one-year changes are the MLS Home Price Index figures Greater Vancouver REALTORS printed for that area and property type.",
    "Sales and new listings are from the board's listing and sales activity summary. The month-over-month percent is the percent that table prints (September compared with August). The year-over-year percent is calculated here from the September 2025 and September 2026 counts in that same table.",
    "Sales-to-listings is the percent the board prints on its listings table: September sales divided by September new listings. It is not a sales-to-active listings ratio. This package publishes a sales-to-active listings ratio for Metro Vancouver, not for Coquitlam, Port Coquitlam, or Port Moody.",
    "The price index uses the word townhouse. The sales tables use the word attached. The board's index note says townhomes are similar to attached properties but do not include duplexes, so those two rows are not the same set of homes.",
    "Median selling prices are blank where the board did not publish one. Its sales table says medians are not reported for areas with fewer than 20 sales.",
    "Coquitlam, Port Coquitlam, and Port Moody benchmarks are for those names on the index pages. Sales and new listings for Port Moody are the Port Moody/Belcarra column. This report does not split Belcarra out, because the table does not.",
    "Fraser Valley figures are the Fraser Valley Real Estate Board's, for the municipalities named in that release. They are not Tri-Cities, BC prices. Greater Vancouver REALTORS' Lower Mainland benchmark mixes both boards, so it is not used here.",
]


class MarketReportError(Exception):
    pass


def money(n):
    return f"${int(n):,}"


def round_half_up(value, places):
    quantum = decimal.Decimal("1") if places == 0 else decimal.Decimal("0.1")
    return decimal.Decimal(str(value)).quantize(quantum, rounding=decimal.ROUND_HALF_UP)


def places_fixed(n, places):
    return f"{abs(decimal.Decimal(str(n))):.{places}f}"


def signed_pct(n, places=1):
    body = places_fixed(n, places) + "%"
    if n < 0:
        return MINUS + body
    if n > 0:
        return "+" + body
    return body


def downup(n, places=1):
    body = places_fixed(n, places) + "%"
    if n < 0:
        return "down " + body
    if n > 0:
        return "up " + body
    return "unchanged"


def long_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def yoy_pct(current, previous):
    if not previous:
        return None
    return float(round_half_up((current - previous) / previous * 100, 1))


def esc(s):
    return html.escape(str(s), quote=True)


def find_chrome():
    for c in (os.environ.get("CHROME"), "google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        if c and shutil.which(c):
            return shutil.which(c)
    raise MarketReportError("Chrome/Chromium is required to render the PDF (set CHROME=/path)")


def load_raw():
    paths = sorted(glob.glob(os.path.join(DATA_DIR, "*.json")))
    if not paths:
        raise MarketReportError(f"No JSON files in {DATA_DIR}")
    reports = []
    for path in paths:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
        data["_file"] = os.path.basename(path)
        validate_raw(data)
        reports.append(data)
    reports.sort(key=lambda r: (r["published"], r["id"]), reverse=True)
    return reports


def validate_raw(data):
    fn = data["_file"]
    if data["id"] + ".json" != fn:
        raise MarketReportError(f"{fn}: id {data['id']!r} must match the file name")
    if not re.fullmatch(r"\d{4}-\d{2}", data["id"]):
        raise MarketReportError(f"{fn}: id must look like 2026-10")
    need = ("edition_label", "period_label", "compare_month_label", "compare_year_label", "published", "period", "sources", "metro", "fvreb", "areas")
    for key in need:
        if key not in data:
            raise MarketReportError(f"{fn}: missing {key}")
    if len(data["areas"]) != 3:
        raise MarketReportError(f"{fn}: expected three areas (Coquitlam, Port Coquitlam, Port Moody)")
    names = [a["name"] for a in data["areas"]]
    if names != ["Coquitlam", "Port Coquitlam", "Port Moody"]:
        raise MarketReportError(f"{fn}: areas must be Coquitlam, Port Coquitlam, Port Moody, in that order")
    for area in data["areas"]:
        btypes = [b["type"] for b in area["benchmarks"]]
        if btypes != ["All residential", "Detached", "Townhouse", "Apartment"]:
            raise MarketReportError(f"{fn}: {area['name']} benchmarks must be All residential, Detached, Townhouse, Apartment")
        atypes = [r["type"] for r in area["activity"]]
        if atypes != ["Detached", "Attached", "Apartment"]:
            raise MarketReportError(f"{fn}: {area['name']} activity must be Detached, Attached, Apartment")
        for row in area["activity"]:
            if row["listings"] <= 0:
                raise MarketReportError(f"{fn}: {area['name']} {row['type']} listings must be positive")
            calc_ratio = int(round_half_up(row["sales"] / row["listings"] * 100, 0))
            if calc_ratio != int(row["sales_to_listings"]):
                raise MarketReportError(
                    f"{fn}: {area['name']} {row['type']} sales-to-listings is {row['sales_to_listings']} "
                    f"but sales/listings rounds to {calc_ratio}"
                )
            for kind in ("sales", "listings"):
                prev = row[f"{kind}_prev_month"]
                if not prev:
                    continue
                calc = float(round_half_up((row[kind] - prev) / prev * 100, 1))
                printed = float(row[f"{kind}_mom"])
                if abs(calc - printed) > 0.001:
                    raise MarketReportError(
                        f"{fn}: {area['name']} {row['type']} {kind} month change prints {printed} "
                        f"but the counts calculate to {calc}"
                    )
    src_ids = {s["id"] for s in data["sources"]}
    for block in (data["metro"], data["fvreb"]):
        if block["source"] not in src_ids:
            raise MarketReportError(f"{fn}: source id {block['source']!r} is not in sources")


class Allowed:
    def __init__(self):
        self.money = set()
        self.pct = set()
        self.grouped = set()
        self.ints = set()
        for part in re.findall(r"\d+", PHONE + " " + BROKERAGE_ADDR):
            self.ints.add(int(part))

    def add_money(self, n):
        self.money.add(money(n))
        self.ints.add(int(n))

    def add_count(self, n):
        n = int(n)
        self.ints.add(n)
        if abs(n) >= 1000:
            self.grouped.add(f"{n:,}")

    def add_pct(self, n, places):
        self.pct.add(places_fixed(n, places) + "%")

    def add_year(self, year):
        self.ints.add(int(year))


def add_report_numbers(data, allowed):
    for src in data["sources"]:
        allowed.add_year(src["date"][:4])
    allowed.add_year(data["published"][:4])
    allowed.add_year(data["period"][:4])
    allowed.add_year(int(data["period"][:4]) - 1)
    metro = data["metro"]
    for key in (
        "sales", "sales_prev_year", "sales_10yr_avg", "new_listings", "new_listings_prev_year",
        "new_listings_10yr_avg", "active_listings", "active_listings_prev_year", "active_10yr_avg",
        "pressure_below", "pressure_above", "detached_sales", "detached_sales_prev_year",
        "apartment_sales", "apartment_sales_prev_year", "attached_sales", "attached_sales_prev_year",
    ):
        allowed.add_count(metro[key])
    for key in ("composite_benchmark", "detached_benchmark", "apartment_benchmark", "townhouse_benchmark"):
        allowed.add_money(metro[key])
    for key, places in METRO_PLACES.items():
        allowed.add_pct(metro[key], places)
    allowed.add_pct(data["fvreb"]["balanced_low"], 0)
    allowed.add_pct(data["fvreb"]["balanced_high"], 0)
    fv = data["fvreb"]
    for key in ("sales", "sales_prev_year", "sales_prev_month", "new_listings", "active_listings", "balanced_low", "balanced_high"):
        allowed.add_count(fv[key])
    for key in ("detached_benchmark", "townhouse_benchmark", "apartment_benchmark"):
        allowed.add_money(fv[key])
    for key in ("sales_yoy", "sales_mom", "detached_mom", "detached_yoy", "townhouse_mom", "townhouse_yoy", "apartment_mom", "apartment_yoy"):
        allowed.add_pct(fv[key], 1)
    for area in data["areas"]:
        for b in area["benchmarks"]:
            allowed.add_money(b["price"])
            allowed.add_pct(b["mom"], 1)
            allowed.add_pct(b["yoy"], 1)
        sales = listings = sales_y = listings_y = sales_m = listings_m = 0
        for row in area["activity"]:
            for key in ("sales", "sales_prev_month", "sales_prev_year", "listings", "listings_prev_month", "listings_prev_year"):
                allowed.add_count(row[key])
            allowed.add_pct(row["sales_mom"], 1)
            allowed.add_pct(row["listings_mom"], 1)
            allowed.add_pct(row["sales_to_listings"], 0)
            if row["median"] is not None:
                allowed.add_money(row["median"])
            for kind in ("sales", "listings"):
                prev = row[f"{kind}_prev_year"]
                if prev:
                    allowed.add_pct(yoy_pct(row[kind], prev), 1)
            sales += row["sales"]
            listings += row["listings"]
            sales_y += row["sales_prev_year"]
            listings_y += row["listings_prev_year"]
            sales_m += row["sales_prev_month"]
            listings_m += row["listings_prev_month"]
        for n in (sales, listings, sales_y, listings_y, sales_m, listings_m):
            allowed.add_count(n)
        if sales_y:
            allowed.add_pct(yoy_pct(sales, sales_y), 1)
        if listings_y:
            allowed.add_pct(yoy_pct(listings, listings_y), 1)


def audit(fragment, allowed, label):
    # The sitewide tenant promo is not a market figure. Keep it out of the number check.
    fragment = re.sub(r'<aside class="tenant-cta-bar"[\s\S]*?</aside>', " ", fragment)
    text = re.sub(r"<style[\s\S]*?</style>", " ", fragment, flags=re.I)
    text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.I)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = re.sub(r"https?://\S+", " ", text)
    for found in re.findall(r"\$\d{1,3}(?:,\d{3})+", text):
        if found not in allowed.money:
            raise MarketReportError(f"{label}: dollar amount {found} is not in the data file")
    rest = re.sub(r"\$\d{1,3}(?:,\d{3})+", " ", text)
    for found in re.findall(r"\d+(?:\.\d+)?%", rest):
        if found not in allowed.pct:
            raise MarketReportError(f"{label}: percent {found} is not in the data file")
    rest = re.sub(r"[−+\-]?\d+(?:\.\d+)?%", " ", rest)
    for found in re.findall(r"\d{1,3}(?:,\d{3})+", rest):
        if found not in allowed.grouped:
            raise MarketReportError(f"{label}: number {found} is not in the data file")
    rest = re.sub(r"\d{1,3}(?:,\d{3})+", " ", rest)
    for found in re.findall(r"\d+", rest):
        number = int(found)
        if number not in allowed.ints and number > 31:
            raise MarketReportError(f"{label}: number {number} is not in the data file")
    if re.search(r"\bbest\b", text, re.I) or re.search(r"\btop\b", text, re.I) or re.search(r"\bguaranteed\b", text, re.I):
        raise MarketReportError(f"{label}: remove best, top, or guaranteed")
    if re.search(r"Tri-Cities(?!, BC)", text):
        raise MarketReportError(f"{label}: write Tri-Cities, BC")
    if "Axford Real Estate" not in text:
        raise MarketReportError(f"{label}: show Axford Real Estate as the brokerage")


def source_by_id(data, sid):
    for src in data["sources"]:
        if src["id"] == sid:
            return src
    raise MarketReportError(f"missing source {sid}")


def prepare_area(area):
    sales = sum(r["sales"] for r in area["activity"])
    listings = sum(r["listings"] for r in area["activity"])
    sales_y = sum(r["sales_prev_year"] for r in area["activity"])
    listings_y = sum(r["listings_prev_year"] for r in area["activity"])
    comp = area["benchmarks"][0]
    return {
        "name": area["name"],
        "hpi_name": area["hpi_name"],
        "activity_name": area["activity_name"],
        "benchmarks": area["benchmarks"],
        "activity": area["activity"],
        "sales": sales,
        "listings": listings,
        "sales_yoy": yoy_pct(sales, sales_y),
        "listings_yoy": yoy_pct(listings, listings_y),
        "composite": comp,
    }


def row_lookup(areas, name, table, typ):
    for area in areas:
        if area["name"] == name:
            rows = area[table]
            for row in rows:
                if row["type"] == typ:
                    return area, row
    raise MarketReportError(f"missing {name} {table} {typ}")


def extreme_ratio(areas):
    rows = []
    for area in areas:
        for row in area["activity"]:
            rows.append((area, row))
    low = min(rows, key=lambda item: item[1]["sales_to_listings"])
    high = max(rows, key=lambda item: item[1]["sales_to_listings"])
    jump = max(rows, key=lambda item: item[1]["listings_mom"])
    return low, high, jump


def fit_and_faq(data, areas):
    """Plain-language sections. Every figure is pulled from `data`."""
    year = esc(data["compare_year_label"])
    month = esc(data["compare_month_label"])
    period = esc(data["period_label"])
    m = data["metro"]
    fv = data["fvreb"]
    gvr = source_by_id(data, "gvr-package")
    fsrc = source_by_id(data, "fvreb-package")
    low, high, jump = extreme_ratio(areas)
    comp_bits = []
    for area in areas:
        c = area["composite"]
        comp_bits.append(
            f"{esc(area['name'])} {money(c['price'])} ({downup(c['yoy'])} from {year}, {downup(c['mom'])} from {month})"
        )
    all_down = all(b["yoy"] < 0 for area in areas for b in area["benchmarks"])
    price_lead = (
        "Yes. On the MLS Home Price Index, every published benchmark in these three cities was lower than a year earlier."
        if all_down else
        "Here are the composite benchmarks the board published. Read each one against its own year-ago figure."
    )
    median_bits = []
    unpublished = []
    for area in areas:
        label = area["activity_name"]
        for row in area["activity"]:
            if row["median"] is None:
                unpublished.append(f"{label} {row['type'].lower()} ({row['sales']} sales)")
            else:
                median_bits.append(f"{label} {row['type'].lower()} {money(row['median'])} ({row['sales']} sales)")
    detached_bits = []
    apartment_bits = []
    small_base = []
    for area in areas:
        d_area, d_row = row_lookup([area], area["name"], "activity", "Detached")
        a_area, a_row = row_lookup([area], area["name"], "activity", "Apartment")
        detached_bits.append(
            f"{esc(area['activity_name'])} {d_row['sales']} detached sales, compared with {d_row['sales_prev_year']} in {year} ({downup(yoy_pct(d_row['sales'], d_row['sales_prev_year']))})"
        )
        apartment_bits.append(
            f"{esc(area['activity_name'])} {a_row['sales']} apartment sales, compared with {a_row['sales_prev_year']} in {year} ({downup(yoy_pct(a_row['sales'], a_row['sales_prev_year']))})"
        )
        for row in area["activity"]:
            prev = row["sales_prev_year"]
            if prev and prev < 10 and row["sales"] != prev:
                small_base.append(
                    f"{esc(area['activity_name'])} {row['type'].lower()} sales went from {prev} in {year} to {row['sales']} ({downup(yoy_pct(row['sales'], prev))})"
                )
    small_para = ""
    if small_base:
        small_para = "<p>Where the year-ago count was under 10, read the two counts, not only the percent: " + "; ".join(small_base) + ".</p>"
    buyer = f"""
<p>If you are buying in the Tri-Cities, BC, the published composite benchmarks are {'; '.join(comp_bits)}. That index is not a price for the home you want, and it is not a promise about the next sale.</p>
<p>Greater Vancouver REALTORS published a sales-to-active listings ratio of {places_fixed(m['sales_to_active'], 1)}% for Metro Vancouver in {period}: {places_fixed(m['sales_to_active_detached'], 1)}% for detached homes, {places_fixed(m['sales_to_active_attached'], 1)}% for attached homes, and {places_fixed(m['sales_to_active_apartment'], 1)}% for apartments. The board says prices tend to face downward pressure when that ratio stays below {int(m['pressure_below'])}% for a sustained period, and upward pressure when it stays above {int(m['pressure_above'])}% for several months. That ratio is for the whole region. This release does not publish one for Coquitlam, Port Coquitlam, or Port Moody.</p>
<p>What the city tables do print is sales divided by that month's new listings. In {period} the lowest of those figures was {esc(low[0]['activity_name'])} {low[1]['type'].lower()} at {int(low[1]['sales_to_listings'])}% ({low[1]['sales']} sales, {low[1]['listings']} new listings). The highest was {esc(high[0]['activity_name'])} {high[1]['type'].lower()} at {int(high[1]['sales_to_listings'])}% ({high[1]['sales']} sales, {high[1]['listings']} new listings).</p>
<p>The useful part is time. Line up a pre-approval, compare recent sales of the same kind of home, and keep subjects such as financing and inspection in the offer. Neighbourhood notes for the Tri-Cities, BC are on the <a href="__ROOT__buyers.html">buyers page</a>. These figures are resale benchmarks and MLS sales, not asking rents.</p>
""".strip()
    seller = f"""
<p>If you are selling, buyers can compare more new listings than they could in {month} in the segments where that count jumped. The largest of those printed month-to-month increases was {esc(jump[0]['activity_name'])} {jump[1]['type'].lower()} new listings: {jump[1]['listings']} in {period}, from {jump[1]['listings_prev_month']} in {month} ({signed_pct(jump[1]['listings_mom'])}).</p>
<p>Detached sales against {year}: {'; '.join(detached_bits)}.</p>
{small_para}
<p>Apartment sales against {year}: {'; '.join(apartment_bits)}.</p>
<p>I would price from recent sales near the property, not from the city benchmark. When several similar homes are listed, the one that sits above those sales is the one buyers can skip. Axford Real Estate is the brokerage. If you want that read on a specific address, use the form on the <a href="__ROOT__contact.html#qualify">contact page</a>.</p>
""".strip()
    faqs = [
        (
            "Are home prices down from last year in the Tri-Cities, BC?",
            f"<p>{price_lead} Composite benchmarks for {period}: {'; '.join(comp_bits)}. Detached, townhouse, and apartment benchmarks are in the tables above, each with the one-month and one-year change the board printed.</p>",
        ),
        (
            "Is this a buyer's market?",
            f"<p>Greater Vancouver REALTORS did not publish a sales-to-active listings ratio for Coquitlam, Port Coquitlam, or Port Moody in this package. For Metro Vancouver the ratio was {places_fixed(m['sales_to_active'], 1)}% in {period}. The board says downward pressure tends to show up when the ratio stays below {int(m['pressure_below'])}% for a sustained period, and upward pressure when it stays above {int(m['pressure_above'])}% for several months. One month under {int(m['pressure_below'])}% is not a forecast.</p>"
            f"<p>The city figure they do publish is sales divided by new listings. For example, {esc(low[0]['activity_name'])} {low[1]['type'].lower()} was {int(low[1]['sales_to_listings'])}%.</p>",
        ),
        (
            "What is a benchmark price, and how is that different from a median?",
            "<p>The benchmark is the MLS Home Price Index estimate for a typical property, so the mix of what happened to sell that month moves it less. The median is the middle price among homes that actually sold. The board says a benchmark is an estimated sale price of a typical property, not a price tag for one home.</p>"
            f"<p>Published medians for {period}: {'; '.join(median_bits)}. Not published, because the row had fewer than 20 sales: {'; '.join(unpublished)}.</p>",
        ),
        (
            "Why are Port Moody sales grouped with Belcarra?",
            "<p>On the benchmark pages the area is Port Moody. On the sales and listings tables the column is Port Moody/Belcarra. This report keeps that split: benchmarks are Port Moody, and sales, new listings, sales-to-listings, and medians are Port Moody/Belcarra. Belcarra is not given its own sales count in the table, so I do not invent one. Anmore is not named in that column.</p>",
        ),
        (
            "Do these numbers include the Fraser Valley?",
            f"<p>No. Coquitlam, Port Coquitlam, and Port Moody are in the Greater Vancouver REALTORS area. The Fraser Valley Real Estate Board's release of {esc(long_date(fsrc['date']))} covers {esc(', '.join(fv['areas']))}. That release recorded {fv['sales']:,} Fraser Valley sales in {period} ({downup(fv['sales_yoy'])} from {fv['sales_prev_year']:,} a year earlier, and {downup(fv['sales_mom'])} from {fv['sales_prev_month']:,} in {esc(data['compare_month_label'])}). Its detached benchmark was {money(fv['detached_benchmark'])}, townhome {money(fv['townhouse_benchmark'])}, and apartment {money(fv['apartment_benchmark'])}. The board described the composite benchmark as {esc(fv['composite_change'])}, and it did not print a dollar figure for that composite in the news release. Those are Fraser Valley figures, not Tri-Cities, BC prices.</p>"
            f"<p>Source: <a href=\"{esc(fsrc['url'])}\">{esc(fsrc['publisher'])}, {esc(long_date(fsrc['date']))}</a>. The Tri-Cities, BC tables above are from <a href=\"{esc(gvr['url'])}\">{esc(gvr['publisher'])}, {esc(long_date(gvr['date']))}</a>.</p>",
        ),
    ]
    return buyer, seller, faqs


def compared_with_avg(n, places, avg):
    body = places_fixed(n, places) + "%"
    if n < 0:
        return f"{body} below the 10-year average ({avg:,})"
    if n > 0:
        return f"{body} above the 10-year average ({avg:,})"
    return f"level with the 10-year average ({avg:,})"


def table_benchmarks(area, period_label):
    rows = []
    for b in area["benchmarks"]:
        rows.append(
            "<tr>"
            f"<th scope=\"row\">{esc(b['type'])}</th>"
            f"<td>{money(b['price'])}</td>"
            f"<td>{signed_pct(b['mom'])}</td>"
            f"<td>{signed_pct(b['yoy'])}</td>"
            "</tr>"
        )
    name = esc(area["hpi_name"])
    return f"""
<div class="mr-table-wrap">
<table class="mr-table">
<caption>MLS Home Price Index benchmarks, {name}, {esc(period_label)} — one-month and one-year change as printed</caption>
<thead><tr><th scope="col">Type</th><th scope="col">Benchmark</th><th scope="col">1 month</th><th scope="col">1 year</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
</div>
""".strip()


def year_cell(current, previous):
    y = yoy_pct(current, previous)
    return f"{previous:,} ({signed_pct(y)})"


def table_activity(area, data):
    rows = []
    for row in area["activity"]:
        median = money(row["median"]) if row["median"] is not None else "Not published"
        rows.append(
            "<tr>"
            f"<th scope=\"row\">{esc(row['type'])}</th>"
            f"<td>{row['sales']}</td>"
            f"<td>{signed_pct(row['sales_mom'])}</td>"
            f"<td>{year_cell(row['sales'], row['sales_prev_year'])}</td>"
            f"<td>{row['listings']}</td>"
            f"<td>{signed_pct(row['listings_mom'])}</td>"
            f"<td>{year_cell(row['listings'], row['listings_prev_year'])}</td>"
            f"<td>{int(row['sales_to_listings'])}%</td>"
            f"<td>{median}</td>"
            "</tr>"
        )
    name = esc(area["activity_name"])
    month = esc(data["compare_month_label"])
    year = esc(data["compare_year_label"])
    return f"""
<div class="mr-table-wrap">
<table class="mr-table">
<caption>Sales and new listings, {name}. Month change is the percent Greater Vancouver REALTORS printed versus {month}. Year change is calculated from the {year} count shown in the same cell.</caption>
<thead><tr>
<th scope="col">Type</th><th scope="col">Sales</th><th scope="col">Sales, month</th><th scope="col">Sales, year</th>
<th scope="col">New listings</th><th scope="col">Listings, month</th><th scope="col">Listings, year</th>
<th scope="col">Sales-to-listings</th><th scope="col">Median sale price</th>
</tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
</div>
""".strip()


def p(key):
    return METRO_PLACES[key]


def metro_block(data):
    m = data["metro"]
    period = esc(data["period_label"])
    return f"""
<p>For context, Greater Vancouver REALTORS reported {m['sales']:,} residential sales in Metro Vancouver in {period}, {downup(m['sales_yoy'], p('sales_yoy'))} from {m['sales_prev_year']:,} a year earlier, and {compared_with_avg(m['sales_vs_10yr'], p('sales_vs_10yr'), m['sales_10yr_avg'])} for the month. New listings were {m['new_listings']:,}, {downup(m['new_listings_yoy'], p('new_listings_yoy'))} from {m['new_listings_prev_year']:,}, and {compared_with_avg(m['new_listings_vs_10yr'], p('new_listings_vs_10yr'), m['new_listings_10yr_avg'])}. Homes listed for sale totalled {m['active_listings']:,}, {downup(m['active_listings_yoy'], p('active_listings_yoy'))} from {m['active_listings_prev_year']:,}, and {compared_with_avg(m['active_vs_10yr'], p('active_vs_10yr'), m['active_10yr_avg'])}.</p>
<p>The regional sales-to-active listings ratio was {places_fixed(m['sales_to_active'], p('sales_to_active'))}%. By type it was {places_fixed(m['sales_to_active_detached'], p('sales_to_active_detached'))}% detached, {places_fixed(m['sales_to_active_attached'], p('sales_to_active_attached'))}% attached, and {places_fixed(m['sales_to_active_apartment'], p('sales_to_active_apartment'))}% apartment. The composite benchmark was {money(m['composite_benchmark'])}, {downup(m['composite_yoy'], p('composite_yoy'))} from a year earlier and {downup(m['composite_mom'], p('composite_mom'))} from the previous month on the price-index table. Detached sales were {m['detached_sales']:,} ({downup(m['detached_sales_yoy'], p('detached_sales_yoy'))} from {m['detached_sales_prev_year']:,}), apartment sales {m['apartment_sales']:,} ({downup(m['apartment_sales_yoy'], p('apartment_sales_yoy'))} from {m['apartment_sales_prev_year']:,}), and attached sales {m['attached_sales']:,} ({downup(m['attached_sales_yoy'], p('attached_sales_yoy'))} from {m['attached_sales_prev_year']:,}).</p>
""".strip()


def fvreb_block(data):
    fv = data["fvreb"]
    fsrc = source_by_id(data, "fvreb-package")
    return f"""
<p>The Fraser Valley Real Estate Board release of {esc(long_date(fsrc['date']))} covers {esc(', '.join(fv['areas']))}. It does not cover Coquitlam, Port Coquitlam, or Port Moody. That release recorded {fv['sales']:,} Fraser Valley sales ({downup(fv['sales_yoy'])} from {fv['sales_prev_year']:,} a year earlier, and {downup(fv['sales_mom'])} from {fv['sales_prev_month']:,} in {esc(data['compare_month_label'])}). The detached benchmark was {money(fv['detached_benchmark'])}, the townhome benchmark {money(fv['townhouse_benchmark'])}, and the apartment benchmark {money(fv['apartment_benchmark'])}. The board described the composite benchmark as {esc(fv['composite_change'])}, and the news release did not print a dollar figure for that composite. Those are Fraser Valley figures, not Tri-Cities, BC prices. Source: <a href="{esc(fsrc['url'])}">{esc(fsrc['publisher'])}, {esc(long_date(fsrc['date']))}</a>.</p>
""".strip()


def sources_html(data, root):
    items = []
    for src in data["sources"]:
        items.append(
            f"<li><a href=\"{esc(src['url'])}\">{esc(src['title'])}</a> "
            f"— {esc(src['publisher'])}, {esc(long_date(src['date']))}.</li>"
        )
    return f"<ol class=\"mr-sources\">{''.join(items)}</ol>"


def footnotes_html():
    return "<ul class=\"mr-notes\">" + "".join(f"<li>{esc(note)}</li>" for note in FOOTNOTES) + "</ul>"


def faq_html(faqs):
    blocks = []
    for i, (q, a) in enumerate(faqs, 1):
        blocks.append(f"<details class=\"mr-faq\"><summary>{esc(q)}</summary><div class=\"mr-faq-a\">{a}</div></details>")
    return "\n".join(blocks)


def json_ld(data, faqs, page_url):
    gvr = source_by_id(data, "gvr-package")
    report = {
        "@context": "https://schema.org",
        "@type": ["Report", "Article"],
        "headline": f"{data['period_label']} Tri-Cities, BC market report",
        "description": meta_description(data),
        "url": SITE + page_url,
        "mainEntityOfPage": SITE + page_url,
        "datePublished": data["published"],
        "dateModified": data["published"],
        "temporalCoverage": data["period"],
        "inLanguage": "en-CA",
        "author": {
            "@type": "Person",
            "name": "Devin Desaulniers",
            "jobTitle": "Real Estate Associate",
            "url": SITE,
            "worksFor": {"@type": "RealEstateAgent", "name": BROKERAGE},
        },
        "publisher": {
            "@type": "Organization",
            "name": BROKERAGE,
            "url": SITE,
            "logo": {"@type": "ImageObject", "url": SITE + "assets/img/axford-logo.png"},
        },
        "about": {
            "@type": "Place",
            "name": "Tri-Cities, BC",
            "description": "Coquitlam, Port Coquitlam, and Port Moody, British Columbia",
        },
        "citation": [s["url"] for s in data["sources"]],
        "isBasedOn": gvr["url"],
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", a))).strip()},
            }
            for q, a in faqs
        ],
    }
    return (
        '<script type="application/ld+json">\n' + json.dumps(report, indent=2) + "\n</script>\n"
        '<script type="application/ld+json">\n' + json.dumps(faq, indent=2) + "\n</script>\n"
    )


def meta_description(data):
    bits = []
    for area in data["areas"]:
        comp = area["benchmarks"][0]
        bits.append(f"{area['name']} {money(comp['price'])}")
    gvr = source_by_id(data, "gvr-package")
    return (
        f"{data['period_label']} composite benchmarks for the Tri-Cities, BC: {', '.join(bits)}. "
        f"Sales and new listings from {gvr['publisher']}, {long_date(gvr['date'])}."
    )


def apply_root(fragment, root):
    return fragment.replace("__ROOT__", root)


def edition_page(data, areas, buyer, seller, faqs):
    root = "../"
    page_url = f"market-report/{data['id']}.html"
    gvr = source_by_id(data, "gvr-package")
    pdf_name = f"tri-cities-bc-market-report-{data['id']}.pdf"
    title = f"{data['period_label']} Tri-Cities, BC Market Report | Devin Desaulniers, Axford Real Estate"
    desc = meta_description(data)
    extra = json_ld(data, faqs, page_url) + f'<script src="{root}assets/js/market-report.js" defer></script>\n'
    page = head(title, esc(desc), "market-report", page_url=page_url, extra_head=extra, root=root, og_type="article")
    cards = []
    for area in areas:
        c = area["composite"]
        sales_line = f"{area['sales']} sales, {downup(area['sales_yoy'])} from {esc(data['compare_year_label'])}"
        list_line = f"{area['listings']} new listings, {downup(area['listings_yoy'])} from {esc(data['compare_year_label'])}"
        cards.append(f"""
<article class="mr-card">
  <h3>{esc(area['name'])}</h3>
  <p class="mr-price">{money(c['price'])}</p>
  <p class="mr-price-label">Composite benchmark</p>
  <p class="mr-changes"><span>{signed_pct(c['mom'])} month</span><span>{signed_pct(c['yoy'])} year</span></p>
  <p class="mr-sub">{sales_line}</p>
  <p class="mr-sub">{list_line}</p>
</article>""")
    city_sections = []
    for area in areas:
        same = area["hpi_name"] == area["activity_name"]
        scope = "" if same else (
            f"<p class=\"mr-scope\">Benchmarks below are for {esc(area['hpi_name'])}. "
            f"Sales and new listings are the {esc(area['activity_name'])} column.</p>"
        )
        city_sections.append(f"""
<section class="mr-city" id="{esc(area['name'].lower().replace(' ', '-'))}">
  <h3>{esc(area['name'])}</h3>
  {scope}
  {table_benchmarks(area, data['period_label'])}
  {table_activity(area, data)}
</section>""")
    nav = (
        '<nav class="page-nav" aria-label="On this page"><div class="container"><span class="pn-label">On this page</span>'
        '<a href="#numbers">Headline numbers</a><a href="#cities">By city</a><a href="#region">Region</a>'
        '<a href="#fit">Buyers and sellers</a><a href="#faq">Questions</a><a href="#download">PDF</a>'
        "</div></nav>"
    )
    main = f"""
<!-- Generated by _build/market_report.py from _build/market_data/{esc(data['_file'])}. Do not edit by hand. -->
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Market report · {esc(data['edition_label'])}</span>
    <h1>{esc(data['period_label'])} in the Tri-Cities, BC</h1>
    <p class="lead">Benchmark prices, sales, and new listings for Coquitlam, Port Coquitlam, and Port Moody, from the Greater Vancouver REALTORS release of {esc(long_date(gvr['date']))}. This edition covers {esc(data['period_label'])} only. A later month is not included until that release is published.</p>
    <p class="byline-inline">Devin Desaulniers, Real Estate Associate, Axford Real Estate</p>
    <div class="btn-row">
      <a class="btn btn-light" href="#download">Download the PDF</a>
      <a class="btn btn-ghost-light" href="{root}contact.html#qualify">Talk with Devin</a>
    </div>
  </div>
</section>
{nav}
<section class="section" id="numbers">
  <div class="container">
    <span class="eyebrow">Headline numbers</span>
    <h2>Three cities, {esc(data['period_label'])}</h2>
    <p class="lead">The composite benchmark is the board's estimate for a typical home of all types together. Sales and new listings under each price are the sum of the detached, attached, and apartment rows. The year change on those sums is calculated from the {esc(data['compare_year_label'])} counts. A sales-to-active listings ratio was not published for these cities.</p>
    <div class="mr-cards">{''.join(cards)}</div>
    <p class="mr-region-call"><strong>Metro Vancouver sales-to-active listings ratio: {places_fixed(data['metro']['sales_to_active'], 1)}%.</strong> That is the regional figure Greater Vancouver REALTORS published for {esc(data['period_label'])}, not a Tri-Cities, BC ratio. By type: {places_fixed(data['metro']['sales_to_active_detached'], 1)}% detached, {places_fixed(data['metro']['sales_to_active_attached'], 1)}% attached, {places_fixed(data['metro']['sales_to_active_apartment'], 1)}% apartment.</p>
  </div>
</section>
<section class="section section--paper" id="cities">
  <div class="container">
    <span class="eyebrow">By city</span>
    <h2>Benchmarks, sales, and listings</h2>
    <p>One-month and one-year benchmark changes are printed in the statistics package. Sales-to-listings is also printed. Year-over-year changes on sales and new listings are calculated from the two counts in the activity summary, and the cell shows the older count beside that percent.</p>
    {''.join(city_sections)}
    {footnotes_html()}
  </div>
</section>
<section class="section" id="region">
  <div class="container narrow-wide">
    <span class="eyebrow">The wider region</span>
    <h2>Metro Vancouver, then the Fraser Valley</h2>
    {metro_block(data)}
    <h3>Fraser Valley, not the Tri-Cities, BC</h3>
    {fvreb_block(data)}
  </div>
</section>
<section class="section section--paper" id="fit">
  <div class="container">
    <span class="eyebrow">Who this market is good for right now</span>
    <h2>Buyers and sellers</h2>
    <div class="mr-fit">
      <article class="mr-fit-card">
        <h3>If you are buying</h3>
        {apply_root(buyer, root)}
      </article>
      <article class="mr-fit-card">
        <h3>If you are selling</h3>
        {apply_root(seller, root)}
      </article>
    </div>
  </div>
</section>
<section class="section" id="faq">
  <div class="container narrow-wide">
    <span class="eyebrow">What people are asking</span>
    <h2>Questions buyers and sellers actually ask</h2>
    {apply_root(faq_html(faqs), root)}
  </div>
</section>
<section class="section section--paper" id="sources">
  <div class="container narrow-wide">
    <span class="eyebrow">Sources</span>
    <h2>Where the numbers come from</h2>
    <p>Every figure on this page is copied from the releases below, or calculated from two counts those releases print. The calculated ones are marked in the tables and notes.</p>
    {sources_html(data, root)}
    <p class="mr-disclaimer">{esc(DISCLAIMER)} MLS® and the MLS® Home Price Index are trademarks of The Canadian Real Estate Association.</p>
  </div>
</section>
<section class="section" id="download">
  <div class="container">
    <div class="mr-gate">
      <div>
        <span class="eyebrow">PDF</span>
        <h2>Download this report</h2>
        <p>The PDF is the same {esc(data['period_label'])} figures, laid out for printing. Leave your name and email and the file downloads on this page. Devin Desaulniers at Axford Real Estate gets a copy of the request. It has not been test-submitted.</p>
        <p class="mr-gate-note">Or skip the file and <a href="{root}contact.html#qualify">answer a few questions</a> about buying or selling.</p>
      </div>
      <form class="form-card" data-market-report action="https://formsubmit.co/ajax/devin@axfordrealestate.ca" method="POST" data-pdf="{esc(pdf_name)}" data-report-label="{esc(data['period_label'])} Tri-Cities, BC market report">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_subject" value="">
        <input type="hidden" name="form" value="Market report download">
        <input type="hidden" name="edition" value="{esc(data['edition_label'])}">
        <input type="hidden" name="report" value="{esc(data['period_label'])} Tri-Cities, BC">
        <div class="hp" aria-hidden="true"><label>Leave this field empty <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
        <div class="form-grid cols-2">
          <div class="field"><label for="mr-name">Name <span class="req">*</span></label><input id="mr-name" name="name" type="text" required autocomplete="name"></div>
          <div class="field"><label for="mr-email">Email <span class="req">*</span></label><input id="mr-email" name="email" type="email" required autocomplete="email"></div>
          <div class="field full"><label class="consent"><input type="checkbox" name="consent" value="yes" required> <span>I agree to be contacted by Devin Desaulniers (Axford Real Estate) by email or phone about my request. I can opt out at any time. <span class="req">*</span></span></label></div>
          <div class="full"><button type="submit" class="btn btn-primary">Send me the PDF</button><div class="form-status" role="status" aria-live="polite"></div></div>
        </div>
        <div data-report-thanks hidden tabindex="-1">
          <h3>The PDF is ready</h3>
          <p><a data-report-download href="{esc(pdf_name)}" download>Download the {esc(data['period_label'])} Tri-Cities, BC market report (PDF)</a></p>
        </div>
        <noscript><p>This download needs JavaScript. Email <a href="mailto:{EMAIL}">{EMAIL}</a> and ask for the {esc(data['period_label'])} Tri-Cities, BC market report.</p></noscript>
      </form>
    </div>
  </div>
</section>
<section class="section section--night" id="qualify">
  <div class="container narrow">
    <span class="eyebrow">Next step</span>
    <h2>Want this read against a home you have in mind?</h2>
    <p>Tell me whether you are buying or selling, the area in the Tri-Cities, BC, and your timeline. I will follow up from Axford Real Estate.</p>
    <a class="btn btn-light" href="{root}contact.html#qualify">Go to the contact form</a>
  </div>
</section>
"""
    # The Fraser Valley answer is also rendered inside #region via a second call.
    # Rebuild once so the region section and the FAQ stay identical.
    return page + main + foot(root)


def index_page(reports, prepared):
    root = "../"
    title = "Tri-Cities, BC Market Reports | Devin Desaulniers, Axford Real Estate"
    desc = "Monthly benchmark prices, sales, and new listings for Coquitlam, Port Coquitlam, and Port Moody, from Greater Vancouver REALTORS. Prepared by Devin Desaulniers, Axford Real Estate."
    items = []
    list_ld = []
    for data, areas in prepared:
        gvr = source_by_id(data, "gvr-package")
        comps = ", ".join(f"{esc(a['name'])} {money(a['composite']['price'])}" for a in areas)
        href = f"{data['id']}.html"
        url = SITE + "market-report/" + href
        items.append(f"""
<article class="mr-index-card">
  <p class="eyebrow">{esc(data['edition_label'])}</p>
  <h2><a href="{esc(href)}">{esc(data['period_label'])} Tri-Cities, BC market report</a></h2>
  <p>Composite benchmarks: {comps}.</p>
  <p class="mr-index-meta">Source: {esc(gvr['publisher'])}, {esc(long_date(gvr['date']))}.</p>
  <a class="btn btn-outline" href="{esc(href)}">Read the report</a>
</article>""")
        list_ld.append({
            "@type": "ListItem",
            "position": len(list_ld) + 1,
            "url": url,
            "name": f"{data['period_label']} Tri-Cities, BC market report",
        })
    ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Tri-Cities, BC market reports",
        "url": SITE + "market-report/",
        "isPartOf": SITE,
        "publisher": {"@type": "Organization", "name": BROKERAGE},
        "mainEntity": {"@type": "ItemList", "itemListElement": list_ld},
    }
    extra = '<script type="application/ld+json">\n' + json.dumps(ld, indent=2) + "\n</script>\n"
    page = head(title, esc(desc), "market-report", page_url="market-report/", extra_head=extra, root=root)
    newest = prepared[0][0]
    main = f"""
<!-- Generated by _build/market_report.py. Do not edit by hand. -->
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Market reports</span>
    <h1>Tri-Cities, BC market reports</h1>
    <p class="lead">Once a month I publish the benchmark prices, sales, and new listings Greater Vancouver REALTORS released for Coquitlam, Port Coquitlam, and Port Moody. The current edition is {esc(newest['period_label'])}.</p>
    <p class="byline-inline">Devin Desaulniers, Real Estate Associate, Axford Real Estate</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="mr-index">{''.join(items)}</div>
    <p class="mr-disclaimer">{esc(DISCLAIMER)}</p>
  </div>
</section>
"""
    return page + main + foot(root)


def pdf_html(data, areas, buyer, seller, faqs):
    gvr = source_by_id(data, "gvr-package")
    fsrc = source_by_id(data, "fvreb-package")
    root_img = "file://" + os.path.join(ROOT, "assets/img")
    cards = []
    for area in areas:
        c = area["composite"]
        cards.append(
            f"<div class='card'><p class='k'>{esc(area['name'])}</p>"
            f"<p class='p'>{money(c['price'])}</p>"
            f"<p class='s'>{signed_pct(c['mom'])} month · {signed_pct(c['yoy'])} year</p>"
            f"<p class='s'>{area['sales']} sales · {area['listings']} new listings</p></div>"
        )
    city_html = []
    for area in areas:
        block = [f"<h2>{esc(area['name'])}</h2>"]
        if area["hpi_name"] != area["activity_name"]:
            block.append(f"<p class='note'>Benchmarks: {esc(area['hpi_name'])}. Sales and listings: {esc(area['activity_name'])}.</p>")
        block.append(table_benchmarks(area, data["period_label"]).replace('class="mr-table-wrap"', "class='wrap'").replace('class="mr-table"', "class='t'"))
        block.append(table_activity(area, data).replace('class="mr-table-wrap"', "class='wrap'").replace('class="mr-table"', "class='t'"))
        city_html.append("<div class='city'>" + "".join(block) + "</div>")
    faq_bits = "".join(f"<h3>{esc(q)}</h3>{a}" for q, a in faqs)
    src_bits = "".join(
        f"<li>{esc(s['publisher'])}, {esc(long_date(s['date']))}. {esc(s['title'])}. {esc(s['url'])}</li>"
        for s in data["sources"]
    )
    return f"""<!doctype html>
<html lang="en-CA"><head><meta charset="utf-8"><title>{esc(data['period_label'])} Tri-Cities, BC market report</title>
<style>
  @page {{ size: letter; margin: 12mm 12mm 14mm; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font-family: "Iowan Old Style", Palatino, Georgia, serif; color: #132639; font-size: 11pt; line-height: 1.45; }}
  h1, h2, h3 {{ font-weight: 500; line-height: 1.15; margin: 0 0 .35em; color: #132639; }}
  h1 {{ font-size: 26pt; }}
  h2 {{ font-size: 16pt; margin-top: 1.1em; color: #173a5e; }}
  h3 {{ font-size: 12.5pt; margin: .8em 0 .2em; }}
  p {{ margin: 0 0 .6em; }}
  a {{ color: #24578c; }}
  header {{ display: flex; gap: 16px; align-items: center; border-bottom: 4px solid #3474b6; padding-bottom: 12px; margin-bottom: 16px; }}
  header img.mark {{ height: 72px; width: auto; }}
  header img.photo {{ height: 84px; width: 68px; object-fit: cover; border-radius: 4px; }}
  header img.ax {{ height: 28px; width: auto; margin-top: 6px; }}
  .who {{ flex: 1; }}
  .brand {{ font-family: Montserrat, "Segoe UI", sans-serif; font-weight: 700; letter-spacing: .08em; font-size: 11pt; margin: 0; }}
  .brand span {{ color: #808082; font-weight: 600; }}
  .role {{ margin: 2px 0 0; font-family: "Segoe UI", sans-serif; font-size: 9.5pt; color: #56616d; }}
  .eyebrow {{ font-family: "Segoe UI", sans-serif; font-size: 9pt; letter-spacing: .14em; text-transform: uppercase; color: #24578c; font-weight: 700; margin: 0 0 4px; }}
  .cards {{ display: flex; gap: 8px; margin: 12px 0 8px; }}
  .card {{ flex: 1; background: #f4f6f8; border-top: 3px solid #3474b6; padding: 8px 10px; }}
  .card .k {{ font-family: "Segoe UI", sans-serif; font-size: 9pt; letter-spacing: .08em; text-transform: uppercase; color: #24578c; font-weight: 700; margin: 0; }}
  .card .p {{ font-size: 16pt; margin: 2px 0; color: #173a5e; }}
  .card .s {{ font-family: "Segoe UI", sans-serif; font-size: 8.5pt; color: #27333f; margin: 0; }}
  table.t {{ width: 100%; border-collapse: collapse; font-family: "Segoe UI", sans-serif; font-size: 8pt; margin: 6px 0 12px; }}
  table.t caption {{ caption-side: bottom; text-align: left; font-size: 7.5pt; color: #56616d; padding-top: 4px; }}
  table.t th, table.t td {{ border-bottom: 1px solid #e1e6eb; padding: 3px 4px; text-align: right; vertical-align: top; }}
  table.t th {{ color: #173a5e; font-weight: 650; }}
  table.t thead th {{ text-align: right; border-bottom: 2px solid #3474b6; }}
  table.t th[scope="row"], table.t thead th:first-child {{ text-align: left; }}
  .note, .fine {{ font-family: "Segoe UI", sans-serif; font-size: 8.5pt; color: #56616d; }}
  ul {{ margin: .2em 0 .8em 1.1em; padding: 0; }}
  li {{ margin: 0 0 .25em; }}
  .break {{ break-before: page; }}
  .city {{ break-inside: avoid; }}
  h2, h3 {{ break-after: avoid; }}
  footer.colophon {{ margin-top: 16px; border-top: 3px solid #3474b6; padding-top: 8px; font-family: "Segoe UI", sans-serif; font-size: 8.5pt; color: #56616d; break-inside: avoid; }}
</style></head>
<body>
<header>
  <img class="mark" src="{root_img}/devin-mark.png" alt="">
  <img class="photo" src="{root_img}/devin-headshot-480.jpg" alt="Devin Desaulniers">
  <div class="who">
    <p class="brand">DEVIN <span>DESAULNIERS</span></p>
    <p class="role">Real Estate Associate · Axford Real Estate · Port Moody, BC</p>
    <img class="ax" src="{root_img}/axford-logo.png" alt="Axford Real Estate">
  </div>
</header>
<p class="eyebrow">{esc(data['edition_label'])} · devindesaulniers.ca</p>
<h1>{esc(data['period_label'])} Tri-Cities, BC market report</h1>
<p>Coquitlam, Port Coquitlam, and Port Moody. Figures from Greater Vancouver REALTORS, {esc(long_date(gvr['date']))}. This edition does not include a later month, because it has not been published. Brokerage: Axford Real Estate.</p>
<div class="cards">{''.join(cards)}</div>
<p class="note">Sales and new listings on the cards are the sum of the detached, attached, and apartment rows. Metro Vancouver sales-to-active listings ratio, {esc(data['period_label'])}: {places_fixed(data['metro']['sales_to_active'], 1)}% (detached {places_fixed(data['metro']['sales_to_active_detached'], 1)}%, attached {places_fixed(data['metro']['sales_to_active_attached'], 1)}%, apartment {places_fixed(data['metro']['sales_to_active_apartment'], 1)}%). A city sales-to-active ratio was not published.</p>
<div class="break"></div>
<h2>Benchmarks, sales, and new listings</h2>
{''.join(city_html)}
<ul>{''.join(f'<li>{esc(n)}</li>' for n in FOOTNOTES)}</ul>
<div class="break"></div>
<h2>Who this market is good for right now</h2>
<h3>If you are buying</h3>
{buyer.replace('__ROOT__', 'https://devindesaulniers.ca/')}
<h3>If you are selling</h3>
{seller.replace('__ROOT__', 'https://devindesaulniers.ca/')}
<h2>What people are asking</h2>
{faq_bits.replace('__ROOT__', 'https://devindesaulniers.ca/')}
<h2>Sources</h2>
<ul>{src_bits}</ul>
<p class="fine">{esc(DISCLAIMER)} MLS® and the MLS® Home Price Index are trademarks of The Canadian Real Estate Association. {esc(gvr['publisher'])}, {esc(long_date(gvr['date']))}. {esc(fsrc['publisher'])}, {esc(long_date(fsrc['date']))}.</p>
<footer class="colophon">Devin Desaulniers, Real Estate Associate · Axford Real Estate, 2326 Clarke St, Port Moody, BC · devindesaulniers.ca · {esc(PHONE)}</footer>
</body></html>
"""


def write_pdf(data, html_doc):
    os.makedirs(OUT_DIR, exist_ok=True)
    dest = os.path.join(OUT_DIR, f"tri-cities-bc-market-report-{data['id']}.pdf")
    with tempfile.TemporaryDirectory() as td:
        page = os.path.join(td, "report.html")
        with open(page, "w", encoding="utf-8") as handle:
            handle.write(html_doc)
        cmd = [
            find_chrome(), "--headless=new", "--no-sandbox", "--disable-gpu", "--mute-audio",
            "--allow-file-access-from-files", "--no-pdf-header-footer",
            "--virtual-time-budget=8000",
            f"--user-data-dir={os.path.join(td, 'profile')}",
            f"--print-to-pdf={dest}", "file://" + page,
        ]
        # Chrome writes the PDF and then often stays running in this environment.
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            _, err = proc.communicate(timeout=25)
        except subprocess.TimeoutExpired:
            proc.kill()
            _, err = proc.communicate()
        if not os.path.isfile(dest) or os.path.getsize(dest) < 5000:
            raise MarketReportError("Chrome did not write the PDF\n" + (err or "")[-2000:])
    return dest


def build_one(data):
    allowed = Allowed()
    add_report_numbers(data, allowed)
    areas = [prepare_area(a) for a in data["areas"]]
    buyer, seller, faqs = fit_and_faq(data, areas)
    fragment = "\n".join([
        buyer, seller, metro_block(data),
        "".join(table_benchmarks(a, data["period_label"]) + table_activity(a, data) for a in areas),
        "".join(a for _, a in faqs),
    ])
    audit(fragment, allowed, data["_file"])
    page = edition_page(data, areas, buyer, seller, faqs)
    main = page.split("<main", 1)[1].split("</main>", 1)[0]
    audit(main, allowed, data["_file"] + " page")
    pdf_doc = pdf_html(data, areas, buyer, seller, faqs)
    audit(pdf_doc, allowed, data["_file"] + " pdf")
    return page, pdf_doc, areas


def write_reports(root=None):
    """Write HTML and PDF files. Returns sitemap entries [(path, lastmod), ...]."""
    reports = load_raw()
    os.makedirs(OUT_DIR, exist_ok=True)
    prepared = []
    for data in reports:
        page, pdf_doc, areas = build_one(data)
        html_path = os.path.join(OUT_DIR, data["id"] + ".html")
        with open(html_path, "w", encoding="utf-8") as handle:
            handle.write(page)
        pdf_path = write_pdf(data, pdf_doc)
        prepared.append((data, areas))
        print(f"  market report: market-report/{data['id']}.html + {os.path.basename(pdf_path)} ({os.path.getsize(pdf_path)//1024} KB)")
    index = index_page(reports, prepared)
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as handle:
        handle.write(index)
    print(f"  market report: market-report/index.html ({len(prepared)} edition(s))")
    newest = prepared[0][0]["published"]
    entries = [("market-report/", newest)]
    for data, _areas in prepared:
        entries.append((f"market-report/{data['id']}.html", data["published"]))
    return entries


def sitemap_entries():
    """Lastmod dates for pages that already exist, without rebuilding."""
    reports = load_raw()
    if not reports:
        return []
    newest = reports[0]["published"]
    entries = [("market-report/", newest)]
    for data in reports:
        entries.append((f"market-report/{data['id']}.html", data["published"]))
    return entries


if __name__ == "__main__":
    write_reports(ROOT)
