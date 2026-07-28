"""
Relative Performance Analyzer – compares an asset's recent performance to its own historical average.
"""

import pandas as pd

from ..models import ProfileDimensionScore


def analyze_relative_performance(df: pd.DataFrame) -> ProfileDimensionScore:
    """
    Compare the asset's recent return to its long-term average return.

    Returns:
        ProfileDimensionScore with score (0-1) and details.
    """
    if df is None or len(df) < 50:
        return ProfileDimensionScore(
            dimension="relative_performance",
            score=0.0,
            details={"reason": "Insufficient data"},
        )

    close = df["close"].values

    # Recent return (20-day)
    recent_return = (close[-1] / close[-20]) - 1 if close[-20] > 0 else 0

    # Long-term average return (over the entire series)
    long_avg_return = (close[-1] / close[0]) - 1 if close[0] > 0 else 0

    # Compare: if recent return > long-term average, performance is improving
    # Normalize: relative performance score = 0-1
    if abs(long_avg_return) > 0.0001:
        relative_perf = recent_return - long_avg_return
        # Scale: 5% above average -> 1.0, 5% below -> 0.0
        perf_score = min(1.0, max(0.0, (relative_perf + 0.05) / 0.10))
    else:
        # If long-term average is near zero, use the recent return itself
        perf_score = min(1.0, max(0.0, (recent_return + 0.05) / 0.10))

    return ProfileDimensionScore(
        dimension="relative_performance",
        score=perf_score,
        direction="bullish" if recent_return > 0 else "bearish",
        details={
            "recent_return": recent_return,
            "long_avg_return": long_avg_return,
            "relative_perf": recent_return - long_avg_return
            if abs(long_avg_return) > 0.0001
            else None,
        },
    )
