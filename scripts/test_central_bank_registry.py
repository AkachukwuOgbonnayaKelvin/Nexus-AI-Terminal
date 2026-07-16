#!/usr/bin/env python3
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from central_bank_engine.collectors import RateCollector
from central_bank_engine.registry import get_all_banks


class DummyRateCollector(RateCollector):
    async def collect(self):
        return [{"event_id": "dummy", "title": "Dummy event"}]


async def main():
    print("Central Bank Registry:")
    for bank in get_all_banks():
        print(f"  {bank.id}: {bank.name} ({bank.currency})")

    print("\nTesting dummy collector:")
    collector = DummyRateCollector("federal_reserve")
    events = await collector.collect()
    print(f"  Collected {len(events)} events")
    print("✅ Test complete.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
