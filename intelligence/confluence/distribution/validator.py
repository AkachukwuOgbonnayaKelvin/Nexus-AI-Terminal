"""
Phase 6: Distribution API - Output Validator

Validates output integrity before publishing.
Acts as the final quality gate.
"""

import logging
from typing import List

from ..contracts import (
    GlobalEntityRating,
    AssetClassRating,
    GlobalIntelligenceOutput,
    AssetIntelligenceFeed,
    Direction,
)
from ..entity.direction import classify_direction

logger = logging.getLogger(__name__)


class ValidationResult:
    """Result of validation."""

    def __init__(self):
        self.valid = True
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def add_error(self, message: str) -> None:
        self.valid = False
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)

    def __repr__(self) -> str:
        status = "✅ VALID" if self.valid else "❌ INVALID"
        return f"ValidationResult({status}, errors={len(self.errors)}, warnings={len(self.warnings)})"


class OutputValidator:
    """
    Validates outputs before publishing.

    Checks:
    - Required fields present
    - Score ranges (-100 to +100)
    - Direction consistency
    - Rank sequential integrity
    - Confidence ranges (0-100)
    - No duplicate entities
    - Timestamp validity
    - Status validity
    """

    def validate_entity_ratings(
        self, ratings: List[GlobalEntityRating]
    ) -> ValidationResult:
        """Validate entity ratings."""
        result = ValidationResult()

        if not ratings:
            result.add_warning("No entity ratings provided")
            return result

        entities_seen = set()

        for i, rating in enumerate(ratings):
            # Check entity
            if not rating.entity:
                result.add_error(f"Entity rating {i}: Missing entity name")

            # Check duplicate entity
            if rating.entity in entities_seen:
                result.add_error(f"Duplicate entity: {rating.entity}")
            entities_seen.add(rating.entity)

            # Check score range
            if not (-100 <= rating.score <= 100):
                result.add_error(
                    f"Entity {rating.entity}: Score {rating.score} out of range [-100, 100]"
                )

            # Check confidence range
            if not (0 <= rating.confidence <= 100):
                result.add_error(
                    f"Entity {rating.entity}: Confidence {rating.confidence} out of range [0, 100]"
                )

            # Check direction consistency
            expected_direction = classify_direction(rating.score)
            if rating.direction != expected_direction:
                result.add_warning(
                    f"Entity {rating.entity}: Direction {rating.direction.value} "
                    f"does not match expected {expected_direction.value} for score {rating.score}"
                )

            # Check rank
            if rating.rank is not None and rating.rank <= 0:
                result.add_error(f"Entity {rating.entity}: Invalid rank {rating.rank}")

        # Check rank sequential integrity
        ranks = [r.rank for r in ratings if r.rank is not None]
        if ranks:
            sorted_ranks = sorted(ranks)
            expected = list(range(1, len(sorted_ranks) + 1))
            if sorted_ranks != expected:
                result.add_error(
                    f"Rank sequence invalid: {sorted_ranks} vs expected {expected}"
                )

        return result

    def validate_asset_class_ratings(
        self, ratings: List[AssetClassRating]
    ) -> ValidationResult:
        """Validate asset-class ratings."""
        result = ValidationResult()

        if not ratings:
            result.add_warning("No asset-class ratings provided")
            return result

        classes_seen = set()

        for i, rating in enumerate(ratings):
            # Check asset class
            if not rating.asset_class:
                result.add_error(f"Asset-class rating {i}: Missing asset class")

            # Check duplicate
            if rating.asset_class in classes_seen:
                result.add_error(f"Duplicate asset class: {rating.asset_class}")
            classes_seen.add(rating.asset_class)

            # Check score range
            if not (-100 <= rating.score <= 100):
                result.add_error(
                    f"Asset class {rating.name}: Score {rating.score} out of range [-100, 100]"
                )

            # Check confidence range
            if not (0 <= rating.confidence <= 100):
                result.add_error(
                    f"Asset class {rating.name}: Confidence {rating.confidence} out of range [0, 100]"
                )

            # Check direction consistency
            expected_direction = classify_direction(rating.score)
            if rating.direction != expected_direction:
                result.add_warning(
                    f"Asset class {rating.name}: Direction {rating.direction.value} "
                    f"does not match expected {expected_direction.value} for score {rating.score}"
                )

        return result

    def validate_global_output(
        self, output: GlobalIntelligenceOutput
    ) -> ValidationResult:
        """Validate GlobalIntelligenceOutput."""
        result = ValidationResult()

        # Check required fields
        if not output.global_regime:
            result.add_error("Missing global_regime")

        if output.global_regime_confidence < 0 or output.global_regime_confidence > 100:
            result.add_error(
                f"Invalid global_regime_confidence: {output.global_regime_confidence}"
            )

        if not output.global_risk_level:
            result.add_error("Missing global_risk_level")

        # Validate embedded ratings
        if output.currency_rankings:
            currency_result = self.validate_entity_ratings(output.currency_rankings)
            if not currency_result.valid:
                for error in currency_result.errors:
                    result.add_error(f"Currency rankings: {error}")

        if output.asset_class_rankings:
            class_result = self.validate_asset_class_ratings(
                output.asset_class_rankings
            )
            if not class_result.valid:
                for error in class_result.errors:
                    result.add_error(f"Asset-class rankings: {error}")

        return result

    def validate_asset_feed(self, feed: AssetIntelligenceFeed) -> ValidationResult:
        """Validate AssetIntelligenceFeed."""
        result = ValidationResult()

        # Check required fields
        if not feed.symbol:
            result.add_error("Missing symbol")

        if not feed.asset_type:
            result.add_error("Missing asset_type")

        # Check global bias
        if feed.global_bias not in [
            Direction.BULLISH,
            Direction.BEARISH,
            Direction.NEUTRAL,
        ]:
            result.add_error(f"Invalid global_bias: {feed.global_bias}")

        # Check score range
        if not (-100 <= feed.global_score <= 100):
            result.add_error(
                f"global_score {feed.global_score} out of range [-100, 100]"
            )

        # Check confidence range
        if not (0 <= feed.global_confidence <= 100):
            result.add_error(
                f"global_confidence {feed.global_confidence} out of range [0, 100]"
            )

        # Check status
        if feed.status.value not in ["SEMI_FINISHED", "COMPLETE", "PENDING", "ERROR"]:
            result.add_error(f"Invalid status: {feed.status}")

        return result

    def validate_asset_feeds(
        self, feeds: List[AssetIntelligenceFeed]
    ) -> ValidationResult:
        """Validate multiple asset feeds."""
        result = ValidationResult()

        if not feeds:
            result.add_warning("No asset feeds provided")
            return result

        symbols_seen = set()

        for feed in feeds:
            if feed.symbol in symbols_seen:
                result.add_error(f"Duplicate asset feed: {feed.symbol}")
            symbols_seen.add(feed.symbol)

            feed_result = self.validate_asset_feed(feed)
            if not feed_result.valid:
                for error in feed_result.errors:
                    result.add_error(f"{feed.symbol}: {error}")

        return result
