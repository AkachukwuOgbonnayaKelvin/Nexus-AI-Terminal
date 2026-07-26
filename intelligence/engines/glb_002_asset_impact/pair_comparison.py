"""
GLB-002 Asset Impact Engine - Pair Comparison
"""

import logging
from typing import Any

from .constants import FX_PAIRS, Bias
from .schemas import CurrencyStrength, PairComparison

logger = logging.getLogger(__name__)


class PairComparisonEngine:
    """
    Compares two currencies and determines directional bias.
    """

    def compare_pairs(
        self, strengths: dict[str, CurrencyStrength], global_factors: dict[str, Any]
    ) -> dict[str, PairComparison]:
        """
        Compare all FX pairs.

        Args:
            strengths: Individual currency strengths
            global_factors: Global intelligence factors

        Returns:
            Dictionary of pair → PairComparison
        """
        results = {}

        for pair_config in FX_PAIRS:
            pair = pair_config["pair"]
            base = pair_config["base"]
            quote = pair_config["quote"]

            results[pair] = self._compare_pair(
                pair=pair,
                base=base,
                quote=quote,
                base_strength=strengths.get(base),
                quote_strength=strengths.get(quote),
                global_factors=global_factors,
            )

        return results

    def _compare_pair(
        self,
        pair: str,
        base: str,
        quote: str,
        base_strength: CurrencyStrength,
        quote_strength: CurrencyStrength,
        global_factors: dict[str, Any],
    ) -> PairComparison:
        """
        Compare a single pair.
        """
        base_score = base_strength.score if base_strength else 50.0
        quote_score = quote_strength.score if quote_strength else 50.0

        differential = base_score - quote_score

        # Determine bias
        if differential > 5:
            bias = Bias.BULLISH
        elif differential < -5:
            bias = Bias.BEARISH
        else:
            bias = Bias.NEUTRAL

        # Calculate confidence
        confidence = self._calculate_confidence(
            base_strength, quote_strength, differential
        )

        # Build drivers
        drivers = self._build_drivers(
            base, quote, base_strength, quote_strength, global_factors
        )

        # Build evidence
        evidence = self._build_evidence(base, quote, base_strength, quote_strength)

        # Identify risks
        risks = self._identify_risks(base, quote, base_strength, quote_strength)

        return PairComparison(
            pair=pair,
            base_currency=base,
            quote_currency=quote,
            base_score=base_score,
            quote_score=quote_score,
            differential=differential,
            bias=bias,
            confidence=confidence,
            drivers=drivers,
            risks=risks,
            evidence=evidence,
        )

    def _calculate_confidence(
        self,
        base_strength: CurrencyStrength,
        quote_strength: CurrencyStrength,
        differential: float,
    ) -> float:
        """Calculate confidence in the pair comparison."""
        base_conf = base_strength.confidence if base_strength else 50.0
        quote_conf = quote_strength.confidence if quote_strength else 50.0

        # Average confidence
        avg_conf = (base_conf + quote_conf) / 2.0

        # Adjust for differential magnitude
        diff_factor = min(1.0, abs(differential) / 30.0)

        return min(95.0, avg_conf * (0.7 + 0.3 * diff_factor))

    def _build_drivers(
        self,
        base: str,
        quote: str,
        base_strength: CurrencyStrength,
        quote_strength: CurrencyStrength,
        global_factors: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Build drivers for the pair comparison."""
        drivers = []

        if not base_strength or not quote_strength:
            return drivers

        # Compare factors
        base_factors = base_strength.factors
        quote_factors = quote_strength.factors

        for factor in base_factors.keys():
            base_val = base_factors.get(factor, 50)
            quote_val = quote_factors.get(factor, 50)
            diff = base_val - quote_val

            if abs(diff) > 10:
                drivers.append(
                    {
                        "factor": factor,
                        "base_value": base_val,
                        "quote_value": quote_val,
                        "impact": diff,
                        "direction": "BULLISH" if diff > 0 else "BEARISH",
                    }
                )

        # Sort by impact
        drivers.sort(key=lambda x: abs(x["impact"]), reverse=True)

        return drivers[:5]  # Top 5 drivers

    def _build_evidence(
        self,
        base: str,
        quote: str,
        base_strength: CurrencyStrength,
        quote_strength: CurrencyStrength,
    ) -> list[dict[str, Any]]:
        """Build evidence for the pair comparison."""
        evidence = []

        if base_strength:
            evidence.append(
                {
                    "source": "CURRENCY_STRENGTH",
                    "currency": base,
                    "score": base_strength.score,
                    "confidence": base_strength.confidence,
                }
            )

        if quote_strength:
            evidence.append(
                {
                    "source": "CURRENCY_STRENGTH",
                    "currency": quote,
                    "score": quote_strength.score,
                    "confidence": quote_strength.confidence,
                }
            )

        return evidence

    def _identify_risks(
        self,
        base: str,
        quote: str,
        base_strength: CurrencyStrength,
        quote_strength: CurrencyStrength,
    ) -> list[str]:
        """Identify risks for the pair."""
        risks = []

        if base_strength:
            risks.extend(base_strength.risks)

        if quote_strength:
            risks.extend(quote_strength.risks)

        # Remove duplicates
        seen = set()
        unique_risks = []
        for risk in risks:
            if risk not in seen:
                seen.add(risk)
                unique_risks.append(risk)

        return unique_risks[:5]  # Top 5 risks
