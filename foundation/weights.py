"""Intelligence engine weights configuration.

This module defines the weighting system for combining multiple intelligence sources.
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class EngineWeights:
    """Configuration for intelligence engine weights."""

    # Default weights for different engine types
    technical_weight: float = 0.25
    macro_weight: float = 0.25
    institutional_weight: float = 0.25
    sentiment_weight: float = 0.15
    intermarket_weight: float = 0.10

    # Adjustments based on market regime
    regime_adjustments: Dict[str, Dict[str, float]] = field(
        default_factory=lambda: {
            "trending": {
                "technical": 1.2,
                "macro": 1.0,
                "institutional": 1.1,
                "sentiment": 0.8,
                "intermarket": 0.9,
            },
            "ranging": {
                "technical": 0.8,
                "macro": 1.1,
                "institutional": 1.0,
                "sentiment": 1.1,
                "intermarket": 1.0,
            },
            "risk_on": {
                "technical": 0.9,
                "macro": 1.2,
                "institutional": 1.0,
                "sentiment": 1.3,
                "intermarket": 0.8,
            },
            "risk_off": {
                "technical": 1.0,
                "macro": 1.3,
                "institutional": 1.1,
                "sentiment": 0.9,
                "intermarket": 0.9,
            },
            "volatile": {
                "technical": 0.7,
                "macro": 0.9,
                "institutional": 0.8,
                "sentiment": 0.6,
                "intermarket": 0.7,
            },
        }
    )

    def get_weights(self, regime: str = "default") -> Dict[str, float]:
        """Get weights for a specific market regime."""
        base = {
            "technical": self.technical_weight,
            "macro": self.macro_weight,
            "institutional": self.institutional_weight,
            "sentiment": self.sentiment_weight,
            "intermarket": self.intermarket_weight,
        }

        if regime in self.regime_adjustments:
            adjustment = self.regime_adjustments[regime]
            for key in base:
                base[key] *= adjustment.get(key, 1.0)

        return base

    def normalize_weights(self, weights: Dict[str, float]) -> Dict[str, float]:
        """Normalize weights to sum to 1.0."""
        total = sum(weights.values())
        if total > 0:
            return {k: v / total for k, v in weights.items()}
        return weights


# Default weights instance
weights = EngineWeights()
