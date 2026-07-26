"""
GLB-005 Central Bank Intelligence Engine - Policy Analyzer
"""

import logging

from ..constants import CENTRAL_BANK_METADATA, PolicyStance
from ..input.schemas import CentralBankInput

logger = logging.getLogger(__name__)


class PolicyAnalyzer:
    """Analyze central bank policy stance"""

    def __init__(self):
        self._metadata = CENTRAL_BANK_METADATA

    def analyze_bank(self, bank_data: CentralBankInput) -> dict:
        """
        Analyze a single central bank's policy stance.

        Returns:
            Dict with policy analysis
        """
        metadata = self._metadata.get(bank_data.bank.value, {})

        return {
            "bank": bank_data.bank.value,
            "currency": bank_data.currency,
            "name": metadata.get("name", bank_data.bank.value),
            "policy_stance": bank_data.policy_stance.value,
            "policy_score": bank_data.policy_score,
            "confidence": bank_data.confidence,
            "current_rate": bank_data.current_rate,
            "forward_guidance_tone": bank_data.forward_guidance_tone.value,
            "forward_guidance_score": bank_data.forward_guidance_score,
            "next_meeting": bank_data.next_meeting.isoformat()
            if bank_data.next_meeting
            else None,
            "expected_change": bank_data.expected_change,
            "has_balance_sheet": bank_data.balance_sheet is not None,
        }

    def analyze_all_banks(self, banks: list[CentralBankInput]) -> dict:
        """
        Analyze all central banks and derive global policy conditions.

        Returns:
            Dict with global policy analysis
        """
        if not banks:
            return {
                "status": "NO_DATA",
                "banks": {},
                "overall_bias": PolicyStance.NEUTRAL.value,
                "policy_divergence": {"level": "LOW", "score": 0},
                "strongest_hawkish": None,
                "strongest_dovish": None,
            }

        bank_analyses = {}
        hawkish_scores = {}

        for bank_data in banks:
            analysis = self.analyze_bank(bank_data)
            bank_analyses[bank_data.bank.value] = analysis
            hawkish_scores[bank_data.bank.value] = bank_data.policy_score

        # Determine overall bias
        avg_score = (
            sum(hawkish_scores.values()) / len(hawkish_scores) if hawkish_scores else 50
        )
        overall_bias = self._determine_overall_bias(avg_score)

        # Find strongest hawkish and dovish
        strongest_hawkish = (
            max(hawkish_scores.items(), key=lambda x: x[1])
            if hawkish_scores
            else (None, None)
        )
        strongest_dovish = (
            min(hawkish_scores.items(), key=lambda x: x[1])
            if hawkish_scores
            else (None, None)
        )

        # Calculate divergence
        divergence_score = self._calculate_divergence(hawkish_scores)

        return {
            "banks": bank_analyses,
            "overall_bias": overall_bias,
            "global_policy_score": avg_score,
            "policy_divergence": {
                "level": self._determine_divergence_level(divergence_score),
                "score": divergence_score,
                "strongest_hawkish": strongest_hawkish[0]
                if strongest_hawkish[0]
                else None,
                "strongest_dovish": strongest_dovish[0]
                if strongest_dovish[0]
                else None,
            },
            "bank_count": len(banks),
            "confidence": sum(b.confidence for b in banks) / len(banks)
            if banks
            else 50,
        }

    def _determine_overall_bias(self, score: float) -> str:
        """Determine overall policy bias from average score"""
        if score >= 60:
            return PolicyStance.HAWKISH.value
        elif score <= 40:
            return PolicyStance.DOVISH.value
        return PolicyStance.NEUTRAL.value

    def _calculate_divergence(self, scores: dict[str, float]) -> float:
        """Calculate policy divergence score"""
        if len(scores) < 2:
            return 0.0

        values = list(scores.values())
        max_score = max(values)
        min_score = min(values)

        # Divergence as percentage of max range (0-100)
        range_span = max_score - min_score
        divergence = (range_span / 100) * 100

        return min(100, divergence)

    def _determine_divergence_level(self, score: float) -> str:
        """Determine divergence level"""
        if score >= 70:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        return "LOW"
