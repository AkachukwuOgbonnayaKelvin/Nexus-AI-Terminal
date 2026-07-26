"""Base provider interface for market data sources"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class OHLCVData:
    """Standardized OHLCV data structure"""

    symbol: str
    timeframe: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float | None = None
    source: str = "unknown"
    quality_score: float = 100.0


class MarketDataProvider(ABC):
    """Base class for all market data providers"""

    @abstractmethod
    def get_historical_bars(
        self, symbol: str, timeframe: str, start_date: datetime, end_date: datetime
    ) -> list[OHLCVData]:
        """Get historical OHLCV data for a symbol"""

    @abstractmethod
    def get_current_quote(self, symbol: str) -> dict[str, Any] | None:
        """Get current bid/ask for a symbol"""

    @abstractmethod
    def get_available_symbols(self) -> list[str]:
        """Get all available symbols from this provider"""

    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the provider's name"""

    @abstractmethod
    def get_health(self) -> dict[str, Any]:
        """Get provider health status"""

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is currently available"""
