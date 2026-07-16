from datetime import datetime
from typing import Any, Dict, List, Optional

import yfinance as yf

from providers.interfaces.base_provider import BaseProvider


class YahooConnector(BaseProvider):
    def __init__(self):
        self._connected = False
        self._tier = 2
        self._priority = 5

    def connect(self) -> bool:
        self._connected = True
        return True

    def disconnect(self) -> None:
        self._connected = False

    def _map_symbol(self, symbol: str) -> List[str]:
        """Return a list of possible Yahoo tickers for an internal symbol."""
        mapping = {
            "XAUUSD": ["GC=F", "XAUUSD=X"],
            "XAGUSD": ["SI=F", "XAGUSD=X"],
            "WTI": ["CL=F"],
            "BRENT": ["BZ=F"],
            "NG": ["NG=F"],
            "COPPER": ["HG=F"],
            "PLATINUM": ["PL=F"],
            "PALLADIUM": ["PA=F"],
            "US500": ["^GSPC"],
            "US30": ["^DJI"],
            "US100": ["^IXIC"],
            "GER40": ["^GDAXI"],
            "UK100": ["^FTSE"],
            "FRA40": ["^FCHI"],
            "JP225": ["^N225"],
            "HK50": ["^HSI"],
            "AU200": ["^AXJO"],
        }
        return mapping.get(symbol, [symbol])

    def get_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        if not self._connected:
            return None
        # For forex (6 letters, all alpha), try with =X suffix first
        if len(symbol) == 6 and symbol.isalpha():
            tickers_to_try = [f"{symbol}=X"]
        else:
            tickers_to_try = self._map_symbol(symbol)

        for yahoo_symbol in tickers_to_try:
            try:
                ticker = yf.Ticker(yahoo_symbol)
                data = ticker.history(period="1d")
                if not data.empty:
                    latest = data.iloc[-1]
                    return {
                        "symbol": symbol,
                        "close": float(latest["Close"]),
                        "open": float(latest["Open"]),
                        "high": float(latest["High"]),
                        "low": float(latest["Low"]),
                        "volume": int(latest["Volume"]),
                        "timestamp": datetime.now().isoformat(),
                        "source": "yahoo",
                        "raw": latest.to_dict(),
                    }
            except Exception:
                continue
        return None

    def get_multiple(self, symbols: List[str]) -> List[Dict[str, Any]]:
        results = []
        for sym in symbols:
            data = self.get_price(sym)
            if data:
                results.append(data)
        return results

    def health_check(self) -> bool:
        return self.get_price("EURUSD") is not None

    def get_capabilities(self) -> Dict[str, bool]:
        return {
            "realtime": False,
            "historical": True,
            "forex": True,
            "equities": True,
            "crypto": True,
        }

    def get_rate_limit(self) -> Dict[str, int]:
        return {"requests_per_second": 5, "requests_per_minute": 300}

    def get_available_symbols(self) -> List[str]:
        return ["EURUSD", "GBPUSD", "AAPL", "MSFT", "GC=F", "^GSPC"]

    def supports_symbol(self, symbol: str) -> bool:
        return True
