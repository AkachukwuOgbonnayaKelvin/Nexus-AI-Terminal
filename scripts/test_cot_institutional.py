#!/usr/bin/env python3
"""Test full institutional COT pipeline."""

import asyncio
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from institutional_positioning_engine.discovery import ReportDiscovery
from institutional_positioning_engine.downloader import ReportDownloader
from institutional_positioning_engine.historical import HistoricalBackfill
from institutional_positioning_engine.parser import COTParser
from institutional_positioning_engine.runtime import COTScheduler


async def main():
    print("=" * 60)
    print("INS-001 INSTITUTIONAL POSITIONING DATA PLATFORM")
    print("=" * 60)

    # Test discovery
    print("\n[1] Testing Report Discovery...")
    discovery = ReportDiscovery()
    reports = discovery.discover_all()
    print(f"  Found {len(reports)} reports")

    # Test parser with stub data
    print("\n[2] Testing Parser...")
    parser = COTParser()
    # Create a sample record manually for testing
    sample_record = {
        "market_code": "EUR",
        "market_name": "Euro FX",
        "report_date": "2026-07-16",
        "open_interest": 100000,
        "dealer_long": 20000,
        "dealer_short": 15000,
    }
    parser._discover_market(sample_record)
    markets = parser.get_discovered_markets()
    print(f"  Markets discovered: {len(markets)}")
    for code, info in markets.items():
        print(f"    - {code}: {info.get('market_name')} ({info.get('asset_class')})")

    # Test scheduler
    print("\n[3] Testing Runtime Scheduler...")
    scheduler = COTScheduler()
    result = await scheduler.run_weekly()
    print(f"  Scheduler result: {result}")

    print("\n✅ Test complete.")


if __name__ == "__main__":
    asyncio.run(main())
