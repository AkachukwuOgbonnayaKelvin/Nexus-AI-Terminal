"""Publication Validator – Checks publication layer."""

from pathlib import Path
from typing import List
from tools.architecture.validators.base import BaseValidator
from tools.architecture.models import ARCResult


class PublicationValidator(BaseValidator):
    """Validates publication layer exists."""

    def get_severity(self) -> str:
        return "high"

    def validate(self) -> List[ARCResult]:
        results = []
        engines = self._find_engines()

        for engine in engines:
            pub_dir = engine / "publication"
            if not pub_dir.exists():
                results.append(
                    self.result(
                        False,
                        f"{engine.name} missing publication/ folder",
                        severity="high",
                    )
                )
            else:
                publisher_file = pub_dir / "publisher.py"
                if not publisher_file.exists():
                    results.append(
                        self.result(
                            False,
                            f"{engine.name} missing publication/publisher.py",
                            severity="high",
                        )
                    )

        if not results:
            results.append(self.result(True, "All engines have publication layer"))
        return results

    def _find_engines(self) -> List[Path]:
        engines = []
        for path in self.root.glob("**/*_engine"):
            if path.is_dir() and not any(
                p in str(path) for p in [".venv", "__pycache__", "tools"]
            ):
                engines.append(path)
        return engines
