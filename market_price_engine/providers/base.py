# -*- coding: utf-8 -*-
"""Base provider interface for market data sources"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass


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
    volume: Optional[float] = None
    source: str = "unknown"
    quality_score: float = 100.0


class MarketDataProvider(ABC):
    """Base class for all market data providers"""

    @abstractmethod
    def get_historical_bars(
        self, symbol: str, timeframe: str, start_date: datetime, end_date: datetime
    ) -> List[OHLCVData]:
        """Get historical OHLCV data for a symbol"""
        pass

    @abstractmethod
    def get_current_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get current bid/ask for a symbol"""
        pass

    @abstractmethod
    def get_available_symbols(self) -> List[str]:
        """Get all available symbols from this provider"""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the provider's name"""
        pass

    @abstractmethod
    def get_health(self) -> Dict[str, Any]:
        """Get provider health status"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is currently available"""
        pass
