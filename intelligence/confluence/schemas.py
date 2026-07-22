"""
Confluence Engine - Canonical Schemas

All GLB engines must eventually speak this common language.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


class SignalType(str, Enum):
    """Type of signal from an engine"""

    CURRENCY_BIAS = "CURRENCY_BIAS"
    ASSET_BIAS = "ASSET_BIAS"
    ASSET_CLASS_BIAS = "ASSET_CLASS_BIAS"
    REGIME = "REGIME"
    RISK = "RISK"
    MACRO = "MACRO"
    EVENT = "EVENT"
    POLICY = "POLICY"
    FLOW = "FLOW"
    SENTIMENT = "SENTIMENT"
    MEMORY = "MEMORY"


class Direction(str, Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"


class ConflictLevel(str, Enum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


# ============================================================
# NORMALIZED SIGNAL
# ============================================================


class NormalizedSignal(BaseModel):
    """
    Canonical signal from any GLB engine.

    All engines must eventually produce this format.
    """

    engine_id: str
    domain: str
    entity: str  # e.g., "USD", "EURUSD", "GOLD"
    signal_type: SignalType

    # Core signal
    score: float = Field(ge=-100, le=100)
    direction: Direction
    confidence: float = Field(ge=0, le=100)

    # Metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    freshness: float = Field(ge=0, le=1, default=0.9)

    # Drivers and evidence
    drivers: List[str] = Field(default_factory=list)
    evidence_quality: float = Field(ge=0, le=1, default=0.7)
    reliability: float = Field(ge=0, le=1, default=0.7)

    # Source details
    raw_report: Optional[Dict[str, Any]] = None

    def is_fresh(self, max_age_seconds: int = 3600) -> bool:
        """Check if signal is fresh."""
        age = (datetime.utcnow() - self.timestamp).total_seconds()
        return age < max_age_seconds


# ============================================================
# EVIDENCE
# ============================================================


class Evidence(BaseModel):
    """Consolidated evidence from one or more engines"""

    signal_id: str
    entity: str
    signal_type: SignalType

    # Consolidated signal
    score: float = Field(ge=-100, le=100)
    direction: Direction
    confidence: float = Field(ge=0, le=100)

    # Source engines
    source_engines: List[str]
    source_count: int

    # Quality metrics
    average_reliability: float = Field(ge=0, le=1)
    freshness: float = Field(ge=0, le=1)
    evidence_quality: float = Field(ge=0, le=1)

    # Agreement
    agreement_ratio: float = Field(ge=0, le=1)
    conflict_level: ConflictLevel

    # Drivers
    drivers: List[str] = Field(default_factory=list)

    # Raw signals
    raw_signals: List[NormalizedSignal] = Field(default_factory=list)


# ============================================================
# CURRENCY RATING
# ============================================================


class CurrencyRating(BaseModel):
    """Rating for a single currency"""

    currency: str
    score: float = Field(ge=-100, le=100)
    direction: Direction
    rank: int
    confidence: float = Field(ge=0, le=100)

    supporting_engines: List[str] = Field(default_factory=list)
    contradicting_engines: List[str] = Field(default_factory=list)

    drivers: List[str] = Field(default_factory=list)
    conflict_level: ConflictLevel

    evidence_count: int
    evidence_quality: float = Field(ge=0, le=1)


# ============================================================
# ASSET CLASS RATING
# ============================================================


class AssetClassRating(BaseModel):
    """Rating for an asset class"""

    asset_class: str
    score: float = Field(ge=-100, le=100)
    direction: Direction
    confidence: float = Field(ge=0, le=100)

    drivers: List[str] = Field(default_factory=list)
    supporting_engines: List[str] = Field(default_factory=list)

    evidence_count: int


# ============================================================
# ASSET RATING
# ============================================================


class AssetRating(BaseModel):
    """Rating for a specific tradable asset"""

    asset: str
    asset_class: str
    score: float = Field(ge=-100, le=100)
    direction: Direction
    confidence: float = Field(ge=0, le=100)

    # Currency breakdown for FX pairs
    base_currency_score: Optional[float] = None
    quote_currency_score: Optional[float] = None

    supporting_engines: List[str] = Field(default_factory=list)
    conflicts: List[str] = Field(default_factory=list)

    drivers: List[str] = Field(default_factory=list)
    evidence_count: int


# ============================================================
# CONFLUENCE REPORT
# ============================================================


class Opportunity(BaseModel):
    """Trading opportunity"""

    asset: str
    action: str  # BUY, SELL, HOLD
    score: float = Field(ge=-100, le=100)
    confidence: float = Field(ge=0, le=100)
    drivers: List[str] = Field(default_factory=list)


class Risk(BaseModel):
    """Identified risk"""

    description: str
    category: str
    severity: str  # HIGH, MEDIUM, LOW
    probability: float = Field(ge=0, le=1)
    affected_assets: List[str] = Field(default_factory=list)


class ConfluenceReport(BaseModel):
    """Complete Confluence Engine output"""

    engine_id: str = "CONFLUENCE"
    engine_name: str = "Global Intelligence Confluence Engine"
    version: str = "1.0.0"
    status: str = "OPERATIONAL"
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    # Global State
    global_regime: Optional[str] = None
    global_risk_score: float = Field(ge=0, le=100, default=50)
    dominant_theme: str = "UNKNOWN"
    global_confidence: float = Field(ge=0, le=100, default=50)

    # Rankings
    currency_rankings: List[CurrencyRating] = Field(default_factory=list)
    asset_class_rankings: List[AssetClassRating] = Field(default_factory=list)
    asset_ratings: List[AssetRating] = Field(default_factory=list)

    # Opportunities and Risks
    top_opportunities: List[Opportunity] = Field(default_factory=list)
    top_risks: List[Risk] = Field(default_factory=list)

    # Engine Status
    engines_processed: List[str] = Field(default_factory=list)
    engines_missing: List[str] = Field(default_factory=list)

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
