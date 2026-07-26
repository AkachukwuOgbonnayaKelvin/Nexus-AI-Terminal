"""Base provider interface for macroeconomic data sources"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class MacroObservation:
    """Standardized macroeconomic observation with currency preservation"""

    indicator: str
    country: str
    period: str
    value: float
    unit: str
    currency: str = "USD"  # Native currency
    frequency: str = "annual"
    source: str = "unknown"
    source_tier: int = 1
    release_date: datetime = None
    vintage_date: datetime = None
    revision_number: int = 0
    previous: float | None = None
    forecast: float | None = None
    quality_score: float = 100.0
    status: str = "official"
    metadata: dict[str, Any] = field(default_factory=dict)


class MacroProvider(ABC):
    """Base class for all macroeconomic data providers"""

    @abstractmethod
    def get_indicator(
        self,
        indicator: str,
        country: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[MacroObservation]:
        """Get a specific indicator for a country"""

    @abstractmethod
    def get_available_indicators(self, country: str) -> list[str]:
        """Get all available indicators for a country"""

    @abstractmethod
    def get_available_countries(self) -> list[str]:
        """Get all available countries"""

    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the provider's name"""

    @abstractmethod
    def get_tier(self) -> int:
        """Get the provider's tier (1, 2, or 3)"""

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is currently available"""

    @abstractmethod
    def get_health(self) -> dict[str, Any]:
        """Get provider health status"""
