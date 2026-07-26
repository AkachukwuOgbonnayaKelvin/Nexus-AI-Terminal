"""
Dependency Analyzer - Analyzes engine dependencies
"""

import ast
from pathlib import Path
from typing import Any

import yaml


class DependencyAnalyzer:
    """Analyzes engine dependencies"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.imports = []

    def analyze(self, engine_path: Path, engine_data: dict) -> dict[str, Any]:
        """Analyze engine dependencies"""
        result = {
            "score": 100,
            "status": "Healthy",
            "dependencies": [],
            "internal_dependencies": [],
            "external_dependencies": [],
            "circular_dependencies": [],
            "issues": [],
            "warnings": [],
        }

        # Get dependencies from engine.yaml
        if engine_data.get("dependencies"):
            result["dependencies"] = engine_data["dependencies"]

        # Scan Python files for imports
        for py_file in engine_path.rglob("*.py"):
            if "__init__" not in py_file.name:
                self._scan_imports(py_file, result)

        # Check for internal vs external dependencies
        engine_id = engine_data.get("id", engine_path.name)
        for dep in result["dependencies"]:
            dep_path = self.project_root / dep.lower().replace("-", "_")
            if dep_path.exists():
                result["internal_dependencies"].append(dep)
            else:
                # Check if it's an engine directory
                for pattern in ["*_engine", "engine_*", "*-engine"]:
                    for found_path in self.project_root.glob(pattern):
                        if (
                            found_path.name.lower()
                            .replace("_engine", "")
                            .replace("-engine", "")
                            == dep.lower()
                        ):
                            result["internal_dependencies"].append(dep)
                            break
                if dep not in result["internal_dependencies"]:
                    result["external_dependencies"].append(dep)

        # Check for circular dependencies
        self._check_circular_dependencies(engine_id, result)

        # Score calculation
        if result["circular_dependencies"]:
            result["score"] = 60
            result["status"] = "Warning"
            result["issues"].append(
                {
                    "type": "CIRCULAR_DEPENDENCY",
                    "severity": "High",
                    "message": f"Circular dependencies detected: {', '.join(result['circular_dependencies'])}",
                    "fix": "Break the circular dependency chain",
                }
            )
        elif not result["dependencies"]:
            result["score"] = 100
            result["status"] = "Healthy"
            result["warnings"].append(
                {
                    "type": "NO_DEPENDENCIES",
                    "severity": "Info",
                    "message": "No external dependencies declared",
                    "fix": "If this engine depends on others, declare them in engine.yaml",
                }
            )

        return result

    def _scan_imports(self, file_path: Path, result: dict) -> None:
        """Scan Python file for imports"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module = alias.name.split(".")[0]
                        if module not in result[
                            "dependencies"
                        ] and not module.startswith("_"):
                            result["dependencies"].append(module)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module = node.module.split(".")[0]
                        if module not in result[
                            "dependencies"
                        ] and not module.startswith("_"):
                            result["dependencies"].append(module)
        except Exception:
            pass

    def _check_circular_dependencies(self, engine_id: str, result: dict) -> None:
        """Check for circular dependencies"""
        # Simple check: see if any dependency depends back on this engine
        for dep in result["dependencies"]:
            dep_path = self.project_root / dep.lower().replace("-", "_")
            if dep_path.exists():
                dep_engine_yaml = dep_path / "engine.yaml"
                if dep_engine_yaml.exists():
                    try:
                        with open(dep_engine_yaml) as f:
                            dep_data = yaml.safe_load(f)
                        dep_deps = dep_data.get("dependencies", [])
                        if engine_id.lower() in [d.lower() for d in dep_deps]:
                            result["circular_dependencies"].append(
                                f"{engine_id} -> {dep} -> {engine_id}"
                            )
                    except Exception:
                        pass
