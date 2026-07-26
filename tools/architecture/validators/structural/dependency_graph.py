"""Dependency Graph Validator – Builds and validates the dependency graph."""

import ast
from collections import defaultdict
from pathlib import Path

from tools.architecture.models import ARCResult
from tools.architecture.validators.base import BaseValidator


class DependencyGraphValidator(BaseValidator):
    """Validates the dependency graph for cycles."""

    def __init__(self, root_path: Path):
        super().__init__(root_path)
        self.graph: dict[str, set[str]] = defaultdict(set)

    def get_severity(self) -> str:
        return "critical"

    def validate(self) -> list[ARCResult]:
        results = []

        self._build_graph()
        cycles = self._find_cycles()

        if cycles:
            results.append(
                self.result(
                    False,
                    f"Found {len(cycles)} circular dependencies",
                    details=cycles[:10],
                    severity="critical",
                )
            )
        else:
            results.append(self.result(True, "No circular dependencies found"))

        return results

    def _build_graph(self) -> None:
        """Build the dependency graph."""
        for py_file in self.root.rglob("*.py"):
            if any(e in str(py_file) for e in [".venv", "__pycache__", "tools"]):
                continue

            rel_path = py_file.relative_to(self.root)
            module_name = (
                str(rel_path).replace("\\", ".").replace("/", ".").replace(".py", "")
            )

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if alias.name.startswith("."):
                                continue
                            self.graph[module_name].add(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module and not node.module.startswith("."):
                            self.graph[module_name].add(node.module)
            except Exception:
                pass

    def _find_cycles(self) -> list[list[str]]:
        """Find circular dependencies."""
        cycles = []
        visited = set()

        def dfs(node: str, path: list[str]) -> None:
            if node in path:
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return
            if node in visited:
                return
            visited.add(node)
            for dep in self.graph.get(node, []):
                if dep in self.graph:
                    dfs(dep, path + [node])

        for module in self.graph:
            if module not in visited:
                dfs(module, [])

        return cycles
