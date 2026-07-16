#!/usr/bin/env python3
"""Test Macroeconomic Events Engine (MAC-002) with multiple providers."""

import asyncio
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from macroeconomic_events_engine.acquisition import MacroCollector
from macroeconomic_events_engine.classification import MacroClassifier
from macroeconomic_events_engine.consensus import ConsensusResolver
from macroeconomic_events_engine.impact import ImpactScorer
from macroeconomic_events_engine.providers.tier1_primary.tradingeconomics import (
    TradingEconomicsAdapter,
    TradingEconomicsConnector,
)
from macroeconomic_events_engine.providers.tier2_secondary.forexfactory import (
    ForexFactoryAdapter,
    ForexFactoryConnector,
)
from macroeconomic_events_engine.providers.tier2_secondary.investing import (
    InvestingAdapter,
    InvestingConnector,
)
from macroeconomic_events_engine.warehouse import ConsensusWarehouse, RawWarehouse
from ndip.utils.db_connector import close_pool
from providers.provider_manager import ProviderManager


async def main():
    print("=" * 60)
    print("TESTING MACROECONOMIC EVENTS ENGINE (MAC-002)")
    print("=" * 60)

    pm = ProviderManager()

    # Register providers
    te = TradingEconomicsConnector()
    te_adapter = TradingEconomicsAdapter()
    pm.register_provider(
        "trading_economics", te, te_adapter, capabilities=["macroeconomic_events"]
    )

    ff = ForexFactoryConnector()
    ff_adapter = ForexFactoryAdapter()
    pm.register_provider(
        "forexfactory", ff, ff_adapter, capabilities=["macroeconomic_events"]
    )

    inv = InvestingConnector()
    inv_adapter = InvestingAdapter()
    pm.register_provider(
        "investing", inv, inv_adapter, capabilities=["macroeconomic_events"]
    )

    collector = MacroCollector(pm)
    raw_warehouse = RawWarehouse()
    consensus_warehouse = ConsensusWarehouse()
    classifier = MacroClassifier()
    resolver = ConsensusResolver()
    scorer = ImpactScorer()

    print("\nCollecting today's events from all providers...")
    events = await collector.collect_today()

    # Group events by their base title for consensus
    grouped = {}
    for ev in events:
        key = ev.title.split("(")[0].strip()
        grouped.setdefault(key, []).append(ev)

    for key, evs in grouped.items():
        # Classify and score each event
        for ev in evs:
            ev = classifier.classify(ev)
            ev = scorer.score(ev)
            await raw_warehouse.store(ev, ev.provider)
        # Resolve consensus if multiple providers
        if len(evs) > 1:
            consensus_event = resolver.resolve(evs)
            if consensus_event:
                await consensus_warehouse.store(consensus_event)
                print(
                    f"  Consensus for {key}: forecast={consensus_event.consensus} (conf: {consensus_event.confidence:.2f})"
                )
        else:
            await consensus_warehouse.store(evs[0])
            print(f"  {key}: forecast={evs[0].forecast} (from {evs[0].provider})")

    print("\nLatest high-impact events:")
    high = await consensus_warehouse.get_high_impact()
    for h in high:
        print(f"  {h['title']} - {h['importance']} - {h['release_time_utc']}")

    await close_pool()
    print("\n✅ Test complete.")


if __name__ == "__main__":
    asyncio.run(main())
