"""Message bus implementation."""

from collections.abc import Callable
from typing import Any


class Event:
    """Base event class."""

    def __init__(self, name: str, data: Any = None):
        self.name = name
        self.data = data


class EventBus:
    """Event bus for publish-subscribe communication."""

    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable) -> None:
        """Subscribe to an event."""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(callback)

    def publish(self, event: Event) -> None:
        """Publish an event."""
        if event.name in self._subscribers:
            for callback in self._subscribers[event.name]:
                callback(event)

    def unsubscribe(self, event_name: str, callback: Callable) -> None:
        """Unsubscribe from an event."""
        if event_name in self._subscribers:
            self._subscribers[event_name].remove(callback)
