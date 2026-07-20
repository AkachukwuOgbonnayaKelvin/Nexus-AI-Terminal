# -*- coding: utf-8 -*-
"""OHLCV Repository - Stores and retrieves OHLCV data with file persistence"""

from typing import List, Optional, Dict
from datetime import datetime
import sys
import pickle
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from providers.base import OHLCVData


class OHLCVRepository:
    """Repository for OHLCV data storage and retrieval with file persistence"""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._data: Dict[str, List[OHLCVData]] = {}
        self._load_from_disk()

    def _get_file_path(self, key: str) -> Path:
        """Get the file path for a key"""
        return self.data_dir / f"{key}.pkl"

    def _load_from_disk(self):
        """Load data from disk"""
        for file_path in self.data_dir.glob("*.pkl"):
            try:
                with open(file_path, "rb") as f:
                    data = pickle.load(f)
                key = file_path.stem
                self._data[key] = data
            except Exception as e:
                print(f"Error loading {file_path}: {e}")

    def _save_to_disk(self, key: str):
        """Save data to disk"""
        if key in self._data and self._data[key]:
            file_path = self._get_file_path(key)
            try:
                with open(file_path, "wb") as f:
                    pickle.dump(self._data[key], f)
            except Exception as e:
                print(f"Error saving {key}: {e}")

    def save(self, bar: OHLCVData) -> bool:
        """Save an OHLCV bar"""
        key = f"{bar.symbol}_{bar.timeframe}"
        if key not in self._data:
            self._data[key] = []
        self._data[key].append(bar)
        # Save to disk after each bar (for safety)
        self._save_to_disk(key)
        return True

    def save_many(self, bars: List[OHLCVData]) -> int:
        """Save multiple bars"""
        count = 0
        for bar in bars:
            if self.save(bar):
                count += 1
        return count

    def get_last_record(self, symbol: str, timeframe: str) -> Optional[OHLCVData]:
        """Get the last record for a symbol/timeframe"""
        key = f"{symbol}_{timeframe}"
        if key in self._data and self._data[key]:
            return self._data[key][-1]
        return None

    def get_all(self, symbol: str, timeframe: str) -> List[OHLCVData]:
        """Get all records for a symbol/timeframe"""
        key = f"{symbol}_{timeframe}"
        return self._data.get(key, [])

    def get_symbols(self) -> List[str]:
        """Get all unique symbols in the warehouse"""
        symbols = set()
        for key in self._data.keys():
            symbol = key.split("_")[0]
            symbols.add(symbol)
        return sorted(list(symbols))

    def get_timeframes(self, symbol: str) -> List[str]:
        """Get all timeframes available for a symbol"""
        timeframes = []
        for key in self._data.keys():
            if key.startswith(f"{symbol}_"):
                tf = key.split("_")[1]
                timeframes.append(tf)
        return sorted(timeframes)

    def get_range(
        self, symbol: str, timeframe: str, start_date: datetime, end_date: datetime
    ) -> List[OHLCVData]:
        """Get records in a date range"""
        key = f"{symbol}_{timeframe}"
        if key not in self._data:
            return []

        return [
            bar for bar in self._data[key] if start_date <= bar.timestamp <= end_date
        ]

    def get_stats(self, symbol: str, timeframe: str) -> dict:
        """Get statistics for a symbol/timeframe"""
        bars = self.get_all(symbol, timeframe)
        if not bars:
            return {"count": 0}

        return {
            "count": len(bars),
            "first_date": bars[0].timestamp.isoformat(),
            "last_date": bars[-1].timestamp.isoformat(),
            "source": bars[0].source,
            "symbol": symbol,
            "timeframe": timeframe,
        }

    def clear(self):
        """Clear all data"""
        self._data.clear()
        for file_path in self.data_dir.glob("*.pkl"):
            file_path.unlink()

    def get_summary(self) -> dict:
        """Get a summary of all data in the warehouse"""
        symbols = self.get_symbols()
        summary = {"total_symbols": len(symbols), "symbols": {}}

        for symbol in symbols:
            timeframes = self.get_timeframes(symbol)
            summary["symbols"][symbol] = {
                "timeframes": timeframes,
                "total_bars": sum([len(self.get_all(symbol, tf)) for tf in timeframes]),
            }

        return summary

    def get_total_bars(self) -> int:
        """Get total number of bars stored"""
        total = 0
        for key, bars in self._data.items():
            total += len(bars)
        return total
