#!/usr/bin/env python3
"""Check ads/copy.md headline and description lines against ad length limits.

Reads the copy doc only. Does not contact Meta or Google.
"""

from pathlib import Path
import sys

TEXT = Path(__file__).with_name("copy.md").read_text(encoding="utf-8")

# (section start marker, section end marker, limit, label)
# Headlines and descriptions are pulled from the fenced-looking lists by
# scanning lines that match the patterns below inside each audience block.

META_HEAD = 40
META_DESC = 30
GOOG_HEAD = 30
GOOG_DESC = 90
SITELINK = 25
SITELINK_LINE = 35


def between(src: str, start: str, end: str) -> str:
    i = src.find(start)
    if i < 0:
        raise SystemExit(f"missing section: {start}")
    j = src.find(end, i + len(start))
    if j < 0:
        raise SystemExit(f"missing end after: {start}")
    return src[i:j]


def field(block: str, label: str) -> str:
    needle = f"**{label}:** "
    for line in block.splitlines():
        if line.startswith(needle):
            return line[len(needle):].strip()
    raise SystemExit(f"missing {label}")


def numbered(block: str, heading_prefix: str) -> list[str]:
    lines = block.splitlines()
    out = []
    seen = False
    for line in lines:
        if line.startswith(heading_prefix):
            seen = True
            continue
        if seen:
            if line.startswith("**") or line.startswith("### ") or line.startswith("## "):
                break
            stripped = line.strip()
            dot = stripped.find(". ")
            if dot > 0 and stripped[:dot].isdigit():
                out.append(stripped[dot + 2:].strip())
    if not out:
        raise SystemExit(f"no numbered items under {heading_prefix}")
    return out


def check(items: list[tuple[str, str, int]]) -> list[str]:
    bad = []
    for label, value, limit in items:
        n = len(value)
        flag = "OVER" if n > limit else "ok"
        print(f"{flag:4}  {n:3}/{limit:<3}  {label}: {value}")
        if n > limit:
            bad.append(label)
    return bad


def main() -> int:
    renters = between(TEXT, "## Audience 1", "## Audience 2")
    buyers = between(TEXT, "## Audience 2", "## Audience 3")
    google = between(TEXT, "## Audience 3", "## Claims these ads")

    items: list[tuple[str, str, int]] = []
    for key in ("R1", "R2", "R3", "R4"):
        block = between(renters, f"### {key}", "### ") if key != "R4" else renters[renters.find(f"### {key}"):]
        # R4 runs to the end of the renter section; between() needs an end marker.
        items.append((f"{key} headline", field(block, "Headline"), META_HEAD))
        items.append((f"{key} description", field(block, "Description"), META_DESC))
    for key in ("B1", "B2", "B3", "B4"):
        if key != "B4":
            block = between(buyers, f"### {key}", "### ")
        else:
            block = buyers[buyers.find(f"### {key}"):]
        items.append((f"{key} headline", field(block, "Headline"), META_HEAD))
        items.append((f"{key} description", field(block, "Description"), META_DESC))

    group_a = between(google, "### Ad group A", "### Ad group B")
    group_b = between(google, "### Ad group B", "### Sitelinks")
    for i, line in enumerate(numbered(group_a, "**Headlines**"), 1):
        items.append((f"Google rentals headline {i}", line, GOOG_HEAD))
    for i, line in enumerate(numbered(group_a, "**Descriptions**"), 1):
        items.append((f"Google rentals description {i}", line, GOOG_DESC))
    for i, line in enumerate(numbered(group_b, "**Headlines**"), 1):
        items.append((f"Google relocation headline {i}", line, GOOG_HEAD))
    for i, line in enumerate(numbered(group_b, "**Descriptions**"), 1):
        items.append((f"Google relocation description {i}", line, GOOG_DESC))

    # Sitelink table rows: | text | line1 | line2 | url |
    sit = between(google, "### Sitelinks", "**Callouts:**")
    for line in sit.splitlines():
        if not line.startswith("| ") or line.startswith("| Sitelink") or line.startswith("| ---"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 3:
            continue
        items.append((f"Sitelink {cols[0]}", cols[0], SITELINK))
        items.append((f"Sitelink line {cols[0]} / 1", cols[1], SITELINK_LINE))
        items.append((f"Sitelink line {cols[0]} / 2", cols[2], SITELINK_LINE))

    # Display paths are the backtick segments on the Display path line.
    for label, block in (("rentals path", group_a), ("relocation path", group_b)):
        for line in block.splitlines():
            if line.startswith("**Display path:**"):
                segs = [p for p in line.split("`")[1::2] if p]
                for seg in segs:
                    items.append((f"{label} {seg}", seg, 15))

    bad = check(items)
    print(f"\n{len(items)} lines checked, {len(bad)} over the limit.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
