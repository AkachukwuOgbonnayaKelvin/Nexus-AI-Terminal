"""Universal Intelligence Standard.

Every intelligence engine in Nexus AI Terminal MUST produce output conforming to
this standard. This ensures all intelligence can be consumed uniformly by hubs,
publish caches, and the master orchestrator.

Required Output Structure:
- executive_summary: Human-readable summary
- executive_ai_summary: AI-generated summary
- confidence: Confidence scoring object
- evidence: Supporting and contradicting evidence
- risk: Risk assessment
- recommendations: List of recommendations
- metadata: Engine metadata
- health: Engine health status
"""

from .schemas import (
    ConfidenceScore,
    EvidenceItem,
    IntelligenceHealth,
    IntelligenceMetadata,
    Recommendation,
    RiskAssessment,
    UniversalIntelligence,
)

__all__ = [
    "UniversalIntelligence",
    "ConfidenceScore",
    "EvidenceItem",
    "RiskAssessment",
    "Recommendation",
    "IntelligenceMetadata",
    "IntelligenceHealth",
]
