# -*- coding: utf-8 -*-
"""Base provider interface for corporate earnings data"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class EarningsObservation:
    """Standardized earnings observation"""

    symbol: str
    company_name: str
    period: str
    period_type: str  # quarterly, annual
    actual_eps: Optional[float] = None
    estimated_eps: Optional[float] = None
    actual_revenue: Optional[float] = None
    estimated_revenue: Optional[float] = None
    currency: str = "USD"
    fiscal_period_end: Optional[datetime] = None
    announcement_date: Optional[datetime] = None
    source: str = "unknown"
    source_tier: int = 1
    quality_score: float = 100.0
    provenance: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FinancialStatement:
    """Financial statement data"""

    symbol: str
    company_name: str
    period: str
    period_type: str
    revenue: Optional[float] = None
    net_income: Optional[float] = None
    operating_income: Optional[float] = None
    gross_profit: Optional[float] = None
    ebitda: Optional[float] = None
    total_assets: Optional[float] = None
    total_liabilities: Optional[float] = None
    total_equity: Optional[float] = None
    operating_cash_flow: Optional[float] = None
    free_cash_flow: Optional[float] = None
    currency: str = "USD"
    fiscal_period_end: Optional[datetime] = None
    source: str = "unknown"
    source_tier: int = 1


class EarningsProvider(ABC):
    """Base class for all earnings data providers"""

    @abstractmethod
    def get_earnings(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[EarningsObservation]:
        """Get earnings data for a symbol"""
        pass

    @abstractmethod
    def get_financial_statements(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[FinancialStatement]:
        """Get financial statements for a symbol"""
        pass

    @abstractmethod
    def get_available_symbols(self) -> List[str]:
        """Get all available symbols"""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the provider's name"""
        pass

    @abstractmethod
    def get_tier(self) -> int:
        """Get the provider's tier (1 or 2)"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is currently available"""
        pass

    @abstractmethod
    def get_health(self) -> Dict[str, Any]:
        """Get provider health status"""
        pass
