import logging

import pandas as pd

from intelligence.technical.stores.microstructure.writer import MicrostructureWriter
from intelligence.technical.stores.ohlc.writer import OHLCWriter


class TechnicalDataDistributor:
    def __init__(self, ohlc_writer: OHLCWriter, micro_writer: MicrostructureWriter):
        self.ohlc = ohlc_writer
        self.micro = micro_writer
        self.logger = logging.getLogger(__name__)

    def ingest_ohlc(self, symbol: str, timeframe: str, df: pd.DataFrame):
        if df.empty:
            self.logger.warning(f"Empty OHLC data for {symbol} {timeframe}")
            return
        required = ["time", "open", "high", "low", "close"]
        for col in required:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        if "symbol" not in df.columns:
            df["symbol"] = symbol
        if "volume" not in df.columns:
            df["volume"] = 0
        self.ohlc.write_bars(df, timeframe)
        self.logger.info(f"Ingested {len(df)} bars for {symbol} {timeframe}")

    def ingest_ticks(self, symbol: str, df: pd.DataFrame):
        if df.empty:
            self.logger.warning(f"Empty tick data for {symbol}")
            return
        required = ["time", "price"]
        for col in required:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        if "symbol" not in df.columns:
            df["symbol"] = symbol
        if "volume" not in df.columns:
            df["volume"] = 0
        self.micro.write_ticks(df)
        self.logger.info(f"Ingested {len(df)} ticks for {symbol}")
