"""
GLB-006 Geopolitical Risk Intelligence Engine - Main Engine
"""

import logging
import time
from datetime import datetime
from typing import Any

from .analysis.geopolitical_score import GeopoliticalScoreEngine
from .analysis.severity_analyzer import SeverityAnalyzer
from .constants import NDIP_TOPICS, GeopoliticalEventType
from .impact.asset_impact_matrix import AssetImpactMatrixGenerator
from .input.schemas import GeopoliticalEventInput
from .transmission.risk_transmission import RiskTransmissionEngine

logger = logging.getLogger(__name__)


class GeopoliticalRiskEngine:
    """GLB-006 Geopolitical Risk Intelligence Engine"""

    def __init__(self):
        self.severity_analyzer = SeverityAnalyzer()
        self.score_engine = GeopoliticalScoreEngine()
        self.transmission_engine = RiskTransmissionEngine()

        self.last_report: dict | None = None
        self.last_run_time: datetime | None = None
        self._latest_data: dict[str, Any] = {}

    def consume_ndip(self, topic: str, payload: dict[str, Any]) -> None:
        """Consume NDIP contract."""
        self._latest_data[topic] = payload

    def run(self) -> dict[str, Any]:
        """Run the engine analysis."""
        start_time = time.time()

        events = self._parse_events()

        if not events:
            return self._empty_report()

        # Calculate global geopolitical state
        global_state = self.score_engine.calculate_global_state(events)

        # Analyze risk transmission
        transmission = self.transmission_engine.analyze_global_transmission(events)

        # Build core intelligence
        core_intelligence = self._build_core_intelligence(global_state, transmission)

        # Generate asset impact matrix
        impact_matrix = AssetImpactMatrixGenerator.generate(
            events,
            global_state,
            transmission,
            core_intelligence["confidence"],
            diagnostic=False,
        )

        # Use model_dump instead of dict (Pydantic v2)
        report = {
            "engine_id": "GLB-006",
            "engine_name": "Geopolitical Risk Intelligence Engine",
            "version": "1.0.0",
            "status": "OPERATIONAL",
            "generated_at": datetime.utcnow().isoformat(),
            "core_intelligence": core_intelligence,
            "asset_impact_matrix": impact_matrix.model_dump()
            if impact_matrix
            else None,
            "metadata": {
                "calculation_time_ms": int((time.time() - start_time) * 1000),
                "event_count": len(events),
                "model_version": "1.0.0",
            },
        }

        self.last_report = report
        self.last_run_time = datetime.utcnow()

        logger.info(f"GLB-006 completed: {len(events)} events analyzed")

        return report

    def _parse_events(self) -> list[GeopoliticalEventInput]:
        """Parse events from NDIP data."""
        events_data = self._latest_data.get(NDIP_TOPICS["GEOPOLITICAL_EVENTS"], {})
        raw_events = events_data.get("events", [])

        parsed = []
        for raw in raw_events:
            try:
                parsed.append(
                    GeopoliticalEventInput(
                        event_id=raw.get(
                            "event_id", f"GEO_{datetime.utcnow().timestamp()}"
                        ),
                        event_type=GeopoliticalEventType(
                            raw.get("event_type", "POLITICAL_INSTABILITY")
                        ),
                        headline=raw.get("headline", "Unknown event"),
                        description=raw.get("description"),
                        countries=raw.get("countries", []),
                        region=raw.get("region", "UNKNOWN"),
                        severity=raw.get("severity", 50.0),
                        escalation_probability=raw.get("escalation_probability", 50.0),
                        strategic_importance=raw.get("strategic_importance", 50.0),
                        economic_exposure=raw.get("economic_exposure", 50.0),
                        market_sensitivity=raw.get("market_sensitivity", 50.0),
                        timestamp=datetime.fromisoformat(
                            raw.get("timestamp", datetime.utcnow().isoformat())
                        ),
                        source=raw.get("source", "unknown"),
                        confidence=raw.get("confidence", 70.0),
                        context=raw.get("context"),
                    )
                )
            except Exception as e:
                logger.warning(f"Failed to parse event: {e}")

        return parsed

    def _build_core_intelligence(self, global_state: dict, transmission: dict) -> dict:
        """Build core intelligence report"""
        return {
            "global_geopolitical_risk": global_state.get("global_risk_score", 0),
            "risk_state": global_state.get("risk_state", "LOW"),
            "dominant_theme": global_state.get("dominant_theme", "UNKNOWN"),
            "dominant_region": global_state.get("dominant_region", "UNKNOWN"),
            "escalation_level": global_state.get("escalation_level", "LOW"),
            "risk_trend": global_state.get("risk_trend", "STABLE"),
            "active_events": global_state.get("event_count", 0),
            "critical_events": global_state.get("critical_events", 0),
            "primary_transmission_channel": transmission.get(
                "primary_channel", "UNKNOWN"
            ),
            "transmission_channels": transmission.get("channels", {}),
            "event_analyses": global_state.get("event_analyses", [])[:5],
            "confidence": global_state.get("confidence", 50.0),
        }

    def _empty_report(self) -> dict:
        """Return empty report when no events."""
        return {
            "engine_id": "GLB-006",
            "engine_name": "Geopolitical Risk Intelligence Engine",
            "version": "1.0.0",
            "status": "OPERATIONAL",
            "generated_at": datetime.utcnow().isoformat(),
            "core_intelligence": {
                "global_geopolitical_risk": 0,
                "risk_state": "LOW",
                "dominant_theme": "UNKNOWN",
                "dominant_region": "UNKNOWN",
                "escalation_level": "LOW",
                "risk_trend": "STABLE",
                "active_events": 0,
                "critical_events": 0,
                "confidence": 50.0,
            },
            "asset_impact_matrix": None,
            "metadata": {"event_count": 0},
        }

    def get_last_report(self) -> dict | None:
        """Get the last generated report."""
        return self.last_report

    def health_check(self) -> dict[str, Any]:
        """Check engine health."""
        return {
            "engine_id": "GLB-006",
            "status": "OPERATIONAL",
            "last_run": self.last_run_time.isoformat() if self.last_run_time else None,
            "has_report": self.last_report is not None,
        }
