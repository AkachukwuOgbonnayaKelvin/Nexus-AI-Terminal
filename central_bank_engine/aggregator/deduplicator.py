"""Deduplicator – merges duplicate events from different sources."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class Deduplicator:
    def deduplicate(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen = {}
        deduped = []
        for event in events:
            # Use a composite key: bank + event_type + title (or a hash)
            key = f"{event.get('bank')}_{event.get('event_type')}_{event.get('title', '')[:50]}"
            if key in seen:
                # Merge metadata (keep the most complete)
                existing = seen[key]
                # Prefer non-None values
                for k, v in event.items():
                    if v and not existing.get(k):
                        existing[k] = v
                # Keep the most confident
                if event.get("confidence", 0) > existing.get("confidence", 0):
                    existing["confidence"] = event["confidence"]
                    existing["source"] = event.get("source", "unknown")
                logger.debug(f"Duplicate merged for {key}")
            else:
                seen[key] = event
                deduped.append(event)
        logger.info(f"Deduplicated {len(events)} -> {len(deduped)} events")
        return deduped
