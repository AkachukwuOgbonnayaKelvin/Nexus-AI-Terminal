"""Standard Report Schema - Unified output for all consumers"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class StandardReport:
    """
    Standard Report is the unified output format for all consumers.

    This is what the Master Orchestrator and other downstream
    consumers receive. It is a standardized, simplified version
    of the Workspace Snapshot.
    """

    # REQUIRED fields (no defaults)
    report_id: str
    domain: str

    # OPTIONAL fields with defaults
    report_type: str = "intelligence_report"
    version: str = "1.0.0"
    overall_score: float = 50.0
    confidence: float = 70.0

    # OPTIONAL fields with None default
    direction: str | None = None
    risk_level: str | None = None
    summary: str | None = None

    # FACTORY defaults
    timestamp: datetime = field(default_factory=datetime.now)
    top_drivers: list[str] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    consumers: list[str] = field(
        default_factory=lambda: ["asset_intelligence", "master_orchestrator"]
    )
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "report_id": self.report_id,
            "domain": self.domain,
            "type": self.report_type,
            "timestamp": self.timestamp.isoformat(),
            "version": self.version,
            "data": {
                "overall_score": self.overall_score,
                "confidence": self.confidence,
                "direction": self.direction,
                "risk_level": self.risk_level,
                "top_drivers": self.top_drivers,
                "evidence": self.evidence,
                "summary": self.summary,
                "recommendations": self.recommendations,
            },
            "consumers": self.consumers,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StandardReport":
        """Create from dictionary"""
        report_data = data.get("data", {})
        return cls(
            report_id=data["report_id"],
            domain=data["domain"],
            report_type=data.get("type", "intelligence_report"),
            timestamp=datetime.fromisoformat(data["timestamp"])
            if "timestamp" in data
            else datetime.now(),
            version=data.get("version", "1.0.0"),
            overall_score=report_data.get("overall_score", 50.0),
            confidence=report_data.get("confidence", 70.0),
            direction=report_data.get("direction"),
            risk_level=report_data.get("risk_level"),
            summary=report_data.get("summary"),
            top_drivers=report_data.get("top_drivers", []),
            evidence=report_data.get("evidence", []),
            recommendations=report_data.get("recommendations", []),
            consumers=data.get(
                "consumers", ["asset_intelligence", "master_orchestrator"]
            ),
            metadata=data.get("metadata", {}),
        )

    def add_evidence(self, engine: str, contribution: float):
        """Add evidence to the report"""
        self.evidence.append({"engine": engine, "contribution": contribution})

    def add_driver(self, driver: str):
        """Add a top driver"""
        self.top_drivers.append(driver)

    def add_recommendation(self, recommendation: str):
        """Add a recommendation"""
        self.recommendations.append(recommendation)

    def to_snapshot(self) -> dict:
        """Convert to a snapshot-compatible format"""
        return {
            "standard_report": self.to_dict(),
            "version": self.version,
            "domain": self.domain,
            "timestamp": self.timestamp.isoformat(),
        }

    @property
    def is_high_confidence(self) -> bool:
        """Check if confidence is high"""
        return self.confidence >= 80.0

    @property
    def is_positive(self) -> bool:
        """Check if direction is positive"""
        return self.direction in ["BULLISH", "RISK_ON", "EXPANDING"]

    @property
    def evidence_count(self) -> int:
        """Number of evidence pieces"""
        return len(self.evidence)

    @property
    def driver_count(self) -> int:
        """Number of top drivers"""
        return len(self.top_drivers)
