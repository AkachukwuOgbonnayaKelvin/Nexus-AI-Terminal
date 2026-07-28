#!/usr/bin/env python
"""
Production‑grade test pipeline with health checks and secure configuration.
"""

import logging
import os
import sys
from datetime import UTC, datetime

from dotenv import load_dotenv

load_dotenv()

# All imports at the top
from intelligence.technical.data_access import TechnicalDataPlatform
from intelligence.technical.data_health import DataHealthChecker, DataSourceStatus
from intelligence.technical.engines.liquidity.adapters.platform_adapter import (
    TechnicalPlatformAdapter,
)
from intelligence.technical.engines.liquidity.engine import LiquidityEngine
from intelligence.technical.engines.liquidity.enums import Timeframe
from intelligence.technical.market_profile.config import MarketProfileConfig
from intelligence.technical.market_profile.engine import MarketProfileEngine
from intelligence.technical.market_profile.tosp.hub import TOSPHub
from intelligence.technical.stores.ohlc.repository import PostgresOHLCRepository

# Setup logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    logger.critical("DATABASE_URL not set in environment.")
    sys.exit(1)


def main():
    logger.info("=== Full Pipeline with Health Check ===")
    logger.info(f"Start time: {datetime.now(UTC).isoformat()}")

    # --- Health Check ---
    logger.info("Checking database health...")
    health = DataHealthChecker(DB_URL).check()
    if health.status != DataSourceStatus.HEALTHY:
        logger.critical(f"Data source unhealthy: {health.message}")
        sys.exit(1)
    else:
        logger.info(f"Database healthy (latency: {health.latency_ms:.1f} ms)")

    # --- Create repository and platform ---
    ohlc_repo = PostgresOHLCRepository(connection_string=DB_URL)
    data_platform = TechnicalDataPlatform(ohlc_provider=ohlc_repo, micro_provider=None)

    # --- Manual Data Fetch Test ---
    logger.info("--- Manual Data Fetch Test ---")
    test_symbol = "EURUSD"
    test_tf = "H1"
    try:
        df = data_platform.get_last_bars(test_symbol, test_tf, 100)
        logger.info(f"Fetched {len(df)} bars for {test_symbol} {test_tf}")
        if len(df) > 0:
            logger.debug(f"First 5 rows:\n{df.head()}")
        else:
            logger.warning(f"No data for {test_symbol} {test_tf}")
    except Exception as e:
        logger.error(f"Data fetch failed: {e}")

    # --- Define Symbols ---
    all_symbols = [
        "EURUSD",
        "GBPUSD",
        "USDJPY",
        "AUDUSD",
        "USDCAD",
        "USDCHF",
        "NZDUSD",
        "EURGBP",
        "EURJPY",
        "EURCHF",
        "EURNZD",
        "EURCAD",
        "GBPAUD",
        "GBPJPY",
        "GBPCAD",
        "GBPCHF",
        "GBPNZD",
        "AUDCAD",
        "AUDJPY",
        "AUDNZD",
        "CADJPY",
        "CADCHF",
        "CHFJPY",
        "NZDCAD",
        "NZDJPY",
        "XAUUSD",
        "XAGUSD",
        "US500",
        "GER40",
        "UK100",
        "BTCUSD",
    ]

    # --- Create Config with Relaxed Staleness ---
    config = MarketProfileConfig()
    # Allow data up to 30 days old (since warehouse hasn't updated recently)
    config.data_quality.max_stale_hours = {"H1": 720.0, "H4": 720.0, "default": 720.0}
    config.data_quality.min_bars = 20
    config.lookback_bars = 100

    # --- Instantiate TOSP Hub ---
    tosp_hub = TOSPHub(redis_client=None, db_connection=None)

    # --- Instantiate Market Profile Engine ---
    logger.info("Initializing Market Profile Engine...")
    profile_engine = MarketProfileEngine(
        data_platform=data_platform,
        symbols=all_symbols,
        config=config,
        tosp_hub=tosp_hub,
    )

    # --- Run the Engine ---
    logger.info("Running Market Profile Engine on H1 and H4...")
    result = profile_engine.run(timeframes=["H1", "H4"])

    logger.info(f"System status: {result.system_status}")
    logger.info(
        f"Scanned {result.total_assets_scanned} assets, "
        f"data quality passed: {result.data_quality_passed}, "
        f"candidates: {len(result.candidates)}"
    )

    if result.system_status == "failed":
        logger.critical("Market Profile Engine failed due to data access error.")
        if result.config.get("error"):
            logger.critical(f"Error: {result.config['error']}")
        sys.exit(1)

    logger.info("Top Candidates:")
    for c in result.candidates[:5]:
        logger.info(f"  {c.symbol} (score: {c.opportunity_score:.1f}, rank: {c.rank})")

    # --- Liquidity Engine on Candidates ---
    candidate_symbols = tosp_hub.get_latest_candidate_symbols()
    logger.info(f"Liquidity Engine will analyse: {candidate_symbols}")

    if not candidate_symbols:
        logger.warning("No candidates, skipping liquidity analysis.")
        return

    # Liquidity Engine components
    liquidity_engine = LiquidityEngine()
    # We don't need a hub for this simple test
    liquidity_adapter = TechnicalPlatformAdapter(data_platform)

    for symbol in candidate_symbols[:2]:
        for tf in [Timeframe.H1, Timeframe.H4]:
            try:
                bundle = liquidity_adapter.create_data_bundle(
                    symbol, tf, lookback_days=90
                )
                if bundle.ohlc_data_quality.value != "insufficient":
                    analysis = liquidity_engine.analyze(bundle)
                    logger.info(
                        f"Liquidity analysis OK for {symbol} {tf.value}: "
                        f"state={analysis.liquidity_state}, "
                        f"target={analysis.primary_target.midpoint if analysis.primary_target else 'None'}"
                    )
                else:
                    logger.warning(f"Insufficient data for {symbol} {tf.value}")
            except Exception as e:
                logger.error(f"Liquidity analysis failed for {symbol} {tf.value}: {e}")

    logger.info("Test completed.")


if __name__ == "__main__":
    main()
