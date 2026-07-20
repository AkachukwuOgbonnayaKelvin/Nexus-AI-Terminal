"""Blueprint Validator – Ensures engines follow the Nexus blueprint."""

from pathlib import Path
from typing import List
from tools.architecture.models import ARCResult
from tools.architecture.validators.base import BaseValidator


class BlueprintValidator(BaseValidator):
    """Validates that engines follow the Nexus blueprint."""

    REQUIRED_FOLDERS = [
        "acquisition",
        "providers",
        "warehouse",
        "publication",
        "runtime",
        "configuration",
        "tests",
        "gateway",
        "observability",
    ]

    REQUIRED_FILES = {
        "warehouse": ["repository.py", "models.py"],
        "publication": ["publisher.py"],
        "runtime": ["scheduler.py"],
        "acquisition": ["collector.py"],
    }

    def get_severity(self) -> str:
        return "critical"

    def validate(self) -> List[ARCResult]:
        results = []
        engines = self._find_engines()

        for engine_path in engines:
            engine_name = engine_path.name
            missing_folders = []

            for folder in self.REQUIRED_FOLDERS:
                if not (engine_path / folder).exists():
                    missing_folders.append(folder)

            if missing_folders:
                results.append(
                    self.result(
                        False,
                        f"{engine_name} missing folders: {', '.join(missing_folders)}",
                        details={
                            "engine": engine_name,
                            "missing_folders": missing_folders,
                        },
                        severity="high",
                    )
                )

            # Check required files
            for folder, files in self.REQUIRED_FILES.items():
                folder_path = engine_path / folder
                if folder_path.exists():
                    missing_files = [f for f in files if not (folder_path / f).exists()]
                    if missing_files:
                        results.append(
                            self.result(
                                False,
                                f"{engine_name} missing files in {folder}: {', '.join(missing_files)}",
                                severity="medium",
                            )
                        )

        if not results:
            results.append(self.result(True, "All engines follow the Nexus blueprint"))

        return results

    def _find_engines(self) -> List[Path]:
        engines = []
        for path in self.root.glob("**/*_engine"):
            if path.is_dir() and not any(
                p in str(path) for p in [".venv", "__pycache__", "tools"]
            ):
                engines.append(path)
        return engines
