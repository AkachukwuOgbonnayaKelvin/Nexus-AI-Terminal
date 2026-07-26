"""
GLB-009 - Canonical Historical Memory Connector

Loads and provides access to canonical global windows.
"""

import json
import logging
from typing import Any

from intelligence.memory.historical.schemas import HistoricalWindow

logger = logging.getLogger(__name__)


class CanonicalMemoryConnector:
    """Connects GLB-009 to canonical historical memory"""

    def __init__(self, data_file: str | None = None):
        self.data_file = data_file
        self.windows: list[HistoricalWindow] = []
        self._loaded = False

    def load(self, data_file: str | None = None) -> bool:
        """Load canonical windows from JSON file"""
        if data_file:
            self.data_file = data_file

        if not self.data_file:
            logger.warning("No data file specified")
            return False

        try:
            with open(self.data_file, "r") as f:
                raw_data = json.load(f)

            self.windows = []
            for raw in raw_data:
                try:
                    window = HistoricalWindow(**raw)
                    if window.is_valid:
                        self.windows.append(window)
                except Exception as e:
                    logger.debug(f"Error loading window: {e}")
                    continue

            self._loaded = True
            logger.info(f"Loaded {len(self.windows)} canonical windows")
            return True

        except FileNotFoundError:
            logger.warning(f"Data file not found: {self.data_file}")
            return False
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False

    def get_windows(self) -> list[HistoricalWindow]:
        """Get all canonical windows"""
        if not self._loaded:
            self.load()
        return self.windows

    def get_symbols(self) -> list[str]:
        """Get all available symbols"""
        if not self._loaded:
            self.load()

        symbols = set()
        for w in self.windows:
            symbols.update(w.assets.keys())
        return list(symbols)

    def get_window_by_id(self, window_id: str) -> HistoricalWindow | None:
        """Get a specific window by ID"""
        if not self._loaded:
            self.load()

        for w in self.windows:
            if w.window_id == window_id:
                return w
        return None

    def is_ready(self) -> bool:
        """Check if data is loaded"""
        return self._loaded and len(self.windows) > 0

    def get_stats(self) -> dict[str, Any]:
        """Get statistics about the loaded data"""
        if not self._loaded:
            return {"status": "NOT_LOADED"}

        symbols = self.get_symbols()
        asset_coverage = {}

        for symbol in symbols:
            count = sum(1 for w in self.windows if symbol in w.assets)
            asset_coverage[symbol] = count / len(self.windows) if self.windows else 0

        return {
            "status": "READY",
            "total_windows": len(self.windows),
            "symbols": symbols,
            "symbol_count": len(symbols),
            "asset_coverage": asset_coverage,
            "min_coverage": min(asset_coverage.values()) if asset_coverage else 0,
            "max_coverage": max(asset_coverage.values()) if asset_coverage else 0,
        }
