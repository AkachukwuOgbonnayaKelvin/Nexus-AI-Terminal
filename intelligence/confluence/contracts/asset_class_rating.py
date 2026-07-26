"""
Confluence Engine - AssetClassRating Contract

Output of Phase 5: Asset-Class Intelligence.
Represents the intelligence rating for a global asset class.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from .entity_rating import GlobalEntityRating
from .normalized_signal import Direction


class AssetClass(str, Enum):
    """Global asset classes."""

    FX = "FX"
    GOLD = "GOLD"
    SILVER = "SILVER"
    EQUITIES = "EQUITIES"
    BONDS = "BONDS"
    ENERGY = "ENERGY"
    METALS = "METALS"
    COMMODITIES = "COMMODITIES"
    CRYPTO = "CRYPTO"


@dataclass
class AssetClassRating:
    """
    Intelligence rating for a global asset class.

    This is the output of Phase 5 and input to Phase 6.
    """

    # REQUIRED FIELDS (no defaults)
    asset_class: AssetClass
    name: str
    score: float  # -100 to +100
    direction: Direction
    confidence: float  # 0-100

    # OPTIONAL FIELDS (with defaults)
    rank: int | None = None
    supporting_entities: list[str] = field(default_factory=list)
    supporting_ratings: list[GlobalEntityRating] = field(default_factory=list)
    drivers: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    regime_compatibility: float = 0.5
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: str = "1.0"

    def is_bullish(self) -> bool:
        return self.direction == Direction.BULLISH

    def is_bearish(self) -> bool:
        return self.direction == Direction.BEARISH

    def is_neutral(self) -> bool:
        return self.direction == Direction.NEUTRAL

    def __repr__(self) -> str:
        return f"AssetClassRating({self.name}, {self.score:+.1f}, {self.direction.value}, rank={self.rank})"
