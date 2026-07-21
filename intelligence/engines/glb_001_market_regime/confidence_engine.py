"""
GLB-001 Market Regime Engine - Confidence Engine
"""

import logging
from typing import Dict, List

from .schemas import MarketDimension, RegimeEvidence

logger = logging.getLogger(__name__)


class ConfidenceEngine:
    """Calculates confidence in regime classification."""

    def calculate_confidence(
        self,
        primary_regime: str,
        dimensions: Dict[str, MarketDimension],
        evidence: List[RegimeEvidence],
        regime_probabilities: Dict[str, float],
    ) -> float:
        """Calculate confidence score."""
        confidence = 0.0
        evidence_score = self._score_evidence(primary_regime, evidence)
        confidence += evidence_score * 0.30
        agreement_score = self._score_agreement(dimensions)
        confidence += agreement_score * 0.30
        prob_gap = self._score_probability_gap(regime_probabilities)
        confidence += prob_gap * 0.25
        quality_score = self._score_data_quality()
        confidence += quality_score * 0.15
        return min(100, confidence)

    def _score_evidence(
        self, primary_regime: str, evidence: List[RegimeEvidence]
    ) -> float:
        if not evidence:
            return 0
        supporting = 0
        for ev in evidence:
            if primary_regime == "RISK_ON" and ev.direction == "BULLISH":
                supporting += ev.contribution
            elif primary_regime == "RISK_OFF" and ev.direction == "BEARISH":
                supporting += ev.contribution
            elif primary_regime == "TRENDING" and ev.direction != "NEUTRAL":
                supporting += ev.contribution * 0.5
            else:
                supporting += ev.contribution * 0.25
        max_support = sum(ev.contribution for ev in evidence)
        return (supporting / max_support) * 100 if max_support > 0 else 50

    def _score_agreement(self, dimensions: Dict[str, MarketDimension]) -> float:
        if len(dimensions) < 2:
            return 50
        bullish = 0
        bearish = 0
        for dim in dimensions.values():
            if dim.direction == "BULLISH":
                bullish += 1
            elif dim.direction == "BEARISH":
                bearish += 1
        total = bullish + bearish
        if total == 0:
            return 50
        agreement = max(bullish, bearish) / total * 100
        return agreement * 0.5 + 50 * 0.5

    def _score_probability_gap(self, probabilities: Dict[str, float]) -> float:
        if not probabilities:
            return 50
        sorted_probs = sorted(probabilities.values(), reverse=True)
        if len(sorted_probs) < 2:
            return 50
        gap = sorted_probs[0] - sorted_probs[1]
        return min(100, 50 + (gap * 50))

    def _score_data_quality(self) -> float:
        return 80
