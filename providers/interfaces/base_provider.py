"""Abstract base class for all providers."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional


class ProviderStatus(Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    DEGRADED = "DEGRADED"
    INITIALIZING = "INITIALIZING"
    FAILED = "FAILED"
    MAINTENANCE = "MAINTENANCE"


class BaseProvider(ABC):
    """Abstract base class for all providers."""

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the external source."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close connection."""
        pass

    @abstractmethod
    def get_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch raw price data for a symbol."""
        pass

    @abstractmethod
    def get_multiple(self, symbols: List[str]) -> List[Dict[str, Any]]:
        """Fetch raw price data for multiple symbols."""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check if provider is healthy."""
        pass

    def get_status(self) -> ProviderStatus:
        """Return current provider status."""
        if self.health_check():
            return ProviderStatus.ONLINE
        return ProviderStatus.OFFLINE

    @abstractmethod
    def get_capabilities(self) -> Dict[str, bool]:
        """Return capabilities (realtime, historical, websocket, etc.)."""
        pass

    @abstractmethod
    def get_rate_limit(self) -> Dict[str, int]:
        """Return rate limit info (requests per second/minute)."""
        pass

    def supports_symbol(self, symbol: str) -> bool:
        """Check if provider supports a symbol."""
        return symbol in self.get_available_symbols()

    @abstractmethod
    def get_available_symbols(self) -> List[str]:
        """Return list of available symbols."""
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def tier(self) -> int:
        return getattr(self, "_tier", 2)

    @property
    def priority(self) -> int:
        return getattr(self, "_priority", 0)
