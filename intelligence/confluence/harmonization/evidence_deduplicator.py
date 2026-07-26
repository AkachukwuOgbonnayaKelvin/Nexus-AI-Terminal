"""
Confluence Engine - Evidence Deduplicator

Removes duplicate evidence from dependent engines.
"""

import logging

from ..evidence.evidence_model import EvidenceGroup
from ..schemas import NormalizedSignal

logger = logging.getLogger(__name__)


class EvidenceDeduplicator:
    """
    Removes duplicate evidence from dependent engines.
    """

    def __init__(self):
        self._dependency_map: dict[str, set[str]] = {}
        self._transitive_dependencies: dict[str, set[str]] = {}

    def set_dependencies(self, dependencies: dict[str, set[str]]) -> None:
        """
        Set the dependency map and compute transitive dependencies.
        """
        self._dependency_map = dependencies
        self._transitive_dependencies = self._compute_transitive_dependencies()

    def _compute_transitive_dependencies(self) -> dict[str, set[str]]:
        """
        Compute transitive dependencies (follow the chain).

        Example:
            GLB-003 depends on GLB-001
            GLB-006 depends on GLB-003

            Transitive: GLB-006 depends on GLB-001 and GLB-003
        """
        transitive = {}

        for engine, deps in self._dependency_map.items():
            transitive[engine] = set(deps)

            # Follow the chain
            to_process = list(deps)
            processed = set()

            while to_process:
                current = to_process.pop()
                if current in processed:
                    continue
                processed.add(current)

                if current in self._dependency_map:
                    for dep in self._dependency_map[current]:
                        if dep not in transitive[engine]:
                            transitive[engine].add(dep)
                            to_process.append(dep)

        return transitive

    def deduplicate(self, signals: list[NormalizedSignal]) -> list[NormalizedSignal]:
        """
        Remove duplicate signals from dependent engines.
        """
        if not signals:
            return []

        # Group signals by entity and signal type
        groups = {}
        for signal in signals:
            key = (signal.entity, signal.signal_type.value)
            if key not in groups:
                groups[key] = []
            groups[key].append(signal)

        # Process each group
        result = []
        for key, group_signals in groups.items():
            deduped = self._deduplicate_group(group_signals)
            result.extend(deduped)

        return result

    def _deduplicate_group(
        self, signals: list[NormalizedSignal]
    ) -> list[NormalizedSignal]:
        """
        Deduplicate signals within a group.
        """
        if len(signals) <= 1:
            return signals

        # Sort by reliability (higher = keep)
        sorted_signals = sorted(signals, key=lambda s: s.reliability, reverse=True)

        kept = []
        kept_engines = set()

        for signal in sorted_signals:
            engine_id = signal.engine_id

            # Check if this engine is already represented
            if engine_id in kept_engines:
                continue

            # Check if this engine depends on any kept engine
            is_dependent = False
            if engine_id in self._transitive_dependencies:
                # Check if any dependency is already kept
                deps = self._transitive_dependencies[engine_id]
                if deps.intersection(kept_engines):
                    is_dependent = True

            # Also check if any kept engine depends on this one
            if not is_dependent:
                for kept_id in kept_engines:
                    if kept_id in self._transitive_dependencies:
                        if engine_id in self._transitive_dependencies[kept_id]:
                            is_dependent = True
                            break

            if not is_dependent:
                kept.append(signal)
                kept_engines.add(engine_id)

        return kept

    def _are_dependent(self, engine1: str, engine2: str) -> bool:
        """
        Check if two engines are dependent (directly or transitively).
        """
        if not self._transitive_dependencies:
            return False

        # Check if engine1 depends on engine2
        if engine1 in self._transitive_dependencies:
            if engine2 in self._transitive_dependencies[engine1]:
                return True

        # Check if engine2 depends on engine1
        if engine2 in self._transitive_dependencies:
            if engine1 in self._transitive_dependencies[engine2]:
                return True

        # Check direct dependencies
        if engine1 in self._dependency_map:
            if engine2 in self._dependency_map[engine1]:
                return True

        if engine2 in self._dependency_map:
            if engine1 in self._dependency_map[engine2]:
                return True

        return False

    def get_independent_evidence(
        self, groups: list[EvidenceGroup]
    ) -> list[EvidenceGroup]:
        """
        Get independent evidence from groups.
        """
        independent_groups = []

        for group in groups:
            # Get all signals from this group
            all_signals = [e.signal for e in group.evidence]

            # Deduplicate
            independent_signals = self.deduplicate(all_signals)

            if independent_signals:
                # Create a new group with independent signals
                new_group = EvidenceGroup(
                    entity=group.entity, signal_type=group.signal_type
                )
                for signal in independent_signals:
                    new_group.add_evidence(signal)
                independent_groups.append(new_group)

        return independent_groups
