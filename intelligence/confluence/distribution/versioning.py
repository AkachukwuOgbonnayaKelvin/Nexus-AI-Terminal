"""
Phase 6: Distribution API - Schema Versioning

Manages schema versions for all outputs.
"""

from typing import Dict
from enum import Enum


class SchemaVersion(str, Enum):
    """Schema versions for outputs."""

    V1_0_0 = "1.0.0"
    V1_1_0 = "1.1.0"
    V2_0_0 = "2.0.0"


class VersionManager:
    """Manages schema versions for outputs."""

    # Current schema versions
    CURRENT_GLOBAL_SCHEMA = SchemaVersion.V1_0_0
    CURRENT_ASSET_FEED_SCHEMA = SchemaVersion.V1_0_0

    # Schema compatibility matrix
    _compatibility: Dict[str, Dict[str, bool]] = {
        "1.0.0": {"1.0.0": True, "1.1.0": True, "2.0.0": False},
        "1.1.0": {"1.0.0": True, "1.1.0": True, "2.0.0": False},
        "2.0.0": {"1.0.0": False, "1.1.0": False, "2.0.0": True},
    }

    @classmethod
    def get_current_version(cls, output_type: str) -> str:
        """Get current schema version for an output type."""
        if output_type == "GLOBAL_INTELLIGENCE":
            return cls.CURRENT_GLOBAL_SCHEMA.value
        elif output_type == "ASSET_INTELLIGENCE_FEED":
            return cls.CURRENT_ASSET_FEED_SCHEMA.value
        return SchemaVersion.V1_0_0.value

    @classmethod
    def is_compatible(cls, version: str, target_version: str) -> bool:
        """Check if two schema versions are compatible."""
        if version not in cls._compatibility:
            return False
        if target_version not in cls._compatibility[version]:
            return False
        return cls._compatibility[version][target_version]

    @classmethod
    def get_supported_versions(cls) -> list:
        """Get all supported schema versions."""
        return list(cls._compatibility.keys())

    @classmethod
    def validate_version(cls, version: str) -> bool:
        """Validate a schema version string."""
        return version in cls._compatibility

    @classmethod
    def get_version_metadata(cls, version: str) -> Dict[str, str]:
        """Get metadata for a schema version."""
        metadata = {
            "1.0.0": {
                "release_date": "2026-07-21",
                "description": "Initial schema release",
                "changes": ["Initial release of Confluence output schemas"],
            },
            "1.1.0": {
                "release_date": "2026-08-01",
                "description": "Added support for multi-timeframe context",
                "changes": ["Added timeframe field", "Added historical context"],
            },
            "2.0.0": {
                "release_date": "2026-09-01",
                "description": "Major schema revision",
                "changes": ["Restructured output format", "Added AI context field"],
            },
        }
        return metadata.get(version, {})
