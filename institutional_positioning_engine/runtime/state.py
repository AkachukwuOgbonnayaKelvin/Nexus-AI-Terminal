"""COT Runtime State – tracks runtime status."""

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class COTRuntimeState:
    """Persistent state for COT runtime."""

    def __init__(self, state_file: str = "data/state/cot_runtime.json"):
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self._state = self._load_state()

    def _load_state(self) -> dict:
        """Load state from file."""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_state(self) -> None:
        """Save state to file."""
        try:
            with open(self.state_file, "w") as f:
                json.dump(self._state, f, default=str)
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

    async def get_last_run(self) -> datetime | None:
        """Get the last run time."""
        last_run = self._state.get("last_run")
        if last_run:
            return datetime.fromisoformat(last_run)
        return None

    async def update_last_run(self, timestamp: datetime) -> None:
        """Update the last run time."""
        self._state["last_run"] = timestamp.isoformat()
        self._save_state()

    async def get_last_report(self) -> str | None:
        """Get the last processed report ID."""
        return self._state.get("last_report")

    async def update_last_report(self, report_id: str) -> None:
        """Update the last processed report ID."""
        self._state["last_report"] = report_id
        self._save_state()

    async def get_backfill_status(self) -> dict:
        """Get backfill status."""
        return self._state.get("backfill", {"complete": False, "records": 0})

    async def update_backfill_status(self, processed: int, records: int) -> None:
        """Update backfill status."""
        self._state["backfill"] = {
            "complete": True,
            "processed": processed,
            "records": records,
            "completed_at": datetime.now().isoformat(),
        }
        self._save_state()
