"""
GLB-001 Market Regime Engine - Main Engine Class
"""

import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime

from .constants import MarketRegime, TransitionState
from .schemas import RegimeReport, RegimeSignal
from .input_normalizer import InputNormalizer
from .state_extractor import StateExtractor
from .regime_classifier import RegimeClassifier
from .evidence_builder import EvidenceBuilder
from .confidence_engine import ConfidenceEngine
from .risk_engine import RiskEngine
from .report_generator import ReportGenerator
from .asset_impact_matrix import RegimeAssetImpactMatrix

logger = logging.getLogger(__name__)


class MarketRegimeEngine:
    """
    GLB-001 Market Regime Engine

    Consumes NDIP contracts and produces a Market Regime Report.
    """

    def __init__(self):
        self.input_normalizer = InputNormalizer()
        self.state_extractor = StateExtractor()
        self.regime_classifier = RegimeClassifier()
        self.evidence_builder = EvidenceBuilder()
        self.confidence_engine = ConfidenceEngine()
        self.risk_engine = RiskEngine()
        self.report_generator = ReportGenerator()

        self.last_report: Optional[RegimeReport] = None
        self.last_run_time: Optional[datetime] = None

    def consume_ndip(self, topic: str, payload: Dict[str, Any]) -> None:
        """Consume NDIP contract."""
        self.input_normalizer.consume_ndip(topic, payload)

    def run(self) -> RegimeReport:
        """Run the engine analysis."""
        start_time = time.time()

        if not self.input_normalizer.has_required_data():
            logger.warning("Missing required NDIP data")
            return self._error_report("MISSING_DATA")

        if not self.input_normalizer.is_fresh():
            logger.warning("NDIP data is stale")
            return self._error_report("STALE_DATA")

        normalized = self.input_normalizer.normalize()
        dimensions = self.state_extractor.extract(normalized)
        primary_regime, regime_score, regime_probabilities = (
            self.regime_classifier.classify(dimensions)
        )
        transition_state = self.regime_classifier.determine_transition_state(
            primary_regime, regime_probabilities
        )
        signals = self._build_signals(dimensions)
        evidence = self.evidence_builder.build_evidence(dimensions, normalized)
        confidence = self.confidence_engine.calculate_confidence(
            primary_regime.value, dimensions, evidence, regime_probabilities
        )
        risks = self.risk_engine.identify_risks(
            primary_regime, normalized, regime_probabilities
        )
        drivers = self._build_drivers(dimensions)
        secondary_regime = self._determine_secondary_regime(regime_probabilities)

        report = self.report_generator.generate(
            primary_regime=primary_regime,
            secondary_regime=secondary_regime,
            transition_state=transition_state,
            regime_score=regime_score,
            confidence=confidence,
            dimensions=list(dimensions.values()),
            regime_probabilities=regime_probabilities,
            signals=signals,
            evidence=evidence,
            risks=risks,
            drivers=drivers,
            normalized_data=normalized,
        )

        # Generate Asset Impact Matrix
        impact_matrix = RegimeAssetImpactMatrix.generate(
            primary_regime.value, confidence
        )
        report.asset_impact_matrix = impact_matrix

        report.metadata["calculation_time_ms"] = int((time.time() - start_time) * 1000)
        report.generated_at = datetime.utcnow()

        self.last_report = report
        self.last_run_time = datetime.utcnow()

        logger.info(
            f"GLB-001 completed: {primary_regime.value} (score: {regime_score:.1f}, confidence: {confidence:.1f}%)"
        )

        return report

    def _build_signals(self, dimensions: Dict[str, Any]) -> list:
        signals = []
        for name, dim in dimensions.items():
            signals.append(
                RegimeSignal(
                    name=name.replace("_", " ").title(),
                    value=dim.direction,
                    weight=dim.weight,
                    contribution=dim.contribution,
                )
            )
        return signals

    def _build_drivers(self, dimensions: Dict[str, Any]) -> list:
        from .schemas import RegimeDriver

        drivers = []
        for name, dim in dimensions.items():
            if dim.direction != "NEUTRAL":
                drivers.append(
                    RegimeDriver(
                        name=name.replace("_", " ").title(),
                        direction=dim.direction,
                        strength=dim.value / 100,
                    )
                )
        return drivers

    def _determine_secondary_regime(
        self, probabilities: Dict[str, float]
    ) -> Optional[MarketRegime]:
        sorted_regimes = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_regimes) >= 2:
            return sorted_regimes[1][0]
        return None

    def _error_report(self, error_code: str) -> RegimeReport:
        from .schemas import RegimeReport

        return RegimeReport(
            primary_regime=MarketRegime.TRANSITION,
            transition_state=TransitionState.STABLE,
            regime_score=0,
            confidence=0,
            dimensions=[],
            regime_probabilities={},
            signals=[],
            evidence=[],
            risks=[],
            drivers=[],
            asset_context={},
            metadata={"error": error_code, "status": "ERROR"},
        )

    def get_last_report(self) -> Optional[RegimeReport]:
        return self.last_report

    def health_check(self) -> Dict[str, Any]:
        return {
            "engine_id": "GLB-001",
            "status": "OPERATIONAL",
            "last_run": self.last_run_time.isoformat() if self.last_run_time else None,
            "has_report": self.last_report is not None,
            "ready": self.input_normalizer.has_required_data(),
        }
