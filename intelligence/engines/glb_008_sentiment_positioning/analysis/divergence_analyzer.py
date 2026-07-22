"""
GLB-008 Sentiment & Positioning Intelligence Engine - Divergence Analyzer
"""

import logging
from typing import Dict, Any

from ..constants import SentimentState

logger = logging.getLogger(__name__)


class DivergenceAnalyzer:
    """Analyze divergence between sentiment and positioning"""

    def analyze_divergence(
        self,
        sentiment_score: float,
        sentiment_state: str,
        positioning_bias: str,
        crowding_score: float,
    ) -> Dict[str, Any]:
        """
        Analyze divergence between sentiment and positioning.

        Returns:
            Dict with divergence analysis
        """
        divergence_detected = False
        divergence_type = "NONE"

        # Check for divergence: Risk-on sentiment but short positioning
        if (
            sentiment_state == SentimentState.RISK_ON.value
            and positioning_bias == "SHORT"
        ):
            divergence_detected = True
            divergence_type = "BULLISH_SENTIMENT_BEARISH_POSITIONING"

        # Check for divergence: Risk-off sentiment but long positioning
        elif (
            sentiment_state == SentimentState.RISK_OFF.value
            and positioning_bias == "LONG"
        ):
            divergence_detected = True
            divergence_type = "BEARISH_SENTIMENT_BULLISH_POSITIONING"

        # Check for extreme sentiment vs neutral positioning
        elif (sentiment_score > 75 or sentiment_score < 25) and crowding_score < 50:
            divergence_detected = True
            divergence_type = "EXTREME_SENTIMENT_NEUTRAL_POSITIONING"

        return {
            "divergence_detected": divergence_detected,
            "divergence_type": divergence_type,
            "contrarian_signal": divergence_detected,
            "confidence": 65.0 if divergence_detected else 85.0,
        }
