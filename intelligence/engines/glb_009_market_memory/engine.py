"""
GLB-009 Market Memory & Historical Analogy Intelligence Engine - Main Engine
"""

import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime

from .input.schemas import MarketSnapshot
from .canonical_memory_connector import CanonicalMemoryConnector
from .analogues.analogue_engine import AnalogueEngine
from .analogues.outcome_analyzer import OutcomeAnalyzer
from .analogues.cross_asset_confirmation import CrossAssetConfirmation
from .impact.asset_impact_matrix import AssetImpactMatrixGenerator

logger = logging.getLogger(__name__)


class MarketMemoryEngine:
    """
    GLB-009 Market Memory & Historical Analogy Intelligence Engine

    Analyzes historical analogues and produces:
    1. Core Intelligence: Historical analogy analysis
    2. Asset Impact Matrix: Historical outcome-based asset impacts
    """

    def __init__(self, data_file: str = "canonical_historical_windows.json"):
        self.historical_memory = CanonicalMemoryConnector(data_file)
        self.analogue_engine = AnalogueEngine()
        self.outcome_analyzer = OutcomeAnalyzer()
        self.cross_asset_confirmation = CrossAssetConfirmation()

        self.last_report: Optional[Dict] = None
        self.last_run_time: Optional[datetime] = None
        self._latest_data: Dict[str, Any] = {}

        # Load historical data
        self.historical_memory.load()

        # Set available assets for outcome analyzer
        available_assets = self.historical_memory.get_symbols()
        self.outcome_analyzer.set_available_assets(available_assets)

    def consume_ndip(self, topic: str, payload: Dict[str, Any]) -> None:
        """Consume NDIP contract."""
        self._latest_data[topic] = payload

    def run(self) -> Dict[str, Any]:
        """Run the engine analysis."""
        start_time = time.time()

        # 1. Build current snapshot
        current = self._build_current_snapshot()

        # 2. Check historical memory
        if not self.historical_memory.is_ready():
            return self._memory_not_ready_report()

        # 3. Get historical windows
        historical_windows = self.historical_memory.get_windows()

        if not historical_windows:
            return self._empty_report()

        # 4. Find analogues
        analogue_analysis = self.analogue_engine.find_analogues(
            current, historical_windows
        )

        if analogue_analysis.get("status") != "OPERATIONAL":
            return self._empty_report()

        analogues = analogue_analysis.get("analogues", [])

        # 5. Analyze outcomes for each available asset
        available_assets = self.historical_memory.get_symbols()
        asset_outcomes = {}

        for asset in available_assets:
            outcome = self.outcome_analyzer.analyze_outcomes(analogues, asset)
            asset_outcomes[asset] = outcome

        # 6. Cross-asset confirmation
        current_environment = {"asset_impacts": self._get_current_asset_impacts()}
        cross_asset = self.cross_asset_confirmation.analyze_confirmation(
            analogues, current_environment
        )

        # 7. Build core intelligence
        core_intelligence = self._build_core_intelligence(
            analogue_analysis, asset_outcomes, cross_asset
        )

        # 8. Generate asset impact matrix (using available assets)
        impact_matrix = AssetImpactMatrixGenerator.generate(
            {"asset_outcomes": asset_outcomes, "analogues": analogues},
            cross_asset,
            analogue_analysis,
            core_intelligence["confidence"],
            available_assets=available_assets,
        )

        # 9. Build final report
        report = {
            "engine_id": "GLB-009",
            "engine_name": "Market Memory & Historical Analogy Intelligence Engine",
            "version": "1.0.0",
            "status": "OPERATIONAL",
            "generated_at": datetime.utcnow().isoformat(),
            "historical_memory_status": self.historical_memory.get_stats(),
            "core_intelligence": core_intelligence,
            "analogue_analysis": analogue_analysis,
            "cross_asset_confirmation": cross_asset,
            "asset_outcomes": asset_outcomes,
            "asset_impact_matrix": impact_matrix.model_dump()
            if impact_matrix
            else None,
            "metadata": {
                "calculation_time_ms": int((time.time() - start_time) * 1000),
                "analogues_found": len(analogues),
                "windows_processed": len(historical_windows),
                "available_assets": len(available_assets),
                "model_version": "1.0.0",
            },
        }

        self.last_report = report
        self.last_run_time = datetime.utcnow()

        logger.info(
            f"GLB-009 completed: {len(analogues)} analogues found from {len(historical_windows)} windows"
        )

        return report

    def _build_current_snapshot(self) -> MarketSnapshot:
        """Build current market snapshot from NDIP data"""
        prices = self._latest_data.get("asset_prices", {})
        if not prices:
            prices = {"AUDUSD": 0.6650, "US500": 4800.0, "XAUUSD": 1950.0}

        return MarketSnapshot(
            timestamp=datetime.utcnow(),
            regime=self._latest_data.get("regime", "UNKNOWN"),
            macro_score=self._latest_data.get("macro_score", 50),
            central_bank_score=self._latest_data.get("central_bank_score", 50),
            geopolitical_risk=self._latest_data.get("geopolitical_risk", 50),
            capital_flow_score=self._latest_data.get("capital_flow_score", 50),
            sentiment_score=self._latest_data.get("sentiment_score", 50),
            positioning_score=self._latest_data.get("positioning_score", 50),
            volatility_score=self._latest_data.get("volatility_score", 50),
            asset_prices=prices,
        )

    def _get_current_asset_impacts(self) -> Dict:
        """Get current asset impacts from other GLB engines"""
        return {}

    def _build_core_intelligence(
        self, analogue_analysis: Dict, asset_outcomes: Dict, cross_asset: Dict
    ) -> Dict:
        """Build core intelligence report"""
        distribution = {"BULLISH": 0, "BEARISH": 0, "NEUTRAL": 0}
        count = 0
        for asset, outcome in asset_outcomes.items():
            if outcome.get("status") == "OPERATIONAL":
                dist = outcome.get("outcome_distribution", {})
                distribution["BULLISH"] += dist.get("BULLISH", 0)
                distribution["BEARISH"] += dist.get("BEARISH", 0)
                distribution["NEUTRAL"] += dist.get("NEUTRAL", 0)
                count += 1

        if count > 0:
            distribution["BULLISH"] = distribution["BULLISH"] / count
            distribution["BEARISH"] = distribution["BEARISH"] / count
            distribution["NEUTRAL"] = distribution["NEUTRAL"] / count

        return {
            "historical_bias": self._determine_bias(asset_outcomes),
            "preferred_horizon": self._determine_horizon(asset_outcomes),
            "expected_environment": self._determine_environment(analogue_analysis),
            "historical_confidence": analogue_analysis.get("confidence", 50),
            "analogue_quality": analogue_analysis.get("quality", "LOW"),
            "cross_asset_confirmation": cross_asset.get("confirmation_level", "NONE"),
            "analogues_found": analogue_analysis.get("qualified_analogues", 0),
            "best_match": analogue_analysis.get("best_match", 0),
            "match_confidence": analogue_analysis.get("match_confidence", 50),
            "outcome_distribution": distribution,
            "confidence": analogue_analysis.get("confidence", 50),
        }

    def _determine_bias(self, asset_outcomes: Dict) -> str:
        bullish_count = 0
        bearish_count = 0
        for asset, outcome in asset_outcomes.items():
            if outcome.get("overall_direction") == "BULLISH":
                bullish_count += 1
            elif outcome.get("overall_direction") == "BEARISH":
                bearish_count += 1
        if bullish_count > bearish_count:
            return "BULLISH"
        elif bearish_count > bullish_count:
            return "BEARISH"
        return "MIXED"

    def _determine_horizon(self, asset_outcomes: Dict) -> str:
        horizon_scores = {
            "INTRADAY": 0,
            "SHORT_TERM": 0,
            "MEDIUM_TERM": 0,
            "LONG_TERM": 0,
        }
        for asset, outcome in asset_outcomes.items():
            for horizon, data in outcome.get("horizon_results", {}).items():
                if data.get("bullish_percent", 0) > data.get("bearish_percent", 0):
                    horizon_scores[horizon] += 1
        best = max(horizon_scores.items(), key=lambda x: x[1])
        return best[0] if best[1] > 0 else "MIXED"

    def _determine_environment(self, analogue_analysis: Dict) -> str:
        if analogue_analysis.get("quality") == "HIGH":
            return "RISK_OFF CONTINUATION"
        return "MIXED"

    def _memory_not_ready_report(self) -> Dict:
        return {
            "engine_id": "GLB-009",
            "engine_name": "Market Memory & Historical Analogy Intelligence Engine",
            "version": "1.0.0",
            "status": "COLD_START",
            "generated_at": datetime.utcnow().isoformat(),
            "historical_memory_status": self.historical_memory.get_stats(),
            "core_intelligence": {
                "historical_bias": "NEUTRAL",
                "preferred_horizon": "MIXED",
                "historical_confidence": 50.0,
                "analogue_quality": "INSUFFICIENT",
                "confidence": 50.0,
                "reason": "Insufficient historical observations for statistically valid analogue comparison",
            },
            "asset_impact_matrix": None,
            "metadata": {"analogues_found": 0, "status": "COLD_START"},
        }

    def _empty_report(self) -> Dict:
        return {
            "engine_id": "GLB-009",
            "engine_name": "Market Memory & Historical Analogy Intelligence Engine",
            "version": "1.0.0",
            "status": "OPERATIONAL",
            "generated_at": datetime.utcnow().isoformat(),
            "historical_memory_status": self.historical_memory.get_stats(),
            "core_intelligence": {
                "historical_bias": "NEUTRAL",
                "preferred_horizon": "MIXED",
                "historical_confidence": 50.0,
                "analogue_quality": "INSUFFICIENT",
                "confidence": 50.0,
                "reason": "No qualified analogues found in historical memory",
            },
            "asset_impact_matrix": None,
            "metadata": {"analogues_found": 0},
        }

    def get_last_report(self) -> Optional[Dict]:
        return self.last_report

    def health_check(self) -> Dict[str, Any]:
        return {
            "engine_id": "GLB-009",
            "status": "OPERATIONAL"
            if self.historical_memory.is_ready()
            else "COLD_START",
            "last_run": self.last_run_time.isoformat() if self.last_run_time else None,
            "has_report": self.last_report is not None,
            "historical_memory": self.historical_memory.get_stats(),
        }
