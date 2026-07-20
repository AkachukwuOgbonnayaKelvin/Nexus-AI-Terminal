"""Runtime Validator – Checks DAR integration."""

from typing import List
from tools.architecture.validators.base import BaseValidator
from tools.architecture.models import ARCResult


class RuntimeValidator(BaseValidator):
    """Validates engine runtime integration."""

    def get_severity(self) -> str:
        return "critical"

    def validate(self) -> List[ARCResult]:
        results = []
        runtime_file = self.root / "runtime" / "runtime.py"
        if not runtime_file.exists():
            results.append(
                self.result(False, "DAR-001 runtime.py not found", severity="critical")
            )
            return results

        registry_file = self.root / "runtime" / "engine_registry.py"
        if not registry_file.exists():
            results.append(
                self.result(False, "Engine registry not found", severity="high")
            )
        else:
            results.append(self.result(True, "Runtime and registry found"))

        return results
