# -*- coding: utf-8 -*-
"""MT5 Provider Client - Primary execution-market feed"""

from typing import Optional, Dict, Any, List
from datetime import datetime

# Try to import MetaTrader5
try:
    import MetaTrader5 as mt5

    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False
    print("Warning: MetaTrader5 not installed. Install with: pip install MetaTrader5")


class MT5Client:
    """MT5 client for Pepperstone integration"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connected = False
        self.terminal_path = config.get("terminal_path", None)
        self.login = config.get("login", None)
        self.password = config.get("password", None)
        self.server = config.get("server", None)
        self.timeout = config.get("timeout", 60)

    def connect(self) -> bool:
        """Establish connection to MT5 terminal"""
        if not MT5_AVAILABLE:
            return False

        try:
            # Initialize MT5
            if self.terminal_path:
                mt5.initialize(terminal=self.terminal_path)
            else:
                mt5.initialize()

            # Login if credentials provided
            if self.login and self.password:
                authorized = mt5.login(
                    login=self.login, password=self.password, server=self.server
                )
                if not authorized:
                    print(f"MT5 login failed: {mt5.last_error()}")
                    return False

            self.connected = True
            return True

        except Exception as e:
            print(f"MT5 connection error: {e}")
            return False

    def disconnect(self):
        """Disconnect from MT5"""
        if self.connected and MT5_AVAILABLE:
            mt5.shutdown()
            self.connected = False

    def get_symbols(self) -> List[str]:
        """Get all available symbols"""
        if not self.connected or not MT5_AVAILABLE:
            return []

        try:
            symbols = mt5.symbols_get()
            return [s.name for s in symbols] if symbols else []
        except Exception as e:
            print(f"Error getting symbols: {e}")
            return []

    def get_tick(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get current tick for symbol"""
        if not self.connected or not MT5_AVAILABLE:
            return None

        try:
            tick = mt5.symbol_info_tick(symbol)
            if tick:
                return {
                    "symbol": symbol,
                    "bid": tick.bid,
                    "ask": tick.ask,
                    "last": tick.last,
                    "volume": tick.volume,
                    "time": tick.time,
                    "time_msc": tick.time_msc,
                    "flags": tick.flags,
                    "volume_real": tick.volume_real,
                }
        except Exception as e:
            print(f"Error getting tick for {symbol}: {e}")
        return None

    def get_rates(
        self, symbol: str, timeframe: int, count: int
    ) -> Optional[List[Dict[str, Any]]]:
        """Get OHLCV rates"""
        if not self.connected or not MT5_AVAILABLE:
            return None

        try:
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
            if rates is not None and len(rates) > 0:
                return [
                    {
                        "time": r[0],
                        "open": r[1],
                        "high": r[2],
                        "low": r[3],
                        "close": r[4],
                        "tick_volume": r[5],
                        "spread": r[6],
                        "real_volume": r[7],
                    }
                    for r in rates
                ]
        except Exception as e:
            print(f"Error getting rates for {symbol}: {e}")
        return None

    def get_historical_rates(
        self, symbol: str, timeframe: int, start_date: datetime, end_date: datetime
    ) -> Optional[List[Dict[str, Any]]]:
        """Get historical rates for date range"""
        if not self.connected or not MT5_AVAILABLE:
            return None

        try:
            rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)
            if rates is not None and len(rates) > 0:
                return [
                    {
                        "time": r[0],
                        "open": r[1],
                        "high": r[2],
                        "low": r[3],
                        "close": r[4],
                        "tick_volume": r[5],
                        "spread": r[6],
                        "real_volume": r[7],
                    }
                    for r in rates
                ]
        except Exception as e:
            print(f"Error getting historical rates for {symbol}: {e}")
        return None

    def is_connected(self) -> bool:
        """Check if MT5 is connected"""
        return self.connected and MT5_AVAILABLE

    def get_health(self) -> Dict[str, Any]:
        """Get MT5 health status"""
        return {
            "connected": self.connected,
            "available": MT5_AVAILABLE,
            "symbol_count": len(self.get_symbols()) if self.connected else 0,
            "terminal_path": self.terminal_path,
            "timestamp": datetime.now().isoformat(),
        }
