"""Continuous policy - For MKT-001 (24/7 live data)"""

from datetime import datetime, timedelta

from orchestrator.policies.base import SchedulerPolicy


class ContinuousPolicy(SchedulerPolicy):
    """Continuous execution policy for market data"""

    def __init__(self, interval_minutes: int = 1):
        self.interval_minutes = interval_minutes
        self.last_run: datetime | None = None

    def is_due(self, dataset_id: str) -> bool:
        """Check if continuous update is due"""
        if self.last_run is None:
            return True

        next_run = self.last_run + timedelta(minutes=self.interval_minutes)
        return datetime.now() >= next_run

    def get_next_run_time(self, dataset_id: str) -> datetime | None:
        if self.last_run is None:
            return datetime.now()
        return self.last_run + timedelta(minutes=self.interval_minutes)

    def mark_run(self):
        """Mark that a run has occurred"""
        self.last_run = datetime.now()
