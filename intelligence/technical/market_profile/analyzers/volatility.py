"""
Volatility Analyzer – computes ATR, historical percentile, and expansion/contraction.
"""

import numpy as np
import pandas as pd

from ..models import ProfileDimensionScore


def analyze_volatility(df: pd.DataFrame) -> ProfileDimensionScore:
    """
    Analyze volatility using ATR normalised by price, historical percentile, and regime.

    Returns:
        ProfileDimensionScore with score (0-1), regime, and details.
    """
    if df is None or len(df) < 20:
        return ProfileDimensionScore(
            dimension="volatility",
            score=0.0,
            regime="insufficient_data",
            details={"reason": "Insufficient data"},
        )

    high = df["high"].values
    low = df["low"].values
    close = df["close"].values

    # True Range
    tr = np.maximum(
        high - low, np.abs(high - np.roll(close, 1)), np.abs(low - np.roll(close, 1))
    )
    tr[0] = high[0] - low[0]
    atr = np.mean(tr[-14:]) if len(tr) >= 14 else np.mean(tr)
    avg_price = np.mean(close)
    atr_pct = atr / avg_price if avg_price > 0 else 0

    # Volatility score: higher volatility generally increases opportunity (for short-term trades)
    # Cap at 2% daily volatility (normalised)
    vol_score = min(1.0, atr_pct * 100)  # 1% = 1.0 score

    # Historical percentile: compare current ATR to its 50-bar average
    if len(tr) >= 50:
        atr_50 = np.mean(tr[-50:])
        atr_percentile = min(1.0, atr / (atr_50 + 0.001))
        # Determine regime
        if atr > atr_50 * 1.2:
            regime = "expanding"
        elif atr < atr_50 * 0.8:
            regime = "contracting"
        else:
            regime = "stable"
    else:
        atr_percentile = 0.5
        regime = "unknown"

    # Combine: vol_score (70%) + percentile (30%)
    combined = 0.7 * vol_score + 0.3 * atr_percentile
    combined = min(1.0, max(0.0, combined))

    return ProfileDimensionScore(
        dimension="volatility",
        score=combined,
        regime=regime,
        details={
            "atr": atr,
            "atr_pct": atr_pct,
            "atr_percentile": atr_percentile,
            "regime": regime,
        },
    )
