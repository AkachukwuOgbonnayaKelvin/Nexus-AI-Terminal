"""
Global Intelligence Hub - Immutable Snapshot

Snapshots are immutable records of the global state at a point in time.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class GlobalSnapshot:
    """
    Immutable snapshot of the global intelligence state.

    Once created, a snapshot CANNOT be modified.
    This ensures historical integrity for audit and backtesting.
    """

    # Identity
    snapshot_id: str
    state_id: str

    # Timestamps
    generated_at: datetime
    valid_until: datetime

    # The actual state (stored as a tuple of key-value pairs for immutability)
    _state_items: tuple

    # Lineage
    previous_snapshot_id: str | None = None
    source: str = "GLOBAL_INTELLIGENCE_HUB"

    # Version
    schema_version: str = "1.0.0"

    @classmethod
    def from_state(cls, state, snapshot_id: str) -> "GlobalSnapshot":
        """Create a snapshot from a state object."""
        # Convert state to immutable tuple of items
        state_items = tuple(sorted(state.__dict__.items()))
        return cls(
            snapshot_id=snapshot_id,
            state_id=state.state_id,
            generated_at=state.generated_at,
            valid_until=state.valid_until,
            _state_items=state_items,
            previous_snapshot_id=getattr(state, "previous_state_id", None),
        )

    def get_state_data(self) -> dict[str, Any]:
        """Get state data as a dictionary (read-only copy)."""
        return dict(self._state_items)

    def is_expired(self) -> bool:
        """Check if the snapshot has expired."""
        return datetime.utcnow() > self.valid_until

    def age_seconds(self) -> float:
        """Get age in seconds since generation."""
        return (datetime.utcnow() - self.generated_at).total_seconds()

    def get_freshness_status(self) -> str:
        """Get freshness status."""
        if self.is_expired():
            return "EXPIRED"
        age = self.age_seconds()
        if age < 600:  # < 10 minutes
            return "CURRENT"
        elif age < 1800:  # < 30 minutes
            return "AGING"
        elif age < 3600:  # < 1 hour
            return "STALE"
        else:
            return "EXPIRED"

    def __repr__(self) -> str:
        return f"GlobalSnapshot(snapshot_id={self.snapshot_id}, state_id={self.state_id}, expired={self.is_expired()})"
