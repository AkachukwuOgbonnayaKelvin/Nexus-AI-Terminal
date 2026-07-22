"""
Market Positioning Warehouse

Stores and manages institutional positioning data from multiple sources.
"""

import json
import logging
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class PositioningWarehouse:
    """
    Warehouse for institutional positioning data.

    Data stored:
    - COT (Commitment of Traders) data
    - Fund flows
    - Institutional long/short positions
    - Smart money indicators
    """

    def __init__(self, storage_path: str = "./data/positioning"):
        self.storage_path = storage_path
        self._cot_data: List[Dict] = []
        self._fund_flows: List[Dict] = []
        self._institutional_positions: List[Dict] = []
        self._load()

    def _load(self) -> None:
        """Load existing data from disk."""
        try:
            os.makedirs(self.storage_path, exist_ok=True)
            if os.path.exists(f"{self.storage_path}/cot.json"):
                with open(f"{self.storage_path}/cot.json", "r") as f:
                    self._cot_data = json.load(f)
            if os.path.exists(f"{self.storage_path}/fund_flows.json"):
                with open(f"{self.storage_path}/fund_flows.json", "r") as f:
                    self._fund_flows = json.load(f)
            if os.path.exists(f"{self.storage_path}/institutional.json"):
                with open(f"{self.storage_path}/institutional.json", "r") as f:
                    self._institutional_positions = json.load(f)
        except Exception as e:
            logger.warning(f"Could not load positioning data: {e}")

    def _save(self) -> None:
        """Save data to disk."""
        try:
            os.makedirs(self.storage_path, exist_ok=True)
            with open(f"{self.storage_path}/cot.json", "w") as f:
                json.dump(self._cot_data, f, default=str)
            with open(f"{self.storage_path}/fund_flows.json", "w") as f:
                json.dump(self._fund_flows, f, default=str)
            with open(f"{self.storage_path}/institutional.json", "w") as f:
                json.dump(self._institutional_positions, f, default=str)
        except Exception as e:
            logger.error(f"Failed to save positioning data: {e}")

    def store_cot(self, data: Dict[str, Any]) -> None:
        """Store COT data."""
        record = {**data, "stored_at": datetime.utcnow().isoformat()}
        self._cot_data.append(record)
        self._save()

    def store_fund_flows(self, data: Dict[str, Any]) -> None:
        """Store fund flow data."""
        record = {**data, "stored_at": datetime.utcnow().isoformat()}
        self._fund_flows.append(record)
        self._save()

    def store_institutional_positions(self, data: Dict[str, Any]) -> None:
        """Store institutional positioning data."""
        record = {**data, "stored_at": datetime.utcnow().isoformat()}
        self._institutional_positions.append(record)
        self._save()

    def get_cot(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get COT data."""
        if symbol:
            return [r for r in self._cot_data if r.get("symbol") == symbol]
        return self._cot_data

    def get_fund_flows(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get fund flow data."""
        if symbol:
            return [r for r in self._fund_flows if r.get("symbol") == symbol]
        return self._fund_flows

    def get_institutional_positions(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get institutional positioning data."""
        if symbol:
            return [
                r for r in self._institutional_positions if r.get("symbol") == symbol
            ]
        return self._institutional_positions

    def get_stats(self) -> Dict[str, int]:
        """Get storage statistics."""
        return {
            "cot_records": len(self._cot_data),
            "fund_flow_records": len(self._fund_flows),
            "institutional_records": len(self._institutional_positions),
        }
