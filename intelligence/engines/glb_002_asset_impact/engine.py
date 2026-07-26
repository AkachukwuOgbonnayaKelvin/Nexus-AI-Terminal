"""
GLB-002 Asset Impact Engine - Main Engine
"""

import logging
import time
from datetime import datetime
from typing import Any

from .asset_impact_matrix import AssetImpactMatrixGenerator
from .constants import Bias
from .currency_strength import CurrencyStrengthEngine
from .pair_comparison import PairComparisonEngine
from .schemas import AssetImpactReport, CurrencyStrength, PairComparison

logger = logging.getLogger(__name__)


class AssetImpactEngine:
    """
    GLB-002 Asset Impact Engine

    Analyzes global factors and produces:
    1. Individual currency strengths
    2. Pair comparisons with directional bias
    3. Asset Impact Matrix for the Global Intelligence Hub
    """

    def __init__(self):
        self.currency_strength_engine = CurrencyStrengthEngine()
        self.pair_comparison_engine = PairComparisonEngine()

        self.last_report: AssetImpactReport | None = None
        self.last_run_time: datetime | None = None
        self._latest_data: dict[str, Any] | None = None
        self._last_impact_matrix: Any | None = None

    def consume_ndip(self, topic: str, payload: dict[str, Any]) -> None:
        """Consume NDIP contract."""
        self._latest_data = payload

    def run(self, global_factors: dict[str, Any] | None = None) -> AssetImpactReport:
        """Run the engine analysis."""
        start_time = time.time()

        if global_factors is None:
            global_factors = self._get_default_factors()

        # 1. Calculate individual currency strengths
        currency_strengths = self.currency_strength_engine.calculate(global_factors)

        # 2. Compare pairs
        pair_analyses = self.pair_comparison_engine.compare_pairs(
            currency_strengths, global_factors
        )

        # 3. Generate Asset Impact Matrix
        overall_confidence = 85.0  # Confidence in GLB-002's analysis
        impact_matrix = AssetImpactMatrixGenerator.generate(
            currency_strengths, pair_analyses, overall_confidence
        )
        self._last_impact_matrix = impact_matrix

        # 4. Build summary
        summary = self._build_summary(currency_strengths, pair_analyses)

        # 5. Generate report
        report = AssetImpactReport(
            currency_strengths=currency_strengths,
            pair_analyses=pair_analyses,
            summary=summary,
            metadata={
                "calculation_time_ms": int((time.time() - start_time) * 1000),
                "currencies_analyzed": len(currency_strengths),
                "pairs_analyzed": len(pair_analyses),
                "model_version": "1.0.0",
            },
        )

        # Add impact matrix to report
        report.asset_impact_matrix = impact_matrix

        self.last_report = report
        self.last_run_time = datetime.utcnow()

        logger.info(f"GLB-002 completed: {len(pair_analyses)} pairs analyzed")

        return report

    def get_asset_impact_matrix(self) -> Any | None:
        """Get the last generated asset impact matrix."""
        return self._last_impact_matrix

    def _get_default_factors(self) -> dict[str, Any]:
        """Get default global factors for testing."""
        return {
            "currencies": {
                "USD": {
                    "growth": 55,
                    "inflation": 62,
                    "rates": 48,
                    "central_bank": 45,
                    "risk_sentiment": 50,
                    "liquidity": 55,
                    "geopolitical": 50,
                },
                "EUR": {
                    "growth": 72,
                    "inflation": 58,
                    "rates": 65,
                    "central_bank": 70,
                    "risk_sentiment": 68,
                    "liquidity": 65,
                    "geopolitical": 45,
                },
                "GBP": {
                    "growth": 65,
                    "inflation": 60,
                    "rates": 62,
                    "central_bank": 60,
                    "risk_sentiment": 58,
                    "liquidity": 60,
                    "geopolitical": 40,
                },
                "JPY": {
                    "growth": 45,
                    "inflation": 40,
                    "rates": 35,
                    "central_bank": 30,
                    "risk_sentiment": 48,
                    "liquidity": 50,
                    "geopolitical": 55,
                },
                "CHF": {
                    "growth": 50,
                    "inflation": 42,
                    "rates": 38,
                    "central_bank": 40,
                    "risk_sentiment": 45,
                    "liquidity": 55,
                    "geopolitical": 60,
                },
                "CAD": {
                    "growth": 68,
                    "inflation": 52,
                    "rates": 55,
                    "central_bank": 58,
                    "risk_sentiment": 55,
                    "liquidity": 50,
                    "geopolitical": 45,
                },
                "AUD": {
                    "growth": 70,
                    "inflation": 48,
                    "rates": 60,
                    "central_bank": 65,
                    "risk_sentiment": 62,
                    "liquidity": 58,
                    "geopolitical": 50,
                },
                "NZD": {
                    "growth": 72,
                    "inflation": 45,
                    "rates": 62,
                    "central_bank": 68,
                    "risk_sentiment": 60,
                    "liquidity": 55,
                    "geopolitical": 45,
                },
            }
        }

    def _build_summary(
        self,
        currency_strengths: dict[str, CurrencyStrength],
        pair_analyses: dict[str, PairComparison],
    ) -> dict[str, Any]:
        """Build summary statistics."""
        sorted_currencies = sorted(
            currency_strengths.values(), key=lambda x: x.score, reverse=True
        )

        bullish = sum(1 for p in pair_analyses.values() if p.bias == Bias.BULLISH)
        bearish = sum(1 for p in pair_analyses.values() if p.bias == Bias.BEARISH)
        neutral = sum(1 for p in pair_analyses.values() if p.bias == Bias.NEUTRAL)

        return {
            "strongest_currency": sorted_currencies[0].currency
            if sorted_currencies
            else None,
            "strongest_score": sorted_currencies[0].score if sorted_currencies else 0,
            "weakest_currency": sorted_currencies[-1].currency
            if sorted_currencies
            else None,
            "weakest_score": sorted_currencies[-1].score if sorted_currencies else 0,
            "total_currencies": len(currency_strengths),
            "total_pairs": len(pair_analyses),
            "bullish_pairs": bullish,
            "bearish_pairs": bearish,
            "neutral_pairs": neutral,
            "overall_bias": "BULLISH"
            if bullish > bearish
            else "BEARISH"
            if bearish > bullish
            else "NEUTRAL",
        }

    def get_last_report(self) -> AssetImpactReport | None:
        """Get the last generated report."""
        return self.last_report

    def health_check(self) -> dict[str, Any]:
        """Check engine health."""
        return {
            "engine_id": "GLB-002",
            "status": "OPERATIONAL",
            "last_run": self.last_run_time.isoformat() if self.last_run_time else None,
            "has_report": self.last_report is not None,
            "has_impact_matrix": self._last_impact_matrix is not None,
        }
