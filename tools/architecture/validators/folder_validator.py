"""Folder Validator – Checks required top-level folders."""

from pathlib import Path
from typing import List
from tools.architecture.validators.base import BaseValidator
from tools.architecture.models import ARCResult

class FolderValidator(BaseValidator):
    """Validates required top-level folders exist."""

    REQUIRED_FOLDERS = ["foundation", "ndip", "runtime", "providers"]

    def get_severity(self) -> str:
        return "critical"

    def validate(self) -> List[ARCResult]:
        results = []
        missing = [f for f in self.REQUIRED_FOLDERS if not (self.root / f).exists()]
        
        if missing:
            results.append(self.result(
                False,
                f"Missing required top-level folders: {', '.join(missing)}",
                severity="critical"
            ))
        else:
            results.append(self.result(True, "All required folders exist"))
        
        return results
