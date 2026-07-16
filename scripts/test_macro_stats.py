#!/usr/bin/env python3
"""Test Macroeconomic Statistics Engine with multiple FRED series."""

import asyncio
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from economic_events_engine.acquisition import EconomicCollector
from economic_events_engine.providers.tier2_secondary.fred import FredAdapter, FredConnector
from economic_events_engine.warehouse import EconomicWarehouse
from ndip.utils.db_connector import close_pool
from providers.provider_manager import ProviderManager


async def main():
    print("=" * 60)
    print("TESTING MACROECONOMIC STATISTICS ENGINE (FRED)")
    print("=" * 60)

    pm = ProviderManager()
    fred = FredConnector()
    adapter = FredAdapter()
    pm.register_provider("fred", fred, adapter, capabilities=["economic"])

    collector = EconomicCollector(pm)
    warehouse = EconomicWarehouse()

    # List of FRED series to fetch
    series_list = [
        "GDP",
        "CPIAUCSL",
        "UNRATE",
        "FEDFUNDS",
        "PAYEMS",
        "DGS10",
        "PPIACO",
        "PCEPI",
        "M2SL",
        "RSXFS",
    ]

    print(f"\nFetching {len(series_list)} series...")
    for series_id in series_list:
        try:
            event = collector.collect_event(series_id)
            if event:
                stored = await warehouse.store_event(event)
                print(f"  ✅ {series_id}: {event.actual} ({event.release_time_utc.date()}) -> stored={stored}")
            else:
                print(f"  ❌ {series_id}: No data")
        except Exception as e:
            print(f"  ❌ {series_id}: {e}")

    # Print some summary
    print("\nLatest values:")
    for series_id in series_list:
        latest = await warehouse.get_latest_value(series_id)
        if latest:
            print(f"  {series_id}: {latest['actual']} (as of {latest['release_time_utc'].date()})")

    await close_pool()
    print("\n✅ Test complete.")


if __name__ == "__main__":
    asyncio.run(main())
