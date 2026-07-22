"""
Confluence Engine - Harmonization Core

The Harmonization Core calculates weighted consensus, confluence scores,
detects conflicts, and deduplicates evidence.
"""

from .weighted_consensus import WeightedConsensus
from .confluence_score import ConfluenceScore
from .conflict_detector import ConflictDetector
from .evidence_deduplicator import EvidenceDeduplicator

__all__ = [
    "WeightedConsensus",
    "ConfluenceScore",
    "ConflictDetector",
    "EvidenceDeduplicator",
]
