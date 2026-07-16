#!/usr/bin/env python3
"""Test Economic Events Engine with FRED provider."""

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
    print("TESTING ECONOMIC EVENTS ENGINE")
    print("=" * 60)

    # 1. Create and register provider
    pm = ProviderManager()
    fred = FredConnector()
    adapter = FredAdapter()
    pm.register_provider("fred", fred, adapter, capabilities=["economic"])

    # 2. Create collector
    collector = EconomicCollector(pm)

    # 3. Fetch a known series (GDP)
    print("\nFetching GDP...")
    try:
        event = collector.collect_event("GDP")
        print(f"  Event: {event.title} ({event.category})")
        print(f"  Actual: {event.actual}")
        print(f"  Release: {event.release_time_utc}")
    except Exception as e:
        print(f"  Failed: {e}")

    # 4. Fetch CPI
    print("\nFetching CPI...")
    try:
        event = collector.collect_event("CPIAUCSL")
        print(f"  Event: {event.title} ({event.category})")
        print(f"  Actual: {event.actual}")
        print(f"  Release: {event.release_time_utc}")
    except Exception as e:
        print(f"  Failed: {e}")

    # 5. Store in warehouse
    warehouse = EconomicWarehouse()
    # We'll store the GDP event we fetched
    # (We need to fetch it again as a UniversalEconomicEvent)
    event = collector.collect_event("GDP")
    stored = await warehouse.store_event(event)
    print(f"\nStored GDP event: {stored}")

    # 6. Query today's events (should include GDP if release date is today, but likely not)
    print("\nToday's events:")
    today_events = await warehouse.get_today_events()
    print(f"  Count: {len(today_events)}")
    for ev in today_events[:3]:
        print(f"    {ev['title']} ({ev['category']}) - {ev['release_time_utc']}")

    await close_pool()
    print("\n✅ Test complete.")


if __name__ == "__main__":
    asyncio.run(main())
