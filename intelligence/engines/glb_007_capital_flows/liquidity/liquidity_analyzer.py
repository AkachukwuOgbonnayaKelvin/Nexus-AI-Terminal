"""
GLB-007 Capital Flows & Liquidity Intelligence Engine - Liquidity Analyzer
"""

import logging
from typing import Dict, Any, Optional

from ..constants import LiquidityState
from ..input.schemas import LiquidityInput

logger = logging.getLogger(__name__)


class LiquidityAnalyzer:
    """Analyze liquidity conditions"""

    def analyze_liquidity(
        self, liquidity_data: Optional[LiquidityInput]
    ) -> Dict[str, Any]:
        """
        Analyze liquidity conditions.

        Returns:
            Dict with liquidity analysis
        """
        if not liquidity_data:
            return {
                "status": "NO_DATA",
                "liquidity_score": 50.0,
                "liquidity_state": LiquidityState.NORMAL.value,
                "funding_stress": 50.0,
                "confidence": 0,
            }

        # Calculate overall liquidity score
        components = [
            liquidity_data.global_liquidity,
            liquidity_data.central_bank_liquidity,
            liquidity_data.money_market_liquidity,
            liquidity_data.credit_liquidity,
        ]
        liquidity_score = sum(components) / len(components)

        # Determine liquidity state
        state = self._determine_state(liquidity_score, liquidity_data.funding_stress)

        return {
            "status": "OPERATIONAL",
            "liquidity_score": liquidity_score,
            "liquidity_state": state.value,
            "global_liquidity": liquidity_data.global_liquidity,
            "central_bank_liquidity": liquidity_data.central_bank_liquidity,
            "money_market_liquidity": liquidity_data.money_market_liquidity,
            "credit_liquidity": liquidity_data.credit_liquidity,
            "funding_stress": liquidity_data.funding_stress,
            "confidence": liquidity_data.confidence,
        }

    def _determine_state(
        self, liquidity_score: float, funding_stress: float
    ) -> LiquidityState:
        """Determine liquidity state from score and stress"""
        if funding_stress > 70 or liquidity_score < 30:
            return LiquidityState.STRESSED
        elif funding_stress > 50 or liquidity_score < 45:
            return LiquidityState.TIGHTENING
        elif liquidity_score > 75 and funding_stress < 30:
            return LiquidityState.ABUNDANT
        return LiquidityState.NORMAL
