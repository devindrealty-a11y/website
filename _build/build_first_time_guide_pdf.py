#!/usr/bin/env python3
"""Build assets/guides/first-time-home-buyer-guide-bc.pdf from the HTML source.

Requires Google Chrome. Run from anywhere:
  python3 _build/build_first_time_guide_pdf.py
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "assets", "guides", "first-time-home-buyer-guide-bc.html")
PDF = os.path.join(ROOT, "assets", "guides", "first-time-home-buyer-guide-bc.pdf")
CHROME = os.environ.get("CHROME", "/usr/bin/google-chrome-stable")


def main():
    if not os.path.isfile(HTML):
        sys.exit("missing " + HTML)
    url = "file://" + HTML
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--virtual-time-budget=15000",
        f"--print-to-pdf={PDF}",
        url,
    ]
    subprocess.check_call(cmd)
    print(PDF, os.path.getsize(PDF))


if __name__ == "__main__":
    main()
