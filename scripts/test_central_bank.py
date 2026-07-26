#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio

from central_bank_engine.acquisition import CentralBankCollector
from central_bank_engine.dtos import UniversalCentralBankEvent
from central_bank_engine.normalisation import CentralBankNormalizer
from central_bank_engine.providers.tier1_primary.boc import BOCAdapter, BOCConnector
from central_bank_engine.providers.tier1_primary.boe import BOEAdapter, BOEConnector
from central_bank_engine.providers.tier1_primary.boj import BOJAdapter, BOJConnector
from central_bank_engine.providers.tier1_primary.ecb import ECBAdapter, ECBConnector

# Import all 8 central bank connectors and adapters
from central_bank_engine.providers.tier1_primary.federal_reserve import (
    FederalReserveAdapter,
    FederalReserveConnector,
)
from central_bank_engine.providers.tier1_primary.rba import RBAAdapter, RBAConnector
from central_bank_engine.providers.tier1_primary.rbnz import RBNZAdapter, RBNZConnector
from central_bank_engine.providers.tier1_primary.snb import SNBAdapter, SNBConnector
from central_bank_engine.warehouse import CentralBankWarehouse
from ndip.utils.db_connector import close_pool
from providers.provider_manager import ProviderManager


async def main():
    print("=" * 60)
    print("TESTING CENTRAL BANK INTELLIGENCE ENGINE (CENT-001)")
    print("All 8 Major Central Banks")
    print("=" * 60)

    pm = ProviderManager()

    # Register all 8 providers
    banks = [
        ("federal_reserve", FederalReserveConnector, FederalReserveAdapter),
        ("ecb", ECBConnector, ECBAdapter),
        ("boe", BOEConnector, BOEAdapter),
        ("boj", BOJConnector, BOJAdapter),
        ("snb", SNBConnector, SNBAdapter),
        ("boc", BOCConnector, BOCAdapter),
        ("rba", RBAConnector, RBAAdapter),
        ("rbnz", RBNZConnector, RBNZAdapter),
    ]

    for name, connector_cls, adapter_cls in banks:
        connector = connector_cls()
        adapter = adapter_cls()
        pm.register_provider(name, connector, adapter, capabilities=["central_bank"])

    collector = CentralBankCollector(pm)
    warehouse = CentralBankWarehouse()
    normalizer = CentralBankNormalizer()

    print("\nCollecting central bank events from all 8 providers...")
    events = await collector.collect_today()

    print(f"Collected {len(events)} events")

    bank_counts = {}
    stored = 0
    for event in events:
        bank_counts[event.bank] = bank_counts.get(event.bank, 0) + 1
        event_dict = event.to_dict()
        normalized = normalizer.normalize(event_dict)
        result = await warehouse.store(UniversalCentralBankEvent(**normalized))
        if result:
            stored += 1
            print(f"  ✅ {event.bank} - {event.event_type} - {event.title}")

    print(f"\nStored {stored} events")
    print("\nEvents per bank:")
    for bank, count in sorted(bank_counts.items()):
        print(f"  {bank}: {count}")

    # Check latest rates for each bank
    print("\nLatest rates:")
    for name, _, _ in banks:
        rate = await warehouse.get_latest_rate(name.replace("_", " ").title())
        if rate:
            print(
                f"  {rate['bank']}: {rate['new_rate']} (as of {rate['release_time']})"
            )
        else:
            print(f"  {name}: No rate data yet")

    await close_pool()
    print("\n✅ Test complete.")


if __name__ == "__main__":
    asyncio.run(main())
