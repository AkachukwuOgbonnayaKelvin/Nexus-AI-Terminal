"""
GLB-006 Geopolitical Risk Intelligence Engine - Geopolitical Score
"""

import logging
from typing import Dict, List

from ..input.schemas import GeopoliticalEventInput
from .severity_analyzer import SeverityAnalyzer

logger = logging.getLogger(__name__)


class GeopoliticalScoreEngine:
    """Calculate overall geopolitical risk score"""

    def __init__(self):
        self.severity_analyzer = SeverityAnalyzer()

    def calculate_risk_score(self, event: GeopoliticalEventInput) -> float:
        """
        Calculate geopolitical risk score for a single event.

        Risk Score =
            Severity × 0.30
          + Escalation × 0.25
          + Strategic Importance × 0.20
          + Economic Exposure × 0.15
          + Market Sensitivity × 0.10
        """
        severity = event.severity
        escalation = event.escalation_probability
        strategic = event.strategic_importance
        economic = event.economic_exposure
        market = event.market_sensitivity

        risk_score = (
            (severity * 0.30)
            + (escalation * 0.25)
            + (strategic * 0.20)
            + (economic * 0.15)
            + (market * 0.10)
        )

        return min(100, risk_score)

    def calculate_global_state(self, events: List[GeopoliticalEventInput]) -> Dict:
        """
        Calculate global geopolitical state from multiple events.

        Returns:
            Dict with global state analysis
        """
        if not events:
            return {
                "status": "NO_EVENTS",
                "global_risk_score": 0,
                "risk_state": "LOW",
                "dominant_theme": "UNKNOWN",
                "dominant_region": "UNKNOWN",
                "escalation_level": "LOW",
                "risk_trend": "STABLE",
                "event_count": 0,
                "confidence": 50.0,
            }

        # Calculate individual risk scores
        event_analyses = []
        risk_scores = []
        themes = {}
        regions = {}
        severities = []

        for event in events:
            score = self.calculate_risk_score(event)
            risk_scores.append(score)

            # Track themes
            theme = event.event_type.value
            themes[theme] = themes.get(theme, 0) + 1

            # Track regions
            region = event.region
            regions[region] = regions.get(region, 0) + 1

            event_analyses.append(
                {
                    "event_id": event.event_id,
                    "headline": event.headline,
                    "risk_score": score,
                    "severity": event.severity,
                    "escalation": event.escalation_probability,
                    "type": event.event_type.value,
                    "region": event.region,
                }
            )
            severities.append(event.severity)

        # Calculate global risk score (weighted average)
        global_risk_score = sum(risk_scores) / len(risk_scores)

        # Determine dominant theme and region
        dominant_theme = (
            max(themes.items(), key=lambda x: x[1])[0] if themes else "UNKNOWN"
        )
        dominant_region = (
            max(regions.items(), key=lambda x: x[1])[0] if regions else "UNKNOWN"
        )

        # Determine escalation level
        avg_escalation = sum(e.escalation_probability for e in events) / len(events)
        escalation_level = self._determine_level(avg_escalation)

        # Determine risk state
        risk_state = self._determine_risk_state(global_risk_score)

        # Determine risk trend (simplified - using number of critical events)
        critical_events = sum(1 for e in events if e.severity >= 70)
        risk_trend = (
            "RISING"
            if critical_events > 1
            else "FALLING"
            if critical_events == 0
            else "STABLE"
        )

        # Calculate confidence
        avg_confidence = sum(e.confidence for e in events) / len(events)

        return {
            "status": "OPERATIONAL",
            "global_risk_score": global_risk_score,
            "risk_state": risk_state,
            "dominant_theme": dominant_theme,
            "dominant_region": dominant_region,
            "escalation_level": escalation_level,
            "risk_trend": risk_trend,
            "event_count": len(events),
            "critical_events": critical_events,
            "event_analyses": event_analyses,
            "confidence": avg_confidence,
        }

    def _determine_level(self, score: float) -> str:
        """Determine level from score"""
        if score >= 70:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        return "LOW"

    def _determine_risk_state(self, score: float) -> str:
        """Determine risk state from score"""
        if score >= 70:
            return "CRITICAL"
        elif score >= 60:
            return "HIGH"
        elif score >= 40:
            return "ELEVATED"
        elif score >= 20:
            return "MODERATE"
        return "LOW"
