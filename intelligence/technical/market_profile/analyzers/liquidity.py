"""
Liquidity Analyzer – uses volume (or tick volume) to assess market participation.
"""

import numpy as np
import pandas as pd

from ..models import ProfileDimensionScore


def analyze_liquidity(df: pd.DataFrame) -> ProfileDimensionScore:
    """
    Assess liquidity based on volume (or tick volume) relative to recent average.

    Returns:
        ProfileDimensionScore with score (0-1) and details.
    """
    if df is None or len(df) < 20:
        return ProfileDimensionScore(
            dimension="liquidity", score=0.0, details={"reason": "Insufficient data"}
        )

    if "volume" not in df.columns:
        return ProfileDimensionScore(
            dimension="liquidity",
            score=0.5,
            details={"reason": "No volume data; assuming moderate liquidity"},
        )

    volume = df["volume"].values
    avg_volume = np.mean(volume[-50:]) if len(volume) >= 50 else np.mean(volume)
    recent_volume = np.mean(volume[-10:]) if len(volume) >= 10 else np.mean(volume)

    if avg_volume > 0:
        liquidity_ratio = recent_volume / avg_volume
        # Score: 1.0 if volume is > 1.5x average, 0.0 if < 0.5x
        liq_score = min(1.0, max(0.0, (liquidity_ratio - 0.5) / 1.0))
    else:
        liq_score = 0.0

    return ProfileDimensionScore(
        dimension="liquidity",
        score=liq_score,
        details={
            "recent_volume": recent_volume,
            "avg_volume": avg_volume,
            "liquidity_ratio": liquidity_ratio if avg_volume > 0 else None,
        },
    )
