"""MT5 data acquisition module for MKT-001"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from domain.models import OHLCV, Tick
from providers.mt5.client import MT5Client


class MT5Acquirer:
    """Acquires market data from MT5 terminal"""

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize MT5 client"""
        if self.client is None:
            self.client = MT5Client(self.config)
            self.client.connect()

    def acquire_tick(self, symbol: str) -> Tick | None:
        """Acquire current tick data"""
        if not self.client or not self.client.is_connected():
            return None

        tick_data = self.client.get_tick(symbol)
        if tick_data:
            return Tick(
                timestamp=datetime.fromtimestamp(tick_data["time"]),
                symbol=symbol,
                bid=tick_data["bid"],
                ask=tick_data["ask"],
                volume=tick_data.get("volume"),
                source="pepperstone_mt5",
                provenance={"provider": "Pepperstone", "terminal": "MT5"},
            )
        return None

    def acquire_ohlcv(
        self, symbol: str, timeframe: str, count: int = 100
    ) -> list[OHLCV]:
        """Acquire OHLCV data"""
        if not self.client or not self.client.is_connected():
            return []

        timeframe_map = {
            "M1": 1,
            "M5": 5,
            "M15": 15,
            "M30": 30,
            "H1": 60,
            "H4": 240,
            "D1": 1440,
            "W1": 10080,
            "MN1": 43200,
        }

        mt5_timeframe = timeframe_map.get(timeframe, 1)
        rates = self.client.get_rates(symbol, mt5_timeframe, count)

        if rates:
            return [
                OHLCV(
                    timestamp=datetime.fromtimestamp(r["time"]),
                    symbol=symbol,
                    timeframe=timeframe,
                    open=r["open"],
                    high=r["high"],
                    low=r["low"],
                    close=r["close"],
                    tick_volume=r["tick_volume"],
                    spread=r["spread"],
                    source="pepperstone_mt5",
                    provenance={"provider": "Pepperstone", "terminal": "MT5"},
                )
                for r in rates
            ]
        return []
