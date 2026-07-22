"""
Confluence Engine - AssetIntelligenceFeed Contract

Output of Phase 6B: Asset Feed API.
This is SEMI-FINISHED intelligence for Asset Intelligence.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional

from .normalized_signal import Direction
from .harmonized_result import ConflictLevel


class FeedStatus(str, Enum):
    """Status of the asset feed."""

    SEMI_FINISHED = "SEMI_FINISHED"
    COMPLETE = "COMPLETE"
    PENDING = "PENDING"
    ERROR = "ERROR"


@dataclass
class CurrencyContext:
    """Currency context for asset pair analysis."""

    base_currency: str
    base_strength: float  # -100 to +100
    quote_currency: str
    quote_strength: float  # -100 to +100
    spread: float  # base - quote
    direction: Direction


@dataclass
class AssetIntelligenceFeed:
    """
    SEMI-FINISHED intelligence for a specific asset.

    This goes to Asset Intelligence for final processing.
    It contains global context but not asset-specific technical analysis.
    """

    # REQUIRED FIELDS (no defaults)
    symbol: str
    asset_type: str
    global_bias: Direction
    global_score: float
    global_confidence: float
    asset_class: str
    asset_class_score: float
    asset_class_direction: Direction

    # OPTIONAL FIELDS (with defaults)
    currency_context: Optional[CurrencyContext] = None
    supporting_evidence: List[str] = field(default_factory=list)
    contradicting_evidence: List[str] = field(default_factory=list)
    evidence_count: int = 0
    conflict_level: ConflictLevel = ConflictLevel.NONE
    global_drivers: List[str] = field(default_factory=list)
    risk_flags: List[str] = field(default_factory=list)
    global_regime: str = "UNKNOWN"
    regime_compatibility: float = 0.5
    historical_bias: Optional[Direction] = None
    historical_confidence: float = 0.0
    status: FeedStatus = FeedStatus.SEMI_FINISHED
    source: str = "CONFLUENCE_ENGINE"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: str = "1.0"

    def is_bullish(self) -> bool:
        return self.global_bias == Direction.BULLISH

    def is_bearish(self) -> bool:
        return self.global_bias == Direction.BEARISH

    def get_currency_pair_differential(self) -> float:
        """For FX pairs: get the spread between base and quote strength."""
        if not self.currency_context:
            return 0.0
        return self.currency_context.spread

    def __repr__(self) -> str:
        return f"AssetIntelligenceFeed({self.symbol}, {self.global_score:+.1f}, {self.global_bias.value}, status={self.status.value})"
