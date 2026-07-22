"""
Phase 5: Asset-Class Intelligence - Asset-Class Aggregator

Aggregates entity ratings into asset-class groups.
"""

from typing import Dict, List

from ..contracts import GlobalEntityRating, AssetClass
from .mapper import AssetClassMapper


class AssetClassAggregator:
    """
    Aggregates entity ratings into asset-class groups.
    """

    def aggregate(
        self, ratings: List[GlobalEntityRating]
    ) -> Dict[AssetClass, List[GlobalEntityRating]]:
        """
        Aggregate ratings by asset class.

        Args:
            ratings: List of GlobalEntityRating

        Returns:
            Dict mapping AssetClass to list of ratings
        """
        return AssetClassMapper.map_ratings(ratings)

    def get_fx_ratings(
        self, ratings: List[GlobalEntityRating]
    ) -> List[GlobalEntityRating]:
        """Get ratings for FX asset class."""
        grouped = self.aggregate(ratings)
        return grouped.get(AssetClass.FX, [])

    def get_metals_ratings(
        self, ratings: List[GlobalEntityRating]
    ) -> List[GlobalEntityRating]:
        """Get ratings for Metals asset class."""
        grouped = self.aggregate(ratings)
        return grouped.get(AssetClass.METALS, [])

    def get_equities_ratings(
        self, ratings: List[GlobalEntityRating]
    ) -> List[GlobalEntityRating]:
        """Get ratings for Equities asset class."""
        grouped = self.aggregate(ratings)
        return grouped.get(AssetClass.EQUITIES, [])

    def get_bonds_ratings(
        self, ratings: List[GlobalEntityRating]
    ) -> List[GlobalEntityRating]:
        """Get ratings for Bonds asset class."""
        grouped = self.aggregate(ratings)
        return grouped.get(AssetClass.BONDS, [])

    def get_energy_ratings(
        self, ratings: List[GlobalEntityRating]
    ) -> List[GlobalEntityRating]:
        """Get ratings for Energy asset class."""
        grouped = self.aggregate(ratings)
        return grouped.get(AssetClass.ENERGY, [])

    def get_asset_class_summary(
        self, ratings: List[GlobalEntityRating]
    ) -> Dict[AssetClass, Dict[str, any]]:
        """
        Get a summary of each asset class.

        Returns:
            Dict with asset class name, count, avg score, avg confidence
        """
        grouped = self.aggregate(ratings)
        summary = {}

        for asset_class, items in grouped.items():
            if not items:
                continue

            scores = [r.score for r in items]
            confidences = [r.confidence for r in items]

            summary[asset_class] = {
                "count": len(items),
                "avg_score": sum(scores) / len(scores) if scores else 0,
                "avg_confidence": sum(confidences) / len(confidences)
                if confidences
                else 0,
                "entities": [r.entity for r in items],
                "ratings": items,
            }

        return summary
