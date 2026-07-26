"""Base provider interface for corporate earnings data"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class EarningsObservation:
    """Standardized earnings observation"""

    symbol: str
    company_name: str
    period: str
    period_type: str  # quarterly, annual
    actual_eps: float | None = None
    estimated_eps: float | None = None
    actual_revenue: float | None = None
    estimated_revenue: float | None = None
    currency: str = "USD"
    fiscal_period_end: datetime | None = None
    announcement_date: datetime | None = None
    source: str = "unknown"
    source_tier: int = 1
    quality_score: float = 100.0
    provenance: dict[str, Any] = field(default_factory=dict)


@dataclass
class FinancialStatement:
    """Financial statement data"""

    symbol: str
    company_name: str
    period: str
    period_type: str
    revenue: float | None = None
    net_income: float | None = None
    operating_income: float | None = None
    gross_profit: float | None = None
    ebitda: float | None = None
    total_assets: float | None = None
    total_liabilities: float | None = None
    total_equity: float | None = None
    operating_cash_flow: float | None = None
    free_cash_flow: float | None = None
    currency: str = "USD"
    fiscal_period_end: datetime | None = None
    source: str = "unknown"
    source_tier: int = 1


class EarningsProvider(ABC):
    """Base class for all earnings data providers"""

    @abstractmethod
    def get_earnings(
        self,
        symbol: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[EarningsObservation]:
        """Get earnings data for a symbol"""

    @abstractmethod
    def get_financial_statements(
        self,
        symbol: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[FinancialStatement]:
        """Get financial statements for a symbol"""

    @abstractmethod
    def get_available_symbols(self) -> list[str]:
        """Get all available symbols"""

    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the provider's name"""

    @abstractmethod
    def get_tier(self) -> int:
        """Get the provider's tier (1 or 2)"""

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is currently available"""

    @abstractmethod
    def get_health(self) -> dict[str, Any]:
        """Get provider health status"""
