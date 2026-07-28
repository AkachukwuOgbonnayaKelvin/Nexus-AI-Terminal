"""
Market Profile Enumerations – Extended with event types, recalibration reasons, profile status.
"""

from enum import Enum


class AssetClass(str, Enum):
    FX = "fx"
    INDEX = "index"
    COMMODITY = "commodity"
    CRYPTO = "crypto"
    BOND = "bond"
    UNKNOWN = "unknown"


class Regime(str, Enum):
    TRENDING_UP = "trending_up"
    TRENDING_DOWN = "trending_down"
    RANGING = "ranging"
    BREAKOUT = "breakout"
    BREAKOUT_PENDING = "breakout_pending"
    VOLATILITY_EXPANSION = "volatility_expansion"
    VOLATILITY_CONTRACTION = "volatility_contraction"
    TRANSITION = "transition"
    MEAN_REVERSION = "mean_reversion"
    DISORDERED = "disordered"
    INSUFFICIENT_DATA = "insufficient_data"


class LifecycleState(str, Enum):
    DISCOVERED = "discovered"
    MONITORED = "monitored"
    PROFILED = "profiled"
    RANKED = "ranked"
    TOSP_CANDIDATE = "tosp_candidate"
    TOSP_SELECTED = "tosp_selected"
    DEEP_ANALYSIS_ELIGIBLE = "deep_analysis_eligible"
    DEMOTED = "demoted"
    DISQUALIFIED = "disqualified"
    UNKNOWN = "unknown"


class DataQualityStatus(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    DEGRADED = "degraded"
    STALE = "stale"
    MISSING = "missing"
    INSUFFICIENT = "insufficient"
    PARTIAL = "partial"


class ProfileDimension(str, Enum):
    TREND = "trend"
    MOMENTUM = "momentum"
    VOLATILITY = "volatility"
    RELATIVE_STRENGTH = "relative_strength"
    RELATIVE_PERFORMANCE = "relative_performance"
    LIQUIDITY = "liquidity"
    REGIME = "regime"


class TOSPFilter(str, Enum):
    MARKET_REGIME = "market_regime"
    DIRECTION_ALIGNMENT = "direction_alignment"
    OPPORTUNITY_DISCOVERY = "opportunity_discovery"
    TRADE_CLASSIFICATION = "trade_classification"
    ADMISSION_CONTROLLER = "admission_controller"
    TOP_N_SELECTION = "top_n_selection"


class RecalibrationTrigger(str, Enum):
    SCHEDULED = "scheduled"
    PRICE_SHOCK = "price_shock"
    MOMENTUM_ACCELERATION = "momentum_acceleration"
    VOLATILITY_SHOCK = "volatility_shock"
    RANGE_EXPANSION = "range_expansion"
    STRUCTURAL_INVALIDATION = "structural_invalidation"
    ACTIVITY_SHOCK = "activity_shock"
    DATA_REFRESH = "data_refresh"
    MANUAL = "manual"


class ProfileEventType(str, Enum):
    PROFILE_CREATED = "profile_created"
    PROFILE_UPDATED = "profile_updated"
    PROFILE_STRENGTHENED = "profile_strengthened"
    PROFILE_WEAKENED = "profile_weakened"
    PROFILE_INVALIDATED = "profile_invalidated"
    REGIME_CHANGED = "regime_changed"
    TOSP_ENTRY = "tosp_entry"
    TOSP_EXIT = "tosp_exit"
    DATA_QUALITY_DEGRADED = "data_quality_degraded"


class EventPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
