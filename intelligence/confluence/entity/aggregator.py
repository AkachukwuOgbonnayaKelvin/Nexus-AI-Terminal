"""
Phase 4: Global Entity Intelligence - Entity Aggregator

Aggregates harmonized results by entity.
"""

from typing import Dict, List
from collections import defaultdict

from ..contracts import HarmonizedResult, EntityType
from .classifier import EntityClassifier


class EntityAggregator:
    """
    Aggregates harmonized results by entity.

    Groups all HarmonizedResult objects by their entity,
    so each entity has a complete set of intelligence.
    """

    def aggregate(
        self, results: List[HarmonizedResult]
    ) -> Dict[str, List[HarmonizedResult]]:
        """
        Aggregate harmonized results by entity.

        Args:
            results: List of HarmonizedResult objects

        Returns:
            Dict mapping entity name to list of results
        """
        grouped: Dict[str, List[HarmonizedResult]] = defaultdict(list)

        for result in results:
            grouped[result.entity].append(result)

        return dict(grouped)

    def aggregate_by_type(
        self, results: List[HarmonizedResult]
    ) -> Dict[EntityType, List[HarmonizedResult]]:
        """
        Aggregate harmonized results by entity type.

        Args:
            results: List of HarmonizedResult objects

        Returns:
            Dict mapping EntityType to list of results
        """
        grouped: Dict[EntityType, List[HarmonizedResult]] = defaultdict(list)

        for result in results:
            entity_type = EntityClassifier.classify(result.entity)
            grouped[entity_type].append(result)

        return dict(grouped)

    def get_currency_results(
        self, results: List[HarmonizedResult]
    ) -> List[HarmonizedResult]:
        """Get only currency results."""
        return [r for r in results if EntityClassifier.is_currency(r.entity)]

    def get_index_results(
        self, results: List[HarmonizedResult]
    ) -> List[HarmonizedResult]:
        """Get only index results."""
        return [r for r in results if EntityClassifier.is_index(r.entity)]

    def get_commodity_results(
        self, results: List[HarmonizedResult]
    ) -> List[HarmonizedResult]:
        """Get only commodity results."""
        return [r for r in results if EntityClassifier.is_commodity(r.entity)]

    def get_bond_results(
        self, results: List[HarmonizedResult]
    ) -> List[HarmonizedResult]:
        """Get only bond results."""
        return [r for r in results if EntityClassifier.is_bond(r.entity)]

    def get_entity_types(
        self, results: List[HarmonizedResult]
    ) -> Dict[str, EntityType]:
        """
        Get entity types for all results.

        Returns:
            Dict mapping entity name to EntityType
        """
        return {r.entity: EntityClassifier.classify(r.entity) for r in results}
