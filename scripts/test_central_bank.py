#!/usr/bin/env python3
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio  # noqa: E402

from central_bank_engine.acquisition import CentralBankCollector  # noqa: E402
from central_bank_engine.dtos import UniversalCentralBankEvent  # noqa: E402
from central_bank_engine.normalisation import CentralBankNormalizer  # noqa: E402
from central_bank_engine.providers.tier1_primary.federal_reserve import (  # noqa: E402
    FederalReserveAdapter,
    FederalReserveConnector,
)
from central_bank_engine.warehouse import CentralBankWarehouse  # noqa: E402
from ndip.utils.db_connector import close_pool  # noqa: E402
from providers.provider_manager import ProviderManager  # noqa: E402


async def main():
    print("=" * 60)
    print("TESTING CENTRAL BANK INTELLIGENCE ENGINE (CENT-001)")
    print("=" * 60)

    pm = ProviderManager()

    fed = FederalReserveConnector()
    fed_adapter = FederalReserveAdapter()
    pm.register_provider("federal_reserve", fed, fed_adapter, capabilities=["central_bank"])

    collector = CentralBankCollector(pm)
    warehouse = CentralBankWarehouse()
    normalizer = CentralBankNormalizer()

    print("\nCollecting central bank events...")
    events = await collector.collect_today()

    print(f"Collected {len(events)} events")
    stored = 0
    for event in events:
        event_dict = event.to_dict()
        normalized = normalizer.normalize(event_dict)
        result = await warehouse.store(UniversalCentralBankEvent(**normalized))
        if result:
            stored += 1
            print(f"  ✅ {event.bank} - {event.event_type} - {event.title}")

    print(f"\nStored {stored} events")

    print("\nLatest Fed rate:")
    rate = await warehouse.get_latest_rate("Federal Reserve")
    if rate:
        print(f"  {rate['bank']}: {rate['new_rate']} (as of {rate['release_time']})")

    await close_pool()
    print("\n✅ Test complete.")


if __name__ == "__main__":
    asyncio.run(main())
