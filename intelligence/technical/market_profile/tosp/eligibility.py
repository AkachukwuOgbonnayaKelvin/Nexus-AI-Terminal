"""
TOSP Eligibility – checks if an asset passes the TOSP filters.
"""

from typing import Any

from ..enums import LifecycleState, Regime, TOSPFilter
from ..models import AssetProfile


def apply_market_regime_filter(profile: AssetProfile) -> bool:
    """
    Filter 1: Market Regime – exclude assets in undesirable regimes.
    """
    undesirable_regimes = [
        Regime.DISORDERED.value,
        Regime.INSUFFICIENT_DATA.value,
        Regime.MEAN_REVERSION.value,  # mean reversion can be tricky for trend-following
    ]
    regime = profile.regime.regime
    if regime in undesirable_regimes:
        return False
    return True


def apply_direction_alignment_filter(profile: AssetProfile) -> bool:
    """
    Filter 2: Direction Alignment – ensure the asset's trend and momentum directions align.
    """
    trend_dir = profile.trend.direction
    mom_dir = profile.momentum.direction
    if trend_dir == "neutral" or mom_dir == "neutral":
        return True  # Neutral is acceptable
    if trend_dir == mom_dir:
        return True
    return False


def apply_opportunity_discovery_filter(profile: AssetProfile, min_score: float) -> bool:
    """
    Filter 3: Opportunity Discovery – require a minimum opportunity score.
    """
    return profile.opportunity_score >= min_score


def apply_trade_classification_filter(profile: AssetProfile) -> bool:
    """
    Filter 4: Trade Classification – classify the opportunity type and decide if it's worth pursuing.
    Could be more complex in the future.
    """
    # For now, simply check that the lifecycle state is not disqualifying.
    if profile.lifecycle_state in [LifecycleState.DISQUALIFIED, LifecycleState.UNKNOWN]:
        return False
    return True


def apply_admission_controller_filter(
    profile: AssetProfile, min_data_confidence: float, min_acceleration: float
) -> bool:
    """
    Filter 5: Admission Controller – final check on data confidence and acceleration.
    """
    if profile.data_confidence < min_data_confidence:
        return False
    if profile.acceleration < min_acceleration:
        return False
    return True


def apply_tosp_filters(profile: AssetProfile, config: dict[str, Any]) -> list[str]:
    """
    Apply all TOSP filters and return the list of passed filters.

    Args:
        profile: AssetProfile object.
        config: TOSP configuration dict.

    Returns:
        List of filter names that passed.
    """
    passed = []

    if (
        config.get("apply_regime_filter", True)
        and apply_market_regime_filter(profile)
        or not config.get("apply_regime_filter", True)
    ):
        passed.append(TOSPFilter.MARKET_REGIME.value)

    if (
        config.get("apply_direction_alignment", True)
        and apply_direction_alignment_filter(profile)
        or not config.get("apply_direction_alignment", True)
    ):
        passed.append(TOSPFilter.DIRECTION_ALIGNMENT.value)

    if apply_opportunity_discovery_filter(
        profile, config.get("min_opportunity_score", 0.7) / 100.0
    ):
        passed.append(TOSPFilter.OPPORTUNITY_DISCOVERY.value)

    if apply_trade_classification_filter(profile):
        passed.append(TOSPFilter.TRADE_CLASSIFICATION.value)

    if apply_admission_controller_filter(
        profile,
        config.get("min_data_confidence", 0.85),
        config.get("min_acceleration", 0.0),
    ):
        passed.append(TOSPFilter.ADMISSION_CONTROLLER.value)

    return passed
