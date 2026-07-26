"""
Phase 6: Distribution API & Output Contracts

The Distribution API is the publishing and routing boundary
between the Confluence Engine and downstream systems.

It produces two outputs:
1. FINAL Global Intelligence Output → Global Intelligence Hub
2. SEMI-FINISHED Asset Feeds → Asset Intelligence Engine
"""

from .assembler import OutputAssembler
from .asset_feed_builder import AssetFeedBuilder
from .envelope import EnvelopeFactory, OutputEnvelope, OutputStatus, OutputType
from .global_builder import GlobalOutputBuilder
from .health import DistributionHealth, DistributionHealthMonitor
from .package import ConfluenceIntelligencePackage
from .router import DistributionRouter
from .validator import OutputValidator, ValidationResult
from .versioning import SchemaVersion, VersionManager

__all__ = [
    "AssetFeedBuilder",
    "ConfluenceIntelligencePackage",
    "DistributionHealth",
    "DistributionHealthMonitor",
    "DistributionRouter",
    "EnvelopeFactory",
    "GlobalOutputBuilder",
    "OutputAssembler",
    "OutputEnvelope",
    "OutputStatus",
    "OutputType",
    "OutputValidator",
    "SchemaVersion",
    "ValidationResult",
    "VersionManager",
]
