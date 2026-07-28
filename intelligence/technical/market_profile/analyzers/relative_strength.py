"""
Relative Strength Analyzer – compares asset performance to its peers or a benchmark.
"""

import pandas as pd

from ..models import ProfileDimensionScore


def analyze_relative_strength(
    df: pd.DataFrame, benchmark_df: pd.DataFrame = None
) -> ProfileDimensionScore:
    """
    Compute relative strength vs. a benchmark (or peer average).

    If no benchmark provided, uses the asset's own history as a baseline.

    Returns:
        ProfileDimensionScore with score (0-1) and details.
    """
    if df is None or len(df) < 20:
        return ProfileDimensionScore(
            dimension="relative_strength",
            score=0.0,
            direction="neutral",
            details={"reason": "Insufficient data"},
        )

    close = df["close"].values
    # Compute recent return (e.g., 20-day)
    if len(close) >= 20:
        asset_return = (close[-1] / close[-20]) - 1
    else:
        asset_return = (close[-1] / close[0]) - 1 if close[0] > 0 else 0

    # If benchmark provided, compute benchmark return and compare
    if benchmark_df is not None and len(benchmark_df) >= 20:
        bench_close = benchmark_df["close"].values
        bench_return = (
            (bench_close[-1] / bench_close[-20]) - 1 if bench_close[-20] > 0 else 0
        )
        relative = asset_return - bench_return
        # Scale to 0-1: if relative > 5% => 1.0, < -5% => 0.0
        rs_score = min(1.0, max(0.0, (relative + 0.05) / 0.10))
        direction = "bullish" if relative > 0 else "bearish"
    else:
        # Use asset's own momentum as a proxy for relative strength
        # Normalize the return to 0-1 (cap at ±5%)
        rs_score = min(1.0, max(0.0, (asset_return + 0.05) / 0.10))
        direction = "bullish" if asset_return > 0 else "bearish"

    return ProfileDimensionScore(
        dimension="relative_strength",
        score=rs_score,
        direction=direction,
        details={
            "asset_return": asset_return,
            "relative": relative if benchmark_df is not None else None,
        },
    )
