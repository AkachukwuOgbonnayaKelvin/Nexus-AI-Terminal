#!/usr/bin/env python3
"""Test COT Engine – Full Institutional Positioning Data Platform."""

import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio

from institutional_positioning_engine.acquisition import COTCollector
from institutional_positioning_engine.providers.cftc import CFTCAdapter, CFTCConnector
from institutional_positioning_engine.warehouse import COTWarehouse
from ndip.utils.db_connector import close_pool
from providers.provider_manager import ProviderManager


async def main():
    print("=" * 60)
    print("TESTING COT ENGINE – FULL INSTITUTIONAL POSITIONING")
    print("=" * 60)

    pm = ProviderManager()
    cftc = CFTCConnector()
    cftc_adapter = CFTCAdapter()
    pm.register_provider("cftc", cftc, cftc_adapter, capabilities=["institutional_positioning"])

    collector = COTCollector(pm)
    warehouse = COTWarehouse()

    # Discover all markets
    print("\nDiscovering markets...")
    markets = cftc.discover_markets()
    print(f"Found {len(markets)} markets")

    print("\nCollecting COT data for all markets...")
    records = await collector.collect_latest()

    print(f"Collected {len(records)} records")
    stored = 0
    for record in records:
        result = await warehouse.store(record)
        if result:
            stored += 1
            if stored <= 10:  # Show first 10
                print(f"  ✅ {record.market_code} - {record.market_name} - OI: {record.open_interest}")

    print(f"\nStored {stored} records")

    print("\nMarkets by asset class:")
    from collections import defaultdict

    class_counts = defaultdict(int)
    for m in markets:
        class_counts[m["asset_class"]] += 1
    for asset_class, count in sorted(class_counts.items()):
        print(f"  {asset_class}: {count}")

    await close_pool()
    print("\n✅ Test complete.")


if __name__ == "__main__":
    asyncio.run(main())
