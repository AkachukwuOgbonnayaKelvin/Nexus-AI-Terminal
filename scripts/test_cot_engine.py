#!/usr/bin/env python3
"""Test COT Engine (INS-001)."""

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
    print("TESTING COT ENGINE (INS-001)")
    print("=" * 60)

    pm = ProviderManager()
    cftc = CFTCConnector()
    cftc_adapter = CFTCAdapter()
    pm.register_provider(
        "cftc", cftc, cftc_adapter, capabilities=["institutional_positioning"]
    )

    collector = COTCollector(pm)
    warehouse = COTWarehouse()

    print("\nCollecting COT data...")
    records = await collector.collect_latest()

    print(f"Collected {len(records)} records")
    stored = 0
    for record in records:
        result = await warehouse.store(record)
        if result:
            stored += 1
            print(
                f"  ✅ {record.market_code} - {record.market_name} - OI: {record.open_interest}"
            )

    print(f"\nStored {stored} records")

    print("\nLatest reports:")
    reports = await warehouse.get_latest_reports(limit=5)
    for r in reports:
        print(f"  {r['report_date']} - {r['market_name']} - OI: {r['open_interest']}")

    await close_pool()
    print("\n✅ Test complete.")


if __name__ == "__main__":
    asyncio.run(main())
