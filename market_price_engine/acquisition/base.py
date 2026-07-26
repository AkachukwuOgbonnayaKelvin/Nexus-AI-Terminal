"""Base acquisition module"""

from abc import ABC, abstractmethod
from typing import Any

from domain.models import OHLCV, Tick


class BaseAcquirer(ABC):
    """Base class for data acquisition"""

    @abstractmethod
    def acquire_tick(self, symbol: str) -> Tick | None:
        """Acquire current tick data"""

    @abstractmethod
    def acquire_ohlcv(self, symbol: str, timeframe: str, count: int) -> list[OHLCV]:
        """Acquire OHLCV data"""

    @abstractmethod
    def acquire_symbols(self) -> list[str]:
        """Acquire list of available symbols"""

    @abstractmethod
    def get_health(self) -> dict[str, Any]:
        """Get acquirer health status"""
