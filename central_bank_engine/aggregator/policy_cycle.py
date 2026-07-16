"""Policy Cycle Builder – groups events into policy cycles."""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class PolicyCycleBuilder:
    def build(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not events:
            return events
        # Group events by bank and approximate month
        groups = {}
        for event in events:
            bank = event.get("bank")
            release_time = event.get("release_time")
            if isinstance(release_time, str):
                release_time = datetime.fromisoformat(release_time.replace("Z", "+00:00"))
            if not release_time:
                continue
            # Create a cycle key: bank + year + month
            cycle_key = f"{bank}_{release_time.year}_{release_time.month:02d}"
            if cycle_key not in groups:
                groups[cycle_key] = []
            groups[cycle_key].append(event)

        # Assign policy_cycle_id to each event
        for cycle_key, group in groups.items():
            # Use the first event's release time as reference
            first_time = group[0].get("release_time")
            if isinstance(first_time, str):
                first_time = datetime.fromisoformat(first_time.replace("Z", "+00:00"))
            cycle_id = f"{group[0].get('bank', 'CB').replace(' ', '_')}_{first_time.strftime('%Y_%m')}"
            for event in group:
                event["policy_cycle_id"] = cycle_id

        logger.info(f"Assigned policy_cycle_id to {len(events)} events")
        return events
