# -*- coding: utf-8 -*-
"""Intelligence Signal Schema - Derived from evidence"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from intelligence.schemas.evidence import Evidence


class SignalType(str, Enum):
    """Types of signals that can be generated"""

    # Market direction
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"

    # Market state
    RISK_ON = "RISK_ON"
    RISK_OFF = "RISK_OFF"
    TRANSITIONING = "TRANSITIONING"

    # Economic
    EXPANDING = "EXPANDING"
    CONTRACTING = "CONTRACTING"
    STABLE = "STABLE"

    # Policy
    HAWKISH = "HAWKISH"
    DOVISH = "DOVISH"
    NEUTRAL_POLICY = "NEUTRAL_POLICY"


class SignalConfidence(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


@dataclass
class IntelligenceSignal:
    """
    Intelligence Signal is derived from evidence.

    A signal represents a conclusion about market conditions,
    economic state, or policy direction.
    """

    # REQUIRED fields (no defaults)
    signal_id: str
    signal_type: SignalType
    name: str
    direction: SignalType

    # OPTIONAL fields with defaults
    strength: float = 50.0
    confidence: float = 80.0
    confidence_level: SignalConfidence = SignalConfidence.MEDIUM

    # OPTIONAL fields with None default
    description: Optional[str] = None

    # FACTORY defaults
    supporting_evidence: List[Evidence] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    time_horizon: str = "daily"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "signal_id": self.signal_id,
            "signal_type": self.signal_type.value,
            "name": self.name,
            "direction": self.direction.value,
            "strength": self.strength,
            "supporting_evidence": [e.to_dict() for e in self.supporting_evidence],
            "confidence": self.confidence,
            "confidence_level": self.confidence_level.value,
            "timestamp": self.timestamp.isoformat(),
            "time_horizon": self.time_horizon,
            "description": self.description,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "IntelligenceSignal":
        """Create from dictionary"""
        return cls(
            signal_id=data["signal_id"],
            signal_type=SignalType(data["signal_type"]),
            name=data["name"],
            direction=SignalType(data["direction"]),
            strength=data.get("strength", 50.0),
            confidence=data.get("confidence", 80.0),
            confidence_level=SignalConfidence(data.get("confidence_level", "MEDIUM")),
            description=data.get("description"),
            supporting_evidence=[
                Evidence.from_dict(e) for e in data.get("supporting_evidence", [])
            ],
            timestamp=datetime.fromisoformat(data["timestamp"])
            if "timestamp" in data
            else datetime.now(),
            time_horizon=data.get("time_horizon", "daily"),
            metadata=data.get("metadata", {}),
        )

    def add_evidence(self, evidence: Evidence):
        """Add supporting evidence"""
        self.supporting_evidence.append(evidence)

    @property
    def evidence_count(self) -> int:
        """Number of supporting evidence pieces"""
        return len(self.supporting_evidence)

    @property
    def average_confidence(self) -> float:
        """Average confidence of supporting evidence"""
        if not self.supporting_evidence:
            return self.confidence
        return sum(e.confidence for e in self.supporting_evidence) / len(
            self.supporting_evidence
        )
