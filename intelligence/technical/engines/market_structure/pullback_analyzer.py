"""
Pullback detection and projection using ATR.
"""

import pandas as pd


def detect_pullback(mtf_structure: dict) -> dict | None:
    timeframes = mtf_structure.get("timeframes", {})
    if not timeframes:
        return None

    primary_bias = mtf_structure.get("primary_bias")
    if primary_bias not in ["bullish", "bearish"]:
        return None

    execution_tfs = ["H1", "M15"]
    lower_bullish = all(
        timeframes.get(tf, {}).get("bias") == primary_bias
        for tf in execution_tfs
        if tf in timeframes
    )

    if primary_bias == "bullish" and not lower_bullish:
        return {
            "active": True,
            "type": "bullish_pullback",
            "depth_atr": 1.2,
            "expected_zone": None,
            "duration_hours": (4, 8),
        }
    if primary_bias == "bearish" and not lower_bullish:
        return {
            "active": True,
            "type": "bearish_rally",
            "depth_atr": 1.2,
            "expected_zone": None,
            "duration_hours": (4, 8),
        }
    return None


def calculate_pullback_zone(
    df: pd.DataFrame, atr: float, current_price: float, bias: str
) -> dict:
    depth = 1.2 * atr
    if bias == "bullish":
        low_zone = current_price - depth * 1.2
        high_zone = current_price - depth * 0.8
    else:
        low_zone = current_price + depth * 0.8
        high_zone = current_price + depth * 1.2

    return {
        "low": low_zone,
        "high": high_zone,
        "depth_atr": depth / atr if atr > 0 else 1.2,
        "atr_value": atr,
        "confidence": 0.70,
    }


def estimate_time_to_zone(
    current_price: float,
    zone_low: float,
    zone_high: float,
    atr: float,
    timeframe: str = "H1",
) -> dict:
    """
    Estimate time to reach the zone based on distance and ATR.
    Returns min/max hours.
    """
    # Determine direction: if current price is above zone, expect move down; if below, expect up
    if current_price > zone_high:
        distance = current_price - zone_high
        direction = "down"
    elif current_price < zone_low:
        distance = zone_low - current_price
        direction = "up"
    else:
        return {
            "hours_min": 0,
            "hours_max": 0,
            "direction": "inside",
            "distance_atr": 0.0,
        }

    # Estimate hourly volatility from ATR (assuming ATR is per bar, and bar size is 1 hour for H1)
    # For D1, we adjust; but we'll assume the ATR is from the same timeframe as the zone projection.
    # We'll use a simple rule: ATR per hour = ATR / sqrt(period). For H1, period = 1, so ATR per hour ≈ ATR.
    # For D1, we might divide by sqrt(24) but we'll keep it simple: use ATR as daily, then estimate hourly move.
    # Since we have atr value, we'll assume it's per bar of the timeframe used.
    # We'll treat it as approximate hourly move if we are using H1 ATR.
    # We'll set a generic estimate: daily ATR / 24 for hourly.
    # We'll make it configurable later.
    hourly_move = atr / 24  # rough estimate: daily ATR / 24 hours
    if hourly_move <= 0:
        return {
            "hours_min": 0,
            "hours_max": 0,
            "direction": direction,
            "distance_atr": distance / atr,
        }

    hours_estimate = distance / hourly_move
    # Add uncertainty: ±30%
    hours_min = hours_estimate * 0.7
    hours_max = hours_estimate * 1.3
    return {
        "hours_min": round(hours_min, 1),
        "hours_max": round(hours_max, 1),
        "direction": direction,
        "distance_atr": round(distance / atr, 2),
    }
