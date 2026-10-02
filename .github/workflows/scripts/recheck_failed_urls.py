#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Re-verify the URLs lychee reported as failures, using a browser-impersonating
HEAD request (curl_cffi).

Some sites block plain HTTP clients from CI IPs (for example a WAF that gates on
TLS fingerprint), so lychee reports them as errors even though the page exists.
This re-checks only lychee's failures with a Chrome-impersonating client: if the
page returns HTTP 200 it was a false positive and is rescued; otherwise it stays
a failure. This keeps real dead links (404) failing without maintaining a
per-domain ignore list.
"""

import json
import re
import sys
import time
from pathlib import Path

URL_RE = re.compile(r"https?://[^\s\"'<>)\]]+")


def failed_urls(report_path):
    """Extract the set of failing URLs from a lychee --format=json report."""
    data = json.loads(Path(report_path).read_text(encoding="utf-8"))
    urls = set()
    for key in ("error_map", "fail_map"):
        for entries in (data.get(key) or {}).values():
            for entry in entries:
                if isinstance(entry, dict):
                    url = entry.get("url") or entry.get("uri")
                    if url:
                        urls.add(url)
                elif isinstance(entry, str):
                    urls.update(URL_RE.findall(entry))
    return sorted(urls)


def confirm_exists(url, retries=4, wait_seconds=3):
    """Return (ok, detail): ok is True only when a HEAD returns HTTP 200."""
    from curl_cffi import requests

    detail = None
    for attempt in range(retries):
        try:
            response = requests.head(url, impersonate="chrome", timeout=30, allow_redirects=True)
            if response.status_code == 200:
                return True, 200
            detail = response.status_code
            if response.status_code == 404:
                return False, 404
        except Exception as error:  # noqa: BLE001 - report any client/network error
            detail = type(error).__name__
        if attempt < retries - 1:
            time.sleep(wait_seconds)
    return False, detail


def main():
    if len(sys.argv) != 2:
        print("usage: recheck_failed_urls.py <lychee-report.json>")
        return 2

    urls = failed_urls(sys.argv[1])
    if not urls:
        print("lychee reported no failing URLs.")
        return 0

    print(f"Re-checking {len(urls)} lychee failure(s) with browser impersonation:\n")
    still_failing = []
    for url in urls:
        ok, detail = confirm_exists(url)
        print(f"[{'rescued' if ok else 'FAILED '}] {detail}  {url}")
        if not ok:
            still_failing.append((url, detail))

    if still_failing:
        print(f"\nERROR: {len(still_failing)} URL(s) could not be verified:")
        for url, detail in still_failing:
            print(f"  {detail}  {url}")
        return 1

    print(f"\nAll {len(urls)} lychee failure(s) were false positives (confirmed 200).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
