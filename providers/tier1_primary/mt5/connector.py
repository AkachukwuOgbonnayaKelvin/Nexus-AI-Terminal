import os
from typing import Any, Dict, List, Optional

from providers.interfaces.base_provider import BaseProvider


class MT5Connector(BaseProvider):
    def __init__(
        self,
        account: int = None,
        password: str = None,
        server: str = None,
        terminal_path: str = None,
    ):
        self.account = account or int(os.getenv("MT5_ACCOUNT", 0))
        self.password = password or os.getenv("MT5_PASSWORD", "")
        self.server = server or os.getenv("MT5_SERVER", "")
        self.terminal_path = terminal_path or os.getenv("MT5_TERMINAL_PATH")
        self._mt5 = None
        self._connected = False
        self._tier = 1
        self._priority = 100

    def connect(self) -> bool:
        if not self.account or not self.password:
            print("MT5 credentials missing")
            return False
        try:
            import MetaTrader5 as mt5
        except ImportError:
            print(
                "MetaTrader5 module not installed. Install with: pip install MetaTrader5"
            )
            return False
        if not mt5.initialize(self.terminal_path):
            print("MT5 initialize failed")
            return False
        if not mt5.login(self.account, self.password, self.server):
            print("MT5 login failed")
            mt5.shutdown()
            return False
        self._mt5 = mt5
        self._connected = True
        return True

    def disconnect(self) -> None:
        if self._mt5:
            self._mt5.shutdown()
            self._connected = False

    def get_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        if not self._connected:
            return None
        tick = self._mt5.symbol_info_tick(symbol)
        if not tick:
            return None
        info = self._mt5.symbol_info(symbol)
        return {
            "symbol": symbol,
            "bid": tick.bid,
            "ask": tick.ask,
            "last": tick.last,
            "volume": tick.volume,
            "time": tick.time,
            "spread": info.spread if info else None,
            "digits": info.digits if info else None,
            "source": "mt5",
            "raw_tick": tick,
            "raw_info": info,
        }

    def get_multiple(self, symbols: List[str]) -> List[Dict[str, Any]]:
        return [self.get_price(s) for s in symbols if self.get_price(s)]

    def health_check(self) -> bool:
        return self.get_price("EURUSD") is not None

    def get_capabilities(self) -> Dict[str, bool]:
        return {"realtime": True, "historical": True, "forex": True, "cfd": True}

    def get_rate_limit(self) -> Dict[str, int]:
        return {"requests_per_second": 100, "requests_per_minute": 6000}

    def get_available_symbols(self) -> List[str]:
        if not self._connected:
            return []
        symbols = self._mt5.symbols_get()
        return [s.name for s in symbols] if symbols else []

    def supports_symbol(self, symbol: str) -> bool:
        if not self._connected:
            return False
        return self._mt5.symbol_info(symbol) is not None
