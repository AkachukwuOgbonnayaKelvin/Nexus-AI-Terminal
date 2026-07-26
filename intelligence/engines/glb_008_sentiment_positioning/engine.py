"""
GLB-008 Sentiment & Positioning Intelligence Engine - Main Engine
"""

import logging
import time
from datetime import datetime
from typing import Any

from .analysis.crowding_analyzer import CrowdingAnalyzer
from .analysis.divergence_analyzer import DivergenceAnalyzer
from .analysis.positioning_analyzer import PositioningAnalyzer
from .analysis.sentiment_analyzer import SentimentAnalyzer
from .constants import NDIP_TOPICS
from .impact.asset_impact_matrix import AssetImpactMatrixGenerator
from .input.data_normalizer import DataNormalizer
from .input.schemas import (
    COTInput,
    InstitutionalPositioningInput,
    OptionsSentimentInput,
    RetailSentimentInput,
)

logger = logging.getLogger(__name__)


class SentimentPositioningEngine:
    """
    GLB-008 Sentiment & Positioning Intelligence Engine

    Analyzes sentiment and positioning and produces:
    1. Core Intelligence: Sentiment and positioning analysis
    2. Asset Impact Matrix: How sentiment affects assets
    """

    def __init__(self):
        self.data_normalizer = DataNormalizer()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.positioning_analyzer = PositioningAnalyzer()
        self.crowding_analyzer = CrowdingAnalyzer()
        self.divergence_analyzer = DivergenceAnalyzer()

        self.last_report: dict | None = None
        self.last_run_time: datetime | None = None
        self._latest_data: dict[str, Any] = {}

    def consume_ndip(self, topic: str, payload: dict[str, Any]) -> None:
        """Consume NDIP contract."""
        self._latest_data[topic] = payload

    def run(self) -> dict[str, Any]:
        """Run the engine analysis."""
        start_time = time.time()

        # 1. Parse and normalize data
        cot_data = self._parse_cot()
        retail_data = self._parse_retail()
        institutional_data = self._parse_institutional()
        options_data = self._parse_options()

        if (
            not cot_data
            and not retail_data
            and not institutional_data
            and not options_data
        ):
            return self._empty_report()

        # 2. Analyze sentiment
        sentiment_analysis = self.sentiment_analyzer.analyze_sentiment(
            retail_data, options_data
        )

        # 3. Analyze positioning
        positioning_analysis = self.positioning_analyzer.analyze_positioning(
            cot_data, institutional_data
        )

        # 4. Analyze crowding
        crowding_analysis = self.crowding_analyzer.analyze_crowding(
            positioning_analysis.get("positionings", {})
        )

        # 5. Analyze divergence
        divergence_analysis = self.divergence_analyzer.analyze_divergence(
            sentiment_analysis.get("sentiment_score", 50),
            sentiment_analysis.get("sentiment_state", "NEUTRAL"),
            positioning_analysis.get("overall_bias", "NEUTRAL"),
            crowding_analysis.get("crowding_score", 50),
        )

        # 6. Build core intelligence
        core_intelligence = self._build_core_intelligence(
            sentiment_analysis,
            positioning_analysis,
            crowding_analysis,
            divergence_analysis,
        )

        # 7. Generate asset impact matrix
        impact_matrix = AssetImpactMatrixGenerator.generate(
            sentiment_analysis,
            positioning_analysis,
            crowding_analysis,
            divergence_analysis,
            core_intelligence["confidence"],
        )

        # 8. Build final report
        report = {
            "engine_id": "GLB-008",
            "engine_name": "Sentiment & Positioning Intelligence Engine",
            "version": "1.0.0",
            "status": "OPERATIONAL",
            "generated_at": datetime.utcnow().isoformat(),
            "core_intelligence": core_intelligence,
            "positioning": positioning_analysis.get("positionings", {}),
            "asset_impact_matrix": impact_matrix.model_dump()
            if impact_matrix
            else None,
            "metadata": {
                "calculation_time_ms": int((time.time() - start_time) * 1000),
                "cot_count": len(cot_data),
                "retail_count": len(retail_data),
                "model_version": "1.0.0",
            },
        }

        self.last_report = report
        self.last_run_time = datetime.utcnow()

        logger.info(
            f"GLB-008 completed: {len(cot_data)} COT records, {len(retail_data)} retail records"
        )

        return report

    def _parse_cot(self) -> list[COTInput]:
        """Parse COT data from NDIP."""
        data = self._latest_data.get(NDIP_TOPICS["COT_DATA"], {})
        raw_items = data.get("items", [])
        parsed = []
        for raw in raw_items:
            normalized = self.data_normalizer.normalize_cot(raw)
            if normalized:
                parsed.append(normalized)
        return parsed

    def _parse_retail(self) -> list[RetailSentimentInput]:
        """Parse retail sentiment from NDIP."""
        data = self._latest_data.get(NDIP_TOPICS["RETAIL_SENTIMENT"], {})
        raw_items = data.get("items", [])
        parsed = []
        for raw in raw_items:
            normalized = self.data_normalizer.normalize_retail(raw)
            if normalized:
                parsed.append(normalized)
        return parsed

    def _parse_institutional(self) -> list[InstitutionalPositioningInput]:
        """Parse institutional positioning from NDIP."""
        data = self._latest_data.get(NDIP_TOPICS["INSTITUTIONAL_POSITIONING"], {})
        raw_items = data.get("items", [])
        parsed = []
        for raw in raw_items:
            normalized = self.data_normalizer.normalize_institutional(raw)
            if normalized:
                parsed.append(normalized)
        return parsed

    def _parse_options(self) -> list[OptionsSentimentInput]:
        """Parse options sentiment from NDIP."""
        data = self._latest_data.get(NDIP_TOPICS["OPTIONS_DATA"], {})
        raw_items = data.get("items", [])
        parsed = []
        for raw in raw_items:
            normalized = self.data_normalizer.normalize_options(raw)
            if normalized:
                parsed.append(normalized)
        return parsed

    def _build_core_intelligence(
        self, sentiment: dict, positioning: dict, crowding: dict, divergence: dict
    ) -> dict:
        """Build core intelligence report"""
        return {
            "global_sentiment": sentiment.get("sentiment_state", "NEUTRAL"),
            "sentiment_score": sentiment.get("sentiment_score", 50.0),
            "positioning_bias": positioning.get("overall_bias", "NEUTRAL"),
            "crowding_state": crowding.get("crowding_state", "LOW"),
            "crowding_score": crowding.get("crowding_score", 50.0),
            "contrarian_risk": "HIGH"
            if divergence.get("divergence_detected", False)
            else "LOW",
            "positioning_extreme": crowding.get("crowding_state", "LOW")
            in ["HIGH", "EXTREME"],
            "dominant_sentiment_theme": self._determine_theme(sentiment, positioning),
            "divergence_detected": divergence.get("divergence_detected", False),
            "divergence_type": divergence.get("divergence_type", "NONE"),
            "confidence": sentiment.get("confidence", 50.0),
        }

    def _determine_theme(self, sentiment: dict, positioning: dict) -> str:
        """Determine dominant sentiment theme"""
        sentiment_state = sentiment.get("sentiment_state", "NEUTRAL")
        positioning_bias = positioning.get("overall_bias", "NEUTRAL")

        if sentiment_state == "RISK_ON" and positioning_bias == "LONG":
            return "RISK_APPETITE"
        elif sentiment_state == "RISK_OFF" and positioning_bias == "SHORT":
            return "RISK_AVERSION"
        elif sentiment_state == "RISK_ON" and positioning_bias == "SHORT":
            return "BULLISH_SENTIMENT_BEARISH_POSITIONING"
        elif sentiment_state == "RISK_OFF" and positioning_bias == "LONG":
            return "BEARISH_SENTIMENT_BULLISH_POSITIONING"
        return "MIXED_SIGNALS"

    def _empty_report(self) -> dict:
        """Return empty report when no data."""
        return {
            "engine_id": "GLB-008",
            "engine_name": "Sentiment & Positioning Intelligence Engine",
            "version": "1.0.0",
            "status": "OPERATIONAL",
            "generated_at": datetime.utcnow().isoformat(),
            "core_intelligence": {
                "global_sentiment": "NEUTRAL",
                "sentiment_score": 50.0,
                "positioning_bias": "NEUTRAL",
                "crowding_state": "LOW",
                "crowding_score": 50.0,
                "contrarian_risk": "LOW",
                "positioning_extreme": False,
                "dominant_sentiment_theme": "NO_DATA",
                "confidence": 50.0,
            },
            "positioning": {},
            "asset_impact_matrix": None,
            "metadata": {"cot_count": 0, "retail_count": 0},
        }

    def get_last_report(self) -> dict | None:
        return self.last_report

    def health_check(self) -> dict[str, Any]:
        return {
            "engine_id": "GLB-008",
            "status": "OPERATIONAL",
            "last_run": self.last_run_time.isoformat() if self.last_run_time else None,
            "has_report": self.last_report is not None,
        }
