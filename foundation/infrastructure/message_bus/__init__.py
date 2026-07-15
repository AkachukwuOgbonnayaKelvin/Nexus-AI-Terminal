"""Message bus.

Provides event-driven communication between components.
"""

from .bus import Event, EventBus

__all__ = ["EventBus", "Event"]
