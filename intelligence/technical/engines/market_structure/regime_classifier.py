"""
Enhanced regime classification using ATR, ADX (simulated), and structure.
"""

import pandas as pd
import numpy as np
from intelligence.technical.contracts import MarketRegime

def classify_regime(df: pd.DataFrame, swings: list) -> dict:
    if df.empty or len(df) < 20:
        return {"regime": MarketRegime.UNKNOWN, "phase": "unknown", "confidence": 0.0}

    high_low = df['high'] - df['low']
    high_close = abs(df['high'] - df['close'].shift())
    low_close = abs(df['low'] - df['close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(14).mean().iloc[-1]

    sma20 = df['close'].rolling(20).mean()
    if len(sma20) > 5:
        slope = (sma20.iloc[-1] - sma20.iloc[-5]) / sma20.iloc[-5]
    else:
        slope = 0.0

    atr_percentile = min(1.0, atr / (df['close'].mean() * 0.01))

    if len(swings) < 4:
        return {"regime": MarketRegime.UNKNOWN, "phase": "unknown", "confidence": 0.0}

    bullish_swings = sum(1 for s in swings if s.type == 'high' and s.price > (swings[swings.index(s)-1].price if s != swings[0] else s.price))
    bearish_swings = len(swings) - bullish_swings

    if bullish_swings > bearish_swings and slope > 0.001:
        regime = MarketRegime.TRENDING_UP
        phase = "trending"
    elif bearish_swings > bullish_swings and slope < -0.001:
        regime = MarketRegime.TRENDING_DOWN
        phase = "trending"
    elif abs(slope) < 0.001 and atr_percentile < 0.3:
        regime = MarketRegime.RANGING
        phase = "consolidation"
    elif abs(slope) < 0.001 and atr_percentile > 0.5:
        regime = MarketRegime.RANGING
        phase = "volatile_range"
    else:
        regime = MarketRegime.RANGING
        phase = "transition"

    confidence = min(1.0, 0.5 + 0.3 * (1 - atr_percentile) + 0.2 * abs(slope) * 100)
    return {"regime": regime, "phase": phase, "confidence": confidence}
