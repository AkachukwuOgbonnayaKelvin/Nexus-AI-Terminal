"""
Phase 6: Distribution API & Output Contracts

The Distribution API is the publishing and routing boundary
between the Confluence Engine and downstream systems.

It produces two outputs:
1. FINAL Global Intelligence Output → Global Intelligence Hub
2. SEMI-FINISHED Asset Feeds → Asset Intelligence Engine
"""

from .package import ConfluenceIntelligencePackage
from .assembler import OutputAssembler
from .validator import OutputValidator, ValidationResult
from .global_builder import GlobalOutputBuilder
from .asset_feed_builder import AssetFeedBuilder
from .envelope import OutputEnvelope, EnvelopeFactory, OutputStatus, OutputType
from .versioning import VersionManager, SchemaVersion
from .health import DistributionHealth, DistributionHealthMonitor
from .router import DistributionRouter

__all__ = [
    "ConfluenceIntelligencePackage",
    "OutputAssembler",
    "OutputValidator",
    "ValidationResult",
    "GlobalOutputBuilder",
    "AssetFeedBuilder",
    "OutputEnvelope",
    "EnvelopeFactory",
    "OutputStatus",
    "OutputType",
    "VersionManager",
    "SchemaVersion",
    "DistributionHealth",
    "DistributionHealthMonitor",
    "DistributionRouter",
]
