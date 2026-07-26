#!/usr/bin/env python3
"""Test complete institutional COT pipeline."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from institutional_positioning_engine.discovery import ReportDiscovery
from institutional_positioning_engine.historical import HistoricalBackfill
from institutional_positioning_engine.parser import COTParser


async def main():
    print("=" * 60)
    print("INS-001 COMPLETE INSTITUTIONAL POSITIONING PLATFORM")
    print("=" * 60)

    # Test discovery
    print("\n[1] Testing Report Discovery...")
    discovery = ReportDiscovery()
    reports = discovery.discover_all()
    print(f"  Found {len(reports)} reports")

    # Test parser with sample file
    print("\n[2] Testing Universal Parser...")
    parser = COTParser()
    # Create a sample CSV content for testing
    sample_data = """Market and Exchange Names,Report Date,Open Interest,Dealer Long,Dealer Short,Commercial Long,Commercial Short
    Euro FX,2026-07-16,100000,20000,15000,30000,25000
    Gold,2026-07-16,50000,10000,18000,15000,8000
    S&P 500,2026-07-16,80000,12000,10000,25000,20000
    10-Year Treasury,2026-07-16,60000,8000,15000,20000,10000"""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(sample_data)
        f.flush()
        records = parser.parse_file(f.name)
    print(f"  Parsed {len(records)} records")
    markets = parser.get_discovered_markets()
    print(f"  Markets discovered: {len(markets)}")
    for code, info in markets.items():
        print(f"    - {code}: {info.get('market_name')} ({info.get('asset_class')})")

    # Test backfill (limited)
    print("\n[3] Testing Historical Backfill...")
    backfill = HistoricalBackfill()
    result = await backfill.run(limit=5)
    print(f"  Processed {result.get('reports_processed')} reports")
    print(f"  Inserted {result.get('records_inserted')} records")
    print(f"  Discovered {result.get('markets_discovered')} markets")

    print("\n✅ Test complete.")


if __name__ == "__main__":
    asyncio.run(main())
