"""
Opportunity Decay – computes the decay rate and adjusts the opportunity score if needed.
"""

from ..models import AssetProfile


def compute_decay_factor(profile_history: list[AssetProfile]) -> float:
    """
    Compute a decay factor based on how long the opportunity has been active.

    Returns:
        A factor between 0 and 1 (1 = no decay, 0 = fully decayed).
    """
    if not profile_history or len(profile_history) < 2:
        return 1.0

    # Look at the score trend over the last N profiles
    scores = [p.opportunity_score for p in profile_history[-5:]]
    if len(scores) < 2:
        return 1.0

    # If the scores have been decreasing, apply a penalty
    # Simple: if the most recent score is less than the average of the last 3
    recent_avg = sum(scores[-3:]) / len(scores[-3:]) if len(scores) >= 3 else scores[-1]
    if scores[-1] < recent_avg * 0.95:
        decay = max(0.0, 1.0 - (recent_avg - scores[-1]) / recent_avg)
        return decay
    return 1.0
