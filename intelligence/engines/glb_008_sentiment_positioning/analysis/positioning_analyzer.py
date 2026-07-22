"""
GLB-008 Sentiment & Positioning Intelligence Engine - Positioning Analyzer
"""

import logging
from typing import Dict, List, Any

from ..constants import PositioningBias, CrowdingState
from ..input.schemas import COTInput, InstitutionalPositioningInput

logger = logging.getLogger(__name__)


class PositioningAnalyzer:
    """Analyze institutional positioning"""

    def analyze_positioning(
        self,
        cot_data: List[COTInput],
        institutional_data: List[InstitutionalPositioningInput],
    ) -> Dict[str, Any]:
        """
        Analyze positioning from COT and institutional data.

        Returns:
            Dict with positioning analysis
        """
        positionings = {}
        crowding_scores = []

        # Process COT data
        for cot in cot_data:
            symbol = cot.symbol
            positionings[symbol] = {
                "net_position": cot.net_position,
                "percentile": cot.percentile,
                "crowding": self._calculate_crowding(cot),
                "bias": self._determine_bias(cot.net_position),
            }
            crowding_scores.append(self._calculate_crowding(cot))

        # Process institutional data
        for inst in institutional_data:
            asset = inst.asset
            if asset not in positionings:
                positionings[asset] = {
                    "net_position": inst.net_position,
                    "percentile": inst.percentile,
                    "crowding": inst.crowding,
                    "bias": inst.positioning_bias.value,
                }
            else:
                positionings[asset]["crowding"] = max(
                    positionings[asset]["crowding"], inst.crowding
                )

        # Calculate overall crowding
        avg_crowding = (
            sum(crowding_scores) / len(crowding_scores) if crowding_scores else 50.0
        )

        # Determine crowding state
        if avg_crowding > 80:
            crowding_state = CrowdingState.EXTREME.value
        elif avg_crowding > 60:
            crowding_state = CrowdingState.HIGH.value
        elif avg_crowding > 40:
            crowding_state = CrowdingState.MODERATE.value
        else:
            crowding_state = CrowdingState.LOW.value

        # Determine overall bias
        biases = [p["bias"] for p in positionings.values() if "bias" in p]
        long_count = sum(
            1
            for b in biases
            if b in [PositioningBias.LONG.value, PositioningBias.EXTREME_LONG.value]
        )
        short_count = sum(
            1
            for b in biases
            if b in [PositioningBias.SHORT.value, PositioningBias.EXTREME_SHORT.value]
        )

        if long_count > short_count:
            overall_bias = PositioningBias.LONG.value
        elif short_count > long_count:
            overall_bias = PositioningBias.SHORT.value
        else:
            overall_bias = PositioningBias.NEUTRAL.value

        return {
            "status": "OPERATIONAL",
            "positionings": positionings,
            "overall_bias": overall_bias,
            "crowding_state": crowding_state,
            "crowding_score": avg_crowding,
            "asset_count": len(positionings),
            "confidence": 75.0,
        }

    def _calculate_crowding(self, cot: COTInput) -> float:
        """Calculate crowding from COT data"""
        # Higher percentile = more crowded
        crowding = cot.percentile
        return min(100, crowding + (100 - cot.confidence) * 0.1)

    def _determine_bias(self, net_position: float) -> str:
        """Determine bias from net position"""
        if net_position > 10000:
            return PositioningBias.LONG.value
        elif net_position < -10000:
            return PositioningBias.SHORT.value
        return PositioningBias.NEUTRAL.value
