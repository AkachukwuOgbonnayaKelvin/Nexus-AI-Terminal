#!/usr/bin/env python3
"""Test COT discovery and download pipeline."""

import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from institutional_positioning_engine.discovery.catalog import ReportCatalog
from institutional_positioning_engine.discovery.crawler import CFTCWebCrawler
from institutional_positioning_engine.downloader import ReportDownloader


def main():
    print("=" * 60)
    print("INS-001 CFTC DISCOVERY & CATALOG")
    print("=" * 60)

    # Step 1: Crawl CFTC website
    print("\n[1] Crawling CFTC website...")
    crawler = CFTCWebCrawler()
    reports = crawler.discover_reports()
    print(f"  Found {len(reports)} reports")

    # Step 2: Save to catalog
    print("\n[2] Updating catalog...")
    catalog = ReportCatalog()
    catalog.add_reports(reports)
    counts = catalog.get_counts()
    print(f"  Catalog: {counts['total']} total reports")
    print(f"  Pending download: {counts['pending_download']}")
    print(f"  Downloaded: {counts['downloaded']}")

    # Step 3: Download pending reports (limit 5 for testing)
    print("\n[3] Downloading pending reports (limit 5)...")
    downloader = ReportDownloader()
    result = downloader.download_pending(limit=5)
    print(f"  Downloaded: {result['success']}")
    print(f"  Failed: {result['failed']}")

    # Step 4: Show updated catalog
    print("\n[4] Updated catalog:")
    counts = catalog.get_counts()
    print(f"  Downloaded: {counts['downloaded']}")
    print(f"  Parsed: {counts['parsed']}")

    print("\n✅ Test complete.")


if __name__ == "__main__":
    main()
