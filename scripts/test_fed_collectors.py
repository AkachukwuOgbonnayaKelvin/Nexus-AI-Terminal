#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio

from central_bank_engine.collectors.federal_reserve import (
    FedCalendarCollector,
    FedMinutesCollector,
    FedRateCollector,
    FedSpeechCollector,
    FedStatementCollector,
)
from central_bank_engine.provider_manager import ProviderManager


async def main():
    print("=" * 60)
    print("TESTING FEDERAL RESERVE COLLECTORS")
    print("=" * 60)

    pm = ProviderManager()

    # Register collectors
    pm.register_collector(FedRateCollector())
    pm.register_collector(FedSpeechCollector())
    pm.register_collector(FedMinutesCollector())
    pm.register_collector(FedStatementCollector())
    pm.register_collector(FedCalendarCollector())

    print("\nCollectors registered.")
    for c in pm.collectors:
        print(f"  - {c.name}")

    # Run all collectors
    print("\nRunning all collectors...")
    events = await pm.run_all_collectors()

    print(f"\nTotal events collected: {len(events)}")
    for ev in events:
        print(f"  {ev.get('event_type')}: {ev.get('title')}")

    print("\nCollector statuses:")
    for name, status in pm.get_collector_statuses().items():
        print(
            f"  {name}: success={status['success_count']}, errors={status['error_count']}"
        )

    print("\n✅ Test complete.")


if __name__ == "__main__":
    asyncio.run(main())
