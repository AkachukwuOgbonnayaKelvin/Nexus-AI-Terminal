"""
Phase 6: Distribution API - Asset Feed Builder

Builds semi-finished AssetIntelligenceFeed for Asset Intelligence Engine.
Supports asset-aware resolution for currency pairs and other assets.
"""

import logging
from datetime import datetime

from ..asset_class.mapper import AssetClassMapper
from ..contracts import (
    AssetClass,
    AssetClassRating,
    AssetIntelligenceFeed,
    ConflictLevel,
    CurrencyContext,
    Direction,
    FeedStatus,
)
from ..entity.classifier import EntityClassifier
from ..entity.direction import classify_direction
from .package import ConfluenceIntelligencePackage

logger = logging.getLogger(__name__)


class AssetFeedBuilder:
    """
    Builds semi-finished AssetIntelligenceFeed for each asset.

    This is SEMI-FINISHED context for Asset Intelligence Engine.
    Supports:
    - Currency pairs (AUDUSD → AUD + USD)
    - Individual entities (USD, XAUUSD, US500)
    - Asset-aware resolution
    """

    def build_for_entity(
        self, entity: str, package: ConfluenceIntelligencePackage
    ) -> AssetIntelligenceFeed | None:
        """
        Build a feed for a specific entity.

        Args:
            entity: Entity symbol (e.g., "USD", "AUDUSD", "XAUUSD")
            package: ConfluenceIntelligencePackage

        Returns:
            AssetIntelligenceFeed or None if entity not found
        """
        # Check if this is a currency pair
        if self._is_currency_pair(entity):
            return self._build_currency_pair_feed(entity, package)

        # Otherwise, build for individual entity
        return self._build_entity_feed(entity, package)

    def _build_entity_feed(
        self, entity: str, package: ConfluenceIntelligencePackage
    ) -> AssetIntelligenceFeed | None:
        """Build feed for an individual entity."""
        # Get entity rating
        entity_rating = package.get_entity_rating(entity)
        if not entity_rating:
            logger.warning(f"Entity {entity} not found in package")
            return None

        # Determine asset class
        asset_class = self._get_asset_class(entity)

        # Get asset-class context
        asset_class_rating = self._get_asset_class_rating(asset_class, package)

        # Get supporting/contradicting evidence
        supporting, contradicting = self._get_evidence(entity, package)

        feed = AssetIntelligenceFeed(
            symbol=entity,
            asset_type=self._get_asset_type(entity),
            global_bias=entity_rating.direction,
            global_score=entity_rating.score,
            global_confidence=entity_rating.confidence,
            asset_class=asset_class.value if asset_class else "UNKNOWN",
            asset_class_score=asset_class_rating.score if asset_class_rating else 0.0,
            asset_class_direction=asset_class_rating.direction
            if asset_class_rating
            else Direction.NEUTRAL,
            supporting_evidence=supporting,
            contradicting_evidence=contradicting,
            evidence_count=entity_rating.evidence_count,
            conflict_level=entity_rating.conflict_level,
            global_drivers=package.key_drivers[:5],
            risk_flags=[r.name for r in package.global_risks[:3]],
            global_regime=package.global_regime,
            regime_compatibility=entity_rating.regime_compatibility,
            historical_bias=entity_rating.historical_bias,
            historical_confidence=entity_rating.historical_confidence,
            status=FeedStatus.SEMI_FINISHED,
            source="CONFLUENCE_ENGINE",
            timestamp=datetime.utcnow(),
        )

        return feed

    def _build_currency_pair_feed(
        self, pair: str, package: ConfluenceIntelligencePackage
    ) -> AssetIntelligenceFeed | None:
        """
        Build feed for a currency pair.

        Combines base and quote currency intelligence.
        """
        # Split pair into base and quote
        base_currency = pair[:3]
        quote_currency = pair[3:]

        # Get ratings
        base_rating = package.get_entity_rating(base_currency)
        quote_rating = package.get_entity_rating(quote_currency)

        if not base_rating or not quote_rating:
            logger.warning(f"Missing rating for {base_currency} or {quote_currency}")
            return None

        # Calculate relative score
        # Normalized difference to avoid exaggeration
        raw_differential = base_rating.score - quote_rating.score
        relative_score = raw_differential / 2  # Normalize to -100 to +100 range

        # Clamp to valid range
        relative_score = max(-100, min(100, relative_score))

        # Determine direction
        direction = classify_direction(relative_score)

        # Get asset class context
        asset_class = AssetClass.FX
        asset_class_rating = self._get_asset_class_rating(asset_class, package)

        # Build currency context
        currency_context = CurrencyContext(
            base_currency=base_currency,
            base_strength=base_rating.score,
            quote_currency=quote_currency,
            quote_strength=quote_rating.score,
            spread=raw_differential,
            direction=direction,
        )

        # Get evidence
        supporting = base_rating.supporting_engines + quote_rating.supporting_engines
        contradicting = (
            base_rating.contradicting_engines + quote_rating.contradicting_engines
        )

        # Determine conflict level
        conflict_level = self._combine_conflict_levels(
            base_rating.conflict_level, quote_rating.conflict_level
        )

        feed = AssetIntelligenceFeed(
            symbol=pair,
            asset_type="CURRENCY_PAIR",
            global_bias=direction,
            global_score=relative_score,
            global_confidence=(base_rating.confidence + quote_rating.confidence) / 2,
            asset_class="FX",
            asset_class_score=asset_class_rating.score if asset_class_rating else 0.0,
            asset_class_direction=asset_class_rating.direction
            if asset_class_rating
            else Direction.NEUTRAL,
            currency_context=currency_context,
            supporting_evidence=list(set(supporting[:5])),
            contradicting_evidence=list(set(contradicting[:3])),
            evidence_count=base_rating.evidence_count + quote_rating.evidence_count,
            conflict_level=conflict_level,
            global_drivers=package.key_drivers[:5],
            risk_flags=[r.name for r in package.global_risks[:3]],
            global_regime=package.global_regime,
            regime_compatibility=(
                base_rating.regime_compatibility + quote_rating.regime_compatibility
            )
            / 2,
            historical_bias=base_rating.historical_bias,
            historical_confidence=(
                base_rating.historical_confidence + quote_rating.historical_confidence
            )
            / 2,
            status=FeedStatus.SEMI_FINISHED,
            source="CONFLUENCE_ENGINE",
            timestamp=datetime.utcnow(),
        )

        return feed

    def build_for_entities(
        self, entities: list[str], package: ConfluenceIntelligencePackage
    ) -> list[AssetIntelligenceFeed]:
        """
        Build feeds for multiple entities.

        Args:
            entities: List of entity symbols
            package: ConfluenceIntelligencePackage

        Returns:
            List[AssetIntelligenceFeed]
        """
        feeds = []
        for entity in entities:
            feed = self.build_for_entity(entity, package)
            if feed:
                feeds.append(feed)
        return feeds

    def build_for_all_entities(
        self, package: ConfluenceIntelligencePackage
    ) -> list[AssetIntelligenceFeed]:
        """
        Build feeds for all entities in the package.

        Args:
            package: ConfluenceIntelligencePackage

        Returns:
            List[AssetIntelligenceFeed]
        """
        feeds = []

        # Build for all individual entities
        for rating in package.entity_ratings:
            feed = self._build_entity_feed(rating.entity, package)
            if feed:
                feeds.append(feed)

        # Also build for major currency pairs
        currency_pairs = self._generate_currency_pairs(package)
        for pair in currency_pairs:
            feed = self.build_for_entity(pair, package)
            if feed:
                feeds.append(feed)

        return feeds

    def _generate_currency_pairs(
        self, package: ConfluenceIntelligencePackage
    ) -> list[str]:
        """Generate major currency pairs from available currencies."""
        currencies = [r.entity for r in package.currency_ratings]

        # Major pairs to generate
        major_pairs = [
            "AUDUSD",
            "EURUSD",
            "GBPUSD",
            "USDJPY",
            "USDCHF",
            "USDCAD",
            "EURGBP",
            "EURJPY",
            "GBPJPY",
            "AUDJPY",
            "NZDUSD",
        ]

        # Filter to pairs where both currencies exist in package
        available_pairs = []
        for pair in major_pairs:
            base = pair[:3]
            quote = pair[3:]
            if base in currencies and quote in currencies:
                available_pairs.append(pair)

        return available_pairs

    def _is_currency_pair(self, entity: str) -> bool:
        """Check if entity is a currency pair."""
        return (
            len(entity) == 6 and entity.isupper() and all(c.isalpha() for c in entity)
        )

    def _get_asset_class(self, entity: str) -> AssetClass | None:
        """Get asset class for an entity."""
        return AssetClassMapper.map_entity(entity)

    def _get_asset_class_rating(
        self, asset_class: AssetClass | None, package: ConfluenceIntelligencePackage
    ) -> AssetClassRating | None:
        """Get asset-class rating for an asset class."""
        if not asset_class:
            return None
        for rating in package.asset_class_ratings:
            if rating.asset_class == asset_class:
                return rating
        return None

    def _get_asset_type(self, entity: str) -> str:
        """Get asset type for an entity."""
        if self._is_currency_pair(entity):
            return "CURRENCY_PAIR"

        entity_type = EntityClassifier.classify(entity)
        if entity_type.value == "CURRENCY":
            return "CURRENCY"
        elif entity_type.value == "INDEX":
            return "INDEX"
        elif entity_type.value == "COMMODITY":
            return "COMMODITY"
        elif entity_type.value == "BOND":
            return "BOND"
        else:
            return "ASSET"

    def _get_evidence(
        self, entity: str, package: ConfluenceIntelligencePackage
    ) -> tuple[list[str], list[str]]:
        """Get supporting and contradicting evidence for an entity."""
        rating = package.get_entity_rating(entity)
        if not rating:
            return [], []

        supporting = rating.supporting_engines[:5]
        contradicting = rating.contradicting_engines[:3]

        return supporting, contradicting

    def _combine_conflict_levels(
        self, level1: ConflictLevel, level2: ConflictLevel
    ) -> ConflictLevel:
        """Combine two conflict levels (take the higher one)."""
        levels = [
            ConflictLevel.NONE,
            ConflictLevel.LOW,
            ConflictLevel.MEDIUM,
            ConflictLevel.HIGH,
        ]
        idx1 = levels.index(level1)
        idx2 = levels.index(level2)
        return levels[max(idx1, idx2)]
