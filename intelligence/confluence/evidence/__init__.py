"""
Confluence Engine - Evidence Layer

The Evidence Layer collects, validates, and scores evidence from all GLB engines.
It determines signal quality, freshness, independence, and resolves conflicts.
"""

from .conflict_resolver import ConflictResolver
from .dependency_detector import DependencyDetector
from .evidence_collector import EvidenceCollector
from .evidence_model import EvidenceEntry, EvidenceGroup
from .evidence_quality import EvidenceQuality
from .freshness import FreshnessChecker

__all__ = [
    "ConflictResolver",
    "DependencyDetector",
    "EvidenceCollector",
    "EvidenceEntry",
    "EvidenceGroup",
    "EvidenceQuality",
    "FreshnessChecker",
]
