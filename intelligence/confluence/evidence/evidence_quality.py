"""
Confluence Engine - Evidence Quality

Calculates the quality of evidence signals.
"""

from typing import Any

from ..schemas import NormalizedSignal
from .freshness import FreshnessChecker


class EvidenceQuality:
    """
    Calculates overall evidence quality scores.
    """

    def __init__(self):
        self.freshness_checker = FreshnessChecker()

    def calculate_quality(self, signal: NormalizedSignal) -> float:
        """
        Calculate overall quality score for a signal.
        """
        # Components
        reliability = signal.reliability
        confidence = signal.confidence / 100
        freshness = self.freshness_checker.get_freshness_for_signal(signal)
        evidence_quality = signal.evidence_quality

        # Weighted combination
        quality = (
            reliability * 0.30
            + confidence * 0.30
            + freshness * 0.20
            + evidence_quality * 0.20
        )

        return min(1.0, max(0.0, quality))

    def calculate_quality_for_signals(
        self, signals: list[NormalizedSignal]
    ) -> dict[str, float]:
        """
        Calculate quality scores for multiple signals.
        """
        return {s.engine_id: self.calculate_quality(s) for s in signals}

    def get_average_quality(self, signals: list[NormalizedSignal]) -> float:
        """
        Get average quality across signals.
        """
        if not signals:
            return 0.0

        qualities = [self.calculate_quality(s) for s in signals]
        return sum(qualities) / len(qualities)

    def get_quality_summary(self, signals: list[NormalizedSignal]) -> dict[str, Any]:
        """
        Get quality summary for a list of signals.
        """
        if not signals:
            return {"status": "NO_SIGNALS"}

        qualities = [self.calculate_quality(s) for s in signals]
        high_quality = sum(1 for q in qualities if q >= 0.7)
        medium_quality = sum(1 for q in qualities if 0.4 <= q < 0.7)
        low_quality = sum(1 for q in qualities if q < 0.4)

        return {
            "status": "READY",
            "average_quality": sum(qualities) / len(qualities) if qualities else 0,
            "high_quality_count": high_quality,
            "medium_quality_count": medium_quality,
            "low_quality_count": low_quality,
            "total_count": len(signals),
            "best_quality": max(qualities) if qualities else 0,
            "worst_quality": min(qualities) if qualities else 0,
        }

    def filter_by_quality(
        self, signals: list[NormalizedSignal], min_quality: float = 0.3
    ) -> list[NormalizedSignal]:
        """
        Filter signals by minimum quality.
        """
        return [s for s in signals if self.calculate_quality(s) >= min_quality]
