"""
Intelligence Layer - Universal Intelligence Contract

This module defines the universal contract that all intelligence engines must implement.
It provides the foundation for the Global Intelligence Workspace and all downstream
intelligence engines.

Core Components:
- Evidence: Foundation of all intelligence
- IntelligenceSignal: Derived conclusions from evidence
- Risk: Assessment of potential negative outcomes
- EngineReport: Standard output of every intelligence engine
- WorkspaceSnapshot: Authoritative state of a workspace
- StandardReport: Unified output for all consumers
- BaseEngine: Universal lifecycle for all intelligence engines
"""

from intelligence.base.intelligence_engine import IntelligenceEngine
from intelligence.schemas.engine_report import EngineReport, ReportStatus
from intelligence.schemas.evidence import Evidence, EvidenceDirection, EvidenceStrength
from intelligence.schemas.intelligence_signal import (
    IntelligenceSignal,
    SignalConfidence,
    SignalType,
)
from intelligence.schemas.risk import Risk, RiskProbability, RiskSeverity
from intelligence.schemas.standard_report import StandardReport
from intelligence.schemas.workspace_snapshot import WorkspaceSnapshot

__version__ = "1.0.0"
__all__ = [
    # Evidence
    "Evidence",
    "EvidenceDirection",
    "EvidenceStrength",
    # Signals
    "IntelligenceSignal",
    "SignalType",
    "SignalConfidence",
    # Risk
    "Risk",
    "RiskSeverity",
    "RiskProbability",
    # Reports
    "EngineReport",
    "ReportStatus",
    "WorkspaceSnapshot",
    "StandardReport",
    # Base Engine
    "IntelligenceEngine",
]
