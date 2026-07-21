# -*- coding: utf-8 -*-
"""Workspace Snapshot Schema - Authoritative state of a workspace"""

from typing import List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

from intelligence.schemas.engine_report import EngineReport


@dataclass
class WorkspaceSnapshot:
    """
    Workspace Snapshot is the authoritative state of a workspace.

    This is the single source of truth for the workspace.
    All downstream consumers should read from the snapshot.
    """

    # REQUIRED fields (no defaults)
    snapshot_id: str
    workspace: str
    version: str

    # OPTIONAL fields with defaults
    status: str = "FINAL"

    # FACTORY defaults
    timestamp: datetime = field(default_factory=datetime.now)
    engine_reports: List[EngineReport] = field(default_factory=list)
    consensus: Dict[str, Any] = field(default_factory=dict)
    executive_summary: Dict[str, Any] = field(default_factory=dict)
    executive_ai_context: Dict[str, Any] = field(default_factory=dict)
    ui_dataset: Dict[str, Any] = field(default_factory=dict)
    evidence_matrix: Dict[str, float] = field(default_factory=dict)
    standard_report: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "snapshot_id": self.snapshot_id,
            "workspace": self.workspace,
            "version": self.version,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status,
            "engine_reports": [r.to_dict() for r in self.engine_reports],
            "consensus": self.consensus,
            "executive_summary": self.executive_summary,
            "executive_ai_context": self.executive_ai_context,
            "ui_dataset": self.ui_dataset,
            "evidence_matrix": self.evidence_matrix,
            "standard_report": self.standard_report,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WorkspaceSnapshot":
        """Create from dictionary"""
        from intelligence.schemas.engine_report import EngineReport

        return cls(
            snapshot_id=data["snapshot_id"],
            workspace=data["workspace"],
            version=data["version"],
            status=data.get("status", "FINAL"),
            timestamp=datetime.fromisoformat(data["timestamp"])
            if "timestamp" in data
            else datetime.now(),
            engine_reports=[
                EngineReport.from_dict(r) for r in data.get("engine_reports", [])
            ],
            consensus=data.get("consensus", {}),
            executive_summary=data.get("executive_summary", {}),
            executive_ai_context=data.get("executive_ai_context", {}),
            ui_dataset=data.get("ui_dataset", {}),
            evidence_matrix=data.get("evidence_matrix", {}),
            standard_report=data.get("standard_report", {}),
        )

    def add_report(self, report: EngineReport):
        """Add an engine report to the snapshot"""
        self.engine_reports.append(report)

    @property
    def report_count(self) -> int:
        """Number of engine reports"""
        return len(self.engine_reports)

    @property
    def is_complete(self) -> bool:
        """Check if all expected reports are present"""
        return len(self.engine_reports) > 0

    @property
    def top_confidence(self) -> float:
        """Highest confidence among reports"""
        if not self.engine_reports:
            return 0.0
        return max(r.confidence for r in self.engine_reports)

    @property
    def average_confidence(self) -> float:
        """Average confidence across all reports"""
        if not self.engine_reports:
            return 0.0
        return sum(r.confidence for r in self.engine_reports) / len(self.engine_reports)
