"""
Confluence Engine - GlobalEntityRating Contract

Output of Phase 4: Global Entity Intelligence.
Represents the intelligence rating for a single global entity.
"""

from dataclasses import dataclass, field
from datetime import datetime

from .harmonized_result import ConflictLevel
from .normalized_signal import Direction, EntityType


@dataclass
class EntityDriver:
    """A driver of entity strength."""

    name: str
    strength: float  # 0-100
    direction: Direction
    confidence: float  # 0-100
    source_engines: list[str] = field(default_factory=list)


@dataclass
class EntityRisk:
    """A risk to the entity outlook."""

    name: str
    severity: float  # 0-100
    confidence: float  # 0-100
    source_engines: list[str] = field(default_factory=list)


@dataclass
class GlobalEntityRating:
    """
    Intelligence rating for a single global entity.

    This is the output of Phase 4 and input to Phase 5.
    """

    # REQUIRED FIELDS (no defaults)
    entity: str
    entity_type: EntityType
    score: float  # -100 to +100
    direction: Direction
    confidence: float  # 0-100

    # OPTIONAL FIELDS (with defaults)
    rank: int | None = None
    drivers: list[EntityDriver] = field(default_factory=list)
    risks: list[EntityRisk] = field(default_factory=list)
    supporting_engines: list[str] = field(default_factory=list)
    contradicting_engines: list[str] = field(default_factory=list)
    evidence_count: int = 0
    conflict_level: ConflictLevel = ConflictLevel.NONE
    regime_compatibility: float = 0.5
    historical_bias: Direction | None = None
    historical_confidence: float = 0.0
    horizon: str = "SHORT_TERM"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: str = "1.0"

    def is_bullish(self) -> bool:
        return self.direction == Direction.BULLISH

    def is_bearish(self) -> bool:
        return self.direction == Direction.BEARISH

    def is_neutral(self) -> bool:
        return self.direction == Direction.NEUTRAL

    def get_top_drivers(self, n: int = 3) -> list[EntityDriver]:
        """Get top N drivers by strength."""
        sorted_drivers = sorted(self.drivers, key=lambda d: d.strength, reverse=True)
        return sorted_drivers[:n]

    def get_top_risks(self, n: int = 3) -> list[EntityRisk]:
        """Get top N risks by severity."""
        sorted_risks = sorted(self.risks, key=lambda r: r.severity, reverse=True)
        return sorted_risks[:n]

    def __repr__(self) -> str:
        return f"GlobalEntityRating({self.entity}, {self.score:+.1f}, {self.direction.value}, rank={self.rank})"
