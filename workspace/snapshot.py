"""
Workspace Snapshot Contract

This is the immutable contract between the backend intelligence
and the frontend GUI. The GUI should only consume this snapshot.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class WorkspaceSnapshot(BaseModel):
    """
    Global Intelligence Workspace Snapshot.

    This is the single source of truth for the GUI.
    """

    snapshot_id: str
    version: str = "1.0.0"
    generated_at: datetime

    # Core Intelligence
    market_regime: dict[str, Any]
    macro_intelligence: dict[str, Any]
    asset_intelligence: dict[str, Any]

    # Consensus & Confidence
    consensus: dict[str, Any]
    confidence: dict[str, Any]

    # Evidence & Risk
    evidence_matrix: dict[str, Any]
    risk_matrix: dict[str, Any]

    # Summary
    executive_summary: str
    ai_context: dict[str, Any]

    # Health
    health: dict[str, Any]
    metadata: dict[str, Any]
