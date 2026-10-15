#!/usr/bin/env python3
"""Regenerate rent-report.html, the newsletter files, and the weekly history snapshot."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_build"))

import rent_report

if __name__ == "__main__":
    raise SystemExit(rent_report.main())
