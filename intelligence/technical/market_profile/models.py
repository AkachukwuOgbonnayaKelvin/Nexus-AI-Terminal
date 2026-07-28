"""
Market Profile Data Models – Extended with state, event, versioning.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .enums import (
    AssetClass,
    DataQualityStatus,
    EventPriority,
    LifecycleState,
    ProfileEventType,
    RecalibrationTrigger,
)


@dataclass
class DataQualityReport:
    status: DataQualityStatus
    bars_available: int
    latest_age_hours: float
    gap_percentage: float
    ohlc_valid: bool
    timestamp_sequence_valid: bool
    reason: str | None = None
    coverage_percentage: float = 0.0


@dataclass
class ProfileDimensionScore:
    dimension: str
    score: float  # 0-1
    direction: str | None = None
    regime: str | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class AssetProfile:
    symbol: str
    asset_class: AssetClass
    group: str
    timestamp: datetime
    data_quality: DataQualityReport
    trend: ProfileDimensionScore
    momentum: ProfileDimensionScore
    volatility: ProfileDimensionScore
    relative_strength: ProfileDimensionScore
    relative_performance: ProfileDimensionScore
    liquidity: ProfileDimensionScore
    regime: ProfileDimensionScore
    opportunity_score: float
    acceleration: float
    lifecycle_state: LifecycleState
    data_confidence: float
    raw_scores: dict[str, float] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)
    # New fields for state and versioning
    profile_version: int = 0
    previous_profile_version: int | None = None
    recalibration_trigger: RecalibrationTrigger | None = None
    last_calculated_at: datetime | None = None
    next_scheduled_check: datetime | None = None
    last_material_change_at: datetime | None = None


@dataclass
class Candidate:
    symbol: str
    asset_class: AssetClass
    profile: AssetProfile
    opportunity_score: float
    acceleration: float
    lifecycle_state: LifecycleState
    data_confidence: float
    tosp_filters_passed: list[str]
    rank: int
    reason: str
    # TOSP state
    tosp_entry_time: datetime | None = None
    tosp_exit_time: datetime | None = None


@dataclass
class ProfileEvent:
    event_type: ProfileEventType
    symbol: str
    timestamp: datetime
    priority: EventPriority
    old_profile_version: int | None = None
    new_profile_version: int | None = None
    old_score: float | None = None
    new_score: float | None = None
    old_regime: str | None = None
    new_regime: str | None = None
    trigger: RecalibrationTrigger | None = None
    reason: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ProfileState:
    """Persistent state for a symbol's profile."""

    symbol: str
    asset_class: AssetClass
    current_profile: AssetProfile | None = None
    previous_profile: AssetProfile | None = None
    profile_history: list[AssetProfile] = field(default_factory=list)
    profile_version: int = 0
    last_calculated_at: datetime | None = None
    next_scheduled_check: datetime | None = None
    profile_valid: bool = True
    invalidation_reason: str | None = None
    tosp_status: bool = False  # Currently in TOSP?
    tosp_entry_time: datetime | None = None


@dataclass
class QualitySummary:
    total_assets: int
    excellent: int
    good: int
    degraded: int
    stale: int
    missing: int
    rejected_freshness: int
    rejected_missing_ohlc: int
    rejected_insufficient_bars: int
    rejected_gaps: int
    rejected_other: int
    eligible: int
    selected: int
    status: str


@dataclass
class MarketProfileResult:
    timestamp: datetime
    system_status: str
    total_assets_scanned: int
    data_quality_passed: int
    candidates: list[Candidate]
    profiles: list[AssetProfile]
    config: dict[str, Any]
    quality_summary: QualitySummary | None = None
    details_by_symbol: dict[str, dict[str, str]] = field(default_factory=dict)
    events: list[ProfileEvent] = field(default_factory=list)
