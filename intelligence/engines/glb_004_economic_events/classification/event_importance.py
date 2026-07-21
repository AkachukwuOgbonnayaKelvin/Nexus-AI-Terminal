"""
GLB-004 Economic Events Intelligence Engine - Event Importance Engine
"""

import logging
from typing import Dict, List, Optional

from ..input.schemas import EconomicEventInput
from ..constants import EventCategory

logger = logging.getLogger(__name__)


class EventImportanceEngine:
    """
    Calculate dynamic event importance based on:
    1. Base event importance
    2. Current macro sensitivity
    3. Market positioning
    """

    def __init__(self):
        self._macro_sensitivity = {
            EventCategory.INFLATION: 0.95,
            EventCategory.CENTRAL_BANK: 0.90,
            EventCategory.EMPLOYMENT: 0.80,
            EventCategory.GROWTH: 0.75,
            EventCategory.MANUFACTURING: 0.60,
            EventCategory.CONSUMER: 0.55,
            EventCategory.HOUSING: 0.45,
            EventCategory.TRADE: 0.40,
        }
        self._market_positioning = 0.85  # Default positioning factor

    def calculate_importance(self, event: EconomicEventInput) -> float:
        """
        Calculate dynamic event importance.

        Returns:
            Importance score (0-100)
        """
        # Base importance from category
        base_importance = self._macro_sensitivity.get(event.category, 0.5) * 100

        # Adjust by impact level
        impact_factors = {
            "CRITICAL": 1.3,
            "HIGH": 1.2,
            "MEDIUM": 1.0,
            "LOW": 0.8,
        }
        impact_factor = impact_factors.get(event.impact_level.value, 1.0)

        # Calculate dynamic importance
        importance = base_importance * impact_factor * self._market_positioning

        return min(100, importance)

    def calculate_event_risk(self, events: List[EconomicEventInput]) -> float:
        """
        Calculate overall event risk score.

        Returns:
            Risk score (0-100)
        """
        if not events:
            return 0.0

        total_importance = 0.0
        for event in events:
            total_importance += self.calculate_importance(event)

        avg_importance = total_importance / len(events)

        # Factor in number of high-impact events
        high_impact_count = sum(
            1 for e in events if e.impact_level in ["CRITICAL", "HIGH"]
        )
        high_impact_factor = min(1.0, 0.2 * high_impact_count + 0.8)

        return min(100, avg_importance * high_impact_factor)

    def get_next_major_event(self, events: List[EconomicEventInput]) -> Optional[Dict]:
        """Get the next major event"""
        if not events:
            return None

        upcoming = [e for e in events if e.status.value == "UPCOMING"]
        if not upcoming:
            return None

        # Sort by importance
        upcoming_with_importance = [(e, self.calculate_importance(e)) for e in upcoming]
        upcoming_with_importance.sort(key=lambda x: x[1], reverse=True)

        best_event, importance = upcoming_with_importance[0]
        return {
            "event": best_event.event_name,
            "currency": best_event.currency,
            "scheduled_at": best_event.scheduled_at,
            "importance": importance,
        }
