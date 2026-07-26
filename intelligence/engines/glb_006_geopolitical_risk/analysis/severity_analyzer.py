"""
GLB-006 Geopolitical Risk Intelligence Engine - Severity Analyzer
"""

import logging

from ..constants import EVENT_SEVERITY_BASE, RiskSeverity
from ..input.schemas import GeopoliticalEventInput

logger = logging.getLogger(__name__)


class SeverityAnalyzer:
    """Analyze geopolitical event severity"""

    def __init__(self):
        self._severity_base = EVENT_SEVERITY_BASE

    def analyze_severity(self, event: GeopoliticalEventInput) -> dict:
        """
        Analyze severity of a geopolitical event.

        Returns:
            Dict with severity analysis
        """
        # Base severity from event type
        base_severity = self._severity_base.get(event.event_type, 50)

        # Adjust for escalation probability
        escalation_factor = 1 + (event.escalation_probability / 100) * 0.5

        # Adjust for strategic importance
        importance_factor = 1 + (event.strategic_importance / 100) * 0.3

        # Calculate final severity
        adjusted_severity = base_severity * escalation_factor * importance_factor
        final_severity = min(100, adjusted_severity)

        return {
            "event_id": event.event_id,
            "event_type": event.event_type.value,
            "base_severity": base_severity,
            "escalation_factor": escalation_factor,
            "importance_factor": importance_factor,
            "final_severity": final_severity,
            "severity_level": self._determine_level(final_severity),
            "confidence": event.confidence,
        }

    def analyze_multiple(self, events: list[GeopoliticalEventInput]) -> list[dict]:
        """Analyze severity for multiple events"""
        return [self.analyze_severity(e) for e in events]

    def _determine_level(self, score: float) -> str:
        """Determine severity level from score"""
        if score >= 80:
            return RiskSeverity.CRITICAL.value
        elif score >= 60:
            return RiskSeverity.HIGH.value
        elif score >= 40:
            return RiskSeverity.ELEVATED.value
        elif score >= 20:
            return RiskSeverity.MODERATE.value
        return RiskSeverity.LOW.value
