"""
Confluence Engine - HarmonizedResult Contract

Output of the Harmonization Core (Phase 3).
Represents the synthesized intelligence for a single entity.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict

from .normalized_signal import Direction
from .evidence import EvidenceRecord


class ConflictLevel(str, Enum):
    """Level of conflict in the evidence."""

    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass
class HarmonizedResult:
    """
    Harmonized intelligence for a single entity.

    This is the output of Phase 3 and the primary input to Phase 4.
    """

    # REQUIRED FIELDS (no defaults)
    entity: str
    entity_type: str
    consensus_score: float
    final_score: float
    direction: Direction
    confidence: float
    agreement_ratio: float
    conflict_level: ConflictLevel
    conflict_penalty: float
    evidence_count: int

    # OPTIONAL FIELDS (with defaults)
    supporting_engines: List[str] = field(default_factory=list)
    contradicting_engines: List[str] = field(default_factory=list)
    evidence_records: List[EvidenceRecord] = field(default_factory=list)
    drivers: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    weighted_contributions: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: str = "1.0"

    def is_bullish(self) -> bool:
        return self.direction == Direction.BULLISH

    def is_bearish(self) -> bool:
        return self.direction == Direction.BEARISH

    def is_neutral(self) -> bool:
        return self.direction == Direction.NEUTRAL

    def has_conflict(self) -> bool:
        return self.conflict_level in [ConflictLevel.MEDIUM, ConflictLevel.HIGH]

    def __repr__(self) -> str:
        return f"HarmonizedResult({self.entity}, {self.final_score:+.1f}, {self.direction.value})"
