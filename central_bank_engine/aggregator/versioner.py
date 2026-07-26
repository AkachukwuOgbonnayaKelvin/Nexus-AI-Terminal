"""Version Manager – handles versioning of events."""

import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class VersionManager:
    def version(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for event in events:
            # If event already has a version, increment
            if "version" in event:
                event["version"] = event.get("version", 1) + 1
            else:
                event["version"] = 1
            # Add a last_modified timestamp
            event["last_modified"] = datetime.now().isoformat()
        logger.info(f"Versioned {len(events)} events")
        return events
