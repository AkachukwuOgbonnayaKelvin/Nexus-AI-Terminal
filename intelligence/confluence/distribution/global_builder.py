"""
Phase 6: Distribution API - Global Output Builder

Builds the final/polished GlobalIntelligenceOutput for the Global Intelligence Hub.
"""

import logging
from typing import List, Dict, Any
from datetime import datetime
from copy import deepcopy

from ..contracts import GlobalEntityRating, AssetClassRating, GlobalIntelligenceOutput
from .package import ConfluenceIntelligencePackage

logger = logging.getLogger(__name__)


class GlobalOutputBuilder:
    """
    Builds final/polished GlobalIntelligenceOutput.

    This is the FINAL/PUBLISHED output for the Global Intelligence Hub.

    Key principle: Every ranking collection owns its own rank sequence.
    Ranks are resequenced fresh for each domain.
    """

    def build(self, package: ConfluenceIntelligencePackage) -> GlobalIntelligenceOutput:
        """
        Build GlobalIntelligenceOutput from ConfluenceIntelligencePackage.

        Args:
            package: ConfluenceIntelligencePackage

        Returns:
            GlobalIntelligenceOutput: Final/polished output
        """
        logger.info("Building Global Intelligence Output...")

        # Get domain-specific rankings with fresh resequencing
        currency_rankings = self._build_currency_rankings(package)
        entity_rankings = self._build_entity_rankings(package)
        asset_class_rankings = self._build_asset_class_rankings(package)

        # Generate executive summary
        executive_summary = self._generate_executive_summary(package)

        # Build AI context
        ai_context = self._build_ai_context(package)

        output = GlobalIntelligenceOutput(
            global_regime=package.global_regime,
            global_regime_confidence=package.global_regime_confidence,
            global_risk_level=package.global_risk_level,
            global_risk_score=package.global_risk_score,
            currency_rankings=currency_rankings,
            entity_rankings=entity_rankings,
            asset_class_rankings=asset_class_rankings,
            global_drivers=package.key_drivers,
            global_risks=package.global_risks,
            dominant_themes=package.global_themes,
            top_opportunities=package.top_opportunities,
            executive_summary=executive_summary,
            ai_context=ai_context,
            timestamp=datetime.utcnow(),
        )

        logger.info(f"Global output built: {output}")
        return output

    def _resequence_ranks(self, items: List) -> List:
        """
        Resequence ranks for a specific domain.

        This forces fresh sequential ranks (1, 2, 3, ...)
        regardless of any existing rank values.

        Args:
            items: List of items with a 'score' attribute

        Returns:
            List: Same items with fresh ranks assigned
        """
        # Sort by score descending
        sorted_items = sorted(items, key=lambda x: x.score, reverse=True)

        # Assign new sequential ranks
        for i, item in enumerate(sorted_items, start=1):
            item.rank = i

        return sorted_items

    def _build_currency_rankings(
        self, package: ConfluenceIntelligencePackage
    ) -> List[GlobalEntityRating]:
        """
        Build currency rankings with fresh resequencing.

        Takes currency entities from the package and assigns
        fresh ranks 1..N based on score.
        """
        currencies = package.currency_ratings
        if not currencies:
            return []

        # Create deep copies to avoid modifying original package data
        currency_copies = [deepcopy(c) for c in currencies]

        # Resequence ranks
        ranked = self._resequence_ranks(currency_copies)

        logger.info(
            f"Currency rankings: {[(r.entity, r.rank, r.score) for r in ranked]}"
        )
        return ranked

    def _build_entity_rankings(
        self, package: ConfluenceIntelligencePackage
    ) -> List[GlobalEntityRating]:
        """
        Build global entity rankings with fresh resequencing.

        Takes all entities from the package and assigns
        fresh ranks 1..N based on score.
        """
        entities = package.entity_ratings
        if not entities:
            return []

        # Create deep copies to avoid modifying original package data
        entity_copies = [deepcopy(e) for e in entities]

        # Resequence ranks
        ranked = self._resequence_ranks(entity_copies)

        logger.info(f"Entity rankings: {len(ranked)} entities ranked")
        return ranked

    def _build_asset_class_rankings(
        self, package: ConfluenceIntelligencePackage
    ) -> List[AssetClassRating]:
        """
        Build asset-class rankings with fresh resequencing.

        Takes asset-class ratings from the package and assigns
        fresh ranks 1..N based on score.
        """
        classes = package.asset_class_ratings
        if not classes:
            return []

        # Create deep copies to avoid modifying original package data
        class_copies = [deepcopy(c) for c in classes]

        # Resequence ranks
        ranked = self._resequence_ranks(class_copies)

        logger.info(
            f"Asset-class rankings: {[(r.name, r.rank, r.score) for r in ranked]}"
        )
        return ranked

    def _generate_executive_summary(
        self, package: ConfluenceIntelligencePackage
    ) -> str:
        """Generate executive summary."""
        parts = []

        # Regime
        parts.append(f"The current global environment is {package.global_regime}.")

        # Strongest currency
        strongest = package.strongest_currency
        if strongest:
            parts.append(
                f"{strongest.entity} is the strongest currency at {strongest.score:+.1f}."
            )

        # Weakest currency
        weakest = package.weakest_currency
        if weakest:
            parts.append(
                f"{weakest.entity} is the weakest currency at {weakest.score:+.1f}."
            )

        # Strongest asset class
        strongest_class = package.strongest_asset_class
        if strongest_class:
            parts.append(
                f"{strongest_class.name} is the strongest asset class at {strongest_class.score:+.1f}."
            )

        # Weakest asset class
        weakest_class = package.weakest_asset_class
        if weakest_class:
            parts.append(
                f"{weakest_class.name} is the weakest asset class at {weakest_class.score:+.1f}."
            )

        # Themes
        if package.global_themes:
            theme_names = [t.name for t in package.global_themes[:3]]
            parts.append(f"Key themes include: {', '.join(theme_names)}.")

        return " ".join(parts)

    def _build_ai_context(
        self, package: ConfluenceIntelligencePackage
    ) -> Dict[str, Any]:
        """Build AI context for the Executive AI summary."""
        context = {
            "regime": package.global_regime,
            "regime_confidence": package.global_regime_confidence,
            "risk_level": package.global_risk_level,
            "drivers": package.key_drivers[:5],
            "themes": [t.name for t in package.global_themes[:3]],
            "strongest_entity": {
                "name": package.strongest_currency.entity
                if package.strongest_currency
                else None,
                "score": package.strongest_currency.score
                if package.strongest_currency
                else None,
            }
            if package.strongest_currency
            else None,
            "weakest_entity": {
                "name": package.weakest_currency.entity
                if package.weakest_currency
                else None,
                "score": package.weakest_currency.score
                if package.weakest_currency
                else None,
            }
            if package.weakest_currency
            else None,
            "strongest_asset_class": {
                "name": package.strongest_asset_class.name
                if package.strongest_asset_class
                else None,
                "score": package.strongest_asset_class.score
                if package.strongest_asset_class
                else None,
            }
            if package.strongest_asset_class
            else None,
            "weakest_asset_class": {
                "name": package.weakest_asset_class.name
                if package.weakest_asset_class
                else None,
                "score": package.weakest_asset_class.score
                if package.weakest_asset_class
                else None,
            }
            if package.weakest_asset_class
            else None,
            "top_opportunities": package.top_opportunities[:3],
        }
        return context
