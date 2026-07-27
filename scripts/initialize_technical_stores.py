import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging

from intelligence.technical.data_access import TechnicalDataPlatform
from intelligence.technical.stores.microstructure.repository import (
    PostgresMicrostructureRepository,
)
from intelligence.technical.stores.microstructure.writer import MicrostructureWriter
from intelligence.technical.stores.ohlc.repository import PostgresOHLCRepository
from intelligence.technical.stores.ohlc.writer import OHLCWriter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_CONN = "postgresql://user:pass@localhost:5432/nexus_ai_terminal"
SYMBOLS = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "XAUUSD", "US500"]
TIMEFRAMES = ["1H", "4H", "1D"]


def main():
    logger.info("Initializing Technical Intelligence Data Stores...")
    ohlc_repo = PostgresOHLCRepository(DB_CONN)
    micro_repo = PostgresMicrostructureRepository(DB_CONN)
    OHLCWriter(DB_CONN)
    MicrostructureWriter(DB_CONN)
    TechnicalDataPlatform(ohlc_repo, micro_repo)
    logger.info("Verifying data availability...")
    for symbol in SYMBOLS:
        for tf in TIMEFRAMES:
            count = ohlc_repo.get_bar_count(symbol, tf)
            logger.info(f"  {symbol} {tf}: {count} bars")
    logger.info("Initialization complete.")


if __name__ == "__main__":
    main()
