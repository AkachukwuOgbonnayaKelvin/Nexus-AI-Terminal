from abc import ABC, abstractmethod
from datetime import datetime

import pandas as pd

from intelligence.technical.contracts import OHLCRequest, TickRequest, VolumeRequest


class OHLCDataProvider(ABC):
    @abstractmethod
    def get_bars(self, request: OHLCRequest) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_latest_bar(self, symbol: str, timeframe: str) -> dict:
        pass

    @abstractmethod
    def get_bar_count(self, symbol: str, timeframe: str) -> int:
        pass


class MicrostructureDataProvider(ABC):
    @abstractmethod
    def get_ticks(self, request: TickRequest) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_volume_bars(self, request: VolumeRequest) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_latest_tick(self, symbol: str) -> dict:
        pass


class TechnicalDataPlatform:
    def __init__(
        self,
        ohlc_provider: OHLCDataProvider,
        micro_provider: MicrostructureDataProvider,
    ):
        self.ohlc = ohlc_provider
        self.microstructure = micro_provider

    def get_bars(
        self, symbol: str, timeframe: str, start: datetime, end: datetime
    ) -> pd.DataFrame:
        request = OHLCRequest(symbol=symbol, timeframe=timeframe, start=start, end=end)
        return self.ohlc.get_bars(request)

    def get_ticks(self, symbol: str, start: datetime, end: datetime) -> pd.DataFrame:
        request = TickRequest(symbol=symbol, start=start, end=end)
        return self.microstructure.get_ticks(request)

    def get_last_bars(self, symbol: str, timeframe: str, limit: int) -> pd.DataFrame:
        """Convenience method to get the most recent N bars."""
        return self.ohlc.get_last_bars(symbol, timeframe, limit)

    def get_last_bars(self, symbol: str, timeframe: str, limit: int) -> pd.DataFrame:
        """Convenience method to get the most recent N bars."""
        return self.ohlc.get_last_bars(symbol, timeframe, limit)
