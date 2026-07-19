"""COT Runtime Configuration."""


class COTRuntimeConfig:
    """Configuration for COT runtime."""

    def __init__(self):
        self.schedule = {
            "weekly_day": 4,  # Friday
            "weekly_hour": 22,  # 10 PM UTC
            "enabled": True,
        }
        self.backfill = {
            "start_year": 2006,
            "end_year": None,  # None = current year
            "enabled": True,
        }
        self.download = {
            "retry_count": 3,
            "retry_delay": 2,
            "timeout": 30,
        }

    def get_schedule(self) -> dict:
        return self.schedule

    def get_backfill_config(self) -> dict:
        return self.backfill

    def get_download_config(self) -> dict:
        return self.download
