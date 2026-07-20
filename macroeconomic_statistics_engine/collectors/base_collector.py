# -*- coding: utf-8 -*-
"""Base collector for macroeconomic data"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from macroeconomic_statistics_engine.providers.base import MacroObservation
from macroeconomic_statistics_engine.providers.registry import MacroProviderRegistry


class BaseCollector(ABC):
    """Base class for macroeconomic data collectors"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.registry = MacroProviderRegistry(config)
        self._observations: List[MacroObservation] = []
    
    @abstractmethod
    def collect(self) -> List[MacroObservation]:
        """Collect macroeconomic data"""
        pass
    
    @abstractmethod
    def get_indicator_name(self) -> str:
        """Get the indicator name"""
        pass
    
    @abstractmethod
    def get_countries(self) -> List[str]:
        """Get the countries this collector supports"""
        pass
    
    def get_observations(self) -> List[MacroObservation]:
        """Get collected observations"""
        return self._observations
    
    def _add_observation(self, observation: MacroObservation):
        """Add an observation to the collection"""
        self._observations.append(observation)
    
    def _clear_observations(self):
        """Clear collected observations"""
        self._observations = []
