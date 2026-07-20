import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class Validator:
    REQUIRED_FIELDS = ["event_id", "bank", "country", "currency", "event_type", "title"]

    def validate(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        valid_events = []
        for event in events:
            missing = [f for f in self.REQUIRED_FIELDS if not event.get(f)]
            if missing:
                logger.warning(
                    f"Skipping event missing fields: {missing} - {event.get('title', 'unknown')}"
                )
                continue
            # If release_time is missing, set it to now
            if "release_time" not in event or not event["release_time"]:
                event["release_time"] = datetime.now().isoformat()
                logger.debug(f"Added release_time for {event.get('title')}")
            # Validate timestamp format
            if isinstance(event["release_time"], str):
                try:
                    datetime.fromisoformat(event["release_time"].replace("Z", "+00:00"))
                except ValueError:
                    logger.warning(
                        f"Invalid timestamp format: {event['release_time']}, using current time"
                    )
                    event["release_time"] = datetime.now().isoformat()
            valid_events.append(event)
        logger.info(f"Validated {len(valid_events)} / {len(events)} events")
        return valid_events
