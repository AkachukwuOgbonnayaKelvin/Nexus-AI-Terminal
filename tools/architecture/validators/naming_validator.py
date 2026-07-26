"""Naming Validator – Checks naming conventions."""

import re
from pathlib import Path

from tools.architecture.models import ARCResult
from tools.architecture.validators.base import BaseValidator


class NamingValidator(BaseValidator):
    """Validates naming conventions."""

    def get_severity(self) -> str:
        return "medium"

    def validate(self) -> list[ARCResult]:
        results = []
        engine_dirs = self._find_engines()

        for engine in engine_dirs:
            engine_name = engine.name
            if not re.match(r"^[a-z_]+$", engine_name):
                results.append(
                    self.result(
                        False,
                        f"Engine name '{engine_name}' should use snake_case",
                        severity="medium",
                    )
                )

        if not results:
            results.append(self.result(True, "All naming conventions followed"))
        return results

    def _find_engines(self) -> list[Path]:
        engines = []
        for path in self.root.glob("**/*_engine"):
            if path.is_dir() and not any(
                p in str(path) for p in [".venv", "__pycache__", "tools"]
            ):
                engines.append(path)
        return engines
