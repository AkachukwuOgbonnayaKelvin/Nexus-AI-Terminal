# -*- coding: utf-8 -*-
"""Event-driven policy - For ECO-002, CENT-001"""

from datetime import datetime, timedelta
from typing import Optional, Callable

from orchestrator.policies.base import SchedulerPolicy


class EventDrivenPolicy(SchedulerPolicy):
    """Event-driven execution policy"""
    
    def __init__(self, event_check_fn: Optional[Callable] = None):
        self.event_check_fn = event_check_fn
        self.last_check: Optional[datetime] = None
        self.pending_events: dict = {}
    
    def is_due(self, dataset_id: str) -> bool:
        """Check if an event-driven dataset is due"""
        # Check if there are pending events
        if self.pending_events.get(dataset_id, False):
            return True
        
        # Check for new events
        if self.event_check_fn:
            events = self.event_check_fn(dataset_id)
            if events:
                self.pending_events[dataset_id] = True
                return True
        
        return False
    
    def get_next_run_time(self, dataset_id: str) -> Optional[datetime]:
        return datetime.now() if self.is_due(dataset_id) else None
    
    def mark_event_processed(self, dataset_id: str):
        """Mark that an event has been processed"""
        self.pending_events[dataset_id] = False
    
    def set_event_check_fn(self, fn: Callable):
        self.event_check_fn = fn
