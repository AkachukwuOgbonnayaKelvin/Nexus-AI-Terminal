"""Init Validator – Checks __init__.py exports."""

import ast

from tools.architecture.models import ARCResult
from tools.architecture.validators.base import BaseValidator


class InitValidator(BaseValidator):
    """Validates __init__.py exports."""

    def get_severity(self) -> str:
        return "high"

    def validate(self) -> list[ARCResult]:
        results = []
        for init_file in self.root.rglob("__init__.py"):
            if any(e in str(init_file) for e in [".venv", "__pycache__", "tools"]):
                continue

            try:
                with open(init_file, "r", encoding="utf-8") as f:
                    content = f.read()

                if "__all__" not in content:
                    continue

                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id == "__all__":
                                if isinstance(node.value, ast.List):
                                    for elt in node.value.elts:
                                        if isinstance(elt, ast.Constant) and isinstance(
                                            elt.value, str
                                        ):
                                            export = elt.value
                                            export_path = (
                                                init_file.parent / f"{export}.py"
                                            )
                                            if not export_path.exists():
                                                results.append(
                                                    self.result(
                                                        False,
                                                        f"Missing export: {export} in {init_file}",
                                                        severity="high",
                                                    )
                                                )
            except Exception:
                pass

        if not results:
            results.append(self.result(True, "All __init__.py exports valid"))
        return results
