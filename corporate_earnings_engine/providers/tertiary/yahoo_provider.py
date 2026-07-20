# -*- coding: utf-8 -*-
"""Yahoo Finance Provider - Tier 3 Fallback with multiple records"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import sys
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    import yfinance as yf
    YF_AVAILABLE = True
except ImportError:
    YF_AVAILABLE = False
    print("Warning: yfinance not installed. Install with: pip install yfinance")

from corporate_earnings_engine.providers.base import EarningsProvider, EarningsObservation, FinancialStatement


class YahooFinanceProvider(EarningsProvider):
    """Yahoo Finance as fallback provider using modern API"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "yahoo_finance"
        self._cache = {}
    
    def get_provider_name(self) -> str:
        return self.name
    
    def get_tier(self) -> int:
        return 3
    
    def is_available(self) -> bool:
        return YF_AVAILABLE
    
    def get_health(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "available": self.is_available(),
            "status": "healthy" if self.is_available() else "unavailable"
        }
    
    def get_available_symbols(self) -> List[str]:
        return [
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
            "BP.L", "SHEL.L", "HSBA.L",
            "9984.T", "6758.T", "8306.T",
            "NESN.SW", "ROG.SW", "UBSG.SW",
            "RY.TO", "TD.TO", "BNS.TO",
            "BHP.AX", "CBA.AX", "CSL.AX",
            "AIA.NZ", "FPH.NZ"
        ]
    
    def _get_eps_from_income_stmt(self, ticker, period: str = "quarterly") -> List[Dict]:
        """Extract EPS from income statement for multiple periods"""
        results = []
        
        try:
            # Get income statement
            if period == "quarterly":
                income_stmt = ticker.quarterly_income_stmt
            else:
                income_stmt = ticker.income_stmt
            
            if income_stmt is None or income_stmt.empty:
                return results
            
            # Get balance sheet for shares data
            balance_sheet = ticker.quarterly_balance_sheet if period == "quarterly" else ticker.balance_sheet
            
            # Process all periods (columns)
            for col in income_stmt.columns:
                try:
                    net_income = income_stmt.loc['Net Income', col] if 'Net Income' in income_stmt.index else None
                    if net_income is None or net_income == 0:
                        continue
                    
                    shares = None
                    if balance_sheet is not None and not balance_sheet.empty:
                        if 'Ordinary Shares Number' in balance_sheet.index and col in balance_sheet.columns:
                            shares = balance_sheet.loc['Ordinary Shares Number', col]
                        elif 'Common Stock Shares Outstanding' in balance_sheet.index and col in balance_sheet.columns:
                            shares = balance_sheet.loc['Common Stock Shares Outstanding', col]
                    
                    if shares is None or shares == 0:
                        continue
                    
                    eps = net_income / shares
                    results.append({
                        "period": col.strftime("%Y-%m-%d") if hasattr(col, 'strftime') else str(col),
                        "eps": float(eps),
                        "net_income": float(net_income),
                        "shares": float(shares)
                    })
                except Exception as e:
                    continue
            
            # Sort by period (newest first)
            results.sort(key=lambda x: x["period"], reverse=True)
            return results
            
        except Exception as e:
            return results
    
    def get_earnings(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[EarningsObservation]:
        """Get earnings data using modern Yahoo Finance API"""
        if not self.is_available():
            return []
        
        try:
            ticker = yf.Ticker(symbol)
            results = []
            
            # Try quarterly income statement first
            quarterly_data = self._get_eps_from_income_stmt(ticker, "quarterly")
            if quarterly_data:
                for data in quarterly_data[:8]:  # Last 8 quarters
                    results.append(EarningsObservation(
                        symbol=symbol,
                        company_name=symbol,
                        period=data["period"],
                        period_type="quarterly",
                        actual_eps=data["eps"],
                        estimated_eps=None,
                        currency="USD",
                        announcement_date=datetime.strptime(data["period"], "%Y-%m-%d"),
                        source=self.name,
                        source_tier=3,
                        quality_score=75.0,
                        provenance={
                            "source": "yahoo_finance_derived",
                            "method": "quarterly_income_stmt",
                            "net_income": data["net_income"],
                            "shares": data["shares"]
                        }
                    ))
                return results
            
            # Try annual income statement
            annual_data = self._get_eps_from_income_stmt(ticker, "annual")
            if annual_data:
                for data in annual_data[:4]:  # Last 4 years
                    results.append(EarningsObservation(
                        symbol=symbol,
                        company_name=symbol,
                        period=data["period"],
                        period_type="annual",
                        actual_eps=data["eps"],
                        estimated_eps=None,
                        currency="USD",
                        announcement_date=datetime.strptime(data["period"], "%Y-%m-%d"),
                        source=self.name,
                        source_tier=3,
                        quality_score=70.0,
                        provenance={
                            "source": "yahoo_finance_derived",
                            "method": "annual_income_stmt",
                            "net_income": data["net_income"],
                            "shares": data["shares"]
                        }
                    ))
                return results
            
            return results
            
        except Exception as e:
            print(f"[Yahoo] Error for {symbol}: {e}")
            return []
    
    def get_financial_statements(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[FinancialStatement]:
        return []
