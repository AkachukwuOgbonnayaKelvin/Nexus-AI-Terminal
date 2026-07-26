"""Abstract base class for all providers."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


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

    @abstractmethod
    def disconnect(self) -> None:
        """Close connection."""

    @abstractmethod
    def get_price(self, symbol: str) -> dict[str, Any] | None:
        """Fetch raw price data for a symbol."""

    @abstractmethod
    def get_multiple(self, symbols: list[str]) -> list[dict[str, Any]]:
        """Fetch raw price data for multiple symbols."""

    @abstractmethod
    def health_check(self) -> bool:
        """Check if provider is healthy."""

    def get_status(self) -> ProviderStatus:
        """Return current provider status."""
        if self.health_check():
            return ProviderStatus.ONLINE
        return ProviderStatus.OFFLINE

    @abstractmethod
    def get_capabilities(self) -> dict[str, bool]:
        """Return capabilities (realtime, historical, websocket, etc.)."""

    @abstractmethod
    def get_rate_limit(self) -> dict[str, int]:
        """Return rate limit info (requests per second/minute)."""

    def supports_symbol(self, symbol: str) -> bool:
        """Check if provider supports a symbol."""
        return symbol in self.get_available_symbols()

    @abstractmethod
    def get_available_symbols(self) -> list[str]:
        """Return list of available symbols."""

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def tier(self) -> int:
        return getattr(self, "_tier", 2)

    @property
    def priority(self) -> int:
        return getattr(self, "_priority", 0)
