"""
GLB-002 Asset Impact Engine - Currency Strength
"""

import logging
from typing import Any

from .constants import CURRENCIES, FACTOR_WEIGHTS
from .schemas import CurrencyStrength

logger = logging.getLogger(__name__)


class CurrencyStrengthEngine:
    """
    Calculates individual currency strength based on global factors.
    """

    def calculate(self, global_factors: dict[str, Any]) -> dict[str, CurrencyStrength]:
        """
        Calculate strength for all currencies.

        Args:
            global_factors: Global intelligence factors

        Returns:
            Dictionary of currency → CurrencyStrength
        """
        strengths = {}

        for currency in CURRENCIES:
            strengths[currency] = self._calculate_currency(currency, global_factors)

        return strengths

    def _calculate_currency(
        self, currency: str, factors: dict[str, Any]
    ) -> CurrencyStrength:
        """
        Calculate strength for a single currency.
        """
        # Get factors for this currency
        currency_factors = self._get_currency_factors(currency, factors)

        # Calculate weighted score
        score = 0.0
        factor_details = {}
        drivers = []

        for factor_name, weight in FACTOR_WEIGHTS.items():
            factor_value = currency_factors.get(factor_name, 50)
            factor_details[factor_name] = factor_value
            score += factor_value * weight

            # Identify drivers (factors above 60)
            if factor_value > 60:
                drivers.append(f"{factor_name}: {factor_value:.1f}")

        # Determine confidence
        confidence = self._calculate_confidence(factor_details)

        return CurrencyStrength(
            currency=currency,
            score=score,
            confidence=confidence,
            factors=factor_details,
            drivers=drivers[:5],  # Top 5 drivers
            risks=self._identify_risks(currency, factor_details),
        )

    def _get_currency_factors(
        self, currency: str, factors: dict[str, Any]
    ) -> dict[str, float]:
        """
        Get factors for a specific currency.
        """
        # Default factors
        result = {
            "growth": 50.0,
            "inflation": 50.0,
            "rates": 50.0,
            "central_bank": 50.0,
            "risk_sentiment": 50.0,
            "liquidity": 50.0,
            "geopolitical": 50.0,
        }

        # Override with actual factors if available
        if "currencies" in factors and currency in factors["currencies"]:
            cur_factors = factors["currencies"][currency]
            for key in result:
                if key in cur_factors:
                    result[key] = float(cur_factors[key])

        return result

    def _calculate_confidence(self, factors: dict[str, float]) -> float:
        """
        Calculate confidence based on factor consistency.
        """
        if not factors:
            return 50.0

        # Higher confidence when factors agree
        values = list(factors.values())
        avg = sum(values) / len(values)

        # Calculate standard deviation
        variance = sum((v - avg) ** 2 for v in values) / len(values)
        std_dev = variance**0.5

        # Confidence decreases with variance
        max_std = 30.0
        confidence = 100.0 - (std_dev / max_std * 40.0)

        return max(50.0, min(95.0, confidence))

    def _identify_risks(self, currency: str, factors: dict[str, float]) -> list[str]:
        """
        Identify risks for a currency.
        """
        risks = []

        # Check for extreme factors
        for factor, value in factors.items():
            if value > 85:
                risks.append(f"High {factor} could reverse")
            elif value < 15:
                risks.append(f"Low {factor} could worsen")

        return risks[:3]  # Top 3 risks
