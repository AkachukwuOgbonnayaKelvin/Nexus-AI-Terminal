"""
Universal Market Watch – lightweight monitoring for all assets.
"""

import logging
from typing import Any

import numpy as np
import pandas as pd

from .models import ProfileState

logger = logging.getLogger(__name__)


class UniversalWatch:
    """
    Lightweight monitoring for all assets to detect material changes.
    """

    def __init__(self, config):
        self.config = config

    def watch_asset(
        self, symbol: str, df: pd.DataFrame, state: ProfileState
    ) -> dict[str, Any]:
        """
        Run cheap monitoring on a single asset.
        Returns a dict of watch metrics.
        """
        if df is None or len(df) < 10:
            return {"status": "insufficient_data"}

        close = df["close"].values
        high = df["high"].values
        low = df["low"].values
        volume = df["volume"].values if "volume" in df.columns else None

        # Price movement relative to ATR
        atr = self._compute_atr(df)
        recent_move = abs(close[-1] - close[-5]) if len(close) >= 5 else 0
        move_atr = recent_move / atr if atr > 0 else 0

        # Momentum (simple)
        momentum = (close[-1] / close[-20]) - 1 if len(close) >= 20 else 0
        # Momentum acceleration (change over last 5 bars)
        if len(close) >= 10:
            m1 = (close[-1] / close[-5]) - 1
            m2 = (close[-5] / close[-10]) - 1
            accel = m1 - m2
        else:
            accel = 0

        # Volatility
        atr_baseline = (
            np.mean([self._compute_atr(df.iloc[-i - 20 : -i]) for i in range(5)])
            if len(df) >= 30
            else atr
        )
        vol_ratio = atr / atr_baseline if atr_baseline > 0 else 1.0

        # Range expansion
        recent_range = high[-10:].max() - low[-10:].min() if len(high) >= 10 else 0
        prev_range = (
            high[-20:-10].max() - low[-20:-10].min()
            if len(high) >= 20
            else recent_range
        )
        range_ratio = recent_range / prev_range if prev_range > 0 else 1.0

        # Activity (volume/tick)
        if volume is not None and len(volume) >= 20:
            avg_vol = np.mean(volume[-20:])
            recent_vol = np.mean(volume[-5:]) if len(volume) >= 5 else avg_vol
            activity_ratio = recent_vol / avg_vol if avg_vol > 0 else 1.0
        else:
            activity_ratio = 1.0

        return {
            "status": "ok",
            "move_atr": move_atr,
            "momentum": momentum,
            "acceleration": accel,
            "volatility_ratio": vol_ratio,
            "range_ratio": range_ratio,
            "activity_ratio": activity_ratio,
            "atr": atr,
            "price": close[-1],
        }

    def _compute_atr(self, df: pd.DataFrame, period: int = 14) -> float:
        if df is None or len(df) < period + 1:
            return 0.0
        high = df["high"].values
        low = df["low"].values
        close = df["close"].values
        tr = np.maximum(
            high - low,
            np.abs(high - np.roll(close, 1)),
            np.abs(low - np.roll(close, 1)),
        )
        tr[0] = high[0] - low[0]
        return np.mean(tr[-period:]) if len(tr) >= period else np.mean(tr)
