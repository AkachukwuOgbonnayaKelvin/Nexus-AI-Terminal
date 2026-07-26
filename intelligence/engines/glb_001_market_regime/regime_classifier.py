"""
GLB-001 Market Regime Engine - Regime Classifier
"""

import logging

from .constants import MarketRegime, TransitionState
from .schemas import MarketDimension

logger = logging.getLogger(__name__)


class RegimeClassifier:
    """Classifies market regime based on dimension scores."""

    def __init__(self):
        self.dimensions: dict[str, MarketDimension] = {}
        self.regime_scores: dict[MarketRegime, float] = {}

    def classify(
        self, dimensions: dict[str, MarketDimension]
    ) -> tuple[MarketRegime, float, dict[MarketRegime, float]]:
        """Classify market regime from dimensions."""
        self.dimensions = dimensions

        # Calculate scores for each regime
        self.regime_scores = {
            MarketRegime.RISK_ON: self._calculate_risk_on_score(dimensions),
            MarketRegime.RISK_OFF: self._calculate_risk_off_score(dimensions),
            MarketRegime.TRENDING: self._calculate_trending_score(dimensions),
            MarketRegime.RANGING: self._calculate_ranging_score(dimensions),
            MarketRegime.TRANSITION: self._calculate_transition_score(dimensions),
            MarketRegime.VOLATILE: self._calculate_volatile_score(dimensions),
        }

        # Find primary regime
        primary_regime = max(self.regime_scores, key=self.regime_scores.get)
        regime_score = self.regime_scores[primary_regime]

        # Normalize probabilities
        total = sum(self.regime_scores.values())
        regime_probabilities = {
            regime: score / total if total > 0 else 0
            for regime, score in self.regime_scores.items()
        }

        return primary_regime, regime_score, regime_probabilities

    def _calculate_risk_on_score(self, dimensions: dict[str, MarketDimension]) -> float:
        """Calculate RISK_ON score based on evidence."""
        score = 0
        count = 0

        risk_sentiment = dimensions.get("risk_sentiment")
        if risk_sentiment:
            score += risk_sentiment.value * 0.40
            count += 1

        volatility = dimensions.get("volatility")
        if volatility:
            score += (100 - volatility.value) * 0.30
            count += 1

        growth = dimensions.get("macro_growth")
        if growth:
            score += growth.value * 0.30
            count += 1

        return score

    def _calculate_risk_off_score(
        self, dimensions: dict[str, MarketDimension]
    ) -> float:
        """
        Calculate RISK_OFF score based on evidence intensity.

        The score should reflect how intense the risk-off regime is:
        - 55-70: Mild risk aversion
        - 70-85: Strong risk aversion
        - 85-100: Extreme systemic risk

        Test case: risk_sentiment=15, volatility=85, macro_growth=20
        Expected: ~83.8 (Strong risk aversion)
        """
        score = 0
        count = 0

        # Risk sentiment: low = risk-off (inverted)
        risk_sentiment = dimensions.get("risk_sentiment")
        if risk_sentiment:
            score += (100 - risk_sentiment.value) * 0.45
            count += 1

        # Volatility: high = risk-off
        volatility = dimensions.get("volatility")
        if volatility:
            score += volatility.value * 0.30
            count += 1

        # Macro growth: weak = risk-off (inverted)
        growth = dimensions.get("macro_growth")
        if growth:
            score += (100 - growth.value) * 0.25
            count += 1

        # If no dimensions, return neutral
        if count == 0:
            return 50.0

        return score

    def _calculate_trending_score(
        self, dimensions: dict[str, MarketDimension]
    ) -> float:
        """Calculate TRENDING score based on evidence."""
        score = 0
        count = 0

        trend_strength = dimensions.get("trend_strength")
        if trend_strength:
            score += trend_strength.value * 0.50
            count += 1

        momentum = dimensions.get("momentum")
        if momentum:
            score += abs(momentum.value - 50) * 2 * 0.30
            count += 1

        volatility = dimensions.get("volatility")
        if volatility:
            score += (100 - volatility.value) * 0.20
            count += 1

        if count == 0:
            return 50.0

        return score

    def _calculate_ranging_score(self, dimensions: dict[str, MarketDimension]) -> float:
        """Calculate RANGING score based on evidence."""
        score = 0
        count = 0

        trend_strength = dimensions.get("trend_strength")
        if trend_strength:
            score += (100 - trend_strength.value) * 0.40
            count += 1

        momentum = dimensions.get("momentum")
        if momentum:
            score += (100 - abs(momentum.value - 50) * 2) * 0.30
            count += 1

        volatility = dimensions.get("volatility")
        if volatility:
            vol_score = 100 - abs(volatility.value - 50) * 2
            score += vol_score * 0.30
            count += 1

        if count == 0:
            return 50.0

        return score

    def _calculate_transition_score(
        self, dimensions: dict[str, MarketDimension]
    ) -> float:
        """Calculate TRANSITION score based on evidence."""
        score = 0
        count = 0

        risk_sentiment = dimensions.get("risk_sentiment")
        if risk_sentiment:
            score += (1 - abs(risk_sentiment.value - 50) / 50) * 0.40
            count += 1

        volatility = dimensions.get("volatility")
        if volatility:
            score += (volatility.value / 100) * 0.30
            count += 1

        trend_strength = dimensions.get("trend_strength")
        if trend_strength:
            score += (100 - trend_strength.value) * 0.30
            count += 1

        if count == 0:
            return 50.0

        return score

    def _calculate_volatile_score(
        self, dimensions: dict[str, MarketDimension]
    ) -> float:
        """Calculate VOLATILE score based on evidence."""
        score = 0
        count = 0

        volatility = dimensions.get("volatility")
        if volatility:
            score += volatility.value * 0.50
            count += 1

        risk_sentiment = dimensions.get("risk_sentiment")
        if risk_sentiment:
            score += (1 - abs(risk_sentiment.value - 50) / 50) * 0.25
            count += 1

        trend_strength = dimensions.get("trend_strength")
        if trend_strength:
            score += (100 - trend_strength.value) * 0.25
            count += 1

        if count == 0:
            return 50.0

        return score

    def determine_transition_state(
        self,
        primary_regime: MarketRegime,
        regime_probabilities: dict[MarketRegime, float],
    ) -> TransitionState:
        """Determine transition state based on regime probabilities."""
        transition_prob = regime_probabilities.get(MarketRegime.TRANSITION, 0)

        if transition_prob > 0.30:
            primary_prob = regime_probabilities.get(primary_regime, 0)

            if primary_prob > 0.70:
                return TransitionState.STABLE
            elif primary_prob > 0.50:
                return TransitionState.WEAKENING
            elif primary_prob > 0.30:
                return TransitionState.STRENGTHENING
            else:
                return TransitionState.REVERSING

        return TransitionState.STABLE
