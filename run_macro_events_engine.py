#!/usr/bin/env python3
"""Continuous runner for Macroeconomic Events Engine (MAC-002)."""

import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import asyncio
import logging

from macroeconomic_events_engine.acquisition import MacroCollector
from macroeconomic_events_engine.classification import MacroClassifier
from macroeconomic_events_engine.impact import ImpactScorer
from macroeconomic_events_engine.providers.tier1_primary.tradingeconomics import (
    TradingEconomicsAdapter,
    TradingEconomicsConnector,
)
from macroeconomic_events_engine.providers.tier2_secondary.forexfactory import (
    ForexFactoryAdapter,
    ForexFactoryConnector,
)
from macroeconomic_events_engine.providers.tier2_secondary.investing import InvestingAdapter, InvestingConnector
from macroeconomic_events_engine.warehouse import ConsensusWarehouse, RawWarehouse
from ndip.utils.db_connector import close_pool
from providers.provider_manager import ProviderManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def main_loop():
    logger.info("Starting Macroeconomic Events Engine (MAC-002)")

    pm = ProviderManager()

    # Register providers
    te = TradingEconomicsConnector()
    te_adapter = TradingEconomicsAdapter()
    pm.register_provider("trading_economics", te, te_adapter, capabilities=["macroeconomic_events"])

    ff = ForexFactoryConnector()
    ff_adapter = ForexFactoryAdapter()
    pm.register_provider("forexfactory", ff, ff_adapter, capabilities=["macroeconomic_events"])

    inv = InvestingConnector()
    inv_adapter = InvestingAdapter()
    pm.register_provider("investing", inv, inv_adapter, capabilities=["macroeconomic_events"])

    # Reset health for all providers to ensure they are tried
    for name in pm.get_providers(capability="macroeconomic_events"):
        pm.health.set_status(name, True)

    collector = MacroCollector(pm)
    raw_warehouse = RawWarehouse()
    consensus_warehouse = ConsensusWarehouse()
    classifier = MacroClassifier()
    scorer = ImpactScorer()

    while True:
        logger.info("Collecting macro events...")
        events = await collector.collect_today()

        if not events:
            logger.warning("No events collected. Check provider data or health.")
            for name in pm.get_providers(capability="macroeconomic_events"):
                status = pm.health.is_healthy(name)
                logger.info(f"Provider {name} health: {status}")
        else:
            for ev in events:
                ev = classifier.classify(ev)
                ev = scorer.score(ev)
                await raw_warehouse.store(ev, ev.provider)
                await consensus_warehouse.store(ev)
            logger.info(f"Processed {len(events)} events")

        await asyncio.sleep(3600)


if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        logger.info("Shutdown")
    finally:
        asyncio.run(close_pool())
