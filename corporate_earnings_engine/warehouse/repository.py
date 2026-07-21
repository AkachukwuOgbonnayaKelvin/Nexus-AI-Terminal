# -*- coding: utf-8 -*-
"""ECO-002 Warehouse Repository with File Persistence"""

import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime


class EarningsObservation:
    """Earnings observation model for warehouse storage"""

    def __init__(
        self, symbol: str, period: str, actual_eps: float, estimated_eps: float = None
    ):
        self.symbol = symbol
        self.period = period
        self.actual_eps = actual_eps
        self.estimated_eps = estimated_eps
        self.timestamp = datetime.now().isoformat()
        self.record_id = f"{symbol}_{period}_EPS"

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "period": self.period,
            "actual_eps": self.actual_eps,
            "estimated_eps": self.estimated_eps,
            "timestamp": self.timestamp,
            "record_id": self.record_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "EarningsObservation":
        obs = cls(
            data["symbol"],
            data["period"],
            data["actual_eps"],
            data.get("estimated_eps"),
        )
        obs.timestamp = data.get("timestamp", datetime.now().isoformat())
        return obs


class EarningsRepository:
    """Repository for earnings observations with file persistence"""

    def __init__(
        self, data_file: str = "corporate_earnings_engine/data/earnings_data.json"
    ):
        self.data_file = Path(data_file)
        self._observations = []
        self._load()

    def _load(self):
        if self.data_file.exists():
            try:
                with open(self.data_file) as f:
                    data = json.load(f)
                self._observations = [EarningsObservation.from_dict(d) for d in data]
            except Exception as e:
                print(f"Error loading earnings data: {e}")
                self._observations = []

    def _save(self):
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        data = [obs.to_dict() for obs in self._observations]
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2)

    def save_from_provider(self, provider_obs) -> bool:
        """Save an earnings observation from provider format"""
        if hasattr(provider_obs, "record_id"):
            record_id = provider_obs.record_id
        else:
            record_id = f"{provider_obs.symbol}_{provider_obs.period}_EPS"

        if self.exists(record_id):
            return False

        obs = EarningsObservation(
            symbol=provider_obs.symbol,
            period=provider_obs.period,
            actual_eps=provider_obs.actual_eps,
            estimated_eps=provider_obs.estimated_eps,
        )
        self._observations.append(obs)
        self._save()
        return True

    def save(self, observation: EarningsObservation) -> bool:
        if not self.exists(observation.record_id):
            self._observations.append(observation)
            self._save()
            return True
        return False

    def save_many(self, observations: List) -> int:
        count = 0
        for obs in observations:
            if hasattr(obs, "record_id"):
                if self.save(obs):
                    count += 1
            else:
                if self.save_from_provider(obs):
                    count += 1
        return count

    def exists(self, record_id: str) -> bool:
        return any(o.record_id == record_id for o in self._observations)

    def get_latest(self, symbol: str = None) -> Optional[EarningsObservation]:
        if not self._observations:
            return None
        if symbol:
            filtered = [o for o in self._observations if o.symbol == symbol]
            if not filtered:
                return None
            return max(filtered, key=lambda x: x.period)
        return max(self._observations, key=lambda x: x.period)

    def get_all(self) -> List[EarningsObservation]:
        return self._observations.copy()

    def get_count(self) -> int:
        return len(self._observations)

    def get_by_id(self, record_id: str) -> Optional[EarningsObservation]:
        for obs in self._observations:
            if obs.record_id == record_id:
                return obs
        return None

    def get_by_symbol(self, symbol: str) -> List[EarningsObservation]:
        return [o for o in self._observations if o.symbol == symbol]

    def clear(self):
        self._observations = []
        self._save()
