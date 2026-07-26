"""Base collector for macroeconomic data"""

import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from macroeconomic_statistics_engine.providers.base import MacroObservation
from macroeconomic_statistics_engine.providers.registry import MacroProviderRegistry


class BaseCollector(ABC):
    """Base class for macroeconomic data collectors"""

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.registry = MacroProviderRegistry(config)
        self._observations: list[MacroObservation] = []

    @abstractmethod
    def collect(self) -> list[MacroObservation]:
        """Collect macroeconomic data"""

    @abstractmethod
    def get_indicator_name(self) -> str:
        """Get the indicator name"""

    @abstractmethod
    def get_countries(self) -> list[str]:
        """Get the countries this collector supports"""

    def get_observations(self) -> list[MacroObservation]:
        """Get collected observations"""
        return self._observations

    def _add_observation(self, observation: MacroObservation):
        """Add an observation to the collection"""
        self._observations.append(observation)

    def _clear_observations(self):
        """Clear collected observations"""
        self._observations = []
