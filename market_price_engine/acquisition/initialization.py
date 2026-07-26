"""Historical Initialization - Multi-timeframe data bootstrap for 90 days"""

import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from acquisition.incremental_loader import IncrementalLoader
from providers.base import OHLCVData
from providers.registry import ProviderRegistry
from quality.validator import OHLCVValidator


class HistoricalInitializer:
    """
    Initializes the market price engine with multi-timeframe historical data.

    Timeframes: M5, M15, H1, H4, D1, W1, MN1
    First run: Downloads 90 days of data for each timeframe.
    """

    # Timeframes to load
    TIMEFRAMES = ["M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN1"]

    # Primary timeframes for initial bootstrap
    PRIMARY_TIMEFRAMES = ["M5", "M15", "H1", "H4", "D1"]

    # MT5 symbol mapping for special symbols
    MT5_SYMBOL_MAP = {
        # Indices
        "US100": "NAS100",  # NASDAQ 100
        "JP225": "JPN225",  # Nikkei 225
        "AU200": "ASX.AU",  # ASX 200
        "EU50": "STOXX50",  # Euro Stoxx 50
        # Commodities
        "WTI": "CLNX.ES",  # WTI Crude Oil
        "Brent": "SpotBrent",  # Brent Crude Oil
        "Natural Gas": "NATGAS",
        "Platinum": "XPTUSD",
        "Palladium": "XPDUSD",
        "Copper": "Copper",
    }

    # Yahoo symbol mapping for special symbols
    YAHOO_SYMBOL_MAP = {
        "XAUUSD": "GC=F",
        "XAGUSD": "SI=F",
        "WTI": "CL=F",
        "Brent": "BZ=F",
        "Natural Gas": "NG=F",
        "Copper": "HG=F",
        "Platinum": "PL=F",
        "Palladium": "PA=F",
        "US500": "^GSPC",
        "US100": "^IXIC",
        "US30": "^DJI",
        "GER40": "^GDAXI",
        "UK100": "^FTSE",
        "JP225": "^N225",
        "HK50": "^HSI",
        "FRA40": "^FCHI",
        "AU200": "^AXJO",
        "EU50": "^STOXX50E",
    }

    # Core FX symbols
    FX_SYMBOLS = [
        "EURUSD",
        "GBPUSD",
        "USDJPY",
        "USDCHF",
        "USDCAD",
        "AUDUSD",
        "NZDUSD",
        "EURGBP",
        "EURJPY",
        "GBPJPY",
        "AUDJPY",
        "CADJPY",
        "CHFJPY",
        "NZDJPY",
        "EURCHF",
        "GBPCHF",
        "AUDNZD",
        "AUDCAD",
        "NZDCAD",
        "GBPNZD",
        "EURNZD",
        "EURCAD",
        "GBPAUD",
        "GBPCAD",
        "CADCHF",
    ]

    # Indices
    INDICES = [
        "US500",
        "US100",
        "US30",
        "GER40",
        "UK100",
        "FRA40",
        "JP225",
        "HK50",
        "AU200",
        "EU50",
    ]

    # Commodities
    COMMODITIES = [
        "XAUUSD",
        "XAGUSD",
        "WTI",
        "Brent",
        "Natural Gas",
        "Copper",
        "Platinum",
        "Palladium",
    ]

    ALL_SYMBOLS = FX_SYMBOLS + INDICES + COMMODITIES

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.registry = ProviderRegistry(config)
        self.loader = IncrementalLoader(config)
        self.validator = OHLCVValidator()
        self._results = {}

    def _get_mt5_symbol(self, symbol: str) -> str:
        """Get the MT5 symbol for a given symbol"""
        return self.MT5_SYMBOL_MAP.get(symbol, symbol)

    def _get_yahoo_symbol(self, symbol: str) -> str:
        """Get the Yahoo Finance symbol for a given symbol"""
        return self.YAHOO_SYMBOL_MAP.get(symbol, symbol)

    def initialize_90_days(
        self,
        symbols: list[str] | None = None,
        timeframes: list[str] | None = None,
    ) -> dict[str, Any]:
        """Initialize 90 days of historical data for all symbols and timeframes."""
        target_symbols = symbols or self.ALL_SYMBOLS
        target_timeframes = timeframes or self.PRIMARY_TIMEFRAMES

        print()
        print("=" * 70)
        print("  MKT-001 90-DAY HISTORICAL INITIALIZATION")
        print(f"  Symbols: {len(target_symbols)}")
        print(f"  Timeframes: {', '.join(target_timeframes)}")
        print("=" * 70)
        print()

        results = {
            "total_symbols": len(target_symbols),
            "total_timeframes": len(target_timeframes),
            "successful": 0,
            "failed": 0,
            "skipped": 0,
            "details": {},
            "start_time": datetime.now().isoformat(),
        }

        total_attempts = len(target_symbols) * len(target_timeframes)
        attempt_count = 0

        for symbol in target_symbols:
            print()
            print(f"Processing: {symbol}")
            symbol_results = {}
            symbol_success = 0
            symbol_failed = 0

            for timeframe in target_timeframes:
                attempt_count += 1
                print(
                    f"  [{attempt_count}/{total_attempts}] Loading {symbol} ({timeframe})..."
                )

                result = self._initialize_symbol_timeframe(symbol, timeframe)
                symbol_results[timeframe] = result

                if result["status"] == "SUCCESS":
                    symbol_success += 1
                    results["successful"] += 1
                    bars = result.get("bars", 0)
                    provider = result.get("provider", "unknown")
                    print(f"    OK {bars} bars from {provider}")
                else:
                    symbol_failed += 1
                    results["failed"] += 1
                    errors = result.get("errors", ["Unknown error"])
                    print(f"    FAILED - {errors[0] if errors else 'Unknown error'}")

                time.sleep(0.3)

            results["details"][symbol] = {
                "timeframes": symbol_results,
                "successful": symbol_success,
                "failed": symbol_failed,
                "status": "SUCCESS" if symbol_success > 0 else "FAILED",
            }

            print(
                f"  Summary {symbol}: {symbol_success}/{len(target_timeframes)} timeframes loaded"
            )

        results["end_time"] = datetime.now().isoformat()
        results["success_rate"] = (
            (results["successful"] / total_attempts) * 100 if total_attempts > 0 else 0
        )

        print()
        print("=" * 70)
        print("  INITIALIZATION COMPLETE")
        print("=" * 70)
        print(f"  Symbols:        {results['total_symbols']}")
        print(f"  Timeframes:     {results['total_timeframes']}")
        print(f"  Total Attempts: {total_attempts}")
        print(f"  Successful:     {results['successful']}")
        print(f"  Failed:         {results['failed']}")
        print(f"  Success Rate:   {results['success_rate']:.1f}%")
        print("=" * 70)
        print()

        return results

    def _initialize_symbol_timeframe(
        self, symbol: str, timeframe: str
    ) -> dict[str, Any]:
        """Initialize a single symbol for a specific timeframe"""

        result = {
            "symbol": symbol,
            "timeframe": timeframe,
            "status": "PENDING",
            "bars": 0,
            "provider": None,
            "errors": [],
        }

        days_back = 90

        # 1. Try MT5 (Primary) with symbol mapping
        mt5 = self.registry.get_provider("mt5")
        if mt5 and mt5.is_available():
            mt5_symbol = self._get_mt5_symbol(symbol)
            bars = self._load_from_provider(mt5, mt5_symbol, timeframe, days_back)
            if bars and len(bars) > 10:
                result["bars"] = len(bars)
                result["provider"] = "mt5"
                result["status"] = "SUCCESS"
                self._store_bars(bars)
                return result

        # 2. Try Yahoo Finance (Secondary) with symbol mapping
        yahoo = self.registry.get_provider("yahoo")
        if yahoo and yahoo.is_available():
            yahoo_symbol = self._get_yahoo_symbol(symbol)
            bars = self._load_from_provider(yahoo, yahoo_symbol, timeframe, days_back)
            if bars and len(bars) > 10:
                result["bars"] = len(bars)
                result["provider"] = "yahoo"
                result["status"] = "SUCCESS"
                self._store_bars(bars)
                return result

        result["status"] = "FAILED"
        result["errors"].append(f"No provider available for {symbol} ({timeframe})")
        return result

    def _load_from_provider(
        self, provider, symbol: str, timeframe: str, days: int
    ) -> list[OHLCVData]:
        """Load data from a specific provider"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            bars = provider.get_historical_bars(symbol, timeframe, start_date, end_date)

            # Validate bars
            valid_bars = []
            for bar in bars:
                is_valid, _ = self.validator.validate(bar)
                if is_valid:
                    valid_bars.append(bar)

            return valid_bars
        except Exception:
            return []

    def _store_bars(self, bars: list[OHLCVData]):
        """Store bars in warehouse"""
        for bar in bars:
            self.loader._save_record(bar)
