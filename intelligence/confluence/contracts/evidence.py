"""
Confluence Engine - Evidence Contract

Output of the Evidence Layer.
Adds quality, freshness, independence, and dependency tracking.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from .normalized_signal import NormalizedSignal


class EvidenceQuality(str, Enum):
    """Overall quality rating of evidence."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNKNOWN = "UNKNOWN"


@dataclass
class EvidenceRecord:
    """
    Enriched evidence record from the Evidence Layer.

    Adds quality assessment, dependency tracking, and effective
    weight calculations to the original NormalizedSignal.
    """

    # REQUIRED FIELDS (no defaults)
    signal: NormalizedSignal
    quality_score: float  # 0-1, overall quality
    quality_rating: EvidenceQuality  # HIGH, MEDIUM, LOW
    freshness_score: float  # 0-1, how fresh is the evidence
    independence_score: float  # 0-1, how independent from other signals

    # OPTIONAL FIELDS (with defaults)
    dependency_group: str | None = None
    dependencies: list[str] = field(default_factory=list)
    dependents: list[str] = field(default_factory=list)
    conflict_status: str = "NONE"
    effective_weight: float = 0.0
    processed_at: datetime = field(default_factory=datetime.utcnow)

    def calculate_effective_weight(self) -> float:
        """Calculate effective weight from all factors."""
        base = self.signal.effective_weight()
        quality_factor = self.quality_score
        independence_factor = self.independence_score
        freshness_factor = self.freshness_score

        self.effective_weight = (
            base * quality_factor * independence_factor * freshness_factor
        )
        return self.effective_weight

    def __repr__(self) -> str:
        return f"EvidenceRecord({self.signal.engine_id}, {self.signal.entity}, quality={self.quality_rating.value})"
