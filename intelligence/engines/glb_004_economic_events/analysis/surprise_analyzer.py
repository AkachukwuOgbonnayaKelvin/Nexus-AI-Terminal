"""
GLB-004 Economic Events Intelligence Engine - Surprise Analyzer
"""

import logging

from ..constants import EVENT_DIRECTION_MAP, EventDirection
from ..input.schemas import EconomicEventInput

logger = logging.getLogger(__name__)


class SurpriseAnalyzer:
    """
    Analyze event surprises and their market implications.
    """

    def __init__(self):
        self._direction_map = EVENT_DIRECTION_MAP

    def analyze_surprise(self, event: EconomicEventInput) -> dict:
        """
        Analyze surprise for a released event.

        Returns:
            Dict with surprise analysis
        """
        if event.status.value != "RELEASED":
            return {
                "status": "UPCOMING",
                "surprise": None,
                "direction": EventDirection.NEUTRAL.value,
                "interpretation": "Event not yet released",
            }

        if event.actual is None or event.forecast is None:
            return {
                "status": "NO_DATA",
                "surprise": None,
                "direction": EventDirection.NEUTRAL.value,
                "interpretation": "Missing actual or forecast data",
            }

        # Calculate surprise
        surprise = event.actual - event.forecast
        surprise_percent = (
            (surprise / abs(event.forecast) * 100) if event.forecast != 0 else 0
        )

        # Determine direction
        direction = self._get_surprise_direction(event, surprise)

        # Get market implications (used internally)
        implications = self._get_market_implications(event, surprise)

        return {
            "status": "RELEASED",
            "surprise": surprise,
            "surprise_percent": surprise_percent,
            "direction": direction.value,
            "interpretation": self._interpret_surprise(event, surprise),
            "implications": implications,
        }

    def analyze_surprises(self, events: list[EconomicEventInput]) -> list[dict]:
        """Analyze surprises for multiple events"""
        return [self.analyze_surprise(e) for e in events]

    def _get_surprise_direction(
        self, event: EconomicEventInput, surprise: float
    ) -> EventDirection:
        """Get surprise direction based on event type"""
        if abs(surprise) < 0.01:
            return EventDirection.NEUTRAL

        # Check if event has direction map
        event_name = event.event_name
        for key in self._direction_map:
            if key.lower() in event_name.lower() or event_name.lower() in key.lower():
                return (
                    EventDirection.BULLISH if surprise > 0 else EventDirection.BEARISH
                )

        # Default: positive surprise = bullish
        return EventDirection.BULLISH if surprise > 0 else EventDirection.BEARISH

    def _get_market_implications(
        self, event: EconomicEventInput, surprise: float
    ) -> dict:
        """Get market implications of the surprise"""
        event_name = event.event_name

        # Find matching direction map
        for key, direction_map in self._direction_map.items():
            if key.lower() in event_name.lower() or event_name.lower() in key.lower():
                direction = "higher" if surprise > 0 else "lower"
                if direction in direction_map:
                    return direction_map[direction]

        # Default implications
        if surprise > 0:
            return {
                "USD": EventDirection.BULLISH.value,
                "YIELDS": EventDirection.BULLISH.value,
                "GOLD": EventDirection.BEARISH.value,
                "EQUITIES": EventDirection.NEUTRAL.value,
            }
        else:
            return {
                "USD": EventDirection.BEARISH.value,
                "YIELDS": EventDirection.BEARISH.value,
                "GOLD": EventDirection.BULLISH.value,
                "EQUITIES": EventDirection.NEUTRAL.value,
            }

    def _interpret_surprise(self, event: EconomicEventInput, surprise: float) -> str:
        """Interpret the surprise"""
        if abs(surprise) < 0.01:
            return f"{event.event_name} was in line with expectations."

        direction = "higher than" if surprise > 0 else "lower than"
        return f"{event.event_name} came in {direction} expected ({surprise:+.2f} deviation)."
