"""
Market Profile Configuration – Updated with scheduling, event thresholds, TOSP hysteresis.
"""

from dataclasses import dataclass, field


@dataclass
class DataQualityConfig:
    min_bars: int = 50
    max_stale_hours: dict[str, float] = field(
        default_factory=lambda: {
            "H1": 2.0,
            "H4": 8.0,
            "D1": 48.0,
            "default": 24.0,
        }
    )
    max_gap_percentage: float = 0.10


@dataclass
class AnalyzerWeights:
    # Asset-class-specific weights for the 7 analyzers
    fx: dict[str, float] = field(
        default_factory=lambda: {
            "trend": 0.20,
            "momentum": 0.20,
            "volatility": 0.15,
            "relative_strength": 0.25,
            "relative_performance": 0.05,
            "liquidity": 0.10,
            "regime": 0.05,
        }
    )
    index: dict[str, float] = field(
        default_factory=lambda: {
            "trend": 0.25,
            "momentum": 0.20,
            "volatility": 0.15,
            "relative_strength": 0.15,
            "relative_performance": 0.10,
            "liquidity": 0.05,
            "regime": 0.10,
        }
    )
    commodity: dict[str, float] = field(
        default_factory=lambda: {
            "trend": 0.20,
            "momentum": 0.20,
            "volatility": 0.25,
            "relative_strength": 0.10,
            "relative_performance": 0.10,
            "liquidity": 0.05,
            "regime": 0.10,
        }
    )
    crypto: dict[str, float] = field(
        default_factory=lambda: {
            "trend": 0.25,
            "momentum": 0.25,
            "volatility": 0.20,
            "relative_strength": 0.10,
            "relative_performance": 0.05,
            "liquidity": 0.10,
            "regime": 0.05,
        }
    )
    bond: dict[str, float] = field(
        default_factory=lambda: {
            "trend": 0.25,
            "momentum": 0.20,
            "volatility": 0.15,
            "relative_strength": 0.15,
            "relative_performance": 0.10,
            "liquidity": 0.05,
            "regime": 0.10,
        }
    )

    def get_weights(self, asset_class: str) -> dict[str, float]:
        mapping = {
            "fx": self.fx,
            "index": self.index,
            "commodity": self.commodity,
            "crypto": self.crypto,
            "bond": self.bond,
        }
        return mapping.get(asset_class.lower(), self.fx)


@dataclass
class TOSPConfig:
    max_candidates: int = 20
    min_opportunity_score: float = 70.0  # 0-100 scale
    min_data_confidence: float = 85.0  # 0-100 scale
    require_lifecycle: list[str] = field(
        default_factory=lambda: ["developing", "high_priority", "peak_opportunity"]
    )
    min_acceleration: float = 0.0
    apply_regime_filter: bool = True
    apply_direction_alignment: bool = True
    # Hysteresis for promotion/demotion
    promotion_threshold: float = 80.0  # Enter TOSP if score >= this
    demotion_threshold: float = 72.0  # Remain in TOSP if score >= this
    demote_after_stale_hours: float = 48.0  # Remove if data stale for this long


@dataclass
class ScheduleConfig:
    macro_refresh_hours: float = 12.0  # W1/D1
    structural_refresh_hours: float = 4.0  # H4
    tactical_refresh_hours: float = 1.0  # H1
    micro_refresh_minutes: float = 15.0  # M15/M5/M1


@dataclass
class EventThresholds:
    price_shock_atr: float = 1.5  # Price change > this * ATR triggers recalibration
    momentum_acceleration: float = (
        0.02  # Momentum change > this (0-1) triggers recalibration
    )
    volatility_shock_ratio: float = 1.5  # ATR / baseline > this triggers recalibration
    range_expansion_ratio: float = (
        1.5  # Current range / previous range > this triggers recalibration
    )
    activity_shock_ratio: float = (
        2.0  # Volume/tick activity > baseline * this triggers recalibration
    )


@dataclass
class MarketProfileConfig:
    data_quality: DataQualityConfig = field(default_factory=DataQualityConfig)
    weights: AnalyzerWeights = field(default_factory=AnalyzerWeights)
    tosp: TOSPConfig = field(default_factory=TOSPConfig)
    schedule: ScheduleConfig = field(default_factory=ScheduleConfig)
    events: EventThresholds = field(default_factory=EventThresholds)
    lookback_bars: int = 100
    acceleration_window: int = 4
    # Data quality scoring weights
    data_quality_weight: float = 0.15  # How much data quality influences final score
