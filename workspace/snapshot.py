"""
Workspace Snapshot Contract

This is the immutable contract between the backend intelligence
and the frontend GUI. The GUI should only consume this snapshot.
"""

from datetime import datetime
from typing import Dict, Any
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
    market_regime: Dict[str, Any]
    macro_intelligence: Dict[str, Any]
    asset_intelligence: Dict[str, Any]

    # Consensus & Confidence
    consensus: Dict[str, Any]
    confidence: Dict[str, Any]

    # Evidence & Risk
    evidence_matrix: Dict[str, Any]
    risk_matrix: Dict[str, Any]

    # Summary
    executive_summary: str
    ai_context: Dict[str, Any]

    # Health
    health: Dict[str, Any]
    metadata: Dict[str, Any]
