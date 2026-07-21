# -*- coding: utf-8 -*-
"""Evidence Schema - Foundation of all intelligence"""

from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class EvidenceDirection(str, Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"
    MIXED = "MIXED"


class EvidenceStrength(str, Enum):
    WEAK = "WEAK"
    MODERATE = "MODERATE"
    STRONG = "STRONG"
    VERY_STRONG = "VERY_STRONG"


@dataclass
class Evidence:
    """
    Evidence is the foundational building block of all intelligence.

    Every conclusion in the system must be backed by evidence.
    Evidence traces back to source data and provides auditability.
    """

    # REQUIRED fields (no defaults)
    evidence_id: str
    source_engine: str
    source_contract: str
    metric: str
    value: float
    period: str

    # OPTIONAL fields with defaults
    direction: EvidenceDirection = EvidenceDirection.NEUTRAL
    confidence: float = 80.0
    strength: EvidenceStrength = EvidenceStrength.MODERATE

    # OPTIONAL fields with None default
    country: Optional[str] = None
    asset: Optional[str] = None
    source_url: Optional[str] = None

    # FACTORY defaults
    retrieved_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "evidence_id": self.evidence_id,
            "source_engine": self.source_engine,
            "source_contract": self.source_contract,
            "metric": self.metric,
            "value": self.value,
            "direction": self.direction.value,
            "period": self.period,
            "country": self.country,
            "asset": self.asset,
            "confidence": self.confidence,
            "strength": self.strength.value,
            "retrieved_at": self.retrieved_at.isoformat(),
            "source_url": self.source_url,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Evidence":
        """Create from dictionary"""
        return cls(
            evidence_id=data["evidence_id"],
            source_engine=data["source_engine"],
            source_contract=data["source_contract"],
            metric=data["metric"],
            value=data["value"],
            period=data["period"],
            direction=EvidenceDirection(data.get("direction", "NEUTRAL")),
            confidence=data.get("confidence", 80.0),
            strength=EvidenceStrength(data.get("strength", "MODERATE")),
            country=data.get("country"),
            asset=data.get("asset"),
            source_url=data.get("source_url"),
            retrieved_at=datetime.fromisoformat(data["retrieved_at"])
            if "retrieved_at" in data
            else datetime.now(),
            metadata=data.get("metadata", {}),
        )
