"""
Lifecycle State Machine – determines the lifecycle state of an asset based on score, acceleration, and history.
"""

from ..enums import LifecycleState
from ..models import AssetProfile


def determine_lifecycle_state(
    current_profile: AssetProfile, previous_profiles: list[AssetProfile] = None
) -> LifecycleState:
    """
    Determine the lifecycle state of an asset.

    States:
        - EMERGING: score < 0.6 but accelerating (> 0.02)
        - DEVELOPING: score 0.6-0.8 and accelerating (> 0)
        - HIGH_PRIORITY: score >= 0.8
        - PEAK_OPPORTUNITY: score >= 0.85 and acceleration near zero or negative
        - DECAYING: score decreasing over last 3 updates
        - DISQUALIFIED: score < 0.5 or data quality poor
    """
    score = current_profile.opportunity_score
    accel = current_profile.acceleration

    # Check data quality
    if current_profile.data_quality.status.value == "fail":
        return LifecycleState.DISQUALIFIED

    # Check score thresholds
    if score < 0.5:
        return LifecycleState.DISQUALIFIED

    if score >= 0.85:
        # If acceleration is negative, it might be PEAK or DECAYING
        if accel < -0.01:
            return LifecycleState.DECAYING
        else:
            return LifecycleState.PEAK_OPPORTUNITY

    if score >= 0.7:
        if accel > 0.01:
            return LifecycleState.DEVELOPING
        else:
            return LifecycleState.HIGH_PRIORITY

    if score >= 0.5:
        if accel > 0.02:
            return LifecycleState.EMERGING
        else:
            return LifecycleState.DISQUALIFIED

    return LifecycleState.UNKNOWN
