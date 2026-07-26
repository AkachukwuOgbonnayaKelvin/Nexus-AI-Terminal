"""Release-aware policy - For MAC-001, COT-001"""

from datetime import datetime, timedelta

from orchestrator.policies.base import SchedulerPolicy
from orchestrator.release_calendar.calendar import ReleaseCalendar


class ReleaseAwarePolicy(SchedulerPolicy):
    """Release-aware execution policy"""

    def __init__(self, release_calendar: ReleaseCalendar):
        self.calendar = release_calendar
        self.release_detected: dict = {}
        self.retry_count: dict = {}

    def is_due(self, dataset_id: str) -> bool:
        """Check if a release-aware dataset is due"""
        # Check if release has already been processed
        if self.release_detected.get(dataset_id, False):
            return False

        # Get next expected release
        next_release = self.calendar.get_next_release(dataset_id)
        if next_release is None:
            return False

        # Check if we're within the release window
        now = datetime.now()

        # Release window: 30 minutes before to 6 hours after
        window_start = next_release - timedelta(minutes=30)
        window_end = next_release + timedelta(hours=6)

        if window_start <= now <= window_end:
            # Check if we've retried too many times
            retries = self.retry_count.get(dataset_id, 0)
            max_retries = 5
            if retries >= max_retries:
                return False
            return True

        return False

    def get_next_run_time(self, dataset_id: str) -> datetime | None:
        """Get the next expected release time"""
        return self.calendar.get_next_release(dataset_id)

    def mark_release_complete(self, dataset_id: str):
        """Mark a release as complete"""
        self.release_detected[dataset_id] = True
        self.retry_count[dataset_id] = 0

    def mark_retry(self, dataset_id: str):
        """Mark a retry attempt"""
        self.retry_count[dataset_id] = self.retry_count.get(dataset_id, 0) + 1
