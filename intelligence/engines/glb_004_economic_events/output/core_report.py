"""
GLB-004 Economic Events Intelligence Engine - Core Report Builder
"""

import logging
from typing import Dict, List, Any, Optional

from ..input.schemas import EconomicEventInput
from ..constants import EventImpact

logger = logging.getLogger(__name__)


class CoreReportBuilder:
    """Build the core intelligence report"""

    def build(
        self,
        events: List[EconomicEventInput],
        classified: List[Dict],
        event_risk: float,
        next_major: Optional[Dict],
        surprise_analyses: List[Dict],
        transmissions: List[Dict],
        confidence: float,
    ) -> Dict[str, Any]:
        """Build core intelligence report"""

        # Separate upcoming and released events
        upcoming = [e for e in events if e.status.value == "UPCOMING"]
        released = [e for e in events if e.status.value == "RELEASED"]

        # Determine dominant theme
        dominant_theme = self._determine_dominant_theme(events)

        # Generate scenarios
        scenarios = self._generate_scenarios(events)

        # Build report
        return {
            "event_risk_score": event_risk,
            "active_event_risk": self._determine_risk_level(event_risk),
            "next_major_event": next_major,
            "upcoming_events": self._format_upcoming_events(upcoming),
            "recent_events": self._format_recent_events(released),
            "released_events": self._format_released_events(released),
            "dominant_event_theme": dominant_theme,
            "event_scenarios": scenarios,
            "surprise_analyses": surprise_analyses[:5],
            "transmissions": transmissions[:5],
            "confidence": confidence,
            "total_events": len(events),
            "high_impact_events": sum(
                1
                for e in events
                if e.impact_level in [EventImpact.HIGH, EventImpact.CRITICAL]
            ),
        }

    def _determine_risk_level(self, score: float) -> str:
        """Determine risk level from score"""
        if score >= 80:
            return "CRITICAL"
        elif score >= 60:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        else:
            return "LOW"

    def _determine_dominant_theme(self, events: List[EconomicEventInput]) -> str:
        """Determine dominant event theme"""
        if not events:
            return "UNKNOWN"

        categories = {}
        for event in events:
            category = event.category.value
            categories[category] = categories.get(category, 0) + 1

        if not categories:
            return "UNKNOWN"

        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        return sorted_categories[0][0]

    def _generate_scenarios(self, events: List[EconomicEventInput]) -> List[Dict]:
        """Generate event scenarios"""
        if not events:
            return []

        scenarios = []
        high_impact = [
            e
            for e in events
            if e.impact_level in [EventImpact.HIGH, EventImpact.CRITICAL]
        ]

        if high_impact:
            event = high_impact[0]
            scenarios.append(
                {
                    "scenario": f"{event.event_name} exceeds expectations",
                    "probability": 35.0,
                    "impact": "BULLISH" if "CPI" in event.event_name else "BEARISH",
                }
            )
            scenarios.append(
                {
                    "scenario": f"{event.event_name} meets expectations",
                    "probability": 45.0,
                    "impact": "NEUTRAL",
                }
            )
            scenarios.append(
                {
                    "scenario": f"{event.event_name} misses expectations",
                    "probability": 20.0,
                    "impact": "BEARISH" if "CPI" in event.event_name else "BULLISH",
                }
            )
        else:
            scenarios.append(
                {
                    "scenario": "No major events in near term",
                    "probability": 70.0,
                    "impact": "NEUTRAL",
                }
            )

        return scenarios

    def _format_upcoming_events(self, events: List[EconomicEventInput]) -> List[Dict]:
        """Format upcoming events for output"""
        result = []
        for e in events:
            result.append(
                {
                    "event": e.event_name,
                    "country": e.country,
                    "currency": e.currency,
                    "importance": e.impact_level.value,
                    "scheduled_at": e.scheduled_at.isoformat(),
                    "forecast": e.forecast,
                    "previous": e.previous,
                    "unit": e.unit,
                    "status": e.status.value,
                }
            )
        return result[:10]

    def _format_recent_events(self, events: List[EconomicEventInput]) -> List[Dict]:
        """Format recent events for output"""
        result = []
        for e in events:
            result.append(
                {
                    "event": e.event_name,
                    "country": e.country,
                    "currency": e.currency,
                    "actual": e.actual,
                    "forecast": e.forecast,
                    "previous": e.previous,
                    "deviation": e.actual - e.forecast
                    if e.actual and e.forecast
                    else None,
                    "unit": e.unit,
                    "status": e.status.value,
                }
            )
        return result[:5]

    def _format_released_events(self, events: List[EconomicEventInput]) -> List[Dict]:
        """Format released events with context"""
        result = []
        for e in events:
            deviation = e.actual - e.forecast if e.actual and e.forecast else None
            direction = (
                "positive"
                if deviation and deviation > 0
                else "negative"
                if deviation and deviation < 0
                else "in-line"
            )
            result.append(
                {
                    "event": e.event_name,
                    "currency": e.currency,
                    "actual": e.actual,
                    "forecast": e.forecast,
                    "previous": e.previous,
                    "deviation": deviation,
                    "direction": direction,
                    "unit": e.unit,
                }
            )
        return result[:5]
