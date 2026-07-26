from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class EngineBias(Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"


class MarketRegime(Enum):
    TRENDING_UP = "trending_up"
    TRENDING_DOWN = "trending_down"
    RANGING = "ranging"
    CONSOLIDATING = "consolidating"
    EXPANDING = "expanding"
    CONTRACTING = "contracting"
    UNKNOWN = "unknown"


class SignalConfidence(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class TechnicalSignal:
    engine: str
    symbol: str
    timeframe: str
    timestamp: datetime
    bias: EngineBias
    direction: str
    confidence: float
    regime: MarketRegime
    regime_confidence: float
    key_levels: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    invalidation_level: float | None = None
    invalidation_condition: str | None = None
    reasoning: list[str] = field(default_factory=list)
    data_quality: float = 1.0
    data_gaps: bool = False
    version: str = "1.0"
    processing_time_ms: float | None = None
    data_range_start: datetime | None = None
    data_range_end: datetime | None = None
    extras: dict[str, Any] = field(default_factory=dict)


@dataclass
class OHLCRequest:
    symbol: str
    timeframe: str
    start: datetime
    end: datetime
    max_bars: int | None = None


@dataclass
class TickRequest:
    symbol: str
    start: datetime
    end: datetime
    max_ticks: int | None = 100000


@dataclass
class VolumeRequest:
    symbol: str
    start: datetime
    end: datetime
    aggregate: str = "1m"
