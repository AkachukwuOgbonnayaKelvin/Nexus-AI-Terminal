"""
GLB-009 Market Memory & Historical Analogy Intelligence Engine - Similarity Engine
"""

import logging
from typing import Dict, Any

from ..constants import FEATURE_WEIGHTS
from ..input.schemas import MarketSnapshot, HistoricalWindow, EnvironmentState

logger = logging.getLogger(__name__)


class SimilarityEngine:
    """Calculate similarity between current and historical environments"""

    def __init__(self):
        self.feature_weights = FEATURE_WEIGHTS

    def calculate_similarity(
        self, current: MarketSnapshot, historical: HistoricalWindow
    ) -> Dict[str, Any]:
        """
        Calculate similarity between current and historical environment.

        Args:
            current: Current market snapshot
            historical: Historical window (contains environment state)

        Returns:
            Dict with similarity scores per feature and overall
        """
        # Get historical environment
        if hasattr(historical, "environment"):
            hist_env = historical.environment
        else:
            hist_env = EnvironmentState()

        # Also handle case where historical has direct attributes
        if hasattr(historical, "regime") and not hasattr(hist_env, "regime"):
            hist_env = EnvironmentState(
                regime=getattr(historical, "regime", "NEUTRAL"),
                macro_score=getattr(historical, "macro_score", 50.0),
                central_bank_score=getattr(historical, "central_bank_score", 50.0),
                geopolitical_risk=getattr(historical, "geopolitical_risk", 50.0),
                capital_flow_score=getattr(historical, "capital_flow_score", 50.0),
                sentiment_score=getattr(historical, "sentiment_score", 50.0),
                positioning_score=getattr(historical, "positioning_score", 50.0),
                volatility_score=getattr(historical, "volatility_score", 50.0),
            )

        feature_scores = {}
        weighted_sum = 0.0
        total_weight = 0.0

        # Compare each feature
        features = {
            "market_regime": (current.regime, hist_env.regime, self._regime_similarity),
            "macro": (
                current.macro_score,
                hist_env.macro_score,
                self._score_similarity,
            ),
            "central_banks": (
                current.central_bank_score,
                hist_env.central_bank_score,
                self._score_similarity,
            ),
            "geopolitical": (
                current.geopolitical_risk,
                hist_env.geopolitical_risk,
                self._score_similarity,
            ),
            "capital_flows": (
                current.capital_flow_score,
                hist_env.capital_flow_score,
                self._score_similarity,
            ),
            "sentiment": (
                current.sentiment_score,
                hist_env.sentiment_score,
                self._score_similarity,
            ),
            "positioning": (
                current.positioning_score,
                hist_env.positioning_score,
                self._score_similarity,
            ),
            "volatility": (
                current.volatility_score,
                hist_env.volatility_score,
                self._score_similarity,
            ),
        }

        for feature, (current_val, hist_val, similarity_func) in features.items():
            try:
                score = similarity_func(current_val, hist_val)
                weight = self.feature_weights.get(feature, 0.05)
                feature_scores[feature] = score
                weighted_sum += score * weight
                total_weight += weight
            except Exception as e:
                logger.debug(f"Error calculating similarity for {feature}: {e}")
                feature_scores[feature] = 0.5

        # Calculate overall similarity
        overall = weighted_sum / total_weight if total_weight > 0 else 0

        return {
            "overall_similarity": overall * 100,
            "feature_scores": {k: v * 100 for k, v in feature_scores.items()},
            "weighted_sum": weighted_sum,
            "total_weight": total_weight,
        }

    def _regime_similarity(self, current: str, historical: str) -> float:
        """Calculate similarity between regimes"""
        if not current or not historical:
            return 0.5
        if current == historical:
            return 1.0
        regime_map = {
            ("RISK_ON", "TRENDING"): 0.7,
            ("RISK_OFF", "TRENDING"): 0.3,
            ("RISK_ON", "RANGING"): 0.5,
            ("RISK_OFF", "RANGING"): 0.5,
            ("TRENDING", "RANGING"): 0.4,
            ("VOLATILE", "TRANSITION"): 0.6,
        }
        key = tuple(sorted([current, historical]))
        return regime_map.get(key, 0.1)

    def _score_similarity(self, current: float, historical: float) -> float:
        """Calculate similarity between two scores (0-100)"""
        if current is None or historical is None:
            return 0.5
        diff = abs(current - historical)
        return max(0, 1 - (diff / 100))
