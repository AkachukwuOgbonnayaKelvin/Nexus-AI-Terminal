from dataclasses import dataclass
from datetime import datetime
from enum import Enum

import pandas as pd


class DataQuality(Enum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    INSUFFICIENT = "insufficient"
    MISSING = "missing"
    STALE = "stale"
    INVALID = "invalid"


class DataStatus(Enum):
    ANALYZABLE = "analyzable"
    INSUFFICIENT_DATA = "insufficient_data"
    MISSING_DATA = "missing_data"
    STALE_DATA = "stale_data"
    INVALID_DATA = "invalid_data"


# Minimum bar requirements per timeframe
MINIMUM_BARS = {
    "D1": 100,
    "H4": 150,
    "H1": 250,
    "M15": 400,
    "M5": 500,
}

# Preferred bars (for confidence)
PREFERRED_BARS = {
    "D1": 250,
    "H4": 300,
    "H1": 500,
    "M15": 1000,
    "M5": 2000,
}

# Maximum allowed age of latest bar (in hours)
MAX_AGE_HOURS = {
    "D1": 24 * 7,  # 7 days
    "H4": 24 * 3,  # 3 days
    "H1": 48,  # 2 days
    "M15": 12,  # 12 hours
    "M5": 2,  # 2 hours
}


@dataclass
class DataQualityResult:
    status: DataQuality
    is_usable: bool
    bars_available: int
    bars_required: int
    earliest: datetime | None
    latest: datetime | None
    reason: str | None = None


def validate_dataframe(df: pd.DataFrame, timeframe: str) -> DataQualityResult:
    """
    Validate OHLC dataframe for a given timeframe.
    Returns DataQualityResult with status and usability flag.
    """
    if df is None or df.empty:
        return DataQualityResult(
            status=DataQuality.MISSING,
            is_usable=False,
            bars_available=0,
            bars_required=MINIMUM_BARS.get(timeframe, 100),
            earliest=None,
            latest=None,
            reason="No data available.",
        )

    # Check OHLC integrity
    required_cols = ["open", "high", "low", "close"]
    for col in required_cols:
        if col not in df.columns:
            return DataQualityResult(
                status=DataQuality.INVALID,
                is_usable=False,
                bars_available=len(df),
                bars_required=MINIMUM_BARS.get(timeframe, 100),
                earliest=df["time"].min() if "time" in df else None,
                latest=df["time"].max() if "time" in df else None,
                reason=f"Missing required column: {col}",
            )

    # Check OHLC integrity: high >= max(open, close), low <= min(open, close)
    invalid_bars = df[
        (df["high"] < df["open"])
        | (df["high"] < df["close"])
        | (df["low"] > df["open"])
        | (df["low"] > df["close"])
        | (df["high"] < df["low"])
    ]
    if len(invalid_bars) > len(df) * 0.05:  # more than 5% invalid
        return DataQualityResult(
            status=DataQuality.INVALID,
            is_usable=False,
            bars_available=len(df),
            bars_required=MINIMUM_BARS.get(timeframe, 100),
            earliest=df["time"].min() if "time" in df else None,
            latest=df["time"].max() if "time" in df else None,
            reason=f"Too many invalid OHLC bars: {len(invalid_bars)}/{len(df)}",
        )

    bars_available = len(df)
    min_bars = MINIMUM_BARS.get(timeframe, 100)

    # Check if enough bars
    if bars_available < min_bars:
        return DataQualityResult(
            status=DataQuality.INSUFFICIENT,
            is_usable=False,
            bars_available=bars_available,
            bars_required=min_bars,
            earliest=df["time"].min() if "time" in df else None,
            latest=df["time"].max() if "time" in df else None,
            reason=f"Only {bars_available} bars available; minimum required is {min_bars}.",
        )

    # Check freshness (if latest bar is too old)
    if "time" in df and not df["time"].empty:
        latest = df["time"].max()
        max_age_hours = MAX_AGE_HOURS.get(timeframe, 24)
        if (
            latest
            and (datetime.now(latest.tzinfo) - latest).total_seconds() / 3600
            > max_age_hours
        ):
            return DataQualityResult(
                status=DataQuality.STALE,
                is_usable=False,
                bars_available=bars_available,
                bars_required=min_bars,
                earliest=df["time"].min(),
                latest=latest,
                reason=f"Latest bar is {int((datetime.now(latest.tzinfo) - latest).total_seconds() / 3600)} hours old; max allowed {max_age_hours} hours.",
            )

    # Determine if partial or complete
    pref_bars = PREFERRED_BARS.get(timeframe, min_bars * 2)
    if bars_available >= pref_bars:
        status = DataQuality.COMPLETE
    else:
        status = DataQuality.PARTIAL

    return DataQualityResult(
        status=status,
        is_usable=True,
        bars_available=bars_available,
        bars_required=min_bars,
        earliest=df["time"].min() if "time" in df else None,
        latest=df["time"].max() if "time" in df else None,
        reason=f"{status.value} – {bars_available} bars available (preferred: {pref_bars})",
    )


def confidence_cap(data_quality: DataQuality) -> float:
    """Return max confidence allowed based on data quality."""
    if data_quality == DataQuality.COMPLETE:
        return 1.0
    elif data_quality == DataQuality.PARTIAL:
        return 0.60
    else:
        return 0.0
