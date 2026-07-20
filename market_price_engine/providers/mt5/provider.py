# -*- coding: utf-8 -*-
"""MT5 Provider - Primary execution-market feed with multi-instance support"""

from typing import Optional, List, Dict, Any
from datetime import datetime
import sys
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import MetaTrader5 as mt5

    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False
    print("Warning: MetaTrader5 not installed. Install with: pip install MetaTrader5")

from providers.base import MarketDataProvider, OHLCVData


class MT5Provider(MarketDataProvider):
    """MT5 provider for Pepperstone market data with multi-instance support"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "mt5"
        self.terminal_path = self.config.get(
            "terminal_path", "C:/Program Files/Pepperstone MetaTrader 5/terminal64.exe"
        )
        self.login = self.config.get("login", None)
        self.password = self.config.get("password", None)
        self.server = self.config.get("server", None)
        self.timeout = self.config.get("timeout", 60)
        self.retries = self.config.get("retries", 3)
        self.connected = False
        self._cache = {}
        self._mt5_initialized = False

    def get_provider_name(self) -> str:
        return self.name

    def is_available(self) -> bool:
        """Check if MT5 is available and connected"""
        if not MT5_AVAILABLE:
            return False
        if not self.connected:
            self.connect()
        return self.connected

    def get_health(self) -> Dict[str, Any]:
        """Get provider health status"""
        return {
            "provider": self.name,
            "available": self.is_available(),
            "connected": self.connected,
            "terminal_path": self.terminal_path,
            "server": self.server,
            "login": self.login,
            "status": "healthy" if self.connected else "disconnected",
        }

    def connect(self) -> bool:
        """Establish connection to MT5 terminal with multi-instance handling"""
        if not MT5_AVAILABLE:
            print("[MT5] MetaTrader5 library not available")
            return False

        if self.connected:
            return True

        try:
            print(f"[MT5] Connecting to terminal: {self.terminal_path}")

            # Check if terminal exists
            if not os.path.exists(self.terminal_path):
                print(f"[MT5] Terminal not found at: {self.terminal_path}")
                # Try common alternative paths
                alt_paths = [
                    "C:/Program Files/MetaTrader 5/terminal64.exe",
                    "C:/Program Files (x86)/MetaTrader 5/terminal64.exe",
                    "C:/Program Files/Pepperstone MetaTrader 5/terminal64.exe",
                ]
                for alt in alt_paths:
                    if os.path.exists(alt):
                        print(f"[MT5] Found terminal at: {alt}")
                        self.terminal_path = alt
                        break
                else:
                    print("[MT5] No MT5 terminal found")
                    return False

            # Initialize MT5 with terminal path
            print(f"[MT5] Initializing with: {self.terminal_path}")
            initialized = mt5.initialize(
                terminal=self.terminal_path,
                login=self.login,
                password=self.password,
                server=self.server,
                timeout=self.timeout,
            )

            if not initialized:
                error = mt5.last_error()
                print(f"[MT5] Initialize failed: {error}")
                return False

            print("[MT5] Initialized successfully")

            # Login if credentials provided and not already logged in
            if self.login and self.password:
                print(f"[MT5] Logging in as: {self.login}")
                authorized = mt5.login(
                    login=self.login, password=self.password, server=self.server
                )
                if not authorized:
                    error = mt5.last_error()
                    print(f"[MT5] Login failed: {error}")
                    mt5.shutdown()
                    return False
                print("[MT5] Login successful")

            self.connected = True
            self._mt5_initialized = True
            print("[MT5] Connection established successfully")
            return True

        except Exception as e:
            print(f"[MT5] Connection error: {e}")
            if self._mt5_initialized:
                try:
                    mt5.shutdown()
                except:
                    pass
                self._mt5_initialized = False
            self.connected = False
            return False

    def disconnect(self):
        """Disconnect from MT5"""
        if self.connected and MT5_AVAILABLE:
            try:
                mt5.shutdown()
                print("[MT5] Disconnected")
            except:
                pass
            self.connected = False
            self._mt5_initialized = False

    def get_available_symbols(self) -> List[str]:
        """Get all available symbols from MT5"""
        if not self.is_available():
            return []

        try:
            symbols = mt5.symbols_get()
            if symbols:
                symbol_names = [s.name for s in symbols]
                print(f"[MT5] Retrieved {len(symbol_names)} symbols")
                return symbol_names
            else:
                print("[MT5] No symbols found")
                return []
        except Exception as e:
            print(f"[MT5] Error getting symbols: {e}")
            return []

    def get_current_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get current tick/quote for a symbol"""
        if not self.is_available():
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
                    "timestamp": datetime.fromtimestamp(tick.time),
                    "source": self.name,
                    "time_msc": tick.time_msc,
                }
        except Exception as e:
            print(f"[MT5] Quote error for {symbol}: {e}")
        return None

    def get_historical_bars(
        self, symbol: str, timeframe: str, start_date: datetime, end_date: datetime
    ) -> List[OHLCVData]:
        """Get historical OHLCV from MT5 with retry logic"""
        if not self.is_available():
            return []

        timeframe_map = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "M30": mt5.TIMEFRAME_M30,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1,
            "W1": mt5.TIMEFRAME_W1,
            "MN1": mt5.TIMEFRAME_MN1,
        }

        mt5_timeframe = timeframe_map.get(timeframe, mt5.TIMEFRAME_D1)

        # Retry logic
        for attempt in range(self.retries):
            try:
                rates = mt5.copy_rates_range(
                    symbol, mt5_timeframe, start_date, end_date
                )

                if rates is None or len(rates) == 0:
                    if attempt < self.retries - 1:
                        print(f"[MT5] No data for {symbol} ({timeframe}), retrying...")
                        continue
                    return []

                bars = []
                for r in rates:
                    bars.append(
                        OHLCVData(
                            symbol=symbol,
                            timeframe=timeframe,
                            timestamp=datetime.fromtimestamp(r[0]),
                            open=float(r[1]),
                            high=float(r[2]),
                            low=float(r[3]),
                            close=float(r[4]),
                            volume=float(r[5]) if len(r) > 5 else None,
                            source=self.name,
                            quality_score=99.0,
                        )
                    )

                print(f"[MT5] Loaded {len(bars)} bars for {symbol} ({timeframe})")
                return bars

            except Exception as e:
                print(
                    f"[MT5] Historical error (attempt {attempt+1}/{self.retries}) for {symbol}: {e}"
                )
                if attempt == self.retries - 1:
                    return []
                import time

                time.sleep(1)

        return []
