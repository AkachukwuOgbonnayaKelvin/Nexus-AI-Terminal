"""
GLB-004 Economic Events Intelligence Engine - Event Classifier
"""

import logging

from ..constants import EventCategory, EventImpact
from ..input.schemas import EconomicEventInput

logger = logging.getLogger(__name__)


class EventClassifier:
    """Classify events by category and importance"""

    def __init__(self):
        self._category_weights = {
            EventCategory.CENTRAL_BANK: 1.2,
            EventCategory.INFLATION: 1.1,
            EventCategory.EMPLOYMENT: 1.0,
            EventCategory.GROWTH: 0.9,
            EventCategory.MANUFACTURING: 0.7,
            EventCategory.CONSUMER: 0.6,
            EventCategory.HOUSING: 0.5,
            EventCategory.TRADE: 0.4,
        }

    def classify_event(self, event: EconomicEventInput) -> dict:
        """
        Classify an event and return enriched metadata.

        Returns:
            Dict with classification metadata
        """
        return {
            "category": event.category.value,
            "impact": event.impact_level.value,
            "importance_score": self._calculate_importance(event),
            "category_weight": self._category_weights.get(event.category, 0.5),
            "is_high_impact": event.impact_level
            in [EventImpact.HIGH, EventImpact.CRITICAL],
        }

    def classify_events(self, events: list[EconomicEventInput]) -> list[dict]:
        """Classify multiple events"""
        return [self.classify_event(e) for e in events]

    def _calculate_importance(self, event: EconomicEventInput) -> float:
        """Calculate event importance score (0-100)"""
        base_score = self._category_weights.get(event.category, 0.5) * 50

        # Adjust by impact level
        impact_multipliers = {
            EventImpact.CRITICAL: 1.5,
            EventImpact.HIGH: 1.3,
            EventImpact.MEDIUM: 1.0,
            EventImpact.LOW: 0.7,
        }
        multiplier = impact_multipliers.get(event.impact_level, 1.0)

        score = base_score * multiplier
        return min(100, score)
