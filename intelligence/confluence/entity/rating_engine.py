"""
Phase 4: Global Entity Intelligence - Entity Rating Engine

Calculates entity ratings from harmonized results.
"""

from statistics import mean

from ..contracts import (
    ConflictLevel,
    Direction,
    EntityDriver,
    EntityRisk,
    GlobalEntityRating,
    HarmonizedResult,
)
from .classifier import EntityClassifier
from .direction import classify_direction


class EntityRatingEngine:
    """
    Calculates entity ratings from harmonized results.

    For each entity, calculates:
    - Score (-100 to +100)
    - Direction (BULLISH, BEARISH, NEUTRAL) - using centralized classifier
    - Confidence (0-100)
    - Drivers
    - Risks
    """

    def __init__(self):
        self._driver_extractor = None
        self._risk_detector = None

    def rate_entity(self, results: list[HarmonizedResult]) -> GlobalEntityRating:
        """
        Rate a single entity from its harmonized results.

        Args:
            results: List of HarmonizedResult for the same entity

        Returns:
            GlobalEntityRating: The entity rating
        """
        if not results:
            raise ValueError("No results provided for entity rating")

        # Get entity name from first result
        entity = results[0].entity
        entity_type = EntityClassifier.classify(entity)

        # Calculate aggregate score
        scores = [r.final_score for r in results]
        avg_score = mean(scores)

        # Calculate weighted confidence
        weighted_confidence = self._calculate_weighted_confidence(results)

        # Determine direction using centralized classifier
        direction = classify_direction(avg_score)

        # Determine conflict level
        conflict_level = self._determine_conflict_level(results)

        # Collect supporting engines
        supporting = []
        contradicting = []
        for r in results:
            supporting.extend(r.supporting_engines)
            contradicting.extend(r.contradicting_engines)

        # Calculate evidence count
        evidence_count = sum(r.evidence_count for r in results)

        # Extract drivers
        drivers = self._extract_drivers(results)

        # Detect risks
        risks = self._detect_risks(results)

        # Calculate regime compatibility
        regime_compat = self._calculate_regime_compatibility(results)

        return GlobalEntityRating(
            entity=entity,
            entity_type=entity_type,
            score=avg_score,
            direction=direction,
            confidence=weighted_confidence,
            drivers=drivers,
            risks=risks,
            supporting_engines=list(set(supporting)),
            contradicting_engines=list(set(contradicting)),
            evidence_count=evidence_count,
            conflict_level=conflict_level,
            regime_compatibility=regime_compat,
        )

    def rate_entities(
        self, grouped_results: dict[str, list[HarmonizedResult]]
    ) -> list[GlobalEntityRating]:
        """
        Rate multiple entities from grouped results.

        Args:
            grouped_results: Dict mapping entity to list of HarmonizedResult

        Returns:
            List[GlobalEntityRating]: Ratings for all entities
        """
        ratings = []
        for entity, results in grouped_results.items():
            try:
                rating = self.rate_entity(results)
                ratings.append(rating)
            except ValueError:
                continue

        return ratings

    def _calculate_weighted_confidence(self, results: list[HarmonizedResult]) -> float:
        """Calculate weighted confidence from results."""
        if not results:
            return 0.0

        # Weight by evidence count and agreement
        total_weight = 0.0
        weighted_sum = 0.0

        for r in results:
            weight = r.evidence_count * r.agreement_ratio
            weighted_sum += r.confidence * weight
            total_weight += weight

        if total_weight == 0:
            return mean(r.confidence for r in results)

        return weighted_sum / total_weight

    def _determine_conflict_level(
        self, results: list[HarmonizedResult]
    ) -> ConflictLevel:
        """Determine overall conflict level."""
        if not results:
            return ConflictLevel.NONE

        # Get the highest conflict level
        levels = [r.conflict_level for r in results]
        if ConflictLevel.HIGH in levels:
            return ConflictLevel.HIGH
        if ConflictLevel.MEDIUM in levels:
            return ConflictLevel.MEDIUM
        if ConflictLevel.LOW in levels:
            return ConflictLevel.LOW
        return ConflictLevel.NONE

    def _extract_drivers(self, results: list[HarmonizedResult]) -> list[EntityDriver]:
        """Extract drivers from results."""
        driver_map: dict[str, list[float]] = {}

        for r in results:
            for driver in r.drivers:
                if driver not in driver_map:
                    driver_map[driver] = []
                driver_map[driver].append(r.final_score)

        drivers = []
        for name, scores in driver_map.items():
            avg_strength = mean(scores) if scores else 0.0
            direction = Direction.BULLISH if avg_strength > 0 else Direction.BEARISH

            drivers.append(
                EntityDriver(
                    name=name,
                    strength=abs(avg_strength),
                    direction=direction,
                    confidence=min(100, abs(avg_strength)),
                )
            )

        # Sort by strength and return top 5
        drivers.sort(key=lambda d: d.strength, reverse=True)
        return drivers[:5]

    def _detect_risks(self, results: list[HarmonizedResult]) -> list[EntityRisk]:
        """Detect risks from results."""
        risk_map: dict[str, list[float]] = {}

        for r in results:
            for risk in r.risks:
                if risk not in risk_map:
                    risk_map[risk] = []
                risk_map[risk].append(r.confidence)

        risks = []
        for name, confidences in risk_map.items():
            avg_confidence = mean(confidences) if confidences else 0.0
            severity = 100 - avg_confidence  # Lower confidence = higher risk

            risks.append(
                EntityRisk(name=name, severity=severity, confidence=avg_confidence)
            )

        # Sort by severity and return top 5
        risks.sort(key=lambda r: r.severity, reverse=True)
        return risks[:5]

    def _calculate_regime_compatibility(self, results: list[HarmonizedResult]) -> float:
        """Calculate regime compatibility."""
        if not results:
            return 0.5

        # Check if results are consistent
        scores = [r.final_score for r in results]
        if not scores:
            return 0.5

        # Higher consistency = better regime compatibility
        avg_score = mean(scores)
        std_dev = (sum((s - avg_score) ** 2 for s in scores) / len(scores)) ** 0.5

        # Normalize: lower std_dev = higher compatibility
        max_std = 50.0  # Maximum expected standard deviation
        compatibility = 1.0 - min(1.0, std_dev / max_std)

        return compatibility
