from typing import Any

import yfinance as yf

from providers.interfaces.base_provider import BaseProvider


class YahooMetadataConnector(BaseProvider):
    def __init__(self):
        self._connected = True
        self._tier = 2
        self._priority = 5

    def connect(self) -> bool:
        return True

    def disconnect(self) -> None:
        pass

    def get_price(self, symbol: str) -> dict[str, Any] | None:
        return None

    def get_multiple(self, symbols: list[str]) -> list[dict[str, Any]]:
        return []

    def health_check(self) -> bool:
        # Use a reliable symbol; return True only if we get a dict
        result = self.get_metadata("AAPL")
        return isinstance(result, dict)

    def get_capabilities(self) -> dict[str, bool]:
        return {"metadata": True}

    def get_rate_limit(self) -> dict[str, int]:
        return {"requests_per_minute": 10}

    def get_available_symbols(self) -> list[str]:
        return []

    def supports_symbol(self, symbol: str) -> bool:
        return True

    def get_metadata(self, symbol: str) -> dict[str, Any] | None:
        """
        Fetch metadata for a symbol. Returns a dict or None.
        Never returns a bool.
        """
        yahoo_symbol = self._map_symbol(symbol)
        try:
            ticker = yf.Ticker(yahoo_symbol)
            info = ticker.info
            # info can be an empty dict or None; if not a dict, return None
            if not info or not isinstance(info, dict):
                return None

            # Build record
            record = {
                "symbol": symbol,
                "display_symbol": info.get("symbol", symbol),
                "short_name": info.get("shortName", ""),
                "long_name": info.get("longName", ""),
                "description": info.get("longBusinessSummary", ""),
                "asset_class": self._classify(symbol, info),
                "exchange_code": info.get("exchange", ""),
                "base_currency": info.get("currency", ""),
                "tick_size": info.get("priceHint", None),
                "sector": info.get("sector", ""),
                "industry": info.get("industry", ""),
                "country": info.get("country", ""),
                "market_open": info.get("marketOpen", None),
                "market_close": info.get("marketClose", None),
                "timezone": info.get("timezone", ""),
                "website": info.get("website", ""),
                "market_cap": info.get("marketCap", None),
                "avg_daily_volume": info.get("averageVolume", None),
                "provider": "yahoo_metadata",
                "provider_rank": 1,
            }
            # Ensure we have a dict; if not, return None
            if not isinstance(record, dict):
                return None
            return record
        except Exception:
            return None

    def _map_symbol(self, symbol: str) -> str:
        """Map internal symbol to Yahoo ticker."""
        if len(symbol) == 6 and symbol.isalpha():
            return f"{symbol}=X"
        mapping = {
            "US500": "^GSPC",
            "US30": "^DJI",
            "US100": "^IXIC",
            "GER40": "^GDAXI",
            "UK100": "^FTSE",
            "FRA40": "^FCHI",
            "JP225": "^N225",
            "HK50": "^HSI",
            "AU200": "^AXJO",
        }
        return mapping.get(symbol, symbol)

    def _classify(self, symbol: str, info: dict) -> str:
        if len(symbol) == 6 and symbol.isalpha():
            return "forex"
        if info.get("quoteType") == "ETF":
            return "etf"
        if info.get("quoteType") == "FUTURE":
            return "futures"
        if info.get("market") == "us_market" and info.get("quoteType") == "EQUITY":
            return "equity"
        if "crypto" in str(info.get("category", "")).lower():
            return "crypto"
        return "unknown"
