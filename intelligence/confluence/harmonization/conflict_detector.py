"""
Confluence Engine - Conflict Detector

Detects and measures agreement/disagreement between engines.
Separates directional conflict from neutral uncertainty.
"""

import logging
from typing import Dict, List, Any
from collections import defaultdict

from ..evidence.evidence_model import EvidenceGroup
from ..schemas import Direction

logger = logging.getLogger(__name__)


class ConflictDetector:
    """
    Detects and measures conflict between evidence signals.
    """

    def __init__(self):
        self.thresholds = {"none": 0.05, "low": 0.20, "medium": 0.55, "high": 1.00}

    def detect_conflicts(self, groups: List[EvidenceGroup]) -> Dict[str, Any]:
        """Detect conflicts across all evidence groups."""
        results = {}

        for group in groups:
            key = f"{group.entity}_{group.signal_type}"
            results[key] = self._analyze_group_conflicts(group)

        if results:
            conflict_levels = [r["conflict_level"] for r in results.values()]
            level_counts = defaultdict(int)
            for level in conflict_levels:
                level_counts[level] += 1

            total = len(conflict_levels)
            high_conflict = level_counts.get("HIGH", 0)

            return {
                "individual_results": results,
                "summary": {
                    "total_groups": total,
                    "conflict_distribution": dict(level_counts),
                    "high_conflict_percentage": (high_conflict / total * 100)
                    if total > 0
                    else 0,
                },
            }

        return {
            "individual_results": {},
            "summary": {
                "total_groups": 0,
                "conflict_distribution": {},
                "high_conflict_percentage": 0,
            },
        }

    def _analyze_group_conflicts(self, group: EvidenceGroup) -> Dict[str, Any]:
        """Analyze conflicts within a single evidence group."""
        signals = group.evidence
        total = len(signals)

        if total == 0:
            return {
                "entity": group.entity,
                "signal_type": group.signal_type,
                "conflict_level": "NONE",
                "directions": {"BULLISH": 0, "BEARISH": 0, "NEUTRAL": 0, "total": 0},
                "consensus_direction": "NEUTRAL",
                "conflicting_engines": [],
                "conflict_ratio": 0.0,
                "uncertainty_ratio": 0.0,
                "directional_balance": 0.0,
            }

        # Count directions
        bullish = sum(1 for e in signals if e.signal.direction == Direction.BULLISH)
        bearish = sum(1 for e in signals if e.signal.direction == Direction.BEARISH)
        neutral = sum(1 for e in signals if e.signal.direction == Direction.NEUTRAL)

        # Directional conflict
        non_neutral = bullish + bearish

        if non_neutral == 0:
            conflict_ratio = 0.0
            conflict_level = "NONE"
            directional_balance = 0.0
        else:
            max_side = max(bullish, bearish)
            min_side = min(bullish, bearish)
            directional_balance = min_side / max_side if max_side > 0 else 0.0
            conflict_ratio = 1.0 - (max_side / non_neutral)

            if directional_balance < self.thresholds["none"]:
                conflict_level = "NONE"
            elif directional_balance < self.thresholds["low"]:
                conflict_level = "LOW"
            elif directional_balance < self.thresholds["medium"]:
                conflict_level = "MEDIUM"
            else:
                conflict_level = "HIGH"

        # Uncertainty from neutral signals
        uncertainty_ratio = neutral / total if total > 0 else 0.0

        # Downgrade HIGH to MEDIUM when there are neutral signals
        if conflict_level == "HIGH" and uncertainty_ratio >= 0.20:
            conflict_level = "MEDIUM"

        # Determine consensus direction
        if bullish > bearish:
            consensus = "BULLISH"
        elif bearish > bullish:
            consensus = "BEARISH"
        else:
            if bullish > 0 and neutral > 0:
                consensus = "NEUTRAL"
            elif bearish > 0 and neutral > 0:
                consensus = "NEUTRAL"
            elif bullish > 0:
                consensus = "BULLISH"
            elif bearish > 0:
                consensus = "BEARISH"
            else:
                consensus = "NEUTRAL"

        # Identify conflicting engines
        conflicting = []
        if conflict_level in ["MEDIUM", "HIGH"]:
            for e in signals:
                if (
                    e.signal.direction.value != consensus
                    and e.signal.direction != Direction.NEUTRAL
                ):
                    conflicting.append(
                        {
                            "engine_id": e.signal.engine_id,
                            "direction": e.signal.direction.value,
                            "score": e.signal.score,
                            "confidence": e.signal.confidence,
                            "quality": e.quality_score,
                        }
                    )

        return {
            "entity": group.entity,
            "signal_type": group.signal_type,
            "conflict_level": conflict_level,
            "directions": {
                "BULLISH": bullish,
                "BEARISH": bearish,
                "NEUTRAL": neutral,
                "total": total,
            },
            "weights": {
                "bullish_weight": 0.0,
                "bearish_weight": 0.0,
                "neutral_weight": 0.0,
            },
            "consensus_direction": consensus,
            "conflicting_engines": conflicting,
            "conflict_ratio": conflict_ratio,
            "uncertainty_ratio": uncertainty_ratio,
            "directional_balance": directional_balance,
        }

    def get_agreement_score(self, group: EvidenceGroup) -> float:
        """Get agreement score (0-1) for a group."""
        signals = group.evidence
        if not signals:
            return 0.0

        bullish = sum(1 for e in signals if e.signal.direction == Direction.BULLISH)
        bearish = sum(1 for e in signals if e.signal.direction == Direction.BEARISH)
        non_neutral = bullish + bearish

        if non_neutral == 0:
            return 1.0

        max_side = max(bullish, bearish)
        return max_side / non_neutral
