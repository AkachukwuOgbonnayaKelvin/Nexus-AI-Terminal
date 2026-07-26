"""
Phase 6: Distribution API - Distribution Router

Routes outputs to their destinations.
"""

import logging
from typing import Any

from .asset_feed_builder import AssetFeedBuilder
from .envelope import EnvelopeFactory, OutputEnvelope
from .global_builder import GlobalOutputBuilder
from .health import DistributionHealthMonitor
from .package import ConfluenceIntelligencePackage
from .validator import OutputValidator

logger = logging.getLogger(__name__)


class DistributionRouter:
    """
    Routes Confluence outputs to their destinations.

    Destinations:
    - Global Intelligence Hub (FINAL output)
    - Asset Intelligence Engine (SEMI_FINISHED feeds)
    """

    def __init__(self):
        self.global_builder = GlobalOutputBuilder()
        self.asset_feed_builder = AssetFeedBuilder()
        self.validator = OutputValidator()
        self.health = DistributionHealthMonitor()

    def route(
        self, package: ConfluenceIntelligencePackage, strict_validation: bool = True
    ) -> dict[str, Any]:
        """
        Route a ConfluenceIntelligencePackage to its destinations.

        Args:
            package: ConfluenceIntelligencePackage
            strict_validation: If True, fail on validation errors

        Returns:
            Dict with global_output and asset_feeds
        """
        logger.info("Routing Confluence Intelligence Package...")

        # Step 1: Assemble (already done, package provided)
        self.health.check_assembler(package is not None)
        if not package:
            return {"status": "error", "error": "Invalid package"}

        # Step 2: Build Global Output
        logger.info("Building global output...")
        try:
            global_output = self.global_builder.build(package)
            self.health.check_global_builder(True)
        except Exception as e:
            self.health.check_global_builder(False)
            logger.error(f"Failed to build global output: {e}")
            return {"status": "error", "error": str(e)}

        # Step 3: Validate Global Output
        logger.info("Validating global output...")
        validation_result = self.validator.validate_global_output(global_output)
        self.health.check_validator(
            validation_result.valid,
            validation_result.errors,
            validation_result.warnings,
        )

        if strict_validation and not validation_result.valid:
            logger.error(f"Global output validation failed: {validation_result.errors}")
            return {
                "status": "validation_failed",
                "errors": validation_result.errors,
                "warnings": validation_result.warnings,
            }

        # Step 4: Build Asset Feeds
        logger.info("Building asset feeds...")
        try:
            asset_feeds = self.asset_feed_builder.build_for_all_entities(package)
            self.health.check_asset_feed_builder(
                len(asset_feeds), len(package.entity_ratings)
            )
        except Exception as e:
            self.health.check_asset_feed_builder(False, 0)
            logger.error(f"Failed to build asset feeds: {e}")
            return {"status": "error", "error": str(e)}

        # Step 5: Validate Asset Feeds
        logger.info("Validating asset feeds...")
        feed_validation = self.validator.validate_asset_feeds(asset_feeds)
        if not feed_validation.valid:
            logger.warning(f"Asset feed validation errors: {feed_validation.errors}")
            if strict_validation:
                return {
                    "status": "validation_failed",
                    "errors": feed_validation.errors,
                    "warnings": feed_validation.warnings,
                }

        # Step 6: Create Envelopes
        logger.info("Creating envelopes...")
        global_envelope = EnvelopeFactory.create_global_envelope(global_output)
        feed_envelopes = EnvelopeFactory.create_asset_feeds_envelope(asset_feeds)
        self.health.check_envelope(1 + len(feed_envelopes))

        # Step 7: Record successful publish
        self.health.health.record_publish()

        logger.info(
            f"Routing complete: 1 global output, {len(feed_envelopes)} asset feeds"
        )

        return {
            "status": "success",
            "global_output": global_envelope,
            "asset_feeds": feed_envelopes,
            "health": self.health.get_status(),
            "validation": {
                "global_valid": validation_result.valid,
                "global_errors": validation_result.errors,
                "global_warnings": validation_result.warnings,
                "feed_valid": feed_validation.valid,
                "feed_errors": feed_validation.errors,
                "feed_warnings": feed_validation.warnings,
            },
        }

    def route_global_only(
        self, package: ConfluenceIntelligencePackage, strict_validation: bool = True
    ) -> OutputEnvelope | None:
        """
        Route only the global output.

        Args:
            package: ConfluenceIntelligencePackage
            strict_validation: If True, fail on validation errors

        Returns:
            OutputEnvelope or None if failed
        """
        logger.info("Routing global output only...")

        try:
            global_output = self.global_builder.build(package)
            validation = self.validator.validate_global_output(global_output)

            if strict_validation and not validation.valid:
                logger.error(f"Validation failed: {validation.errors}")
                return None

            envelope = EnvelopeFactory.create_global_envelope(global_output)
            self.health.health.record_publish()
            return envelope

        except Exception as e:
            logger.error(f"Failed to route global output: {e}")
            return None

    def route_asset_feeds_only(
        self,
        package: ConfluenceIntelligencePackage,
        entities: list[str] | None = None,
        strict_validation: bool = True,
    ) -> list[OutputEnvelope]:
        """
        Route only asset feeds.

        Args:
            package: ConfluenceIntelligencePackage
            entities: Optional list of entities to feed
            strict_validation: If True, fail on validation errors

        Returns:
            List[OutputEnvelope]
        """
        logger.info("Routing asset feeds only...")

        try:
            if entities:
                feeds = self.asset_feed_builder.build_for_entities(entities, package)
            else:
                feeds = self.asset_feed_builder.build_for_all_entities(package)

            if strict_validation:
                validation = self.validator.validate_asset_feeds(feeds)
                if not validation.valid:
                    logger.error(f"Asset feed validation failed: {validation.errors}")
                    return []

            envelopes = EnvelopeFactory.create_asset_feeds_envelope(feeds)
            self.health.health.record_publish()
            return envelopes

        except Exception as e:
            logger.error(f"Failed to route asset feeds: {e}")
            return []

    def get_health(self) -> dict[str, Any]:
        """Get distribution health status."""
        return self.health.get_status()

    def reset_health(self) -> None:
        """Reset health monitor."""
        self.health.reset()
