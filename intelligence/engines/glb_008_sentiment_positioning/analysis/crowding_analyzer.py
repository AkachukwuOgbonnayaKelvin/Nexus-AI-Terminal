"""
GLB-008 Sentiment & Positioning Intelligence Engine - Crowding Analyzer
"""

import logging
from typing import Dict, Any

from ..constants import CrowdingState, EXTREME_THRESHOLDS

logger = logging.getLogger(__name__)


class CrowdingAnalyzer:
    """Analyze market crowding"""

    def analyze_crowding(self, positionings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze crowding across assets.

        Returns:
            Dict with crowding analysis
        """
        if not positionings:
            return {
                "status": "NO_DATA",
                "crowding_state": CrowdingState.LOW.value,
                "crowding_score": 0,
                "crowded_assets": [],
                "uncrowded_assets": [],
                "confidence": 0,
            }

        crowded = []
        uncrowded = []
        scores = []

        for asset, data in positionings.items():
            crowding = data.get("crowding", 50)
            scores.append(crowding)

            if crowding > EXTREME_THRESHOLDS["crowding_high"]:
                crowded.append(asset)
            elif crowding < 20:
                uncrowded.append(asset)

        avg_crowding = sum(scores) / len(scores) if scores else 50

        # Determine state
        if avg_crowding > 80:
            state = CrowdingState.EXTREME.value
        elif avg_crowding > 60:
            state = CrowdingState.HIGH.value
        elif avg_crowding > 40:
            state = CrowdingState.MODERATE.value
        else:
            state = CrowdingState.LOW.value

        return {
            "status": "OPERATIONAL",
            "crowding_state": state,
            "crowding_score": avg_crowding,
            "crowded_assets": crowded,
            "uncrowded_assets": uncrowded,
            "asset_count": len(positionings),
            "confidence": 70.0,
        }
