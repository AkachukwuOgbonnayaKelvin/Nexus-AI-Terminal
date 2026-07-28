"""
Acceleration Analyzer – computes the change in opportunity score over recent periods.
"""


def compute_acceleration(current_score: float, previous_scores: list[float]) -> float:
    """
    Compute the acceleration (rate of change) of the opportunity score.

    Args:
        current_score: the current opportunity score (0-1).
        previous_scores: list of scores from previous profile runs, most recent last.

    Returns:
        Acceleration value (positive = increasing, negative = decreasing).
    """
    if not previous_scores:
        return 0.0

    # Use the last 4 scores (or fewer)
    recent = previous_scores[-4:]
    if len(recent) < 2:
        return 0.0

    # Linear regression slope on the scores
    import numpy as np

    x = np.arange(len(recent))
    y = np.array(recent)
    if len(x) < 2:
        return 0.0
    slope, _ = np.polyfit(x, y, 1)
    # Scale the slope to a meaningful range: we want acceleration in percentage points
    # If slope is 0.01 per profile update (which is ~1% of the score), that's significant.
    acceleration = slope * 100  # convert to percentage points per update
    return acceleration
