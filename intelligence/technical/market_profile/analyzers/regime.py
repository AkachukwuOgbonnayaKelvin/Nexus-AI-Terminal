"""
Regime Analyzer – classifies the market regime (trending, ranging, breakout, etc.)
"""

import numpy as np
import pandas as pd

from ..enums import Regime
from ..models import ProfileDimensionScore


def analyze_regime(df: pd.DataFrame) -> ProfileDimensionScore:
    """
    Classify the current market regime based on trend, volatility, and price action.

    Returns:
        ProfileDimensionScore with score (0-1), regime, and details.
    """
    if df is None or len(df) < 50:
        return ProfileDimensionScore(
            dimension="regime",
            score=0.0,
            regime=Regime.INSUFFICIENT_DATA.value,
            details={"reason": "Insufficient data"},
        )

    close = df["close"].values
    high = df["high"].values
    low = df["low"].values

    # Trend strength (using linear regression slope)
    x = np.arange(len(close))
    slope, _ = np.polyfit(x, close, 1)
    avg_price = np.mean(close)
    slope_pct = slope / avg_price if avg_price > 0 else 0

    # Volatility (ATR)
    tr = np.maximum(
        high - low, np.abs(high - np.roll(close, 1)), np.abs(low - np.roll(close, 1))
    )
    tr[0] = high[0] - low[0]
    atr = np.mean(tr[-14:]) if len(tr) >= 14 else np.mean(tr)
    atr_pct = atr / avg_price if avg_price > 0 else 0

    # Range: recent high-low range
    recent_high = np.max(high[-20:])
    recent_low = np.min(low[-20:])
    recent_range = recent_high - recent_low
    range_pct = recent_range / avg_price if avg_price > 0 else 0

    # Regime classification logic
    trend_strength = abs(slope_pct) * 100  # in percent

    if trend_strength > 0.2 and atr_pct > 0.005:
        regime = (
            Regime.TRENDING_UP.value if slope_pct > 0 else Regime.TRENDING_DOWN.value
        )
        confidence = min(1.0, trend_strength / 1.0)  # 1% trend strength -> 1.0
    elif range_pct < 0.015 and atr_pct < 0.005:
        regime = Regime.RANGING.value
        confidence = min(
            1.0, 1 - range_pct * 50
        )  # low range -> high confidence for ranging
    elif range_pct > 0.03 and recent_range > 1.5 * (
        np.mean(high[-50:] - low[-50:]) if len(df) >= 50 else range_pct
    ):
        regime = Regime.BREAKOUT.value
        confidence = 0.8
    elif atr_pct > 0.01:
        regime = Regime.VOLATILITY_EXPANSION.value
        confidence = 0.7
    else:
        regime = Regime.TRANSITION.value
        confidence = 0.5

    # Use confidence as the score
    regime_score = confidence

    return ProfileDimensionScore(
        dimension="regime",
        score=regime_score,
        regime=regime,
        details={
            "slope_pct": slope_pct,
            "atr_pct": atr_pct,
            "range_pct": range_pct,
            "trend_strength": trend_strength,
            "confidence": confidence,
        },
    )
