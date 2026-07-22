"""
Confluence Engine - Evidence Layer

The Evidence Layer collects, validates, and scores evidence from all GLB engines.
It determines signal quality, freshness, independence, and resolves conflicts.
"""

from .evidence_model import EvidenceGroup, EvidenceEntry
from .evidence_quality import EvidenceQuality
from .freshness import FreshnessChecker
from .evidence_collector import EvidenceCollector
from .dependency_detector import DependencyDetector
from .conflict_resolver import ConflictResolver

__all__ = [
    "EvidenceGroup",
    "EvidenceEntry",
    "EvidenceQuality",
    "FreshnessChecker",
    "EvidenceCollector",
    "DependencyDetector",
    "ConflictResolver",
]
