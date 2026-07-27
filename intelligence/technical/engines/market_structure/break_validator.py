"""
Calculate quality of structural breaks (BOS/CHoCH) based on displacement, volume, and retest.
"""

import pandas as pd


def calculate_break_quality(
    df: pd.DataFrame,
    break_price: float,
    prev_level: float,
    atr: float,
    volume_avg: float,
) -> float:
    # Displacement score (how far price moved beyond previous level)
    displacement = abs(break_price - prev_level)
    displacement_score = min(1.0, displacement / (atr * 0.5)) if atr > 0 else 0.5

    # Volume score (volume at break bar relative to average)
    volume_score = 0.5
    if "volume" in df.columns and volume_avg > 0:
        last_volume = df["volume"].iloc[-1] if not df.empty else 0
        volume_score = min(1.0, last_volume / volume_avg) if volume_avg > 0 else 0.5

    # Retest score (simplified placeholder – we can improve later)
    retest_score = 0.5

    # Weighted average
    quality = 0.4 * displacement_score + 0.3 * volume_score + 0.3 * retest_score
    return min(1.0, quality)
