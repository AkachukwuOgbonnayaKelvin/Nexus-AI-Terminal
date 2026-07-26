"""
GLB-005 Central Bank Intelligence Engine - Rate Forecaster
"""

import logging

from ..input.schemas import CentralBankInput

logger = logging.getLogger(__name__)


class RateForecaster:
    """Analyze and forecast central bank rates"""

    def __init__(self):
        self._forecast_horizons = ["3m", "6m", "12m"]

    def forecast_rates(self, bank_data: CentralBankInput) -> dict:
        """
        Forecast rate path for a central bank.

        Returns:
            Dict with rate forecast
        """
        expectations = bank_data.rate_expectations

        return {
            "bank": bank_data.bank.value,
            "current_rate": expectations.current,
            "forecasts": {
                "3m": expectations.three_month,
                "6m": expectations.six_month,
                "12m": expectations.twelve_month,
            },
            "expected_change_12m": expectations.twelve_month - expectations.current,
            "expected_direction": self._determine_direction(
                expectations.current, expectations.twelve_month
            ),
            "confidence": expectations.confidence,
        }

    def forecast_all_banks(self, banks: list[CentralBankInput]) -> dict:
        """
        Forecast rates for all central banks.

        Returns:
            Dict with global rate environment
        """
        if not banks:
            return {"status": "NO_DATA", "banks": {}}

        bank_forecasts = {}
        expected_changes = []

        for bank_data in banks:
            forecast = self.forecast_rates(bank_data)
            bank_forecasts[bank_data.bank.value] = forecast
            expected_changes.append(forecast["expected_change_12m"])

        # Determine global rate direction
        avg_change = (
            sum(expected_changes) / len(expected_changes) if expected_changes else 0
        )
        global_direction = self._determine_global_direction(avg_change)

        return {
            "banks": bank_forecasts,
            "global_direction": global_direction,
            "average_expected_change_12m": avg_change,
            "most_aggressive_cutter": self._find_most_aggressive(
                expected_changes, bank_forecasts, "negative"
            ),
            "most_aggressive_hiker": self._find_most_aggressive(
                expected_changes, bank_forecasts, "positive"
            ),
            "confidence": sum(b.rate_expectations.confidence for b in banks)
            / len(banks)
            if banks
            else 50,
        }

    def _determine_direction(self, current: float, future: float) -> str:
        """Determine rate direction"""
        if future > current:
            return "HIKE"
        elif future < current:
            return "CUT"
        return "HOLD"

    def _determine_global_direction(self, avg_change: float) -> str:
        """Determine global rate direction"""
        if avg_change > 0.25:
            return "RESTRICTIVE"
        elif avg_change < -0.25:
            return "ACCOMMODATIVE"
        return "NEUTRAL"

    def _find_most_aggressive(
        self, changes: list[float], forecasts: dict, direction: str
    ) -> str | None:
        """Find the most aggressive bank in a direction"""
        if not changes:
            return None

        # Filter by direction
        filtered = []
        for bank, forecast in forecasts.items():
            change = forecast["expected_change_12m"]
            if (
                direction == "negative"
                and change < 0
                or direction == "positive"
                and change > 0
            ):
                filtered.append((bank, change))

        if not filtered:
            return None

        # Find most extreme
        if direction == "negative":
            return min(filtered, key=lambda x: x[1])[0]
        else:
            return max(filtered, key=lambda x: x[1])[0]
