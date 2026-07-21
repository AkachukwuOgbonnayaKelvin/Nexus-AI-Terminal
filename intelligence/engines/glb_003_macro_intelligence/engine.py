"""
GLB-003 Macro Intelligence Engine - Main Engine
"""

import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime

from .constants import COMPONENT_WEIGHTS
from .schemas import (
    MacroReport,
    MacroComponent,
    MacroSignal,
    MacroEvidence,
    MacroRisk,
    MacroDriver,
)
from .asset_impact_matrix import MacroAssetImpactMatrix

logger = logging.getLogger(__name__)


class MacroIntelligenceEngine:
    """
    GLB-003 Macro Intelligence Engine

    Analyzes macroeconomic conditions and produces:
    1. Macro intelligence report
    2. Asset Impact Matrix for the Global Intelligence Hub
    """

    def __init__(self):
        self.last_report: Optional[MacroReport] = None
        self.last_run_time: Optional[datetime] = None
        self._latest_data: Dict[str, Any] = {}

    def consume_ndip(self, topic: str, payload: Dict[str, Any]) -> None:
        """Consume NDIP contract."""
        self._latest_data[topic] = payload

    def run(self) -> MacroReport:
        """Run the engine analysis."""
        start_time = time.time()

        # 1. Analyze macro components with defaults
        components = self._analyze_components()

        # 2. Calculate overall score
        overall_score = self._calculate_overall_score(components)

        # 3. Calculate confidence
        confidence = self._calculate_confidence(components)

        # 4. Generate signals
        signals = self._generate_signals(components)

        # 5. Build evidence
        evidence = self._build_evidence(components)

        # 6. Identify risks
        risks = self._identify_risks(components)

        # 7. Build drivers
        drivers = self._build_drivers(components)

        # 8. Generate report
        report = MacroReport(
            overall_score=overall_score,
            confidence=confidence,
            macro_components=components,
            signals=signals,
            evidence=evidence,
            risks=risks,
            drivers=drivers,
            metadata={
                "calculation_time_ms": int((time.time() - start_time) * 1000),
                "component_count": len(components),
                "model_version": "1.0.0",
            },
        )

        # 9. Generate Asset Impact Matrix
        growth_score = components.get(
            "growth",
            MacroComponent(
                name="growth",
                score=50,
                value=0,
                trend="STABLE",
                signal="NEUTRAL",
                confidence=50,
            ),
        ).score
        inflation_score = components.get(
            "inflation",
            MacroComponent(
                name="inflation",
                score=50,
                value=0,
                trend="STABLE",
                signal="NEUTRAL",
                confidence=50,
            ),
        ).score
        employment_score = components.get(
            "employment",
            MacroComponent(
                name="employment",
                score=50,
                value=0,
                trend="STABLE",
                signal="NEUTRAL",
                confidence=50,
            ),
        ).score

        impact_matrix = MacroAssetImpactMatrix.generate(
            macro_score=overall_score,
            growth_score=growth_score,
            inflation_score=inflation_score,
            employment_score=employment_score,
            confidence=confidence,
        )
        report.asset_impact_matrix = impact_matrix

        self.last_report = report
        self.last_run_time = datetime.utcnow()

        logger.info(
            f"GLB-003 completed: Macro Score {overall_score:.1f}, Confidence {confidence:.1f}%"
        )

        return report

    def _analyze_components(self) -> Dict[str, MacroComponent]:
        """Analyze macro components with default values."""
        components = {}

        components["growth"] = MacroComponent(
            name="growth",
            score=72.0,
            value=2.8,
            trend="INCREASING",
            signal="BULLISH",
            confidence=70.0,
        )

        components["inflation"] = MacroComponent(
            name="inflation",
            score=35.0,
            value=2.4,
            trend="DECREASING",
            signal="BULLISH",
            confidence=75.0,
        )

        components["employment"] = MacroComponent(
            name="employment",
            score=68.0,
            value=3.2,
            trend="DECREASING",
            signal="BULLISH",
            confidence=80.0,
        )

        components["pmi"] = MacroComponent(
            name="pmi",
            score=54.0,
            value=54.0,
            trend="INCREASING",
            signal="BULLISH",
            confidence=65.0,
        )

        return components

    def _calculate_overall_score(self, components: Dict[str, MacroComponent]) -> float:
        """Calculate overall macro score."""
        total = 0.0
        total_weight = 0.0

        for name, component in components.items():
            weight = COMPONENT_WEIGHTS.get(name, 0.2)
            total += component.score * weight
            total_weight += weight

        return total / total_weight if total_weight > 0 else 50.0

    def _calculate_confidence(self, components: Dict[str, MacroComponent]) -> float:
        """Calculate confidence in macro analysis."""
        if not components:
            return 50.0

        confidences = [c.confidence for c in components.values()]
        return sum(confidences) / len(confidences)

    def _generate_signals(self, components: Dict[str, MacroComponent]) -> list:
        signals = []
        for name, component in components.items():
            signals.append(
                MacroSignal(
                    name=name.title(),
                    value=component.signal,
                    weight=COMPONENT_WEIGHTS.get(name, 0.2),
                )
            )
        return signals

    def _build_evidence(self, components: Dict[str, MacroComponent]) -> list:
        evidence = []
        for name, component in components.items():
            evidence.append(
                MacroEvidence(
                    source="MAC-001",
                    indicator=name.upper(),
                    value=component.value,
                    contribution=component.confidence / 100.0,
                )
            )
        return evidence

    def _identify_risks(self, components: Dict[str, MacroComponent]) -> list:
        risks = []

        growth = components.get("growth")
        if growth and growth.score < 40:
            risks.append(
                MacroRisk(
                    description="Weak growth could lead to recession",
                    probability=0.30,
                    impact="HIGH",
                )
            )

        inflation = components.get("inflation")
        if inflation and inflation.score < 30:
            risks.append(
                MacroRisk(
                    description="High inflation could force central bank action",
                    probability=0.25,
                    impact="HIGH",
                )
            )

        if not risks:
            risks.append(
                MacroRisk(
                    description="Stable macro environment",
                    probability=0.10,
                    impact="LOW",
                )
            )

        return risks

    def _build_drivers(self, components: Dict[str, MacroComponent]) -> list:
        drivers = []
        for name, component in components.items():
            if component.signal != "NEUTRAL":
                drivers.append(
                    MacroDriver(
                        name=f"{name.title()} Momentum",
                        direction=component.signal,
                        strength=component.score / 100.0,
                    )
                )
        return drivers

    def get_last_report(self) -> Optional[MacroReport]:
        return self.last_report

    def health_check(self) -> Dict[str, Any]:
        return {
            "engine_id": "GLB-003",
            "status": "OPERATIONAL",
            "last_run": self.last_run_time.isoformat() if self.last_run_time else None,
            "has_report": self.last_report is not None,
        }
