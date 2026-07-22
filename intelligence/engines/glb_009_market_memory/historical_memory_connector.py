"""
GLB-009 Historical Memory Connector
"""

import json
import logging
from typing import Dict, List, Any, Optional

from .input.schemas import HistoricalWindow
from .converters import WindowConverter

logger = logging.getLogger(__name__)


class HistoricalMemoryConnector:
    """Connects GLB-009 to historical windows data"""

    def __init__(self, data_file: str = "historical_windows_glb009.json"):
        self.data_file = data_file
        self.windows: List[HistoricalWindow] = []
        self._raw_windows = []
        self._loaded = False
        self.converter = WindowConverter()

    def load(self) -> bool:
        """Load and convert historical windows from JSON file"""
        try:
            with open(self.data_file, "r") as f:
                self._raw_windows = json.load(f)

            self._loaded = True

            # Convert all raw windows
            self.windows = self.converter.convert_batch(self._raw_windows)

            logger.info(f"Loaded {len(self.windows)} historical windows")
            return True

        except FileNotFoundError:
            logger.warning(f"Data file not found: {self.data_file}")
            return False
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False

    def get_windows(self, symbol: Optional[str] = None) -> List[HistoricalWindow]:
        """Get historical windows, optionally filtered by symbol"""
        if not self._loaded:
            self.load()

        if symbol:
            return [w for w in self.windows if w.symbol == symbol]
        return self.windows

    def get_symbols(self) -> List[str]:
        """Get all available symbols"""
        if not self._loaded:
            self.load()

        return list(set(w.symbol for w in self.windows if w.symbol))

    def is_ready(self) -> bool:
        """Check if data is loaded"""
        return self._loaded and len(self.windows) > 0

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the loaded data"""
        if not self._loaded:
            return {"status": "NOT_LOADED"}

        return {
            "status": "READY",
            "total_windows": len(self.windows),
            "symbols": self.get_symbols(),
            "symbol_count": len(self.get_symbols()),
            "file": self.data_file,
            "converted": self.converter.converted,
            "errors": self.converter.errors,
        }
