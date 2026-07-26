"""
Confluence Engine - Freshness Checker

Checks the freshness of evidence signals.
"""

from datetime import datetime
from typing import Any

from ..schemas import NormalizedSignal


class FreshnessChecker:
    """
    Checks and scores the freshness of evidence signals.
    """

    def __init__(self, max_age_seconds: int = 3600):
        self.max_age_seconds = max_age_seconds

    def get_freshness_score(self, timestamp: datetime) -> float:
        """
        Calculate freshness score (0-1) for a timestamp.
        """
        age = (datetime.utcnow() - timestamp).total_seconds()

        if age <= 0:
            return 1.0

        # Exponential decay: freshness = e^(-age / half_life)
        half_life = self.max_age_seconds / 2
        freshness = 2 ** (-age / half_life)

        return max(0.0, min(1.0, freshness))

    def get_freshness_for_signal(self, signal: NormalizedSignal) -> float:
        """
        Get freshness score for a normalized signal.
        """
        if not signal.timestamp:
            return 0.0

        return self.get_freshness_score(signal.timestamp)

    def is_fresh(self, timestamp: datetime, threshold: float = 0.5) -> bool:
        """
        Check if a timestamp is considered fresh.
        """
        return self.get_freshness_score(timestamp) >= threshold

    def is_signal_fresh(self, signal: NormalizedSignal, threshold: float = 0.5) -> bool:
        """
        Check if a signal is considered fresh.
        """
        return self.is_fresh(signal.timestamp, threshold)

    def get_freshness_summary(self, signals: list) -> dict[str, Any]:
        """
        Get freshness summary for a list of signals.
        """
        if not signals:
            return {
                "average_freshness": 0.0,
                "fresh_count": 0,
                "stale_count": 0,
                "total_count": 0,
            }

        freshness_scores = [self.get_freshness_for_signal(s) for s in signals]
        fresh_count = sum(1 for f in freshness_scores if f >= 0.5)

        return {
            "average_freshness": sum(freshness_scores) / len(freshness_scores),
            "fresh_count": fresh_count,
            "stale_count": len(signals) - fresh_count,
            "total_count": len(signals),
        }

    def get_signal_age(self, signal: NormalizedSignal) -> float:
        """
        Get the age of a signal in seconds.
        """
        if not signal.timestamp:
            return float("inf")
        return (datetime.utcnow() - signal.timestamp).total_seconds()

    def get_freshness_report(self, signals: list) -> dict[str, Any]:
        """
        Generate a detailed freshness report.
        """
        if not signals:
            return {"status": "NO_SIGNALS", "average_age": 0, "freshness_scores": []}

        ages = [self.get_signal_age(s) for s in signals]
        scores = [self.get_freshness_for_signal(s) for s in signals]

        return {
            "status": "READY",
            "average_age": sum(ages) / len(ages) if ages else 0,
            "average_freshness": sum(scores) / len(scores) if scores else 0,
            "oldest_age": max(ages) if ages else 0,
            "newest_age": min(ages) if ages else 0,
            "fresh_count": sum(1 for s in scores if s >= 0.5),
            "stale_count": sum(1 for s in scores if s < 0.5),
            "total_count": len(signals),
        }
