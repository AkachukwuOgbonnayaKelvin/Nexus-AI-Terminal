"""Circular Validator – Detects circular dependencies."""

import ast
from pathlib import Path
from typing import List, Dict, Set
from tools.architecture.validators.base import BaseValidator
from tools.architecture.models import ARCResult

class CircularValidator(BaseValidator):
    """Detects circular dependencies."""

    def __init__(self, root_path: Path):
        super().__init__(root_path)
        self.imports: Dict[str, Set[str]] = {}

    def get_severity(self) -> str:
        return "critical"

    def validate(self) -> List[ARCResult]:
        self._build_import_graph()
        cycles = self._find_cycles()
        
        if cycles:
            return [self.result(
                False,
                f"Found {len(cycles)} circular dependencies",
                details=cycles[:10],
                severity="critical"
            )]
        return [self.result(True, "No circular dependencies found")]

    def _build_import_graph(self) -> None:
        for py_file in self.root.rglob("*.py"):
            if any(e in str(py_file) for e in [".venv", "__pycache__", "tools"]):
                continue
            rel_path = py_file.relative_to(self.root)
            module_name = str(rel_path).replace("\\", ".").replace("/", ".").replace(".py", "")
            self.imports[module_name] = set()
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if not alias.name.startswith("."):
                                self.imports[module_name].add(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module and not node.module.startswith("."):
                            self.imports[module_name].add(node.module)
            except Exception:
                pass

    def _find_cycles(self) -> List[List[str]]:
        cycles = []
        visited = set()
        
        def dfs(node: str, path: List[str]) -> None:
            if node in path:
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return
            if node in visited:
                return
            visited.add(node)
            for dep in self.imports.get(node, []):
                if dep in self.imports:
                    dfs(dep, path + [node])
        
        for module in self.imports:
            if module not in visited:
                dfs(module, [])
        
        return cycles
