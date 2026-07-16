"""Collector Router – routes events from collectors to the pipeline."""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class CollectorRouter:
    def route(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Route events to the next stage."""
        if not events:
            return []
        logger.info(f"Routing {len(events)} events from collectors")
        return events
