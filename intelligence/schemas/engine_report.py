# -*- coding: utf-8 -*-
"""Engine Report Schema - Standard output of every intelligence engine"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from intelligence.schemas.evidence import Evidence
from intelligence.schemas.intelligence_signal import IntelligenceSignal
from intelligence.schemas.risk import Risk


class ReportStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    ERROR = "error"
    PENDING = "pending"


@dataclass
class EngineReport:
    """
    Engine Report is the standard output of every intelligence engine.

    All engines (GLB-001 to GLB-008) must produce this report format.
    This ensures the Global Intelligence Hub can consume all engines uniformly.
    """

    # REQUIRED fields (no defaults)
    report_id: str
    engine_id: str
    engine_name: str
    domain: str

    # OPTIONAL fields with defaults
    version: str = "1.0.0"
    status: ReportStatus = ReportStatus.SUCCESS
    overall_score: float = 50.0
    confidence: float = 70.0

    # OPTIONAL fields with None default
    direction: Optional[str] = None
    risk_level: Optional[str] = None
    regime: Optional[str] = None
    summary: Optional[str] = None

    # FACTORY defaults
    scope: Dict[str, Any] = field(default_factory=dict)
    signals: List[IntelligenceSignal] = field(default_factory=list)
    evidence: List[Evidence] = field(default_factory=list)
    risks: List[Risk] = field(default_factory=list)
    top_drivers: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "report_id": self.report_id,
            "engine_id": self.engine_id,
            "engine_name": self.engine_name,
            "domain": self.domain,
            "version": self.version,
            "status": self.status.value,
            "scope": self.scope,
            "overall_score": self.overall_score,
            "confidence": self.confidence,
            "direction": self.direction,
            "risk_level": self.risk_level,
            "regime": self.regime,
            "signals": [s.to_dict() for s in self.signals],
            "evidence": [e.to_dict() for e in self.evidence],
            "risks": [r.to_dict() for r in self.risks],
            "top_drivers": self.top_drivers,
            "summary": self.summary,
            "recommendations": self.recommendations,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "EngineReport":
        """Create from dictionary"""
        from intelligence.schemas.evidence import Evidence
        from intelligence.schemas.intelligence_signal import IntelligenceSignal
        from intelligence.schemas.risk import Risk

        return cls(
            report_id=data["report_id"],
            engine_id=data["engine_id"],
            engine_name=data["engine_name"],
            domain=data["domain"],
            version=data.get("version", "1.0.0"),
            status=ReportStatus(data.get("status", "success")),
            scope=data.get("scope", {}),
            overall_score=data.get("overall_score", 50.0),
            confidence=data.get("confidence", 70.0),
            direction=data.get("direction"),
            risk_level=data.get("risk_level"),
            regime=data.get("regime"),
            summary=data.get("summary"),
            signals=[IntelligenceSignal.from_dict(s) for s in data.get("signals", [])],
            evidence=[Evidence.from_dict(e) for e in data.get("evidence", [])],
            risks=[Risk.from_dict(r) for r in data.get("risks", [])],
            top_drivers=data.get("top_drivers", []),
            recommendations=data.get("recommendations", []),
            metadata=data.get("metadata", {}),
            timestamp=datetime.fromisoformat(data["timestamp"])
            if "timestamp" in data
            else datetime.now(),
        )

    def add_signal(self, signal: IntelligenceSignal):
        """Add a signal to the report"""
        self.signals.append(signal)

    def add_evidence(self, evidence: Evidence):
        """Add evidence to the report"""
        self.evidence.append(evidence)

    def add_risk(self, risk: Risk):
        """Add a risk to the report"""
        self.risks.append(risk)

    def add_driver(self, name: str, impact: str, score: float):
        """Add a top driver"""
        self.top_drivers.append({"driver": name, "impact": impact, "score": score})

    @property
    def is_success(self) -> bool:
        """Check if report status is success"""
        return self.status == ReportStatus.SUCCESS

    @property
    def signal_count(self) -> int:
        """Number of signals"""
        return len(self.signals)

    @property
    def evidence_count(self) -> int:
        """Number of evidence pieces"""
        return len(self.evidence)

    @property
    def risk_count(self) -> int:
        """Number of risks"""
        return len(self.risks)

    @property
    def driver_count(self) -> int:
        """Number of top drivers"""
        return len(self.top_drivers)
