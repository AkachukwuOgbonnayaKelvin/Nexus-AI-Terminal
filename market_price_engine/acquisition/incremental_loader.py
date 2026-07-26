"""Incremental Loader - Only loads new records after first run"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from acquisition.historical_loader import HistoricalDataLoader
from providers.base import OHLCVData
from providers.registry import ProviderRegistry
from warehouse.ohlcv_repository import OHLCVRepository


class IncrementalLoader:
    """
    Loads only new records after first run.

    First run: Loads 90 days of historical data.
    Subsequent runs: Only loads records after last stored timestamp.
    Old data is NEVER deleted - only appended to.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.provider_registry = ProviderRegistry(config)
        self.historical_loader = HistoricalDataLoader(config)
        self._warehouse = OHLCVRepository()  # File-backed persistence
        self._state_file = Path(__file__).parent.parent / "data" / "load_state.json"
        self._load_state = self._load_state_from_file()

    def _load_state_from_file(self) -> dict[str, Any]:
        """Load the last load state from file"""
        if self._state_file.exists():
            try:
                with open(self._state_file) as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_state_to_file(self):
        """Save the current load state to file"""
        self._state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self._state_file, "w") as f:
            json.dump(self._load_state, f, indent=2, default=str)

    def get_warehouse(self):
        """Get the warehouse instance"""
        return self._warehouse

    def _save_record(self, bar: OHLCVData) -> bool:
        """Save a record to warehouse"""
        try:
            self._warehouse.save(bar)
            return True
        except Exception as e:
            print(f"Error saving record: {e}")
            return False

    def load_data(
        self,
        symbol: str,
        timeframe: str = "D1",
        days_back: int = 90,
        force_full: bool = False,
    ) -> list[OHLCVData]:
        """
        Load data for a symbol.

        First run: 90 days back
        Subsequent: Only new records
        """

        # Check what we already have
        key = f"{symbol}_{timeframe}"
        last_record = self._warehouse.get_last_record(symbol, timeframe)

        if last_record is None or force_full:
            # First run or forced full reload - load days_back
            print(f"First run for {symbol} ({timeframe}): Loading {days_back} days")
            bars = self.historical_loader.load_historical_bars(
                symbol, timeframe, days_back
            )

            # Store in warehouse
            for bar in bars:
                self._warehouse.save(bar)

            # Update state
            if bars:
                self._load_state[key] = {
                    "last_timestamp": bars[-1].timestamp.isoformat(),
                    "bar_count": len(bars),
                    "last_update": datetime.now().isoformat(),
                }
                self._save_state_to_file()

            return bars
        else:
            # Incremental - only new records
            start_date = last_record.timestamp + timedelta(seconds=1)
            print(f"Incremental for {symbol} ({timeframe}): Loading from {start_date}")

            # Load only new records
            end_date = datetime.now()
            provider = self.provider_registry.get_primary_provider()

            if not provider or not provider.is_available():
                print(f"No provider available for {symbol} ({timeframe})")
                return []

            bars = provider.get_historical_bars(symbol, timeframe, start_date, end_date)

            if bars:
                # Store new records
                for bar in bars:
                    self._warehouse.save(bar)

                # Update state
                self._load_state[key] = {
                    "last_timestamp": bars[-1].timestamp.isoformat(),
                    "bar_count": len(bars),
                    "last_update": datetime.now().isoformat(),
                }
                self._save_state_to_file()
                print(f"Added {len(bars)} new bars for {symbol} ({timeframe})")
            else:
                print(f"No new data for {symbol} ({timeframe})")

            return bars

    def get_load_status(self) -> dict[str, Any]:
        """Get the current load status for all symbols/timeframes"""
        return self._load_state
