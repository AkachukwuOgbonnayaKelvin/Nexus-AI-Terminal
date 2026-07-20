# -*- coding: utf-8 -*-
"""MAC-001 Warehouse Repository with File Persistence"""

import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime


class GDPObservation:
    """GDP observation model for warehouse storage"""
    def __init__(self, country: str, period: str, value: float, currency: str = "USD"):
        self.country = country
        self.period = period
        self.value = value
        self.currency = currency
        self.timestamp = datetime.now().isoformat()
        self.record_id = f"{country}_{period}_{currency}"
    
    def to_dict(self) -> dict:
        return {
            "country": self.country,
            "period": self.period,
            "value": self.value,
            "currency": self.currency,
            "timestamp": self.timestamp,
            "record_id": self.record_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GDPObservation':
        obs = cls(data["country"], data["period"], data["value"], data["currency"])
        obs.timestamp = data.get("timestamp", datetime.now().isoformat())
        return obs


class GDPRepository:
    """Repository for GDP observations with file persistence"""
    
    def __init__(self, data_file: str = "macroeconomic_statistics_engine/data/gdp_data.json"):
        self.data_file = Path(data_file)
        self._observations = []
        self._load()
    
    def _load(self):
        if self.data_file.exists():
            try:
                with open(self.data_file) as f:
                    data = json.load(f)
                self._observations = [GDPObservation.from_dict(d) for d in data]
            except Exception as e:
                print(f"Error loading GDP data: {e}")
                self._observations = []
    
    def _save(self):
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        data = [obs.to_dict() for obs in self._observations]
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def save_from_provider(self, provider_obs) -> bool:
        """Save a GDP observation from provider format"""
        if hasattr(provider_obs, 'record_id'):
            record_id = provider_obs.record_id
        else:
            record_id = f"{provider_obs.country}_{provider_obs.period}_{provider_obs.currency}"
        
        if self.exists(record_id):
            return False
        
        obs = GDPObservation(
            country=provider_obs.country,
            period=provider_obs.period,
            value=provider_obs.value,
            currency=provider_obs.currency
        )
        self._observations.append(obs)
        self._save()
        return True
    
    def save(self, observation: GDPObservation) -> bool:
        if not self.exists(observation.record_id):
            self._observations.append(observation)
            self._save()
            return True
        return False
    
    def save_many(self, observations: List) -> int:
        count = 0
        for obs in observations:
            if hasattr(obs, 'record_id'):
                if self.save(obs):
                    count += 1
            else:
                # Handle provider observations
                if self.save_from_provider(obs):
                    count += 1
        return count
    
    def exists(self, record_id: str) -> bool:
        return any(o.record_id == record_id for o in self._observations)
    
    def get_latest(self, country: str = None) -> Optional[GDPObservation]:
        if not self._observations:
            return None
        if country:
            filtered = [o for o in self._observations if o.country == country]
            if not filtered:
                return None
            return max(filtered, key=lambda x: x.period)
        return max(self._observations, key=lambda x: x.period)
    
    def get_all(self) -> List[GDPObservation]:
        return self._observations.copy()
    
    def get_count(self) -> int:
        return len(self._observations)
    
    def get_by_id(self, record_id: str) -> Optional[GDPObservation]:
        for obs in self._observations:
            if obs.record_id == record_id:
                return obs
        return None
    
    def get_by_country(self, country: str) -> List[GDPObservation]:
        return [o for o in self._observations if o.country == country]
    
    def clear(self):
        self._observations = []
        self._save()
