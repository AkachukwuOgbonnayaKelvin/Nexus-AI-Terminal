# -*- coding: utf-8 -*-
"""Base acquisition module"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

from domain.models import Tick, OHLCV


class BaseAcquirer(ABC):
    """Base class for data acquisition"""

    @abstractmethod
    def acquire_tick(self, symbol: str) -> Optional[Tick]:
        """Acquire current tick data"""
        pass

    @abstractmethod
    def acquire_ohlcv(self, symbol: str, timeframe: str, count: int) -> List[OHLCV]:
        """Acquire OHLCV data"""
        pass

    @abstractmethod
    def acquire_symbols(self) -> List[str]:
        """Acquire list of available symbols"""
        pass

    @abstractmethod
    def get_health(self) -> Dict[str, Any]:
        """Get acquirer health status"""
        pass
