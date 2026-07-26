"""Provider Router - Exchange-aware provider selection with fallback"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from corporate_earnings_engine.providers.base import (
    EarningsObservation,
    EarningsProvider,
)
from corporate_earnings_engine.providers.registry import ProviderRegistry


class ProviderRouter:
    """Routes requests to the best provider for each symbol/exchange"""

    EXCHANGE_PROVIDERS = {
        "NASDAQ": ["sec_edgar", "financial_modeling_prep", "finnhub", "yahoo_finance"],
        "NYSE": ["sec_edgar", "financial_modeling_prep", "finnhub", "yahoo_finance"],
        "LSE": ["financial_modeling_prep", "finnhub", "yahoo_finance"],
        "TSE": ["financial_modeling_prep", "finnhub", "yahoo_finance"],
        "SIX": ["financial_modeling_prep", "finnhub", "yahoo_finance"],
        "TSX": ["financial_modeling_prep", "finnhub", "yahoo_finance"],
        "ASX": ["financial_modeling_prep", "finnhub", "yahoo_finance"],
        "NZX": ["financial_modeling_prep", "finnhub", "yahoo_finance"],
    }

    SYMBOL_EXCHANGE = {
        "AAPL": "NASDAQ",
        "MSFT": "NASDAQ",
        "GOOGL": "NASDAQ",
        "AMZN": "NASDAQ",
        "TSLA": "NASDAQ",
        "META": "NASDAQ",
        "BP.L": "LSE",
        "SHEL.L": "LSE",
        "HSBA.L": "LSE",
        "9984.T": "TSE",
        "6758.T": "TSE",
        "8306.T": "TSE",
        "NESN.SW": "SIX",
        "ROG.SW": "SIX",
        "UBSG.SW": "SIX",
        "RY.TO": "TSX",
        "TD.TO": "TSX",
        "BNS.TO": "TSX",
        "BHP.AX": "ASX",
        "CBA.AX": "ASX",
        "CSL.AX": "ASX",
        "AIA.NZ": "NZX",
        "FPH.NZ": "NZX",
    }

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.registry = ProviderRegistry(config)
        self._cache = {}

    def get_exchange_for_symbol(self, symbol: str) -> str:
        return self.SYMBOL_EXCHANGE.get(symbol, "NASDAQ")

    def get_providers_for_symbol(self, symbol: str) -> list[EarningsProvider]:
        exchange = self.get_exchange_for_symbol(symbol)
        provider_names = self.EXCHANGE_PROVIDERS.get(
            exchange, self.EXCHANGE_PROVIDERS["NASDAQ"]
        )
        providers = []
        for name in provider_names:
            provider = self.registry.get_provider(name)
            if provider:
                providers.append(provider)
        return providers

    def get_earnings_with_fallback(
        self,
        symbol: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[EarningsObservation]:
        cache_key = f"{symbol}_{start_date}_{end_date}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        providers = self.get_providers_for_symbol(symbol)

        for provider in providers:
            if not provider.is_available():
                continue

            try:
                data = provider.get_earnings(symbol, start_date, end_date)
                if data:
                    print(
                        f"[Router] ✅ {symbol} → {provider.get_provider_name()} → {len(data)} records"
                    )
                    self._cache[cache_key] = data
                    return data
                else:
                    print(
                        f"[Router] ⚠️ {symbol} → {provider.get_provider_name()} → No data"
                    )
            except Exception as e:
                print(
                    f"[Router] ❌ {symbol} → {provider.get_provider_name()} → {str(e)[:50]}"
                )
                continue

        print(f"[Router] ❌ {symbol} → No provider returned data")
        return []

    def get_earnings_for_symbols(
        self,
        symbols: list[str],
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> dict[str, list[EarningsObservation]]:
        results = {}
        for symbol in symbols:
            results[symbol] = self.get_earnings_with_fallback(
                symbol, start_date, end_date
            )
        return results
