"""Confidence Engine – assigns confidence scores based on source."""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ConfidenceEngine:
    SOURCE_SCORES = {
        "official": 1.0,
        "RSS": 0.95,
        "FRED": 0.98,
        "Reuters": 0.92,
        "Bloomberg": 0.91,
        "placeholder": 0.5,
        "unknown": 0.7,
    }

    def score(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for event in events:
            source = event.get("source", "unknown")
            base_score = self.SOURCE_SCORES.get(source, 0.7)
            # Adjust based on event type (e.g., rate decisions are more reliable)
            if event.get("event_type") in ["RATE_DECISION", "MINUTES"]:
                base_score += 0.03
            confidence = min(1.0, base_score)
            event["confidence"] = confidence
        logger.info(f"Scored {len(events)} events")
        return events
