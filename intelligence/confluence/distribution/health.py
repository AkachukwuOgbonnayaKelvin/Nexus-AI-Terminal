"""
Phase 6: Distribution API - Distribution Health

Monitors the health of the distribution pipeline.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)


@dataclass
class DistributionHealth:
    """Health status of the distribution pipeline."""

    # Overall status
    healthy: bool = True

    # Component statuses
    assembler_healthy: bool = True
    validator_healthy: bool = True
    global_builder_healthy: bool = True
    asset_feed_builder_healthy: bool = True
    envelope_healthy: bool = True

    # Metrics
    total_outputs_published: int = 0
    last_publish_time: Optional[datetime] = None
    validation_errors: int = 0
    validation_warnings: int = 0

    # Errors
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # Timestamp
    checked_at: datetime = field(default_factory=datetime.utcnow)

    def is_healthy(self) -> bool:
        """Check if the distribution pipeline is healthy."""
        return (
            self.healthy
            and self.assembler_healthy
            and self.validator_healthy
            and self.global_builder_healthy
            and self.asset_feed_builder_healthy
            and self.envelope_healthy
        )

    def record_publish(self) -> None:
        """Record a successful publish."""
        self.total_outputs_published += 1
        self.last_publish_time = datetime.utcnow()

    def record_error(self, error: str) -> None:
        """Record an error."""
        self.errors.append(error)
        self.validation_errors += 1
        self.healthy = False

    def record_warning(self, warning: str) -> None:
        """Record a warning."""
        self.warnings.append(warning)
        self.validation_warnings += 1

    def reset(self) -> None:
        """Reset health status."""
        self.healthy = True
        self.errors = []
        self.warnings = []
        self.validation_errors = 0
        self.validation_warnings = 0
        self.checked_at = datetime.utcnow()


class DistributionHealthMonitor:
    """
    Monitors the health of the distribution pipeline.
    """

    def __init__(self):
        self.health = DistributionHealth()

    def check_assembler(self, package_assembled: bool) -> None:
        """Check assembler health."""
        self.health.assembler_healthy = package_assembled
        if not package_assembled:
            self.health.record_error("Assembler failed to create package")

    def check_validator(
        self, validation_passed: bool, errors: list, warnings: list
    ) -> None:
        """Check validator health."""
        self.health.validator_healthy = validation_passed
        if not validation_passed:
            for error in errors:
                self.health.record_error(f"Validator: {error}")
        for warning in warnings:
            self.health.record_warning(f"Validator: {warning}")

    def check_global_builder(self, built_successfully: bool) -> None:
        """Check global builder health."""
        self.health.global_builder_healthy = built_successfully
        if not built_successfully:
            self.health.record_error("Global builder failed to create output")

    def check_asset_feed_builder(self, feeds_built: int, expected_count: int) -> None:
        """Check asset feed builder health."""
        self.health.asset_feed_builder_healthy = feeds_built > 0
        if feeds_built == 0:
            self.health.record_error("Asset feed builder created no feeds")
        elif feeds_built < expected_count:
            self.health.record_warning(
                f"Asset feed builder: built {feeds_built} of {expected_count} expected"
            )

    def check_envelope(self, envelopes_created: int) -> None:
        """Check envelope health."""
        self.health.envelope_healthy = envelopes_created > 0
        if envelopes_created == 0:
            self.health.record_error("No envelopes created")

    def get_status(self) -> Dict[str, Any]:
        """Get current health status."""
        return {
            "healthy": self.health.is_healthy(),
            "total_outputs": self.health.total_outputs_published,
            "last_publish": self.health.last_publish_time.isoformat()
            if self.health.last_publish_time
            else None,
            "validation_errors": self.health.validation_errors,
            "validation_warnings": self.health.validation_warnings,
            "errors": self.health.errors,
            "warnings": self.health.warnings,
            "checked_at": self.health.checked_at.isoformat(),
            "components": {
                "assembler": self.health.assembler_healthy,
                "validator": self.health.validator_healthy,
                "global_builder": self.health.global_builder_healthy,
                "asset_feed_builder": self.health.asset_feed_builder_healthy,
                "envelope": self.health.envelope_healthy,
            },
        }

    def reset(self) -> None:
        """Reset health monitor."""
        self.health.reset()
