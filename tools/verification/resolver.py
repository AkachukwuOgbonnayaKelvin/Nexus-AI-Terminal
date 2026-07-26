"""
Engine Identity Resolver - Central engine identity management
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class EngineIdentity:
    """Complete engine identity information"""

    id: str
    name: str
    slug: str
    path: Path
    domain: str
    version: str
    stage: str
    engine_yaml: dict[str, Any]
    contract_yaml: dict[str, Any]


class EngineIdentityResolver:
    """Resolves engine IDs to full engine identities"""

    def __init__(self, project_root: Path | None = None):
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self._cache = {}

        # ID mapping: short ID -> engine directory name
        self.id_map = {
            # Existing engines
            "CENT-001": "central_bank_engine",
            "CENTRAL_BANK_ENGINE": "central_bank_engine",
            "central_bank_engine": "central_bank_engine",
            "ECO-001": "economic_events_engine",
            "ECONOMIC_EVENTS_ENGINE": "economic_events_engine",
            "economic_events_engine": "economic_events_engine",
            "NEWS-001": "financial_news_engine",
            "FINANCIAL_NEWS_ENGINE": "financial_news_engine",
            "financial_news_engine": "financial_news_engine",
            "INS-001": "institutional_positioning_engine",
            "INSTITUTIONAL_POSITIONING_ENGINE": "institutional_positioning_engine",
            "institutional_positioning_engine": "institutional_positioning_engine",
            "MAC-002": "macroeconomic_events_engine",
            "MACROECONOMIC_EVENTS_ENGINE": "macroeconomic_events_engine",
            "macroeconomic_events_engine": "macroeconomic_events_engine",
            # MAC-001 Macroeconomic Statistics Engine
            "MAC-001": "macroeconomic_statistics_engine",
            "macroeconomic_statistics_engine": "macroeconomic_statistics_engine",
            # MKT-001 Market Price Engine
            "MKT-001": "market_price_engine",
            "market_price_engine": "market_price_engine",
            # ECO-002 Corporate Earnings Engine
            "ECO-002": "corporate_earnings_engine",
            "corporate_earnings_engine": "corporate_earnings_engine",
            "TEST-001": "TEST-001",
            "test_engine": "TEST-001",
        }

        # Reverse mapping: directory -> short ID
        self.reverse_map = {v: k for k, v in self.id_map.items() if len(k) <= 10}

    def resolve(self, engine_id: str) -> EngineIdentity | None:
        """Resolve an engine ID to a full identity"""
        print(f"[RESOLVER] Resolving: {engine_id}")

        # Check cache
        if engine_id in self._cache:
            print(f"[RESOLVER] Cache hit: {engine_id}")
            return self._cache[engine_id]

        # Get the engine directory name
        dir_name = self.id_map.get(engine_id, engine_id)
        print(f"[RESOLVER] Directory name: {dir_name}")

        # Try to find the engine path
        engine_path = self._find_engine_path(dir_name)

        if not engine_path:
            print(f"[RESOLVER] Failed to find engine: {engine_id}")
            return None

        print(f"[RESOLVER] Engine path: {engine_path}")

        # Load engine.yaml
        engine_yaml_path = engine_path / "engine.yaml"
        if not engine_yaml_path.exists():
            print(f"[RESOLVER] engine.yaml not found at: {engine_yaml_path}")
            return None

        try:
            with open(engine_yaml_path) as f:
                engine_data = yaml.safe_load(f)
        except Exception as e:
            print(f"[RESOLVER] Error loading engine.yaml: {e}")
            return None

        # Extract identity
        if "engine" in engine_data and isinstance(engine_data["engine"], dict):
            data = engine_data["engine"]
        else:
            data = engine_data

        # Load contract.yaml
        contract_yaml_path = engine_path / "contract.yaml"
        contract_data = {}
        if contract_yaml_path.exists():
            try:
                with open(contract_yaml_path) as f:
                    contract_data = yaml.safe_load(f)
            except Exception:
                pass

        # Build identity
        identity = EngineIdentity(
            id=data.get("id", engine_id),
            name=data.get("name", engine_path.name.replace("_", " ").title()),
            slug=engine_path.name,
            path=engine_path,
            domain=data.get("domain", data.get("slug", "unknown")),
            version=data.get("version", "0.0.0"),
            stage=data.get("stage", "development"),
            engine_yaml=data,
            contract_yaml=contract_data,
        )

        print(f"[RESOLVER] Resolved: {identity.id} ({identity.name})")

        # Cache it
        self._cache[engine_id] = identity
        self._cache[identity.id] = identity
        self._cache[identity.slug] = identity

        return identity

    def _find_engine_path(self, dir_name: str) -> Path | None:
        """Find the engine directory path"""
        # Try direct path
        direct_path = self.project_root / dir_name
        if direct_path.exists() and direct_path.is_dir():
            return direct_path

        # Try with _engine suffix
        if not dir_name.endswith("_engine"):
            engine_path = self.project_root / f"{dir_name}_engine"
            if engine_path.exists() and engine_path.is_dir():
                return engine_path

        # Try in engines directory
        engines_dir = self.project_root / "engines"
        if engines_dir.exists():
            for subdir in engines_dir.iterdir():
                if subdir.is_dir():
                    if subdir.name.lower() == dir_name.lower():
                        return subdir
                    if subdir.name.lower().replace("_engine", "") == dir_name.lower():
                        return subdir

        return None

    def list_all_engines(self) -> list:
        """List all registered engine IDs"""
        engines = []

        # Scan for engine.yaml files
        for engine_dir in self.project_root.glob("*_engine"):
            if (engine_dir / "engine.yaml").exists():
                dir_name = engine_dir.name
                engine_id = self.reverse_map.get(dir_name, dir_name.upper())
                if engine_id:
                    engines.append(engine_id)

        # Also check engines directory
        engines_dir = self.project_root / "engines"
        if engines_dir.exists():
            for subdir in engines_dir.iterdir():
                if subdir.is_dir() and (subdir / "engine.yaml").exists():
                    dir_name = subdir.name
                    engine_id = self.reverse_map.get(dir_name, dir_name.upper())
                    if engine_id:
                        engines.append(engine_id)

        return sorted(set(engines))


# Singleton instance
_resolver = None


def get_resolver() -> EngineIdentityResolver:
    """Get the singleton resolver instance"""
    global _resolver
    if _resolver is None:
        _resolver = EngineIdentityResolver()
    return _resolver
