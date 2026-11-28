#!/usr/bin/env python3
"""Build the Greater Vancouver home maintenance guide PDF.

Source: _build/guides/greater-vancouver-home-maintenance-guide.html
Output: assets/guides/greater-vancouver-home-maintenance-guide.pdf

    python3 scripts/build_maintenance_guide.py

Needs Chrome or Chromium. Does not submit any form.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "_build", "guides", "greater-vancouver-home-maintenance-guide.html")
PDF = os.path.join(ROOT, "assets", "guides", "greater-vancouver-home-maintenance-guide.pdf")


def find_chrome():
    for name in (os.environ.get("CHROME"), "google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        if name and shutil.which(name):
            return shutil.which(name)
    sys.exit("Chrome or Chromium is required. Set CHROME=/path/to/chrome")


def check_copy(html):
    visible = re.sub(r"<style[\s\S]*?</style>", " ", html, flags=re.I)
    visible = re.sub(r"<script[\s\S]*?</script>", " ", visible, flags=re.I)
    visible = re.sub(r"\sstyle=\"[^\"]*\"", " ", visible)
    hit = re.search(r"\b(?:best|top|expert)\b", visible, re.I)
    if hit:
        sys.exit(f"guide copy uses {hit.group(0)!r}")
    if re.search(r"Tri-Cities(?!\s*,\s*BC)", html):
        sys.exit("guide copy has a bare Tri-Cities")
    sheets = len(re.findall(r'class="sheet"', html))
    if not 8 <= sheets <= 10:
        sys.exit(f"guide has {sheets} pages; keep it between 8 and 10")
    return sheets


def page_count(path):
    data = open(path, "rb").read()
    return len(re.findall(br"/Type\s*/Page(?!s)", data))


def main():
    html = open(HTML, encoding="utf-8").read()
    sheets = check_copy(html)
    os.makedirs(os.path.dirname(PDF), exist_ok=True)
    chrome = find_chrome()
    with tempfile.TemporaryDirectory() as td:
        dest = os.path.join(td, "guide.pdf")
        cmd = [
            chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--mute-audio",
            "--allow-file-access-from-files", "--no-pdf-header-footer",
            "--virtual-time-budget=20000",
            f"--user-data-dir={os.path.join(td, 'profile')}",
            f"--print-to-pdf={dest}",
            "file://" + HTML,
        ]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            _, err = proc.communicate(timeout=40)
        except subprocess.TimeoutExpired:
            proc.kill()
            _, err = proc.communicate()
        if not os.path.isfile(dest) or os.path.getsize(dest) < 20000:
            sys.exit("Chrome did not write the PDF\n" + (err or "")[-2000:])
        shutil.copyfile(dest, PDF)
    pages = page_count(PDF)
    print(f"wrote {os.path.relpath(PDF, ROOT)} ({pages} PDF pages, {sheets} sheets, {os.path.getsize(PDF)} bytes)")
    if pages != sheets:
        sys.exit(f"PDF page count {pages} does not match {sheets} sheets. Content likely overflowed a sheet.")


if __name__ == "__main__":
    main()
