"""
Workspace Snapshot Service

Manages the creation and retrieval of workspace snapshots.
"""

import logging
from datetime import datetime
from typing import Any

from intelligence.hub import GlobalIntelligenceHub

from .snapshot import WorkspaceSnapshot

logger = logging.getLogger(__name__)


class SnapshotService:
    """
    Service for managing workspace snapshots.
    """

    def __init__(self):
        self.hub = GlobalIntelligenceHub()
        self.last_snapshot: WorkspaceSnapshot | None = None

    def collect_report(self, engine_id: str, report: Any) -> bool:
        """
        Collect a report from an intelligence engine.
        """
        return self.hub.collect_report(engine_id, report)

    def build_snapshot(self) -> WorkspaceSnapshot:
        """
        Build a new workspace snapshot.
        """
        # Build the hub snapshot
        hub_snapshot = self.hub.build_snapshot()

        # Convert to WorkspaceSnapshot
        snapshot = WorkspaceSnapshot(
            snapshot_id=hub_snapshot["snapshot_id"],
            version=hub_snapshot["version"],
            generated_at=datetime.fromisoformat(hub_snapshot["generated_at"]),
            market_regime=hub_snapshot["market_regime"],
            macro_intelligence=hub_snapshot["macro_intelligence"],
            asset_intelligence=hub_snapshot["asset_intelligence"],
            consensus=hub_snapshot["consensus"],
            confidence=hub_snapshot.get(
                "confidence", {"overall_confidence": 0, "status": "UNKNOWN"}
            ),
            evidence_matrix=hub_snapshot["evidence_matrix"],
            risk_matrix=hub_snapshot["risk_matrix"],
            executive_summary=hub_snapshot["executive_summary"],
            ai_context=hub_snapshot["ai_context"],
            health=hub_snapshot["health"],
            metadata=hub_snapshot["metadata"],
        )

        self.last_snapshot = snapshot
        logger.info(f"Workspace snapshot built: {snapshot.snapshot_id}")
        return snapshot

    def get_last_snapshot(self) -> WorkspaceSnapshot | None:
        """
        Get the last built snapshot.
        """
        return self.last_snapshot

    def health_check(self) -> dict[str, Any]:
        """
        Check service health.
        """
        return {
            "service": "SnapshotService",
            "status": "OPERATIONAL",
            "has_snapshot": self.last_snapshot is not None,
            "hub_health": self.hub.health_check(),
        }
