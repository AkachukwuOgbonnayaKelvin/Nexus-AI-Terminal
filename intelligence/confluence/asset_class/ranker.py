"""
Phase 5: Asset-Class Intelligence - Asset-Class Ranker

Ranks asset classes by score.
"""

from ..contracts import AssetClassRating


class AssetClassRanker:
    """
    Ranks asset classes by their score.
    Preserves direction from the rating engine.
    """

    def rank_asset_classes(
        self, ratings: list[AssetClassRating]
    ) -> list[AssetClassRating]:
        """
        Rank all asset classes by score (descending).

        Args:
            ratings: List of AssetClassRating

        Returns:
            List[AssetClassRating]: Sorted ratings with rank assigned
        """
        sorted_ratings = sorted(ratings, key=lambda r: r.score, reverse=True)

        for i, rating in enumerate(sorted_ratings, start=1):
            rating.rank = i

        return sorted_ratings

    def get_top_n(
        self, ratings: list[AssetClassRating], n: int = 5
    ) -> list[AssetClassRating]:
        """Get top N ranked asset classes."""
        ranked = self.rank_asset_classes(ratings)
        return ranked[:n]

    def get_bottom_n(
        self, ratings: list[AssetClassRating], n: int = 5
    ) -> list[AssetClassRating]:
        """Get bottom N ranked asset classes."""
        ranked = self.rank_asset_classes(ratings)
        return ranked[-n:]

    def get_strongest(self, ratings: list[AssetClassRating]) -> AssetClassRating | None:
        """Get the strongest asset class."""
        if not ratings:
            return None
        return self.rank_asset_classes(ratings)[0]

    def get_weakest(self, ratings: list[AssetClassRating]) -> AssetClassRating | None:
        """Get the weakest asset class."""
        if not ratings:
            return None
        return self.rank_asset_classes(ratings)[-1]
