"""
Confluence Engine - Engine Registry

Maps engine IDs to their reliability scores and normalizer functions.
"""

from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class EngineEntry:
    """Entry for a GLB engine in the registry"""

    engine_id: str
    name: str
    domain: str
    reliability: float = 0.80
    normalizer: Callable | None = None
    is_available: bool = True


class EngineRegistry:
    """Registry of all GLB engines"""

    def __init__(self):
        self._engines: dict[str, EngineEntry] = {}
        self._register_defaults()

    def _register_defaults(self):
        """Register all GLB engines with default reliability scores"""
        self.register(
            engine_id="GLB-001",
            name="Market Regime Engine",
            domain="REGIME",
            reliability=0.85,
        )
        self.register(
            engine_id="GLB-002",
            name="Asset Impact Engine",
            domain="ASSET",
            reliability=0.80,
        )
        self.register(
            engine_id="GLB-003",
            name="Macro Intelligence Engine",
            domain="MACRO",
            reliability=0.90,
        )
        self.register(
            engine_id="GLB-004",
            name="Economic Events Engine",
            domain="EVENTS",
            reliability=0.75,
        )
        self.register(
            engine_id="GLB-005",
            name="Central Bank Intelligence Engine",
            domain="CENTRAL_BANK",
            reliability=0.88,
        )
        self.register(
            engine_id="GLB-006",
            name="Geopolitical Risk Engine",
            domain="GEOPOLITICAL",
            reliability=0.82,
        )
        self.register(
            engine_id="GLB-007",
            name="Capital Flows & Liquidity Engine",
            domain="FLOWS",
            reliability=0.78,
        )
        self.register(
            engine_id="GLB-008",
            name="Sentiment & Positioning Engine",
            domain="SENTIMENT",
            reliability=0.70,
        )
        self.register(
            engine_id="GLB-009",
            name="Market Memory Engine",
            domain="MEMORY",
            reliability=0.75,
        )

    def register(
        self,
        engine_id: str,
        name: str,
        domain: str,
        reliability: float = 0.80,
        normalizer: Callable | None = None,
    ):
        """Register an engine"""
        self._engines[engine_id] = EngineEntry(
            engine_id=engine_id,
            name=name,
            domain=domain,
            reliability=reliability,
            normalizer=normalizer,
        )

    def get(self, engine_id: str) -> EngineEntry | None:
        """Get an engine entry"""
        return self._engines.get(engine_id)

    def get_all(self) -> dict[str, EngineEntry]:
        """Get all engine entries"""
        return self._engines.copy()

    def get_engine_ids(self) -> list[str]:
        """Get all engine IDs"""
        return list(self._engines.keys())

    def set_normalizer(self, engine_id: str, normalizer: Callable):
        """Set a normalizer for an engine"""
        if engine_id in self._engines:
            self._engines[engine_id].normalizer = normalizer

    def set_availability(self, engine_id: str, is_available: bool):
        """Set availability of an engine"""
        if engine_id in self._engines:
            self._engines[engine_id].is_available = is_available

    def get_available_engines(self) -> dict[str, EngineEntry]:
        """Get all available engines"""
        return {
            eid: entry for eid, entry in self._engines.items() if entry.is_available
        }

    def get_reliability(self, engine_id: str) -> float:
        """Get reliability score for an engine"""
        entry = self.get(engine_id)
        return entry.reliability if entry else 0.50
