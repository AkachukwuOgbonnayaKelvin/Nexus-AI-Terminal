"""
GLB-004 Economic Events Intelligence Engine - Main Engine
"""

import logging
import time
from datetime import datetime
from typing import Any

from .analysis.surprise_analyzer import SurpriseAnalyzer
from .classification.event_classifier import EventClassifier
from .classification.event_importance import EventImportanceEngine
from .constants import NDIP_TOPICS
from .impact.asset_impact_matrix import AssetImpactMatrixGenerator
from .input.event_normalizer import EventNormalizer
from .input.schemas import EconomicEventInput
from .output.core_report import CoreReportBuilder
from .transmission.macro_transmission import MacroTransmissionEngine

logger = logging.getLogger(__name__)


class EconomicEventsEngine:
    """
    GLB-004 Economic Events Intelligence Engine

    Analyzes economic events and produces:
    1. Core Intelligence: Event impact analysis
    2. Asset Impact Matrix: How events affect assets
    """

    def __init__(self):
        self.event_normalizer = EventNormalizer()
        self.event_classifier = EventClassifier()
        self.event_importance = EventImportanceEngine()
        self.surprise_analyzer = SurpriseAnalyzer()
        self.macro_transmission = MacroTransmissionEngine()
        self.report_builder = CoreReportBuilder()

        self.last_report: dict | None = None
        self.last_run_time: datetime | None = None
        self._latest_data: dict[str, Any] = {}

    def consume_ndip(self, topic: str, payload: dict[str, Any]) -> None:
        """Consume NDIP contract."""
        self._latest_data[topic] = payload

    def run(self) -> dict[str, Any]:
        """Run the engine analysis."""
        start_time = time.time()

        # 1. Parse and normalize events
        raw_events = self._parse_events()
        normalized_events = self._normalize_events(raw_events)

        if not normalized_events:
            return self._empty_report()

        # 2. Classify events
        classified_events = self._classify_events(normalized_events)

        # 3. Calculate importance
        event_risk = self.event_importance.calculate_event_risk(normalized_events)
        next_major = self.event_importance.get_next_major_event(normalized_events)

        # 4. Analyze surprises
        surprise_analyses = self.surprise_analyzer.analyze_surprises(normalized_events)

        # 5. Analyze transmission
        transmissions = []
        for event in normalized_events:
            surprise = self._get_surprise_value(event)
            transmission = self.macro_transmission.analyze_transmission(event, surprise)
            transmissions.append(transmission)

        # 6. Generate core report
        core_report = self.report_builder.build(
            events=normalized_events,
            classified=classified_events,
            event_risk=event_risk,
            next_major=next_major,
            surprise_analyses=surprise_analyses,
            transmissions=transmissions,
            confidence=self._calculate_confidence(normalized_events),
        )

        # 7. Generate Asset Impact Matrix
        events_data = [
            {
                "event": e.event_name,
                "currency": e.currency,
                "impact": e.impact_level.value,
                "deviation": self._get_surprise_value(e),
                "forecast": e.forecast if e.forecast else 0,
                "previous": e.previous if e.previous else 0,
            }
            for e in normalized_events
        ]
        impact_matrix = AssetImpactMatrixGenerator.generate(
            events_data, core_report["confidence"]
        )

        # 8. Build final report
        report = {
            "engine_id": "GLB-004",
            "engine_name": "Economic Events Intelligence Engine",
            "version": "1.0.0",
            "status": "OPERATIONAL",
            "generated_at": datetime.utcnow().isoformat(),
            "core_intelligence": core_report,
            "asset_impact_matrix": impact_matrix.dict() if impact_matrix else None,
            "metadata": {
                "calculation_time_ms": int((time.time() - start_time) * 1000),
                "event_count": len(normalized_events),
                "model_version": "1.0.0",
            },
        }

        self.last_report = report
        self.last_run_time = datetime.utcnow()

        logger.info(f"GLB-004 completed: {len(normalized_events)} events analyzed")

        return report

    def _parse_events(self) -> list[dict]:
        """Parse events from NDIP data."""
        events_data = self._latest_data.get(NDIP_TOPICS["ECONOMIC_EVENTS"], {})
        return events_data.get("events", [])

    def _normalize_events(self, raw_events: list[dict]) -> list[EconomicEventInput]:
        """Normalize raw events."""
        normalized = []
        for raw in raw_events:
            event = self.event_normalizer.normalize(raw)
            if event:
                normalized.append(event)
        return normalized

    def _classify_events(self, events: list[EconomicEventInput]) -> list[dict]:
        """Classify events."""
        return self.event_classifier.classify_events(events)

    def _get_surprise_value(self, event: EconomicEventInput) -> float:
        """Get surprise value for an event."""
        if event.actual is not None and event.forecast is not None:
            return event.actual - event.forecast
        return 0.0

    def _calculate_confidence(self, events: list[EconomicEventInput]) -> float:
        """Calculate overall confidence."""
        if not events:
            return 0.0

        confidences = []
        for event in events:
            if event.actual is not None and event.forecast is not None:
                confidences.append(0.85)  # High confidence for released events
            else:
                confidences.append(0.70)  # Medium confidence for upcoming events

        avg_confidence = sum(confidences) / len(confidences)
        return min(95, avg_confidence * 100)

    def _empty_report(self) -> dict:
        """Return empty report when no events."""
        return {
            "engine_id": "GLB-004",
            "engine_name": "Economic Events Intelligence Engine",
            "version": "1.0.0",
            "status": "OPERATIONAL",
            "generated_at": datetime.utcnow().isoformat(),
            "core_intelligence": {
                "event_risk_score": 0,
                "active_event_risk": "LOW",
                "upcoming_events": [],
                "confidence": 50.0,
            },
            "asset_impact_matrix": None,
            "metadata": {"event_count": 0},
        }

    def get_last_report(self) -> dict | None:
        return self.last_report

    def health_check(self) -> dict[str, Any]:
        return {
            "engine_id": "GLB-004",
            "status": "OPERATIONAL",
            "last_run": self.last_run_time.isoformat() if self.last_run_time else None,
            "has_report": self.last_report is not None,
        }
