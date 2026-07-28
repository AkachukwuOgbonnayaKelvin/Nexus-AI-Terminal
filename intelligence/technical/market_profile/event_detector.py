"""
Event Detector – determines if a material change has occurred requiring recalibration.
"""

import logging
from typing import Any

from .enums import EventPriority, RecalibrationTrigger

logger = logging.getLogger(__name__)


class EventDetector:
    def __init__(self, config):
        self.config = config
        self.thresholds = config.events

    def detect(
        self,
        symbol: str,
        current_watch: dict[str, Any],
        previous_watch: dict[str, Any] | None = None,
        current_profile_score: float | None = None,
        previous_profile_score: float | None = None,
        current_regime: str | None = None,
        previous_regime: str | None = None,
    ) -> dict[str, Any] | None:
        """
        Detect material changes based on watch metrics and profile changes.
        Returns a dict with trigger, priority, and reason if a change is detected.
        """
        if not current_watch or current_watch.get("status") != "ok":
            return None

        triggers = []

        # 1. Price shock
        move_atr = current_watch.get("move_atr", 0)
        if move_atr >= self.thresholds.price_shock_atr:
            triggers.append(
                {
                    "trigger": RecalibrationTrigger.PRICE_SHOCK,
                    "priority": EventPriority.HIGH,
                    "reason": f"Price shock: {move_atr:.2f} ATR",
                }
            )

        # 2. Momentum acceleration
        accel = current_watch.get("acceleration", 0)
        if abs(accel) >= self.thresholds.momentum_acceleration:
            triggers.append(
                {
                    "trigger": RecalibrationTrigger.MOMENTUM_ACCELERATION,
                    "priority": EventPriority.MEDIUM,
                    "reason": f"Momentum acceleration: {accel:.4f}",
                }
            )

        # 3. Volatility shock
        vol_ratio = current_watch.get("volatility_ratio", 1.0)
        if vol_ratio >= self.thresholds.volatility_shock_ratio:
            triggers.append(
                {
                    "trigger": RecalibrationTrigger.VOLATILITY_SHOCK,
                    "priority": EventPriority.HIGH,
                    "reason": f"Volatility shock: {vol_ratio:.2f}x baseline",
                }
            )

        # 4. Range expansion
        range_ratio = current_watch.get("range_ratio", 1.0)
        if range_ratio >= self.thresholds.range_expansion_ratio:
            triggers.append(
                {
                    "trigger": RecalibrationTrigger.RANGE_EXPANSION,
                    "priority": EventPriority.MEDIUM,
                    "reason": f"Range expansion: {range_ratio:.2f}x previous",
                }
            )

        # 5. Activity shock
        activity_ratio = current_watch.get("activity_ratio", 1.0)
        if activity_ratio >= self.thresholds.activity_shock_ratio:
            triggers.append(
                {
                    "trigger": RecalibrationTrigger.ACTIVITY_SHOCK,
                    "priority": EventPriority.MEDIUM,
                    "reason": f"Activity shock: {activity_ratio:.2f}x baseline",
                }
            )

        # 6. Structural invalidation (based on profile change)
        if (
            previous_profile_score is not None
            and current_profile_score is not None
            and previous_regime is not None
            and current_regime is not None
        ):
            # Large score drop
            if current_profile_score < previous_profile_score * 0.8:
                triggers.append(
                    {
                        "trigger": RecalibrationTrigger.STRUCTURAL_INVALIDATION,
                        "priority": EventPriority.CRITICAL,
                        "reason": f"Score dropped from {previous_profile_score:.1f} to {current_profile_score:.1f}",
                    }
                )
            # Regime change
            if current_regime != previous_regime:
                triggers.append(
                    {
                        "trigger": RecalibrationTrigger.STRUCTURAL_INVALIDATION,
                        "priority": EventPriority.HIGH,
                        "reason": f"Regime changed: {previous_regime} → {current_regime}",
                    }
                )

        if triggers:
            # Return the most critical trigger
            triggers.sort(key=lambda x: x["priority"].value, reverse=True)
            return triggers[0]

        return None
