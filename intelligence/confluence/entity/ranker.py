"""
Phase 4: Global Entity Intelligence - Entity Ranker

Ranks entities by score.
Preserves direction from the rating engine.
"""

from typing import List, Optional
from ..contracts import GlobalEntityRating, EntityType


class EntityRanker:
    """
    Ranks entities by their score.

    Entities can be ranked globally or by type.
    Direction is preserved from the rating engine.
    """

    def rank_entities(
        self, ratings: List[GlobalEntityRating]
    ) -> List[GlobalEntityRating]:
        """
        Rank all entities by score (descending).
        Preserves direction from input.

        Args:
            ratings: List of GlobalEntityRating

        Returns:
            List[GlobalEntityRating]: Sorted ratings with rank assigned
        """
        # Sort by score descending (highest first)
        sorted_ratings = sorted(ratings, key=lambda r: r.score, reverse=True)

        # Assign ranks sequentially
        for i, rating in enumerate(sorted_ratings, start=1):
            rating.rank = i

        return sorted_ratings

    def rank_by_type(
        self, ratings: List[GlobalEntityRating], entity_type: EntityType
    ) -> List[GlobalEntityRating]:
        """
        Rank entities of a specific type by score.
        Preserves direction from input.

        Args:
            ratings: List of GlobalEntityRating
            entity_type: EntityType to filter by

        Returns:
            List[GlobalEntityRating]: Filtered and sorted ratings with rank assigned
        """
        filtered = [r for r in ratings if r.entity_type == entity_type]
        return self.rank_entities(filtered)

    def rank_currencies(
        self, ratings: List[GlobalEntityRating]
    ) -> List[GlobalEntityRating]:
        """Rank only currency entities."""
        return self.rank_by_type(ratings, EntityType.CURRENCY)

    def rank_indices(
        self, ratings: List[GlobalEntityRating]
    ) -> List[GlobalEntityRating]:
        """Rank only index entities."""
        return self.rank_by_type(ratings, EntityType.INDEX)

    def rank_commodities(
        self, ratings: List[GlobalEntityRating]
    ) -> List[GlobalEntityRating]:
        """Rank only commodity entities."""
        return self.rank_by_type(ratings, EntityType.COMMODITY)

    def rank_bonds(self, ratings: List[GlobalEntityRating]) -> List[GlobalEntityRating]:
        """Rank only bond entities."""
        return self.rank_by_type(ratings, EntityType.BOND)

    def get_top_n(
        self, ratings: List[GlobalEntityRating], n: int = 5
    ) -> List[GlobalEntityRating]:
        """Get top N ranked entities."""
        ranked = self.rank_entities(ratings)
        return ranked[:n]

    def get_bottom_n(
        self, ratings: List[GlobalEntityRating], n: int = 5
    ) -> List[GlobalEntityRating]:
        """Get bottom N ranked entities."""
        ranked = self.rank_entities(ratings)
        return ranked[-n:]

    def get_strongest_currency(
        self, ratings: List[GlobalEntityRating]
    ) -> Optional[GlobalEntityRating]:
        """Get the strongest currency."""
        currencies = self.rank_currencies(ratings)
        return currencies[0] if currencies else None

    def get_weakest_currency(
        self, ratings: List[GlobalEntityRating]
    ) -> Optional[GlobalEntityRating]:
        """Get the weakest currency."""
        currencies = self.rank_currencies(ratings)
        return currencies[-1] if currencies else None
