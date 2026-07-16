#!/usr/bin/env python3
"""Continuous runner for Market Metadata Engine."""

import asyncio
import logging
import sys
from datetime import datetime, timedelta

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config.symbols import ALL_SYMBOLS
from ndip.acquisition.metadata_collector import MetadataAcquisitionCollector
from ndip.utils.db_connector import close_pool
from providers.provider_manager import ProviderManager
from providers.tier2_secondary.yahoo_metadata import (
    YahooMetadataAdapter,
    YahooMetadataConnector,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main_loop():
    logger.info("Starting Metadata Engine (Continuous)")

    pm = ProviderManager()
    yahoo = YahooMetadataConnector()
    pm.register_provider("yahoo_metadata", yahoo, YahooMetadataAdapter())

    collector = MetadataAcquisitionCollector(pm)

    # Run once per day
    while True:
        datetime.now()
        logger.info(f"Starting metadata collection for {len(ALL_SYMBOLS)} symbols")
        results = await collector.collect(ALL_SYMBOLS)
        success_count = sum(1 for r in results.values() if r.get("status") == "success")
        logger.info(
            f"Collected metadata for {success_count}/{len(ALL_SYMBOLS)} symbols"
        )
        # Sleep until next day
        next_run = datetime.now().replace(
            hour=2, minute=0, second=0, microsecond=0
        ) + timedelta(days=1)
        sleep_seconds = (next_run - datetime.now()).total_seconds()
        if sleep_seconds > 0:
            logger.info(f"Next run at {next_run}")
            await asyncio.sleep(sleep_seconds)


if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
    finally:
        asyncio.run(close_pool())
        logger.info("Metadata Engine stopped")
