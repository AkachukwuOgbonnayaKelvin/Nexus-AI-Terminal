"""
Confluence Engine - NormalizedSignal Contract

The canonical language spoken by GLB-001 through GLB-009.
All engines must output this format for the Confluence Engine.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any


class Direction(str, Enum):
    """Direction of the signal."""

    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"


class SignalType(str, Enum):
    """Type of signal being produced."""

    CURRENCY_BIAS = "CURRENCY_BIAS"
    INDEX_BIAS = "INDEX_BIAS"
    COMMODITY_BIAS = "COMMODITY_BIAS"
    BOND_BIAS = "BOND_BIAS"
    ASSET_BIAS = "ASSET_BIAS"
    REGIME_CLASSIFICATION = "REGIME_CLASSIFICATION"
    RISK_ASSESSMENT = "RISK_ASSESSMENT"
    MACRO_INDICATOR = "MACRO_INDICATOR"


class EntityType(str, Enum):
    """Type of entity being analyzed."""

    CURRENCY = "CURRENCY"
    INDEX = "INDEX"
    COMMODITY = "COMMODITY"
    BOND = "BOND"
    RATE = "RATE"
    ASSET_CLASS = "ASSET_CLASS"
    REGIME = "REGIME"


@dataclass
class NormalizedSignal:
    """
    Canonical signal format for all GLB engines.

    Every engine output is normalized to this structure before
    entering the Confluence Engine pipeline.
    """

    # REQUIRED FIELDS (no defaults)
    engine_id: str  # e.g., "GLB-001", "GLB-003"
    domain: str  # e.g., "REGIME", "MACRO"
    entity: str  # e.g., "USD", "EUR", "XAUUSD"
    entity_type: EntityType  # CURRENCY, INDEX, COMMODITY, etc.
    signal_type: SignalType  # CURRENCY_BIAS, REGIME_CLASSIFICATION, etc.
    score: float  # -100 to +100
    direction: Direction  # BULLISH, BEARISH, NEUTRAL
    confidence: float  # 0-100
    reliability: float  # 0-1
    freshness: float  # 0-1, how recent is the data
    evidence_quality: float  # 0-1, quality of underlying evidence
    timestamp: datetime  # When the signal was generated

    # OPTIONAL FIELDS (with defaults)
    drivers: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    source_data: Dict[str, Any] = field(default_factory=dict)
    horizon: str = "SHORT_TERM"  # SHORT_TERM, MEDIUM_TERM, LONG_TERM
    version: str = "1.0"

    def is_bullish(self) -> bool:
        return self.direction == Direction.BULLISH

    def is_bearish(self) -> bool:
        return self.direction == Direction.BEARISH

    def is_neutral(self) -> bool:
        return self.direction == Direction.NEUTRAL

    def effective_weight(self) -> float:
        """Calculate effective weight for this signal."""
        return (
            self.reliability
            * (self.confidence / 100.0)
            * self.freshness
            * self.evidence_quality
        )

    def __repr__(self) -> str:
        return f"NormalizedSignal({self.engine_id}, {self.entity}, {self.score:+.1f}, {self.direction.value})"
