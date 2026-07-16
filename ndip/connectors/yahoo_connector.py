"""Yahoo Finance Connector - Fetches real market data."""

from datetime import datetime
from typing import Any, Dict, Optional

import yfinance as yf


class YahooConnector:
    """Connector for Yahoo Finance."""

    def __init__(self):
        self._connected = False

    def connect(self) -> bool:
        self._connected = True
        return True

    def disconnect(self) -> None:
        self._connected = False

    def get_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get current price for a symbol."""
        try:
            # Format symbol for Yahoo Finance
            if len(symbol) == 6 and symbol.isalpha():
                ticker = yf.Ticker(f"{symbol}=X")
            else:
                ticker = yf.Ticker(symbol)

            data = ticker.history(period="1d")
            if data.empty:
                return None

            latest = data.iloc[-1]

            return {
                "asset": symbol,
                "value": float(latest["Close"]),
                "volume": int(latest["Volume"]),
                "timestamp": datetime.now().isoformat(),
                "open": float(latest["Open"]),
                "high": float(latest["High"]),
                "low": float(latest["Low"]),
                "close": float(latest["Close"]),
                "source": "yahoo",
                "asset_class": self._classify_asset(symbol),
            }
        except Exception as e:
            print(f"Yahoo Finance error for {symbol}: {e}")
            return None

    def _classify_asset(self, symbol: str) -> str:
        if len(symbol) == 6 and symbol.isalpha():
            return "forex"
        elif "-" in symbol:
            return "crypto"
        elif symbol.endswith("=F") or symbol.endswith(".F"):
            return "future"
        else:
            return "equity"
