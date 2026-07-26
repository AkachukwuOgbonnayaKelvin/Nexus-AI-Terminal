"""
Platform Scanner - Discovers and analyzes the entire Nexus AI Terminal platform
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class EngineMetadata:
    id: str
    name: str
    path: Path
    status: str  # Production, Development, Testing, Prototype
    stage: str  # production, staging, testing, development
    engine_yaml: dict | None = None
    contract_yaml: dict | None = None
    architecture_yaml: dict | None = None
    readme_exists: bool = False
    doc_folder_exists: bool = False
    test_folder_exists: bool = False
    runtime_folder_exists: bool = False

    @property
    def has_runtime(self) -> bool:
        return (self.path / "runtime").exists()

    @property
    def has_tests(self) -> bool:
        return (self.path / "tests").exists()

    @property
    def has_warehouse(self) -> bool:
        return (self.path / "warehouse").exists()

    @property
    def has_publication(self) -> bool:
        return (self.path / "publication").exists()

    @property
    def has_acquisition(self) -> bool:
        return (self.path / "acquisition").exists()

    def get_engine_yaml(self) -> dict:
        if self.engine_yaml:
            return self.engine_yaml
        path = self.path / "engine.yaml"
        if path.exists():
            with open(path) as f:
                self.engine_yaml = yaml.safe_load(f)
            return self.engine_yaml
        return {}

    def get_contract_yaml(self) -> dict:
        if self.contract_yaml:
            return self.contract_yaml
        path = self.path / "contract.yaml"
        if path.exists():
            with open(path) as f:
                self.contract_yaml = yaml.safe_load(f)
            return self.contract_yaml
        return {}


class PlatformScanner:
    """Scans the Nexus AI Terminal platform"""

    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.engines: list[EngineMetadata] = []
        self.ndip_domains: list[str] = []
        self.dar_registrations: list[str] = []
        self.warehouse_domains: list[str] = []

    def scan(self) -> dict[str, Any]:
        """Scan the entire platform"""
        result = {
            "root_path": str(self.root_path),
            "engines": [],
            "ndip_domains": [],
            "dar_registrations": [],
            "warehouse_domains": [],
            "summary": {},
        }

        # Discover engines
        self._discover_engines()
        result["engines"] = [self._engine_to_dict(e) for e in self.engines]
        result["summary"]["total_engines"] = len(self.engines)

        # Discover NDIP domains
        self._discover_ndip()
        result["ndip_domains"] = self.ndip_domains
        result["summary"]["ndip_domains"] = len(self.ndip_domains)

        # Discover DAR registrations
        self._discover_dar()
        result["dar_registrations"] = self.dar_registrations
        result["summary"]["dar_registrations"] = len(self.dar_registrations)

        # Discover warehouses
        self._discover_warehouses()
        result["warehouse_domains"] = self.warehouse_domains
        result["summary"]["warehouse_domains"] = len(self.warehouse_domains)

        # Overall summary
        result["summary"]["total_modules"] = self._count_modules()
        result["summary"]["total_packages"] = self._count_packages()

        return result

    def _discover_engines(self) -> None:
        """Discover all engines in the project"""
        # Engine patterns - look for folders with engine.yaml
        engine_patterns = [
            "*_engine",
            "engine_*",
            "*-engine",
            "engine",
            "*_intelligence",
            "*_processor",
            "*_analyzer",
        ]

        for pattern in engine_patterns:
            for path in self.root_path.glob(pattern):
                if path.is_dir():
                    engine_yaml = path / "engine.yaml"
                    if engine_yaml.exists():
                        try:
                            with open(engine_yaml) as f:
                                data = yaml.safe_load(f)

                            engine = EngineMetadata(
                                id=data.get("id", path.name.upper().replace("-", "_")),
                                name=data.get("name", path.name),
                                path=path,
                                status=data.get("status", "Development"),
                                stage=data.get("stage", "development"),
                                engine_yaml=data,
                            )

                            # Check for contract
                            contract_path = path / "contract.yaml"
                            if contract_path.exists():
                                with open(contract_path) as f:
                                    engine.contract_yaml = yaml.safe_load(f)

                            # Check for architecture.yaml
                            arch_path = path / "architecture.yaml"
                            if arch_path.exists():
                                with open(arch_path) as f:
                                    engine.architecture_yaml = yaml.safe_load(f)

                            # Check for README
                            engine.readme_exists = (path / "README.md").exists()
                            engine.doc_folder_exists = (path / "docs").exists()
                            engine.test_folder_exists = (path / "tests").exists()
                            engine.runtime_folder_exists = (path / "runtime").exists()

                            self.engines.append(engine)
                        except Exception as e:
                            print(f"⚠️ Error scanning {path}: {e}")

        # Also check for engines in specific directories
        engine_dirs = ["engines", "domain_*", "core", "services", "intelligence"]

        for pattern in engine_dirs:
            for dir_path in self.root_path.glob(pattern):
                if dir_path.is_dir():
                    for sub_path in dir_path.iterdir():
                        if sub_path.is_dir() and (sub_path / "engine.yaml").exists():
                            try:
                                with open(sub_path / "engine.yaml") as f:
                                    data = yaml.safe_load(f)

                                engine = EngineMetadata(
                                    id=data.get(
                                        "id", sub_path.name.upper().replace("-", "_")
                                    ),
                                    name=data.get("name", sub_path.name),
                                    path=sub_path,
                                    status=data.get("status", "Development"),
                                    stage=data.get("stage", "development"),
                                    engine_yaml=data,
                                )
                                self.engines.append(engine)
                            except Exception as e:
                                print(f"⚠️ Error scanning {sub_path}: {e}")

    def _discover_ndip(self) -> None:
        """Discover NDIP domains"""
        ndip_path = self.root_path / "ndip"
        if ndip_path.exists():
            for domain in ndip_path.iterdir():
                if domain.is_dir():
                    self.ndip_domains.append(domain.name)

    def _discover_dar(self) -> None:
        """Discover DAR registrations"""
        dar_path = self.root_path / "runtime"
        if dar_path.exists():
            for file in dar_path.glob("*.py"):
                if "registry" in file.name or "register" in file.name:
                    self.dar_registrations.append(file.name)

    def _discover_warehouses(self) -> None:
        """Discover warehouse domains"""
        for engine in self.engines:
            warehouse_path = engine.path / "warehouse"
            if warehouse_path.exists():
                for domain in warehouse_path.iterdir():
                    if domain.is_dir():
                        domain_name = f"{engine.id}.{domain.name}"
                        if domain_name not in self.warehouse_domains:
                            self.warehouse_domains.append(domain_name)

    def _count_modules(self) -> int:
        """Count Python modules"""
        count = 0
        for py_file in self.root_path.rglob("*.py"):
            if "test" not in str(py_file) and "acp" not in str(py_file):
                count += 1
        return count

    def _count_packages(self) -> int:
        """Count Python packages (directories with __init__.py)"""
        count = 0
        for init_file in self.root_path.rglob("__init__.py"):
            if "test" not in str(init_file) and "acp" not in str(init_file):
                count += 1
        return count

    def _engine_to_dict(self, engine: EngineMetadata) -> dict:
        """Convert engine to dictionary"""
        return {
            "id": engine.id,
            "name": engine.name,
            "path": str(engine.path),
            "status": engine.status,
            "stage": engine.stage,
            "has_engine_yaml": engine.engine_yaml is not None,
            "has_contract_yaml": engine.contract_yaml is not None,
            "has_architecture_yaml": engine.architecture_yaml is not None,
            "has_readme": engine.readme_exists,
            "has_docs": engine.doc_folder_exists,
            "has_tests": engine.test_folder_exists,
            "has_runtime": engine.runtime_folder_exists,
            "has_acquisition": engine.has_acquisition,
            "has_warehouse": engine.has_warehouse,
            "has_publication": engine.has_publication,
        }
