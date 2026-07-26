"""
Confluence Engine - Confluence Score

Calculates the final confluence score with conflict penalties.
Uses ConflictDetector for accurate conflict classification.
"""

import logging
from typing import Any

from ..evidence.evidence_model import EvidenceGroup
from ..schemas import Direction
from .conflict_detector import ConflictDetector

logger = logging.getLogger(__name__)


class ConfluenceScore:
    """
    Calculates final confluence scores with conflict penalties.
    Uses ConflictDetector for accurate classification.
    """

    def __init__(self):
        # Penalty multipliers by conflict level
        self.penalty_multipliers = {
            "NONE": 0.0,
            "LOW": 0.10,
            "MEDIUM": 0.25,
            "HIGH": 0.45,
        }
        # Use ConflictDetector for classification
        self.detector = ConflictDetector()

    def calculate_score(
        self, group: EvidenceGroup, consensus: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Calculate final confluence score with conflict penalty.
        Uses ConflictDetector for accurate conflict classification.
        """
        if not group.evidence:
            return {
                "score": 0.0,
                "direction": "NEUTRAL",
                "confidence": 0.0,
                "conflict_penalty": 0.0,
                "base_score": 0.0,
                "conflict_level": "NONE",
                "conflict_ratio": 0.0,
            }

        # Get base score from consensus
        base_score = consensus.get("score", 0.0)
        base_confidence = consensus.get("confidence", 0.0)

        # ✅ FIX: Use ConflictDetector for accurate classification
        result = self.detector._analyze_group_conflicts(group)
        conflict_level = result["conflict_level"]
        conflict_ratio = result["conflict_ratio"]

        # Calculate conflict penalty
        conflict_penalty = self._calculate_conflict_penalty(
            conflict_level, conflict_ratio, group
        )

        # Apply penalty
        final_score = base_score * (1 - conflict_penalty)
        final_confidence = base_confidence * (1 - conflict_penalty * 0.6)

        # Determine direction
        direction = self._determine_direction(group, final_score)

        return {
            "score": final_score,
            "direction": direction,
            "confidence": max(0, min(100, final_confidence)),
            "conflict_penalty": conflict_penalty,
            "base_score": base_score,
            "base_confidence": base_confidence,
            "conflict_level": conflict_level,
            "conflict_ratio": conflict_ratio,
            "engine_count": len(group.evidence),
        }

    def _calculate_conflict_penalty(
        self, conflict_level: str, conflict_ratio: float, group: EvidenceGroup
    ) -> float:
        """
        Calculate conflict penalty based on conflict level and ratio.
        """
        # Base penalty from level
        base_penalty = self.penalty_multipliers.get(conflict_level, 0.0)

        # Adjust by conflict ratio
        ratio_adjustment = conflict_ratio * 0.3

        # Quality factor - higher quality evidence reduces penalty
        avg_quality = group.get_average_reliability()
        quality_factor = 1.0 - (avg_quality * 0.2)

        # Final penalty
        final_penalty = (base_penalty + ratio_adjustment) * quality_factor

        # Cap at 0.5 (50% maximum penalty)
        return min(0.5, final_penalty)

    def _determine_direction(self, group: EvidenceGroup, final_score: float) -> str:
        """
        Determine direction considering all signals including neutrals.
        """
        signals = group.evidence
        if not signals:
            return "NEUTRAL"

        bullish = sum(1 for e in signals if e.signal.direction == Direction.BULLISH)
        bearish = sum(1 for e in signals if e.signal.direction == Direction.BEARISH)
        neutral = sum(1 for e in signals if e.signal.direction == Direction.NEUTRAL)

        # If all signals are neutral
        if neutral == len(signals):
            return "NEUTRAL"

        # Use final score for strong signals
        if final_score > 20:
            return "BULLISH"
        elif final_score < -20:
            return "BEARISH"

        # Use voting with neutral consideration
        if bullish > bearish and bullish >= neutral:
            return "BULLISH"
        elif bearish > bullish and bearish >= neutral:
            return "BEARISH"
        elif (
            bullish > 0
            and bearish > 0
            and bullish == bearish
            or neutral > 0
            and bullish == 0
            and bearish == 0
            or neutral > 0
            and bullish == bearish
        ):
            return "NEUTRAL"
        elif bullish > bearish:
            return "BULLISH"
        elif bearish > bullish:
            return "BEARISH"

        return "NEUTRAL"

    def calculate_scores(self, groups: list[EvidenceGroup]) -> dict[str, Any]:
        """
        Calculate scores for multiple groups.
        """
        results = {}
        for group in groups:
            key = f"{group.entity}_{group.signal_type}"
            consensus = {
                "score": group.get_consensus_score(),
                "confidence": group.get_confidence(),
            }
            results[key] = self.calculate_score(group, consensus)

        # Calculate overall
        if results:
            scores = [r["score"] for r in results.values()]
            avg_score = sum(scores) / len(scores) if scores else 0
            avg_confidence = (
                sum(r["confidence"] for r in results.values()) / len(results)
                if results
                else 0
            )

            bullish_count = sum(
                1 for r in results.values() if r["direction"] == "BULLISH"
            )
            bearish_count = sum(
                1 for r in results.values() if r["direction"] == "BEARISH"
            )

            if bullish_count > bearish_count:
                overall_direction = "BULLISH"
            elif bearish_count > bullish_count:
                overall_direction = "BEARISH"
            else:
                overall_direction = "NEUTRAL"

            avg_penalty = sum(r["conflict_penalty"] for r in results.values()) / len(
                results
            )

            return {
                "individual_results": results,
                "overall_score": avg_score,
                "overall_direction": overall_direction,
                "overall_confidence": avg_confidence,
                "average_conflict_penalty": avg_penalty,
                "group_count": len(results),
            }

        return {
            "individual_results": {},
            "overall_score": 0.0,
            "overall_direction": "NEUTRAL",
            "overall_confidence": 0.0,
            "average_conflict_penalty": 0.0,
            "group_count": 0,
        }
