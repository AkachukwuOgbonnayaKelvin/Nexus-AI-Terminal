"""Collector Router – routes events from collectors to the pipeline."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class CollectorRouter:
    def route(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Route events to the next stage."""
        if not events:
            return []
        logger.info(f"Routing {len(events)} events from collectors")
        return events
