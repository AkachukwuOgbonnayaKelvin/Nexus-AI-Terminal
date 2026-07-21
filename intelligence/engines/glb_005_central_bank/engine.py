"""
GLB-005 Central Bank Intelligence Engine - Main Engine
"""

import logging
import time
from typing import Dict, Any, Optional, List
from datetime import datetime

from .constants import NDIP_TOPICS, CentralBank, PolicyStance
from .input.schemas import CentralBankInput, RateExpectation, BalanceSheetData
from .analysis.policy_analyzer import PolicyAnalyzer
from .analysis.rate_forecaster import RateForecaster
from .transmission.policy_divergence import PolicyDivergenceEngine
from .impact.asset_impact_matrix import AssetImpactMatrixGenerator

logger = logging.getLogger(__name__)


class CentralBankEngine:
    """
    GLB-005 Central Bank Intelligence Engine

    Analyzes central bank policy and produces:
    1. Core Intelligence: Policy environment analysis
    2. Asset Impact Matrix: How policy affects assets
    """

    def __init__(self):
        self.policy_analyzer = PolicyAnalyzer()
        self.rate_forecaster = RateForecaster()
        self.divergence_engine = PolicyDivergenceEngine()

        self.last_report: Optional[Dict] = None
        self.last_run_time: Optional[datetime] = None
        self._latest_data: Dict[str, Any] = {}

    def consume_ndip(self, topic: str, payload: Dict[str, Any]) -> None:
        """Consume NDIP contract."""
        self._latest_data[topic] = payload

    def run(self) -> Dict[str, Any]:
        """Run the engine analysis."""
        start_time = time.time()

        # 1. Parse and normalize central bank data
        bank_data = self._parse_bank_data()

        if not bank_data:
            return self._empty_report()

        # 2. Analyze policy stance
        policy_analysis = self.policy_analyzer.analyze_all_banks(bank_data)

        # 3. Forecast rates
        rate_forecast = self.rate_forecaster.forecast_all_banks(bank_data)

        # 4. Calculate policy divergence
        divergence = self.divergence_engine.calculate_divergence(bank_data)

        # 5. Build core intelligence
        core_intelligence = self._build_core_intelligence(
            policy_analysis, rate_forecast, divergence
        )

        # 6. Generate asset impact matrix
        impact_matrix = AssetImpactMatrixGenerator.generate(
            bank_data, divergence, rate_forecast, core_intelligence["confidence"]
        )

        # 7. Build final report
        report = {
            "engine_id": "GLB-005",
            "engine_name": "Central Bank Intelligence Engine",
            "version": "1.0.0",
            "status": "OPERATIONAL",
            "generated_at": datetime.utcnow().isoformat(),
            "core_intelligence": core_intelligence,
            "asset_impact_matrix": impact_matrix.dict() if impact_matrix else None,
            "metadata": {
                "calculation_time_ms": int((time.time() - start_time) * 1000),
                "bank_count": len(bank_data),
                "model_version": "1.0.0",
            },
        }

        self.last_report = report
        self.last_run_time = datetime.utcnow()

        logger.info(f"GLB-005 completed: {len(bank_data)} banks analyzed")

        return report

    def _parse_bank_data(self) -> List[CentralBankInput]:
        """Parse central bank data from NDIP."""
        cb_data = self._latest_data.get(NDIP_TOPICS["CENTRAL_BANK_DATA"], {})
        banks = cb_data.get("banks", [])

        parsed = []
        for bank in banks:
            try:
                parsed.append(
                    CentralBankInput(
                        bank=CentralBank(bank.get("bank", "FED")),
                        currency=bank.get("currency", "USD"),
                        policy_stance=PolicyStance(
                            bank.get("policy_stance", "NEUTRAL")
                        ),
                        policy_score=bank.get("policy_score", 50.0),
                        confidence=bank.get("confidence", 70.0),
                        current_rate=bank.get("current_rate", 5.0),
                        rate_expectations=RateExpectation(
                            current=bank.get("current_rate", 5.0),
                            three_month=bank.get("rate_3m", 5.0),
                            six_month=bank.get("rate_6m", 5.0),
                            twelve_month=bank.get("rate_12m", 5.0),
                            confidence=bank.get("rate_confidence", 70.0),
                        ),
                        forward_guidance_tone=PolicyStance(
                            bank.get("forward_guidance", "NEUTRAL")
                        ),
                        forward_guidance_score=bank.get("forward_guidance_score", 50.0),
                        balance_sheet=BalanceSheetData(
                            policy=bank.get("balance_sheet_policy", "HOLDING"),
                            size=bank.get("balance_sheet_size", 0),
                            monthly_change=bank.get("balance_sheet_change", 0),
                            direction=bank.get("balance_sheet_direction", "STABLE"),
                        )
                        if "balance_sheet_policy" in bank
                        else None,
                        next_meeting=datetime.fromisoformat(bank["next_meeting"])
                        if "next_meeting" in bank
                        else None,
                        expected_change=bank.get("expected_change", 0.0),
                        source=bank.get("source", "unknown"),
                    )
                )
            except Exception as e:
                logger.warning(f"Failed to parse bank data: {e}")

        return parsed

    def _build_core_intelligence(
        self, policy: Dict, rates: Dict, divergence: Dict
    ) -> Dict:
        """Build core intelligence report"""
        return {
            "overall_policy_bias": policy.get("overall_bias", "NEUTRAL"),
            "global_policy_score": policy.get("global_policy_score", 50.0),
            "policy_divergence": policy.get("policy_divergence", {}),
            "rate_environment": {
                "global_direction": rates.get("global_direction", "NEUTRAL"),
                "average_expected_change_12m": rates.get(
                    "average_expected_change_12m", 0
                ),
                "most_aggressive_cutter": rates.get("most_aggressive_cutter"),
                "most_aggressive_hiker": rates.get("most_aggressive_hiker"),
            },
            "divergence_summary": {
                "max_divergence": divergence.get("max_divergence"),
                "min_divergence": divergence.get("min_divergence"),
                "divergence_count": len(divergence.get("divergence_matrix", {})),
            },
            "central_banks": policy.get("banks", {}),
            "bank_count": policy.get("bank_count", 0),
            "confidence": policy.get("confidence", 70.0),
        }

    def _empty_report(self) -> Dict:
        """Return empty report when no data."""
        return {
            "engine_id": "GLB-005",
            "engine_name": "Central Bank Intelligence Engine",
            "version": "1.0.0",
            "status": "OPERATIONAL",
            "generated_at": datetime.utcnow().isoformat(),
            "core_intelligence": {
                "overall_policy_bias": "NEUTRAL",
                "global_policy_score": 50.0,
                "policy_divergence": {"level": "LOW", "score": 0},
                "bank_count": 0,
                "confidence": 50.0,
            },
            "asset_impact_matrix": None,
            "metadata": {"bank_count": 0},
        }

    def get_last_report(self) -> Optional[Dict]:
        return self.last_report

    def health_check(self) -> Dict[str, Any]:
        return {
            "engine_id": "GLB-005",
            "status": "OPERATIONAL",
            "last_run": self.last_run_time.isoformat() if self.last_run_time else None,
            "has_report": self.last_report is not None,
        }
