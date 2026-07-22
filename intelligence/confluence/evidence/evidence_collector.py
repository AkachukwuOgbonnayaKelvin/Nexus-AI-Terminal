"""
Confluence Engine - Evidence Collector

Collects and organizes normalized signals into evidence groups.
"""

import logging
from typing import Dict, List, Optional, Any
from collections import defaultdict

from .evidence_model import EvidenceGroup
from ..schemas import NormalizedSignal

logger = logging.getLogger(__name__)


class EvidenceCollector:
    """
    Collects normalized signals and organizes them by entity and signal type.
    """

    def __init__(self):
        self.groups: Dict[str, Dict[str, EvidenceGroup]] = defaultdict(
            lambda: defaultdict(EvidenceGroup)
        )
        self._signals: List[NormalizedSignal] = []

    def add_signal(self, signal: NormalizedSignal) -> None:
        """
        Add a normalized signal to the collector.
        """
        self._signals.append(signal)

        # Get or create group
        # group_key = (entity, signal_type)  # Unused
        if signal.entity not in self.groups:
            self.groups[signal.entity] = {}

        if signal.signal_type.value not in self.groups[signal.entity]:
            self.groups[signal.entity][signal.signal_type.value] = EvidenceGroup(
                entity=signal.entity, signal_type=signal.signal_type.value
            )

        # Add evidence to group
        group = self.groups[signal.entity][signal.signal_type.value]
        group.add_evidence(signal)

        logger.debug(
            f"Added signal: {signal.engine_id} -> {signal.entity} ({signal.signal_type.value})"
        )

    def add_signals(self, signals: List[NormalizedSignal]) -> None:
        """
        Add multiple signals.
        """
        for signal in signals:
            self.add_signal(signal)

    def get_group(self, entity: str, signal_type: str) -> Optional[EvidenceGroup]:
        """
        Get an evidence group by entity and signal type.
        """
        if entity in self.groups and signal_type in self.groups[entity]:
            return self.groups[entity][signal_type]
        return None

    def get_groups(self) -> Dict[str, Dict[str, EvidenceGroup]]:
        """
        Get all evidence groups.
        """
        return self.groups

    def get_entities(self) -> List[str]:
        """
        Get all entities with evidence.
        """
        return list(self.groups.keys())

    def get_signal_types_for_entity(self, entity: str) -> List[str]:
        """
        Get all signal types for an entity.
        """
        if entity in self.groups:
            return list(self.groups[entity].keys())
        return []

    def get_all_evidence(self) -> List[EvidenceGroup]:
        """
        Get all evidence groups as a flat list.
        """
        all_groups = []
        for entity_groups in self.groups.values():
            for group in entity_groups.values():
                all_groups.append(group)
        return all_groups

    def get_evidence_for_entity(self, entity: str) -> List[EvidenceGroup]:
        """
        Get all evidence groups for an entity.
        """
        if entity in self.groups:
            return list(self.groups[entity].values())
        return []

    def get_consensus(self, entity: str, signal_type: str) -> Optional[Dict[str, Any]]:
        """
        Get consensus for a specific entity and signal type.
        """
        group = self.get_group(entity, signal_type)
        if not group:
            return None

        return {
            "entity": entity,
            "signal_type": signal_type,
            "score": group.get_consensus_score(),
            "direction": group.get_consensus_direction(),
            "confidence": group.get_confidence(),
            "conflict_level": group.get_conflict_level().value,
            "supporting_engines": group.get_supporting_engines(),
            "contradicting_engines": group.get_contradicting_engines(),
            "drivers": group.get_drivers(),
            "evidence_count": len(group.evidence),
        }

    def clear(self) -> None:
        """
        Clear all collected signals and groups.
        """
        self._signals = []
        self.groups = defaultdict(lambda: defaultdict(EvidenceGroup))

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about collected evidence.
        """
        total_signals = len(self._signals)
        total_groups = sum(len(entity_groups) for entity_groups in self.groups.values())
        total_entities = len(self.groups)

        return {
            "total_signals": total_signals,
            "total_groups": total_groups,
            "total_entities": total_entities,
            "entities": list(self.groups.keys()),
        }
