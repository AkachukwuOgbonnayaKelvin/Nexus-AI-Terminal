"""Import Validator – Checks for broken imports."""

import ast
from pathlib import Path
from typing import List, Dict
from tools.architecture.validators.base import BaseValidator
from tools.architecture.models import ARCResult


class ImportValidator(BaseValidator):
    """Validates all imports resolve correctly."""

    def __init__(self, root_path: Path):
        super().__init__(root_path)
        self.modules: Dict[str, Path] = {}
        self.broken_imports: List[Dict] = []

    def get_severity(self) -> str:
        return "critical"

    def validate(self) -> List[ARCResult]:
        self._discover_modules()
        self._check_imports()

        if self.broken_imports:
            return [
                self.result(
                    False,
                    f"Found {len(self.broken_imports)} broken imports",
                    details=self.broken_imports[:20],
                    severity="critical",
                )
            ]
        return [self.result(True, "All imports resolve correctly")]

    def _discover_modules(self) -> None:
        excluded = ["venv", "__pycache__", ".git", "tools", "reports"]
        for py_file in self.root.rglob("*.py"):
            if any(e in str(py_file) for e in excluded):
                continue
            rel_path = py_file.relative_to(self.root)
            module_name = (
                str(rel_path).replace("\\", ".").replace("/", ".").replace(".py", "")
            )
            self.modules[module_name] = py_file

    def _check_imports(self) -> None:
        for module_name, file_path in self.modules.items():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if (
                                alias.name not in self.modules
                                and not alias.name.startswith(".")
                            ):
                                self.broken_imports.append(
                                    {
                                        "module": module_name,
                                        "import": alias.name,
                                        "file": str(file_path),
                                    }
                                )
                    elif isinstance(node, ast.ImportFrom):
                        if (
                            node.module
                            and node.module not in self.modules
                            and not node.module.startswith(".")
                        ):
                            self.broken_imports.append(
                                {
                                    "module": module_name,
                                    "import": node.module,
                                    "file": str(file_path),
                                }
                            )
            except Exception:
                pass
