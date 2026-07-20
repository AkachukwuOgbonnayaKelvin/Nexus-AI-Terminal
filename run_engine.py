#!/usr/bin/env python3
"""Continuous runner for Market Price Engine."""

import asyncio
import logging
import sys

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config.symbols import ALL_SYMBOLS
from ndip.engines.market_price import MarketPriceEngine
from ndip.utils.db_connector import close_pool
from providers.provider_manager import ProviderManager
from providers.tier1_primary.mt5 import MT5Adapter, MT5Connector
from providers.tier1_primary.polygon import PolygonAdapter, PolygonConnector
from providers.tier2_secondary.alpha_vantage import (
    AlphaVantageAdapter,
    AlphaVantageConnector,
)
from providers.tier2_secondary.yahoo import YahooAdapter, YahooConnector
from providers.tier3_specialized.binance import BinanceAdapter, BinanceConnector

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


async def main_loop():
    logger.info("Starting Market Price Engine (Continuous)")

    pm = ProviderManager()

    # Register providers in priority order
    # MT5 (Tier 1)
    try:
        mt5 = MT5Connector()
        mt5_adapter = MT5Adapter()
        pm.register_provider("mt5", mt5, mt5_adapter)
        logger.info("MT5 provider registered")
    except Exception as e:
        logger.warning(f"MT5 registration failed: {e}")

    # Polygon (Tier 1)
    try:
        polygon = PolygonConnector()
        polygon_adapter = PolygonAdapter()
        pm.register_provider("polygon", polygon, polygon_adapter)
        logger.info("Polygon provider registered")
    except Exception as e:
        logger.warning(f"Polygon registration failed: {e}")

    # Yahoo (Tier 2)
    try:
        yahoo = YahooConnector()
        yahoo_adapter = YahooAdapter()
        pm.register_provider("yahoo", yahoo, yahoo_adapter)
        logger.info("Yahoo provider registered")
    except Exception as e:
        logger.warning(f"Yahoo registration failed: {e}")

    # Alpha Vantage (Tier 2)
    try:
        av = AlphaVantageConnector()
        av_adapter = AlphaVantageAdapter()
        pm.register_provider("alpha_vantage", av, av_adapter)
        logger.info("Alpha Vantage provider registered")
    except Exception as e:
        logger.warning(f"Alpha Vantage registration failed: {e}")

    # Binance (Tier 3)
    try:
        binance = BinanceConnector()
        binance_adapter = BinanceAdapter()
        pm.register_provider("binance", binance, binance_adapter)
        logger.info("Binance provider registered")
    except Exception as e:
        logger.warning(f"Binance registration failed: {e}")

    # Create engine
    engine = MarketPriceEngine(pm)
    engine.set_symbols(ALL_SYMBOLS)
    engine.set_interval(60)  # every minute

    # Run engine
    try:
        await engine.start()
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
    finally:
        engine.stop()
        await close_pool()
        logger.info("Engine stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        logger.info("Exited by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
