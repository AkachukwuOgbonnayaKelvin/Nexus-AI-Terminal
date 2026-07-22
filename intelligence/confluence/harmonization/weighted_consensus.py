"""
Confluence Engine - Weighted Consensus

Calculates weighted consensus from evidence groups.
"""

import logging
from typing import Dict, List, Any

from ..evidence.evidence_model import EvidenceGroup

logger = logging.getLogger(__name__)


class WeightedConsensus:
    """
    Calculates weighted consensus from evidence groups.
    """

    def __init__(self):
        self.engine_weights = {
            "GLB-001": 1.0,
            "GLB-002": 0.9,
            "GLB-003": 1.0,
            "GLB-004": 0.8,
            "GLB-005": 0.95,
            "GLB-006": 0.9,
            "GLB-007": 0.85,
            "GLB-008": 0.75,
            "GLB-009": 0.8,
        }

    def calculate_consensus(self, group: EvidenceGroup) -> Dict[str, Any]:
        """
        Calculate weighted consensus for an evidence group.
        """
        if not group.evidence:
            return {
                "score": 0.0,
                "direction": "NEUTRAL",
                "confidence": 0.0,
                "engine_count": 0,
                "weighted_contributions": {},
            }

        total_weight = 0.0
        weighted_sum = 0.0
        weighted_contributions = {}

        for entry in group.evidence:
            engine_id = entry.signal.engine_id
            weight = self.engine_weights.get(engine_id, 0.8)
            quality = entry.quality_score

            # Combine weight and quality
            effective_weight = weight * quality

            weighted_sum += entry.signal.score * effective_weight
            total_weight += effective_weight

            weighted_contributions[engine_id] = {
                "score": entry.signal.score,
                "weight": weight,
                "quality": quality,
                "effective_weight": effective_weight,
                "direction": entry.signal.direction.value,
                "contribution": entry.signal.score * effective_weight,
            }

        if total_weight == 0:
            return {
                "score": 0.0,
                "direction": "NEUTRAL",
                "confidence": 0.0,
                "engine_count": len(group.evidence),
                "weighted_contributions": weighted_contributions,
            }

        consensus_score = weighted_sum / total_weight

        # Calculate confidence from weighted agreement
        directions = [e.signal.direction.value for e in group.evidence]
        bullish = sum(1 for d in directions if d == "BULLISH")
        bearish = sum(1 for d in directions if d == "BEARISH")
        total = len(directions)
        agreement = max(bullish, bearish) / total if total > 0 else 0

        avg_quality = sum(e.quality_score for e in group.evidence) / len(group.evidence)
        confidence = avg_quality * 0.6 + agreement * 0.4
        confidence = min(1.0, confidence) * 100

        if consensus_score > 10:
            direction = "BULLISH"
        elif consensus_score < -10:
            direction = "BEARISH"
        else:
            direction = "NEUTRAL"

        return {
            "score": consensus_score,
            "direction": direction,
            "confidence": confidence,
            "engine_count": len(group.evidence),
            "agreement_ratio": agreement,
            "weighted_contributions": weighted_contributions,
        }

    def calculate_multi_consensus(self, groups: List[EvidenceGroup]) -> Dict[str, Any]:
        """
        Calculate consensus across multiple evidence groups.
        """
        results = {}
        for group in groups:
            key = f"{group.entity}_{group.signal_type}"
            results[key] = self.calculate_consensus(group)

        # Calculate overall
        if results:
            scores = [r["score"] for r in results.values()]
            avg_score = sum(scores) / len(scores) if scores else 0
            avg_confidence = (
                sum(r["confidence"] for r in results.values()) / len(results)
                if results
                else 0
            )

            # Determine overall direction
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

            return {
                "individual_results": results,
                "overall_score": avg_score,
                "overall_direction": overall_direction,
                "overall_confidence": avg_confidence,
                "group_count": len(results),
            }

        return {
            "individual_results": {},
            "overall_score": 0.0,
            "overall_direction": "NEUTRAL",
            "overall_confidence": 0.0,
            "group_count": 0,
        }

    def set_engine_weight(self, engine_id: str, weight: float) -> None:
        """
        Set a custom weight for an engine.
        """
        self.engine_weights[engine_id] = weight
