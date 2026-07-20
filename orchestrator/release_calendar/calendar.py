# -*- coding: utf-8 -*-
"""Release Calendar - Tracks official data release schedules"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class ReleaseSchedule:
    """Schedule for a data release"""
    dataset_id: str
    frequency: str  # daily, weekly, monthly, quarterly, annual, event
    day_of_week: Optional[int] = None  # 0=Monday, 6=Sunday
    day_of_month: Optional[int] = None
    time_of_day: str = "00:00"
    timezone: str = "UTC"
    release_delay: int = 0  # minutes after scheduled time
    retry_interval: int = 60  # minutes between retries
    max_retries: int = 5


class ReleaseCalendar:
    """Manages release schedules for all datasets"""
    
    def __init__(self, calendar_file: Optional[Path] = None):
        self.calendar_file = calendar_file or Path("orchestrator/release_calendar/schedules.json")
        self.schedules: Dict[str, ReleaseSchedule] = {}
        self._load()
    
    def _load(self):
        """Load schedules from file"""
        if self.calendar_file.exists():
            try:
                with open(self.calendar_file) as f:
                    data = json.load(f)
                for key, value in data.items():
                    self.schedules[key] = ReleaseSchedule(
                        dataset_id=value["dataset_id"],
                        frequency=value["frequency"],
                        day_of_week=value.get("day_of_week"),
                        day_of_month=value.get("day_of_month"),
                        time_of_day=value.get("time_of_day", "00:00"),
                        timezone=value.get("timezone", "UTC"),
                        release_delay=value.get("release_delay", 0),
                        retry_interval=value.get("retry_interval", 60),
                        max_retries=value.get("max_retries", 5)
                    )
            except Exception as e:
                print(f"Error loading calendar: {e}")
    
    def save(self):
        """Save schedules to file"""
        data = {}
        for key, schedule in self.schedules.items():
            data[key] = {
                "dataset_id": schedule.dataset_id,
                "frequency": schedule.frequency,
                "day_of_week": schedule.day_of_week,
                "day_of_month": schedule.day_of_month,
                "time_of_day": schedule.time_of_day,
                "timezone": schedule.timezone,
                "release_delay": schedule.release_delay,
                "retry_interval": schedule.retry_interval,
                "max_retries": schedule.max_retries
            }
        self.calendar_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.calendar_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def register(self, schedule: ReleaseSchedule):
        self.schedules[schedule.dataset_id] = schedule
        self.save()
    
    def get_next_release(self, dataset_id: str) -> Optional[datetime]:
        """Get the next expected release time for a dataset"""
        schedule = self.schedules.get(dataset_id)
        if not schedule:
            return None
        
        now = datetime.now()
        
        if schedule.frequency == "daily":
            next_release = now.replace(hour=int(schedule.time_of_day.split(':')[0]), 
                                       minute=int(schedule.time_of_day.split(':')[1]), 
                                       second=0, microsecond=0)
            if next_release < now:
                next_release += timedelta(days=1)
            return next_release
        
        elif schedule.frequency == "weekly":
            days_ahead = (schedule.day_of_week - now.weekday()) % 7
            if days_ahead == 0 and now.hour >= int(schedule.time_of_day.split(':')[0]):
                days_ahead = 7
            next_release = now + timedelta(days=days_ahead)
            next_release = next_release.replace(hour=int(schedule.time_of_day.split(':')[0]),
                                                minute=int(schedule.time_of_day.split(':')[1]),
                                                second=0, microsecond=0)
            return next_release
        
        elif schedule.frequency == "monthly":
            if now.day > schedule.day_of_month:
                next_month = now.month + 1 if now.month < 12 else 1
                next_year = now.year + 1 if now.month == 12 else now.year
                next_release = datetime(next_year, next_month, schedule.day_of_month)
            else:
                next_release = datetime(now.year, now.month, schedule.day_of_month)
            next_release = next_release.replace(hour=int(schedule.time_of_day.split(':')[0]),
                                                minute=int(schedule.time_of_day.split(':')[1]),
                                                second=0, microsecond=0)
            return next_release
        
        elif schedule.frequency in ["quarterly", "annual", "event"]:
            # For these, we need explicit dates
            return None
        
        return None
