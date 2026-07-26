#!/usr/bin/env python3
"""Test COT data loading from real sources."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from market_positioning_warehouse.parser import ParserFactory
from market_positioning_warehouse.providers.cftc.historical_loader import (
    HistoricalLoader,
)
from market_positioning_warehouse.providers.cftc.weekly_loader import WeeklyLoader
from market_positioning_warehouse.warehouse import Repository


async def main():
    print("=" * 60)
    print("TESTING COT DATA LOADING")
    print("=" * 60)

    # Test Weekly Loader
    print("\n[1] Testing Weekly Loader...")
    weekly = WeeklyLoader()
    data = weekly.load_current_week()
    print(f"  Loaded {len(data)} records")
    if data:
        print(f"  Sample: {data[0]}")

    # Test Historical Loader
    print("\n[2] Testing Historical Loader...")
    historical = HistoricalLoader()
    data = historical.load_year(2026)
    print(f"  Loaded {len(data)} records for 2026")
    if data:
        print(f"  Sample: {data[0]}")

    # Test Parser
    print("\n[3] Testing Parser...")
    parser = ParserFactory()
    positions = parser.parse(data)
    print(f"  Parsed {len(positions)} positions")

    # Test Warehouse
    print("\n[4] Testing Warehouse...")
    repo = Repository()
    for pos in positions[:5]:
        stored = await repo.store(pos)
        print(f"  Stored: {pos.market_name} - {stored}")

    print(f"\n  Total records in warehouse: {await repo.get_count()}")

    print("\n✅ Data loading test complete.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
