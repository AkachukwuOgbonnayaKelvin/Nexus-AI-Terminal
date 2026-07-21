# -*- coding: utf-8 -*-
"""Base scheduler policy"""

from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime


class SchedulerPolicy(ABC):
    """Base class for scheduler policies"""

    @abstractmethod
    def is_due(self, dataset_id: str) -> bool:
        """Check if a dataset is due for execution"""
        pass

    @abstractmethod
    def get_next_run_time(self, dataset_id: str) -> Optional[datetime]:
        """Get the next scheduled run time"""
        pass
