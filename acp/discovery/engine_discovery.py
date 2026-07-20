# -*- coding: utf-8 -*-
"""
Engine Discovery - Finds all engines in the project
Distinguishes between: Registered Engines, Probable Engines, Libraries, Tooling
"""

from pathlib import Path
from typing import List, Dict, Any
import yaml


class EngineDiscovery:
    """Discovers engine implementations in the project"""

    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.engine_patterns = [
            "*_engine",
            "engine_*",
            "*-engine",
            "*_intelligence",
            "*_processor",
            "*_analyzer",
            "*_service",
            "*_collector",
            "*_provider",
        ]

        self.exclude_patterns = [
            "acp",
            "tools",
            "tests",
            "venv",
            "__pycache__",
            ".git",
            "docs",
            "examples",
            "scripts",
            "migrations",
            "bin",
        ]

    def discover(self) -> Dict[str, List[Dict[str, Any]]]:
        """Discover all engines and classify them"""
        result = {
            "registered_engines": [],  # Have engine.yaml
            "probable_engines": [],  # Look like engines but no engine.yaml
            "libraries": [],  # Shared code, not engines
            "tooling": [],  # Development tools
            "unknown": [],  # Unclassified
        }

        # Method 1: Find all engine.yaml files (registered engines)
        for yaml_file in self.root_path.rglob("engine.yaml"):
            engine_dir = yaml_file.parent
            if self._should_exclude(engine_dir):
                continue
            try:
                with open(yaml_file) as f:
                    data = yaml.safe_load(f)

                result["registered_engines"].append(
                    {
                        "id": data.get("id", engine_dir.name.upper()),
                        "name": data.get("name", engine_dir.name),
                        "path": str(engine_dir),
                        "engine_yaml": data,
                        "type": "registered",
                        "status": data.get("status", "Development"),
                        "stage": data.get("stage", "development"),
                    }
                )
            except Exception as e:
                print(f"Warning: Could not read {yaml_file}: {e}")

        # Method 2: Find probable engines (look like engines but no engine.yaml)
        for pattern in self.engine_patterns:
            for path in self.root_path.glob(pattern):
                if path.is_dir() and self._should_exclude(path):
                    continue

                # Check if already discovered as registered
                if any(e["path"] == str(path) for e in result["registered_engines"]):
                    continue

                # Check if it looks like an engine
                engine_signals = 0

                # Look for engine-like components
                if (path / "warehouse").exists():
                    engine_signals += 1
                if (path / "acquisition").exists():
                    engine_signals += 1
                if (path / "publication").exists():
                    engine_signals += 1
                if (path / "providers").exists():
                    engine_signals += 1
                if (path / "parser").exists():
                    engine_signals += 1

                # Look for engine-like imports
                py_files = list(path.rglob("*.py"))
                engine_imports = 0
                for py_file in py_files[:5]:  # Check first 5 files
                    try:
                        with open(py_file) as f:
                            content = f.read()
                            if (
                                "engine" in content.lower()
                                or "provider" in content.lower()
                            ):
                                engine_imports += 1
                    except:
                        pass

                if engine_signals >= 2 or engine_imports >= 2:
                    result["probable_engines"].append(
                        {
                            "id": path.name.upper()
                            .replace("-", "_")
                            .replace("_ENGINE", ""),
                            "name": path.name,
                            "path": str(path),
                            "type": "probable",
                            "engine_signals": engine_signals,
                            "import_signals": engine_imports,
                            "recommendation": "Create engine.yaml to register this engine",
                            "reason": "Directory contains engine-like components but no engine.yaml",
                        }
                    )

        # Method 3: Check for libraries (shared code)
        for path in self.root_path.iterdir():
            if path.is_dir() and self._should_exclude(path):
                continue

            # Check if already classified
            if any(e["path"] == str(path) for e in result["registered_engines"]):
                continue
            if any(e["path"] == str(path) for e in result["probable_engines"]):
                continue

            # Check if it's a library
            if (path / "__init__.py").exists() and not (path / "engine.yaml").exists():
                result["libraries"].append(
                    {
                        "name": path.name,
                        "path": str(path),
                        "type": "library",
                        "note": "Shared library - not an engine",
                    }
                )

        # Method 4: Check for tooling
        for path in self.root_path.iterdir():
            if path.is_dir() and path.name in ["acp", "tools", "scripts", "bin"]:
                result["tooling"].append(
                    {
                        "name": path.name,
                        "path": str(path),
                        "type": "tooling",
                        "note": "Development tool - not an engine",
                    }
                )

        return result

    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded"""
        path_str = str(path)
        for pattern in self.exclude_patterns:
            if pattern in path_str.lower():
                return True
        return False
