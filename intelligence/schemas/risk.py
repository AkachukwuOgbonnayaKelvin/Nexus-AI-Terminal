# -*- coding: utf-8 -*-
"""Risk Assessment Schema - Identifies and evaluates risks"""

from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RiskSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskProbability(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


@dataclass
class Risk:
    """
    Risk represents potential negative outcomes.

    Every intelligence report must identify and assess risks.
    """

    # REQUIRED fields (no defaults)
    risk_id: str
    name: str
    category: str
    description: str
    impact: str

    # OPTIONAL fields with defaults
    severity: RiskSeverity = RiskSeverity.MEDIUM
    probability: RiskProbability = RiskProbability.MEDIUM

    # OPTIONAL fields with None default
    mitigation: Optional[str] = None
    source: Optional[str] = None

    # FACTORY defaults
    score: float = 0.0
    triggered: bool = False
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "risk_id": self.risk_id,
            "name": self.name,
            "category": self.category,
            "severity": self.severity.value,
            "probability": self.probability.value,
            "score": self.score,
            "description": self.description,
            "impact": self.impact,
            "mitigation": self.mitigation,
            "triggered": self.triggered,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Risk":
        """Create from dictionary"""
        return cls(
            risk_id=data["risk_id"],
            name=data["name"],
            category=data["category"],
            description=data["description"],
            impact=data["impact"],
            severity=RiskSeverity(data.get("severity", "MEDIUM")),
            probability=RiskProbability(data.get("probability", "MEDIUM")),
            mitigation=data.get("mitigation"),
            source=data.get("source"),
            score=data.get("score", 0.0),
            triggered=data.get("triggered", False),
            timestamp=datetime.fromisoformat(data["timestamp"])
            if "timestamp" in data
            else datetime.now(),
            metadata=data.get("metadata", {}),
        )

    def calculate_score(self) -> float:
        """Calculate risk score from severity and probability"""
        severity_map = {
            RiskSeverity.LOW: 20,
            RiskSeverity.MEDIUM: 50,
            RiskSeverity.HIGH: 75,
            RiskSeverity.CRITICAL: 100,
        }
        probability_map = {
            RiskProbability.LOW: 20,
            RiskProbability.MEDIUM: 50,
            RiskProbability.HIGH: 75,
            RiskProbability.VERY_HIGH: 100,
        }
        self.score = (
            severity_map[self.severity] + probability_map[self.probability]
        ) / 2
        return self.score
