"""Warehouse Validator – Checks warehouse structure."""

from pathlib import Path

from tools.architecture.models import ARCResult
from tools.architecture.validators.base import BaseValidator


class WarehouseValidator(BaseValidator):
    """Validates warehouse structure."""

    def get_severity(self) -> str:
        return "high"

    def validate(self) -> list[ARCResult]:
        results = []
        engines = self._find_engines()

        for engine in engines:
            warehouse = engine / "warehouse"
            if not warehouse.exists():
                results.append(
                    self.result(
                        False,
                        f"{engine.name} missing warehouse/ folder",
                        severity="high",
                    )
                )
            else:
                repo_file = warehouse / "repository.py"
                if not repo_file.exists():
                    results.append(
                        self.result(
                            False,
                            f"{engine.name} missing warehouse/repository.py",
                            severity="high",
                        )
                    )

        if not results:
            results.append(self.result(True, "All engines have warehouse layer"))
        return results

    def _find_engines(self) -> list[Path]:
        engines = []
        for path in self.root.glob("**/*_engine"):
            if path.is_dir() and not any(
                p in str(path) for p in [".venv", "__pycache__", "tools"]
            ):
                engines.append(path)
        return engines
