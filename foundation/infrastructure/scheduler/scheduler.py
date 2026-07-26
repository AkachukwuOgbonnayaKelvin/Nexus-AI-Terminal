"""Scheduler implementation."""

from collections.abc import Callable
from datetime import datetime
from typing import Any


class Scheduler:
    """Task scheduler."""

    def __init__(self):
        self._tasks: dict[str, dict[str, Any]] = {}

    def add_task(self, name: str, callback: Callable, interval: int) -> None:
        """Add a scheduled task."""
        self._tasks[name] = {
            "callback": callback,
            "interval": interval,
            "last_run": None,
            "next_run": datetime.now(),
        }

    def remove_task(self, name: str) -> None:
        """Remove a scheduled task."""
        self._tasks.pop(name, None)

    def run_pending(self) -> None:
        """Run all pending tasks."""
        # In production, this would check and run tasks

    def get_tasks(self) -> dict[str, Any]:
        """Get all scheduled tasks."""
        return self._tasks
