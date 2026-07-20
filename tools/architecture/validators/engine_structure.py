"""Engine Structure Validator – Checks engine folder structure."""

from pathlib import Path
from typing import List
from tools.architecture.validators.base import BaseValidator
from tools.architecture.models import ARCResult


class EngineStructureValidator(BaseValidator):
    """Validates engine folder structure."""

    REQUIRED_FOLDERS = [
        "acquisition",
        "providers",
        "warehouse",
        "publication",
        "runtime",
        "configuration",
        "tests",
        "gateway",
    ]

    ENGINE_PATTERNS = ["*_engine", "*_events_engine", "*_warehouse"]

    def get_severity(self) -> str:
        return "high"

    def validate(self) -> List[ARCResult]:
        results = []
        engines = self._find_engines()

        if not engines:
            results.append(
                self.result(False, "No engines found in project", severity="critical")
            )
            return results

        for engine_path in engines:
            engine_name = engine_path.name
            missing = [
                f for f in self.REQUIRED_FOLDERS if not (engine_path / f).exists()
            ]

            if missing:
                results.append(
                    self.result(
                        False,
                        f"{engine_name} missing required folders: {', '.join(missing)}",
                        details={"engine": engine_name, "missing": missing},
                        severity="high",
                    )
                )
            else:
                results.append(
                    self.result(True, f"{engine_name} has complete structure")
                )

        return results

    def _find_engines(self) -> List[Path]:
        engines = []
        for pattern in self.ENGINE_PATTERNS:
            for path in self.root.glob(f"**/{pattern}"):
                if path.is_dir() and not any(
                    p in str(path) for p in [".venv", "__pycache__", "tools"]
                ):
                    engines.append(path)
        return engines
