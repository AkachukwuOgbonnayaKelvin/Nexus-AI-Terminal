# -*- coding: utf-8 -*-
"""Base provider interface for macroeconomic data sources"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass, field


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
    previous: Optional[float] = None
    forecast: Optional[float] = None
    quality_score: float = 100.0
    status: str = "official"
    metadata: Dict[str, Any] = field(default_factory=dict)


class MacroProvider(ABC):
    """Base class for all macroeconomic data providers"""

    @abstractmethod
    def get_indicator(
        self,
        indicator: str,
        country: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[MacroObservation]:
        """Get a specific indicator for a country"""
        pass

    @abstractmethod
    def get_available_indicators(self, country: str) -> List[str]:
        """Get all available indicators for a country"""
        pass

    @abstractmethod
    def get_available_countries(self) -> List[str]:
        """Get all available countries"""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the provider's name"""
        pass

    @abstractmethod
    def get_tier(self) -> int:
        """Get the provider's tier (1, 2, or 3)"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is currently available"""
        pass

    @abstractmethod
    def get_health(self) -> Dict[str, Any]:
        """Get provider health status"""
        pass
