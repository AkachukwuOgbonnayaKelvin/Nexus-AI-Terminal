"""Domain models for Market Price Engine"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class AssetClass(str, Enum):
    FOREX = "forex"
    INDICES = "indices"
    COMMODITIES = "commodities"
    BONDS = "bonds"
    METALS = "metals"
    CRYPTO = "crypto"
    STOCKS = "stocks"
    ETFS = "etfs"


class Timeframe(str, Enum):
    TICK = "tick"
    M1 = "M1"
    M5 = "M5"
    M15 = "M15"
    M30 = "M30"
    H1 = "H1"
    H4 = "H4"
    D1 = "D1"
    W1 = "W1"
    MN1 = "MN1"


class SourceType(str, Enum):
    PRIMARY = "primary"
    VALIDATION = "validation"
    RESEARCH = "research"
    FALLBACK = "fallback"


class DataStatus(str, Enum):
    VALID = "valid"
    ANOMALY = "anomaly"
    MISSING = "missing"
    DELAYED = "delayed"
    PENDING = "pending"


@dataclass
class Tick:
    """Tick data model"""

    timestamp: datetime
    symbol: str
    bid: float
    ask: float
    spread: float | None = None
    volume: float | None = None
    source: str = "unknown"
    quality_score: float = 100.0
    provenance: dict[str, Any] = field(default_factory=dict)

    @property
    def mid_price(self) -> float:
        return (self.bid + self.ask) / 2


@dataclass
class OHLCV:
    """OHLCV bar data model"""

    timestamp: datetime
    symbol: str
    timeframe: str
    open: float
    high: float
    low: float
    close: float
    tick_volume: float | None = None
    real_volume: float | None = None
    spread: float | None = None
    source: str = "unknown"
    quality_score: float = 100.0
    provenance: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate OHLCV data integrity"""
        return (
            self.high >= self.low
            and self.high >= self.open
            and self.high >= self.close
            and self.low <= self.open
            and self.low <= self.close
        )


@dataclass
class MarketSnapshot:
    """Current market snapshot"""

    timestamp: datetime
    symbol: str
    bid: float
    ask: float
    spread: float
    last_price: float
    session: str | None = None
    source: str = "unknown"
    quality_score: float = 100.0


@dataclass
class Instrument:
    """Instrument metadata"""

    symbol: str
    asset_class: AssetClass
    description: str
    broker_symbol: str | None = None
    exchange: str | None = None
    currency: str | None = None
    contract_size: float | None = None
    pip_size: float | None = None
    min_volume: float | None = None
    max_volume: float | None = None
    margin_required: float | None = None
    is_active: bool = True
    source: str = "unknown"


@dataclass
class QualityMetrics:
    """Data quality metrics"""

    symbol: str
    timestamp: datetime
    freshness: float
    completeness: float
    consistency: float
    accuracy: float
    overall_score: float
    gap_count: int = 0
    duplicate_count: int = 0
    outlier_count: int = 0
    missing_count: int = 0
    status: DataStatus = DataStatus.VALID
    source: str = "unknown"
