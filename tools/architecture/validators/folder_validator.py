"""Folder Validator – Checks required top-level folders."""

from tools.architecture.models import ARCResult
from tools.architecture.validators.base import BaseValidator


class FolderValidator(BaseValidator):
    """Validates required top-level folders exist."""

    REQUIRED_FOLDERS = ["foundation", "ndip", "runtime", "providers"]

    def get_severity(self) -> str:
        return "critical"

    def validate(self) -> list[ARCResult]:
        results = []
        missing = [f for f in self.REQUIRED_FOLDERS if not (self.root / f).exists()]

        if missing:
            results.append(
                self.result(
                    False,
                    f"Missing required top-level folders: {', '.join(missing)}",
                    severity="critical",
                )
            )
        else:
            results.append(self.result(True, "All required folders exist"))

        return results
