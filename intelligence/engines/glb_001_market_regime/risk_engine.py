"""
GLB-001 Market Regime Engine - Risk Engine
"""

import logging
from typing import List, Dict, Any

from .schemas import RegimeRisk
from .constants import MarketRegime

logger = logging.getLogger(__name__)


class RiskEngine:
    """Identifies risks associated with the current regime."""

    def identify_risks(
        self,
        regime: MarketRegime,
        dimensions: Dict[str, Any],
        probabilities: Dict[str, float],
    ) -> List[RegimeRisk]:
        """Identify risks based on regime classification."""
        risks = []

        if regime == MarketRegime.RISK_ON:
            risks.extend(self._risk_on_risks(dimensions, probabilities))
        elif regime == MarketRegime.RISK_OFF:
            risks.extend(self._risk_off_risks(dimensions, probabilities))
        elif regime == MarketRegime.TRENDING:
            risks.extend(self._trending_risks(dimensions, probabilities))
        elif regime == MarketRegime.RANGING:
            risks.extend(self._ranging_risks(dimensions, probabilities))
        elif regime == MarketRegime.TRANSITION:
            risks.extend(self._transition_risks(dimensions, probabilities))
        elif regime == MarketRegime.VOLATILE:
            risks.extend(self._volatile_risks(dimensions, probabilities))

        risks.extend(self._common_risks(dimensions, probabilities))
        return risks

    def _risk_on_risks(
        self, dimensions: Dict[str, Any], probabilities: Dict[str, float]
    ) -> List[RegimeRisk]:
        risks = []
        risk_sentiment = dimensions.get("risk_sentiment", {}).get("value", 50)
        if risk_sentiment > 80:
            risks.append(
                RegimeRisk(
                    description="Elevated risk appetite may indicate complacency",
                    probability=0.25,
                    impact="HIGH",
                    time_horizon="MEDIUM_TERM",
                )
            )
        if probabilities.get("RISK_ON", 0) > 0.80:
            risks.append(
                RegimeRisk(
                    description="Risk-on regime may be overextended",
                    probability=0.20,
                    impact="MEDIUM",
                    time_horizon="SHORT_TERM",
                )
            )
        return risks

    def _risk_off_risks(
        self, dimensions: Dict[str, Any], probabilities: Dict[str, float]
    ) -> List[RegimeRisk]:
        risks = []
        risk_sentiment = dimensions.get("risk_sentiment", {}).get("value", 50)
        if risk_sentiment < 20:
            risks.append(
                RegimeRisk(
                    description="Extreme risk-off may indicate capitulation",
                    probability=0.30,
                    impact="HIGH",
                    time_horizon="SHORT_TERM",
                )
            )
        growth = dimensions.get("macro_growth", {}).get("value", 50)
        if growth < 30:
            risks.append(
                RegimeRisk(
                    description="Weak growth may lead to further risk-off",
                    probability=0.35,
                    impact="HIGH",
                    time_horizon="MEDIUM_TERM",
                )
            )
        return risks

    def _trending_risks(
        self, dimensions: Dict[str, Any], probabilities: Dict[str, float]
    ) -> List[RegimeRisk]:
        risks = []
        trend_strength = dimensions.get("trend_strength", {}).get("value", 50)
        if trend_strength > 80:
            risks.append(
                RegimeRisk(
                    description="Strong trend may be susceptible to reversal",
                    probability=0.20,
                    impact="MEDIUM",
                    time_horizon="SHORT_TERM",
                )
            )
        return risks

    def _ranging_risks(
        self, dimensions: Dict[str, Any], probabilities: Dict[str, float]
    ) -> List[RegimeRisk]:
        risks = []
        volatility = dimensions.get("volatility", {}).get("value", 50)
        if volatility < 30:
            risks.append(
                RegimeRisk(
                    description="Low volatility may precede a breakout",
                    probability=0.25,
                    impact="HIGH",
                    time_horizon="SHORT_TERM",
                )
            )
        return risks

    def _transition_risks(
        self, dimensions: Dict[str, Any], probabilities: Dict[str, float]
    ) -> List[RegimeRisk]:
        risks = []
        risks.append(
            RegimeRisk(
                description="Transition regime creates uncertainty",
                probability=0.40,
                impact="HIGH",
                time_horizon="SHORT_TERM",
            )
        )
        return risks

    def _volatile_risks(
        self, dimensions: Dict[str, Any], probabilities: Dict[str, float]
    ) -> List[RegimeRisk]:
        risks = []
        volatility = dimensions.get("volatility", {}).get("value", 50)
        if volatility > 70:
            risks.append(
                RegimeRisk(
                    description="High volatility may persist",
                    probability=0.30,
                    impact="MEDIUM",
                    time_horizon="SHORT_TERM",
                )
            )
        return risks

    def _common_risks(
        self, dimensions: Dict[str, Any], probabilities: Dict[str, float]
    ) -> List[RegimeRisk]:
        risks = []
        risks.append(
            RegimeRisk(
                description="Geopolitical tensions could disrupt markets",
                probability=0.15,
                impact="HIGH",
                time_horizon="MEDIUM_TERM",
            )
        )
        return risks
