"""
Momentum Analyzer – computes multi-horizon momentum using ROC and RSI.
"""

import numpy as np
import pandas as pd

from ..models import ProfileDimensionScore


def analyze_momentum(df: pd.DataFrame) -> ProfileDimensionScore:
    """
    Analyze momentum across short, medium, and long horizons.

    Returns:
        ProfileDimensionScore with score (0-1) and details.
    """
    if df is None or len(df) < 20:
        return ProfileDimensionScore(
            dimension="momentum", score=0.0, details={"reason": "Insufficient data"}
        )

    close = df["close"].values

    # Define horizons (in bars)
    horizons = {"short": 5, "medium": 14, "long": 30}

    scores = []
    details = {}

    for name, h in horizons.items():
        if len(close) >= h:
            # Rate of change
            roc = (close[-1] - close[-h]) / (close[-h] + 0.001)
            # Normalize roc to 0-1 (cap at ±5%)
            roc_score = min(1.0, abs(roc) * 20)  # 5% move -> score 1.0
            # Direction: positive = bullish, negative = bearish
            direction = 1 if roc > 0 else -1

            # RSI (approximated)
            gains = np.maximum(np.diff(close), 0)
            losses = np.maximum(-np.diff(close), 0)
            avg_gain = np.mean(gains[-h:]) if len(gains) >= h else np.mean(gains)
            avg_loss = np.mean(losses[-h:]) if len(losses) >= h else np.mean(losses)
            if avg_loss > 0:
                rs = avg_gain / avg_loss
                rsi = 100 - 100 / (1 + rs)
            else:
                rsi = 100 if avg_gain > 0 else 50
            rsi_score = (
                rsi / 100.0
            )  # 0-1, but for momentum we want both overbought/oversold
            # For momentum, we want to see if it's moving in the right direction
            # We'll combine ROC and RSI
            if direction > 0:
                mom_score = 0.6 * roc_score + 0.4 * rsi_score
            else:
                mom_score = 0.6 * roc_score + 0.4 * (1 - rsi_score)

            scores.append(mom_score)
            details[f"roc_{name}"] = roc
            details[f"rsi_{name}"] = rsi
            details[f"score_{name}"] = mom_score

    if scores:
        # Combine: short 40%, medium 35%, long 25%
        weights = [0.4, 0.35, 0.25]
        if len(scores) == 2:
            weights = [0.5, 0.5]
        elif len(scores) == 1:
            weights = [1.0]
        weighted_score = np.average(scores, weights=weights[: len(scores)])
    else:
        weighted_score = 0.0

    # Determine direction from the most recent price movement
    if len(close) >= 5:
        short_move = close[-1] - close[-5]
        direction = (
            "bullish" if short_move > 0 else "bearish" if short_move < 0 else "neutral"
        )
    else:
        direction = "neutral"

    return ProfileDimensionScore(
        dimension="momentum",
        score=min(1.0, max(0.0, weighted_score)),
        direction=direction,
        details=details,
    )
