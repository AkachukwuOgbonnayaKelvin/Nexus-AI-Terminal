#!/usr/bin/env python3
"""Continuous runner for Macroeconomic Statistics Engine."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import asyncio
import logging
from datetime import datetime, timedelta

from economic_events_engine.acquisition import EconomicCollector
from economic_events_engine.providers.tier2_secondary.fred import (
    FredAdapter,
    FredConnector,
)
from economic_events_engine.warehouse import EconomicWarehouse
from ndip.utils.db_connector import close_pool
from providers.provider_manager import ProviderManager

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# FRED series to track
FRED_SERIES = [
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


async def main_loop():
    logger.info("Starting Macroeconomic Statistics Engine (Continuous)")

    pm = ProviderManager()
    fred = FredConnector()
    adapter = FredAdapter()
    pm.register_provider("fred", fred, adapter, capabilities=["economic"])
    collector = EconomicCollector(pm)
    warehouse = EconomicWarehouse()

    while True:
        logger.info(f"Starting collection cycle for {len(FRED_SERIES)} series")
        for series_id in FRED_SERIES:
            try:
                event = collector.collect_event(series_id)
                if event:
                    stored = await warehouse.store_event(event)
                    if stored:
                        logger.info(
                            f"Updated {series_id}: {event.actual} ({event.release_time_utc.date()})"
                        )
                    else:
                        logger.warning(f"Failed to store {series_id}")
                else:
                    logger.warning(f"No data for {series_id}")
            except Exception as e:
                logger.error(f"Error fetching {series_id}: {e}")
        # Sleep until next day at 02:00 UTC
        next_run = datetime.now().replace(
            hour=2, minute=0, second=0, microsecond=0
        ) + timedelta(days=1)
        if next_run < datetime.now():
            next_run += timedelta(days=1)
        sleep_seconds = (next_run - datetime.now()).total_seconds()
        logger.info(f"Next run at {next_run} (sleep {sleep_seconds:.0f}s)")
        await asyncio.sleep(sleep_seconds)


if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
    finally:
        asyncio.run(close_pool())
        logger.info("Engine stopped")
