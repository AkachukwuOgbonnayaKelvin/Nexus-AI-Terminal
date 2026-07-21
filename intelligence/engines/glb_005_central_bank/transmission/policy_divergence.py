"""
GLB-005 Central Bank Intelligence Engine - Policy Divergence
"""

import logging
from typing import Dict, List

from ..input.schemas import CentralBankInput

logger = logging.getLogger(__name__)


class PolicyDivergenceEngine:
    """
    Calculate policy divergence between central banks.

    This is critical for FX analysis and asset impact.
    """

    def calculate_divergence(self, banks: List[CentralBankInput]) -> Dict:
        """
        Calculate policy divergence between all central banks.

        Returns:
            Dict with divergence matrix
        """
        if len(banks) < 2:
            return {
                "status": "INSUFFICIENT_DATA",
                "divergence_matrix": {},
                "max_divergence": 0,
                "min_divergence": 0,
            }

        # Create bank policy profiles
        profiles = {}
        for bank_data in banks:
            profiles[bank_data.bank.value] = {
                "score": bank_data.policy_score,
                "rate": bank_data.current_rate,
                "currency": bank_data.currency,
                "stance": bank_data.policy_stance.value,
            }

        # Calculate pairwise divergence
        divergence_matrix = {}
        bank_names = list(profiles.keys())

        for i, bank1 in enumerate(bank_names):
            for bank2 in bank_names[i + 1 :]:
                pair = f"{bank1}_{bank2}"
                score1 = profiles[bank1]["score"]
                score2 = profiles[bank2]["score"]
                divergence = score1 - score2

                divergence_matrix[pair] = {
                    "bank1": bank1,
                    "bank2": bank2,
                    "divergence": divergence,
                    "direction": self._determine_direction(divergence),
                    "absolute_divergence": abs(divergence),
                    "bank1_score": score1,
                    "bank2_score": score2,
                }

        # Find max and min divergence
        if divergence_matrix:
            max_pair = max(
                divergence_matrix.items(), key=lambda x: x[1]["absolute_divergence"]
            )
            min_pair = min(
                divergence_matrix.items(), key=lambda x: x[1]["absolute_divergence"]
            )
        else:
            max_pair = (None, None)
            min_pair = (None, None)

        return {
            "status": "OPERATIONAL",
            "divergence_matrix": divergence_matrix,
            "max_divergence": {
                "pair": max_pair[0],
                "divergence": max_pair[1]["divergence"] if max_pair[1] else 0,
                "direction": max_pair[1]["direction"] if max_pair[1] else "NEUTRAL",
                "absolute": max_pair[1]["absolute_divergence"] if max_pair[1] else 0,
            }
            if max_pair[0]
            else None,
            "min_divergence": {
                "pair": min_pair[0],
                "divergence": min_pair[1]["divergence"] if min_pair[1] else 0,
                "direction": min_pair[1]["direction"] if min_pair[1] else "NEUTRAL",
                "absolute": min_pair[1]["absolute_divergence"] if min_pair[1] else 0,
            }
            if min_pair[0]
            else None,
        }

    def _determine_direction(self, divergence: float) -> str:
        """Determine direction of divergence"""
        if divergence > 10:
            return "BANK1_BULLISH"
        elif divergence < -10:
            return "BANK2_BULLISH"
        return "NEUTRAL"
