"""
Confluence Engine - Harmonization Core

The Harmonization Core calculates weighted consensus, confluence scores,
detects conflicts, and deduplicates evidence.
"""

from .conflict_detector import ConflictDetector
from .confluence_score import ConfluenceScore
from .evidence_deduplicator import EvidenceDeduplicator
from .weighted_consensus import WeightedConsensus

__all__ = [
    "ConflictDetector",
    "ConfluenceScore",
    "EvidenceDeduplicator",
    "WeightedConsensus",
]
