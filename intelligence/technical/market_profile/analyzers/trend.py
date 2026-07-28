"""
Trend Analyzer – computes trend direction and strength using linear regression, ADX, and MA alignment.
"""

import numpy as np
import pandas as pd

from ..models import ProfileDimensionScore


def analyze_trend(df: pd.DataFrame) -> ProfileDimensionScore:
    """
    Analyze trend using a combination of linear regression slope, ADX, and MA alignment.

    Returns:
        ProfileDimensionScore with score (0-1), direction, and details.
    """
    if df is None or len(df) < 20:
        return ProfileDimensionScore(
            dimension="trend",
            score=0.0,
            direction="neutral",
            details={"reason": "Insufficient data"},
        )

    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    x = np.arange(len(close))

    # 1. Linear regression slope
    slope, _ = np.polyfit(x, close, 1)
    avg_price = np.mean(close)
    slope_pct = slope / avg_price if avg_price > 0 else 0
    trend_strength = min(1.0, abs(slope_pct) * 50)  # 0.01% per bar -> ~0.5 score

    # Direction based on slope
    direction = "neutral"
    if slope_pct > 0.0002:
        direction = "bullish"
    elif slope_pct < -0.0002:
        direction = "bearish"

    # 2. ATR for volatility normalization
    tr = np.maximum(
        high - low, np.abs(high - np.roll(close, 1)), np.abs(low - np.roll(close, 1))
    )
    tr[0] = high[0] - low[0]
    atr = np.mean(tr[-14:]) if len(tr) >= 14 else np.mean(tr)

    # 3. ADX (Average Directional Index) approximation
    up_move = high - np.roll(high, 1)
    down_move = -(low - np.roll(low, 1))
    plus_dm = np.where((up_move > 0) & (up_move > down_move), up_move, 0)
    minus_dm = np.where((down_move > 0) & (down_move > up_move), down_move, 0)
    atr_avg = np.mean(tr[-14:]) if len(tr) >= 14 else np.mean(tr)
    if atr_avg > 0:
        plus_di = 100 * np.mean(plus_dm[-14:]) / atr_avg
        minus_di = 100 * np.mean(minus_dm[-14:]) / atr_avg
        adx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di + 0.001)
    else:
        adx = 0
    adx_score = min(1.0, adx / 60.0)  # 60 is a strong trend

    # 4. MA alignment: check if short MA > medium > long MA
    if len(df) >= 50:
        ma5 = df["close"].rolling(5).mean().iloc[-1]
        ma20 = df["close"].rolling(20).mean().iloc[-1]
        ma50 = df["close"].rolling(50).mean().iloc[-1]
        if ma5 > ma20 > ma50 or ma5 < ma20 < ma50:
            ma_alignment = 1.0
        else:
            ma_alignment = 0.0
    else:
        ma_alignment = 0.5

    # Combine: slope (40%), ADX (30%), MA alignment (30%)
    score = 0.4 * trend_strength + 0.3 * adx_score + 0.3 * ma_alignment
    score = min(1.0, max(0.0, score))

    return ProfileDimensionScore(
        dimension="trend",
        score=score,
        direction=direction,
        details={
            "slope": slope,
            "slope_pct": slope_pct,
            "adx": adx,
            "adx_score": adx_score,
            "ma_alignment": ma_alignment,
            "atr": atr,
        },
    )
