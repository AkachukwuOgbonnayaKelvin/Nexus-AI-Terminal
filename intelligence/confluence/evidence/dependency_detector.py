"""
Confluence Engine - Dependency Detector

Detects dependencies between evidence signals from different engines.
"""

import logging
from collections import defaultdict
from typing import Any

from ..schemas import NormalizedSignal

logger = logging.getLogger(__name__)


class DependencyDetector:
    """
    Detects if multiple engines are measuring the same underlying phenomenon.
    """

    def __init__(self):
        self._dependency_map: dict[str, set[str]] = defaultdict(set)
        self._register_default_dependencies()

    def _register_default_dependencies(self) -> None:
        """
        Register default dependencies between engines.
        """
        # Macro influences Central Bank and Flows
        self.register_dependency("GLB-003", "GLB-005")
        self.register_dependency("GLB-003", "GLB-007")

        # Central Bank influences Flows and Asset Impact
        self.register_dependency("GLB-005", "GLB-007")
        self.register_dependency("GLB-005", "GLB-002")

        # Geopolitical influences Sentiment and Flows
        self.register_dependency("GLB-006", "GLB-008")
        self.register_dependency("GLB-006", "GLB-007")

        # Market Regime influences Asset Impact and Memory
        self.register_dependency("GLB-001", "GLB-002")
        self.register_dependency("GLB-001", "GLB-009")

        # Events influence Market Regime and Macro
        self.register_dependency("GLB-004", "GLB-001")
        self.register_dependency("GLB-004", "GLB-003")

    def register_dependency(self, engine1: str, engine2: str) -> None:
        """
        Register a dependency between two engines.
        """
        self._dependency_map[engine1].add(engine2)
        self._dependency_map[engine2].add(engine1)

    def register_dependencies(self, dependencies: list[tuple]) -> None:
        """
        Register multiple dependencies.
        """
        for eng1, eng2 in dependencies:
            self.register_dependency(eng1, eng2)

    def are_dependent(self, engine1: str, engine2: str) -> bool:
        """
        Check if two engines are dependent.
        """
        return engine2 in self._dependency_map.get(engine1, set())

    def get_dependencies(self, engine: str) -> list[str]:
        """
        Get all engines dependent on the given engine.
        """
        return list(self._dependency_map.get(engine, set()))

    def detect_dependencies(self, signals: list[NormalizedSignal]) -> dict[str, Any]:
        """
        Detect dependencies among signals.
        """
        # Group by entity and signal type
        groups = defaultdict(list)
        for signal in signals:
            key = (signal.entity, signal.signal_type.value)
            groups[key].append(signal)

        dependencies = []

        for (entity, signal_type), group_signals in groups.items():
            engines = [s.engine_id for s in group_signals]
            unique_engines = set(engines)

            if len(unique_engines) > 1:
                for i, eng1 in enumerate(engines):
                    for eng2 in engines[i + 1 :]:
                        if self.are_dependent(eng1, eng2):
                            dependencies.append(
                                {
                                    "engine1": eng1,
                                    "engine2": eng2,
                                    "entity": entity,
                                    "signal_type": signal_type,
                                    "dependency_type": "REGISTERED",
                                }
                            )

        # Calculate independence factor per engine
        independence_factors = self.get_evidence_independence(signals)

        return {
            "dependencies": dependencies,
            "dependency_count": len(dependencies),
            "total_signals": len(signals),
            "independence_factors": independence_factors,
            "average_independence": sum(independence_factors.values())
            / len(independence_factors)
            if independence_factors
            else 1.0,
        }

    def get_independence_factor(self, engine: str, other_engines: list[str]) -> float:
        """
        Calculate independence factor for an engine against others.
        """
        if not other_engines:
            return 1.0

        dependent_count = sum(1 for e in other_engines if self.are_dependent(engine, e))
        total = len(other_engines)

        return 1.0 - (dependent_count / total) if total > 0 else 1.0

    def get_evidence_independence(
        self, signals: list[NormalizedSignal]
    ) -> dict[str, float]:
        """
        Get independence factor for each signal.
        """
        independence = {}

        for i, signal in enumerate(signals):
            other_signals = [s for j, s in enumerate(signals) if j != i]
            other_engines = [s.engine_id for s in other_signals]
            independence[signal.engine_id] = self.get_independence_factor(
                signal.engine_id, other_engines
            )

        return independence
