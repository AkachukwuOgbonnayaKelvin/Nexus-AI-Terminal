"""
GLB-004 Economic Events Intelligence Engine - Macro Transmission Engine
"""

import logging

from ..constants import EventCategory
from ..input.schemas import EconomicEventInput

logger = logging.getLogger(__name__)


class MacroTransmissionEngine:
    """
    Analyze how events transmit through the macro economy.

    Event → Economy → Central Bank → Yields → Currency → Assets
    """

    def __init__(self):
        self._transmission_map = {
            EventCategory.INFLATION: {
                "economy": "Price pressures",
                "central_bank": "Tighter policy",
                "yields": "Higher",
                "currency": "Stronger",
                "assets": {"FX": "USD+", "BONDS": "-", "GOLD": "-", "EQUITIES": "-"},
            },
            EventCategory.EMPLOYMENT: {
                "economy": "Labor market strength",
                "central_bank": "Tighter policy",
                "yields": "Higher",
                "currency": "Stronger",
                "assets": {
                    "FX": "USD+",
                    "BONDS": "-",
                    "GOLD": "-",
                    "EQUITIES": "Conditional",
                },
            },
            EventCategory.GROWTH: {
                "economy": "Economic expansion",
                "central_bank": "Mixed",
                "yields": "Higher",
                "currency": "Stronger",
                "assets": {"FX": "USD+", "BONDS": "-", "GOLD": "-", "EQUITIES": "+"},
            },
            EventCategory.CENTRAL_BANK: {
                "economy": "Policy direction",
                "central_bank": "Policy shift",
                "yields": "Higher/Lower",
                "currency": "Stronger/Weaker",
                "assets": {
                    "FX": "Volatile",
                    "BONDS": "Volatile",
                    "GOLD": "Volatile",
                    "EQUITIES": "Volatile",
                },
            },
        }

    def analyze_transmission(self, event: EconomicEventInput, surprise: float) -> dict:
        """
        Analyze macro transmission of an event.

        Returns:
            Transmission analysis
        """
        transmission = self._transmission_map.get(
            event.category,
            {
                "economy": "Unknown",
                "central_bank": "Unknown",
                "yields": "Unchanged",
                "currency": "Unchanged",
                "assets": {},
            },
        )

        # Determine direction based on surprise
        direction = (
            "Positive" if surprise > 0 else "Negative" if surprise < 0 else "Neutral"
        )

        return {
            "event": event.event_name,
            "category": event.category.value,
            "surprise_direction": direction,
            "transmission": {
                "economy": self._adjust_for_direction(
                    transmission["economy"], direction
                ),
                "central_bank": self._adjust_for_direction(
                    transmission["central_bank"], direction
                ),
                "yields": self._adjust_for_direction(transmission["yields"], direction),
                "currency": self._adjust_for_direction(
                    transmission["currency"], direction
                ),
                "assets": transmission["assets"],
            },
            "confidence": 0.75,
        }

    def _adjust_for_direction(self, text: str, direction: str) -> str:
        """Adjust text based on surprise direction"""
        if direction == "Positive":
            return text
        elif direction == "Negative":
            if "Higher" in text:
                return text.replace("Higher", "Lower")
            elif "Tighter" in text:
                return text.replace("Tighter", "Looser")
            elif "Stronger" in text:
                return text.replace("Stronger", "Weaker")
            elif "+" in text:
                return text.replace("+", "-")
            elif "-" in text:
                return text.replace("-", "+")
        return text
