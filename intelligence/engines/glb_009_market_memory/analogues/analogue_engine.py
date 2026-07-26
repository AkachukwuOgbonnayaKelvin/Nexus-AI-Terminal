"""
GLB-009 Market Memory & Historical Analogy Intelligence Engine - Analogue Engine
"""

import logging
from typing import Any

from ..analysis.similarity_engine import SimilarityEngine
from ..constants import AnalogueQuality
from ..input.schemas import HistoricalWindow, MarketSnapshot

logger = logging.getLogger(__name__)


class AnalogueEngine:
    """Find and qualify historical analogues - GLOBAL WINDOW SELECTION"""

    def __init__(self):
        self.similarity_engine = SimilarityEngine()
        self.min_analogues = 5
        self.max_analogues = 30  # Top-K selection globally

    def find_analogues(
        self,
        current: MarketSnapshot,
        historical_windows: list[HistoricalWindow],
        min_similarity: float = 0.60,
    ) -> dict[str, Any]:
        """
        Find historical analogues matching current environment.

        KEY FIX: This now selects Top-K windows globally, not per-symbol.
        The window identity is the date/window_id, not the symbol.
        """
        if not historical_windows:
            return {
                "status": "NO_DATA",
                "analogues_found": 0,
                "qualified_analogues": 0,
                "quality": AnalogueQuality.INSUFFICIENT.value,
            }

        # Step 1: Calculate similarity for ALL windows globally
        all_candidates = []
        for window in historical_windows:
            try:
                similarity = self.similarity_engine.calculate_similarity(
                    current, window
                )
                all_candidates.append(
                    {
                        "window": window,
                        "window_id": getattr(window, "window_id", "UNKNOWN"),
                        "similarity": similarity,
                        "symbol": getattr(window, "symbol", "UNKNOWN"),
                    }
                )
            except Exception as e:
                logger.debug(f"Error calculating similarity: {e}")
                continue

        # Step 2: Sort ALL candidates by similarity (global sort, not per-symbol)
        all_candidates.sort(
            key=lambda x: x["similarity"]["overall_similarity"], reverse=True
        )

        # Step 3: Select Top-K globally (not per-symbol)
        top_k = all_candidates[: self.max_analogues]
        qualified = len(top_k)

        if qualified < self.min_analogues:
            return {
                "status": "INSUFFICIENT",
                "analogues_found": len(all_candidates),
                "qualified_analogues": qualified,
                "quality": AnalogueQuality.INSUFFICIENT.value,
                "analogues": [],
            }

        # Step 4: Calculate quality metrics from top-K
        best_match = top_k[0]["similarity"]["overall_similarity"] if top_k else 0
        avg_match = (
            sum(a["similarity"]["overall_similarity"] for a in top_k) / qualified
            if qualified > 0
            else 0
        )

        quality = self._determine_quality(qualified, best_match, avg_match)
        feature_consistency = self._calculate_feature_consistency(top_k)

        # Step 5: Log the window identities (dates) found
        window_ids = [c.get("window_id", "UNKNOWN") for c in top_k]
        symbols = list(set(c.get("symbol", "UNKNOWN") for c in top_k))

        logger.info(
            f"Found {qualified} analogues with IDs: {window_ids[:5]}... (symbols: {symbols})"
        )

        return {
            "status": "OPERATIONAL",
            "analogues_found": len(all_candidates),
            "qualified_analogues": qualified,
            "best_match": best_match,
            "average_match": avg_match,
            "quality": quality.value,
            "min_similarity": min_similarity * 100,
            "analogues": top_k,
            "window_ids": window_ids,
            "symbols_found": symbols,
            "feature_consistency": feature_consistency,
            "match_confidence": min(95, 50 + qualified * 1.5),
            "confidence": min(95, 50 + qualified * 1.5),
        }

    def _determine_quality(
        self, count: int, best_match: float, avg_match: float
    ) -> AnalogueQuality:
        if count >= 15 and best_match >= 75 and avg_match >= 65:
            return AnalogueQuality.HIGH
        elif count >= 8 and best_match >= 65 and avg_match >= 55:
            return AnalogueQuality.MODERATE
        elif count >= 5 and best_match >= 55:
            return AnalogueQuality.LOW
        return AnalogueQuality.INSUFFICIENT

    def _calculate_feature_consistency(self, analogues: list[dict]) -> dict[str, float]:
        if not analogues:
            return {}

        consistency = {}
        feature_scores = {}

        for analogue in analogues:
            for feature, score in analogue["similarity"]["feature_scores"].items():
                if feature not in feature_scores:
                    feature_scores[feature] = []
                feature_scores[feature].append(score)

        for feature, scores in feature_scores.items():
            avg = sum(scores) / len(scores)
            std = (sum((s - avg) ** 2 for s in scores) / len(scores)) ** 0.5
            cv = std / avg if avg > 0 else 0
            consistency[feature] = max(0, 100 - (cv * 100))

        return consistency
