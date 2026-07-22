"""
Confluence Engine - Conflict Resolver

Resolves conflicts between signals.
"""

import logging
from typing import Dict, Any

from .evidence_model import EvidenceGroup
from ..schemas import Direction, ConflictLevel

logger = logging.getLogger(__name__)


class ConflictResolver:
    """
    Resolves conflicts between signals.
    """

    def resolve(self, group: EvidenceGroup) -> Dict[str, Any]:
        """
        Resolve conflicts within an evidence group.

        Args:
            group: EvidenceGroup to resolve

        Returns:
            Dict with conflict resolution results
        """
        if not group.evidence:
            return {
                "resolved": True,
                "consensus_direction": "NEUTRAL",
                "conflict_level": "NONE",
                "conflicting_engines": [],
                "resolution_suggestion": "",
            }

        # Count directions
        bullish = sum(
            1 for e in group.evidence if e.signal.direction == Direction.BULLISH
        )
        bearish = sum(
            1 for e in group.evidence if e.signal.direction == Direction.BEARISH
        )
        neutral = sum(
            1 for e in group.evidence if e.signal.direction == Direction.NEUTRAL
        )
        total = len(group.evidence)

        # Determine consensus
        if bullish > bearish:
            consensus = "BULLISH"
        elif bearish > bullish:
            consensus = "BEARISH"
        else:
            consensus = "NEUTRAL"

        # Determine conflict level
        if bullish == 0 or bearish == 0:
            conflict_level = "NONE"
        elif max(bullish, bearish) / total >= 0.7:
            conflict_level = "LOW"
        elif max(bullish, bearish) / total >= 0.5:
            conflict_level = "MEDIUM"
        else:
            conflict_level = "HIGH"

        # Find conflicting engines
        conflicting = []
        for e in group.evidence:
            if (
                e.signal.direction.value != consensus
                and e.signal.direction != Direction.NEUTRAL
            ):
                conflicting.append(e.signal.engine_id)

        # Generate resolution suggestion
        if conflict_level == "NONE":
            suggestion = "No conflict detected. Evidence is aligned."
        elif conflict_level == "LOW":
            suggestion = "Minor conflict. Consensus direction is supported by majority."
        elif conflict_level == "MEDIUM":
            suggestion = "Significant conflict. Consider weighting by reliability."
        else:
            suggestion = "High conflict. Consider seeking additional evidence or reducing confidence."

        return {
            "resolved": conflict_level in ["NONE", "LOW"],
            "consensus_direction": consensus,
            "conflict_level": conflict_level,
            "conflicting_engines": conflicting,
            "resolution_suggestion": suggestion,
            "counts": {
                "bullish": bullish,
                "bearish": bearish,
                "neutral": neutral,
                "total": total,
            },
        }

    def get_conflict_level(self, group: EvidenceGroup) -> ConflictLevel:
        """Get conflict level for a group."""
        result = self.resolve(group)
        level_map = {
            "NONE": ConflictLevel.NONE,
            "LOW": ConflictLevel.LOW,
            "MEDIUM": ConflictLevel.MEDIUM,
            "HIGH": ConflictLevel.HIGH,
        }
        return level_map.get(result["conflict_level"], ConflictLevel.NONE)
