# -*- coding: utf-8 -*-
"""
GLB-003: Macro Intelligence Engine

This engine consumes macroeconomic data from MAC-001 and produces
standardized intelligence reports about the macro environment.
"""

from typing import Dict, Any, List
from datetime import datetime
import logging

from intelligence.base.intelligence_engine import IntelligenceEngine

from intelligence_engines.glb_003_macro_intelligence.analyzers.gdp_analyzer import (
    GDPAnalyzer,
)
from intelligence_engines.glb_003_macro_intelligence.analyzers.cpi_analyzer import (
    CPIAnalyzer,
)
from intelligence_engines.glb_003_macro_intelligence.analyzers.employment_analyzer import (
    EmploymentAnalyzer,
)
from intelligence_engines.glb_003_macro_intelligence.analyzers.pmi_analyzer import (
    PMIAnalyzer,
)
from intelligence_engines.glb_003_macro_intelligence.asset_impact_matrix import (
    MacroAssetImpactMatrix,
)


logger = logging.getLogger(__name__)


class MacroIntelligenceEngine(IntelligenceEngine):
    """Macro Intelligence Engine (GLB-003)"""

    def __init__(self):
        super().__init__(
            engine_id="GLB-003",
            engine_name="Macro Intelligence Engine",
            domain="global",
        )

        self.gdp_analyzer = GDPAnalyzer()
        self.cpi_analyzer = CPIAnalyzer()
        self.employment_analyzer = EmploymentAnalyzer()
        self.pmi_analyzer = PMIAnalyzer()

        self._analysis_results = {}
        self._last_impact_matrix = None

    def get_required_ndip_topics(self) -> List[str]:
        return [
            "macro.statistics.gdp",
            "macro.statistics.cpi",
            "macro.statistics.employment",
            "macro.statistics.pmi",
        ]

    def analyze(self, ndip_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run macro intelligence analysis.
        """
        # Analyze each macro component
        gdp_result = self.gdp_analyzer.analyze(
            ndip_data.get("macro.statistics.gdp", {})
        )
        cpi_result = self.cpi_analyzer.analyze(
            ndip_data.get("macro.statistics.cpi", {})
        )
        employment_result = self.employment_analyzer.analyze(
            ndip_data.get("macro.statistics.employment", {})
        )
        pmi_result = self.pmi_analyzer.analyze(
            ndip_data.get("macro.statistics.pmi", {})
        )

        self._analysis_results = {
            "gdp": gdp_result,
            "cpi": cpi_result,
            "employment": employment_result,
            "pmi": pmi_result,
        }

        # Generate Asset Impact Matrix
        growth_score = gdp_result.get("score", 50)
        inflation_score = cpi_result.get("score", 50)
        employment_score = employment_result.get("score", 50)
        overall_confidence = self._calculate_overall_confidence()

        impact_matrix = MacroAssetImpactMatrix.generate(
            macro_score=self._calculate_overall_score(),
            growth_score=growth_score,
            inflation_score=inflation_score,
            employment_score=employment_score,
            confidence=overall_confidence,
        )
        self._last_impact_matrix = impact_matrix

        return self._build_report()

    def _calculate_overall_score(self) -> float:
        """Calculate overall macro score."""
        if not self._analysis_results:
            return 50.0

        scores = []
        for key, result in self._analysis_results.items():
            if "score" in result:
                scores.append(result["score"])

        if not scores:
            return 50.0

        return sum(scores) / len(scores)

    def _calculate_overall_confidence(self) -> float:
        """Calculate overall confidence."""
        if not self._analysis_results:
            return 50.0

        confidences = []
        for key, result in self._analysis_results.items():
            if "confidence" in result:
                confidences.append(result["confidence"])

        if not confidences:
            return 70.0

        return sum(confidences) / len(confidences)

    def _build_report(self) -> Dict[str, Any]:
        """Build the engine report."""
        overall_score = self._calculate_overall_score()
        confidence = self._calculate_overall_confidence()

        return {
            "engine_id": "GLB-003",
            "engine_name": "Macro Intelligence Engine",
            "status": "OPERATIONAL",
            "generated_at": datetime.utcnow().isoformat(),
            "overall_score": overall_score,
            "confidence": confidence,
            "macro_components": self._analysis_results,
            "asset_impact_matrix": self._last_impact_matrix,
            "metadata": {
                "component_count": len(self._analysis_results),
                "model_version": "1.0.0",
            },
        }

    def get_asset_impact_matrix(self):
        """Get the last generated asset impact matrix."""
        return self._last_impact_matrix

    def health_check(self) -> Dict[str, Any]:
        return {
            "engine_id": "GLB-003",
            "status": "OPERATIONAL",
            "has_analysis": bool(self._analysis_results),
            "has_impact_matrix": self._last_impact_matrix is not None,
        }
