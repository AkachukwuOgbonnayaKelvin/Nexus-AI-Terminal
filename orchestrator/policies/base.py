"""Base scheduler policy"""

from abc import ABC, abstractmethod
from datetime import datetime


class SchedulerPolicy(ABC):
    """Base class for scheduler policies"""

    @abstractmethod
    def is_due(self, dataset_id: str) -> bool:
        """Check if a dataset is due for execution"""

    @abstractmethod
    def get_next_run_time(self, dataset_id: str) -> datetime | None:
        """Get the next scheduled run time"""
