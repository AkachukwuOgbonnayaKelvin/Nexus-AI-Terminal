# -*- coding: utf-8 -*-
"""SEC EDGAR Provider - Official US corporate filings"""

from typing import Optional, List, Dict, Any
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from corporate_earnings_engine.providers.base import (
    EarningsProvider,
    EarningsObservation,
    FinancialStatement,
)


class SECEdgarProvider(EarningsProvider):
    """SEC EDGAR provider for US-listed companies"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "sec_edgar"
        self.base_url = "https://www.sec.gov/Archives/edgar/data"
        self._cache = {}

    def get_provider_name(self) -> str:
        return self.name

    def get_tier(self) -> int:
        return 1

    def is_available(self) -> bool:
        return REQUESTS_AVAILABLE

    def get_health(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "available": self.is_available(),
            "status": "healthy" if self.is_available() else "unavailable",
        }

    def get_available_symbols(self) -> List[str]:
        return ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA"]

    def get_earnings(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[EarningsObservation]:
        """Get earnings data from SEC filings"""
        # SEC EDGAR requires CIK number. For now, return empty.
        # Full implementation would fetch XBRL data from SEC API
        return []

    def get_financial_statements(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[FinancialStatement]:
        """Get financial statements from SEC filings"""
        return []
