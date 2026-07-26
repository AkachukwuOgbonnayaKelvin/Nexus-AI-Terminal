"""
Phase 5: Asset-Class Intelligence - Asset-Class Rating Engine

Calculates ratings for asset classes from entity ratings.
"""

from statistics import mean

from ..contracts import AssetClass, AssetClassRating, Direction, GlobalEntityRating
from ..entity.direction import classify_direction
from .mapper import AssetClassMapper


class AssetClassRatingEngine:
    """
    Calculates ratings for asset classes.

    For each asset class, calculates:
    - Score (-100 to +100)
    - Direction (BULLISH, BEARISH, NEUTRAL)
    - Confidence (0-100)
    - Supporting entities
    """

    def rate_asset_class(
        self, asset_class: AssetClass, ratings: list[GlobalEntityRating]
    ) -> AssetClassRating:
        """
        Rate a single asset class from its entity ratings.

        Args:
            asset_class: The asset class to rate
            ratings: List of GlobalEntityRating for entities in this class

        Returns:
            AssetClassRating: The asset-class rating
        """
        if not ratings:
            # Return neutral for empty asset class
            return AssetClassRating(
                asset_class=asset_class,
                name=AssetClassMapper.get_asset_class_name(asset_class),
                score=0.0,
                direction=Direction.NEUTRAL,
                confidence=0.0,
            )

        # Calculate aggregate score (weighted by confidence)
        total_weight = sum(r.confidence for r in ratings)
        if total_weight == 0:
            avg_score = mean(r.score for r in ratings)
        else:
            weighted_sum = sum(r.score * r.confidence for r in ratings)
            avg_score = weighted_sum / total_weight

        # Calculate average confidence
        avg_confidence = mean(r.confidence for r in ratings)

        # Determine direction using centralized classifier
        direction = classify_direction(avg_score)

        # Get supporting entities
        supporting_entities = [r.entity for r in ratings]

        # Extract drivers from entity ratings
        drivers = self._extract_drivers(ratings)

        # Extract risks from entity ratings
        risks = self._extract_risks(ratings)

        # Calculate regime compatibility
        regime_compat = self._calculate_regime_compatibility(ratings)

        return AssetClassRating(
            asset_class=asset_class,
            name=AssetClassMapper.get_asset_class_name(asset_class),
            score=avg_score,
            direction=direction,
            confidence=avg_confidence,
            supporting_entities=supporting_entities,
            supporting_ratings=ratings,
            drivers=drivers,
            risks=risks,
            regime_compatibility=regime_compat,
        )

    def rate_asset_classes(
        self, grouped: dict[AssetClass, list[GlobalEntityRating]]
    ) -> list[AssetClassRating]:
        """
        Rate multiple asset classes from grouped ratings.

        Args:
            grouped: Dict mapping AssetClass to list of ratings

        Returns:
            List[AssetClassRating]: Ratings for all asset classes
        """
        ratings = []

        for asset_class, entity_ratings in grouped.items():
            rating = self.rate_asset_class(asset_class, entity_ratings)
            ratings.append(rating)

        return ratings

    def _extract_drivers(self, ratings: list[GlobalEntityRating]) -> list[str]:
        """Extract drivers from entity ratings."""
        driver_map: dict[str, float] = {}

        for r in ratings:
            for driver in r.drivers:
                if driver.name not in driver_map:
                    driver_map[driver.name] = 0.0
                driver_map[driver.name] += driver.strength

        # Sort by strength and return top 5
        sorted_drivers = sorted(driver_map.items(), key=lambda x: x[1], reverse=True)
        return [d[0] for d in sorted_drivers[:5]]

    def _extract_risks(self, ratings: list[GlobalEntityRating]) -> list[str]:
        """Extract risks from entity ratings."""
        risk_map: dict[str, float] = {}

        for r in ratings:
            for risk in r.risks:
                if risk.name not in risk_map:
                    risk_map[risk.name] = 0.0
                risk_map[risk.name] += risk.severity

        # Sort by severity and return top 5
        sorted_risks = sorted(risk_map.items(), key=lambda x: x[1], reverse=True)
        return [r[0] for r in sorted_risks[:5]]

    def _calculate_regime_compatibility(
        self, ratings: list[GlobalEntityRating]
    ) -> float:
        """Calculate regime compatibility from entity ratings."""
        if not ratings:
            return 0.5

        scores = [r.score for r in ratings]
        avg_score = mean(scores)
        std_dev = (sum((s - avg_score) ** 2 for s in scores) / len(scores)) ** 0.5

        max_std = 50.0
        return 1.0 - min(1.0, std_dev / max_std)
