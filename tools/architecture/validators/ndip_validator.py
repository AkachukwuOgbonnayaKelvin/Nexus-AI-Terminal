"""NDIP Validator – Checks NDIP integration."""

from typing import List
from tools.architecture.validators.base import BaseValidator
from tools.architecture.models import ARCResult


class NDIPValidator(BaseValidator):
    """Validates NDIP integration."""

    def get_severity(self) -> str:
        return "critical"

    def validate(self) -> List[ARCResult]:
        results = []

        ndip_dir = self.root / "ndip"
        if not ndip_dir.exists():
            results.append(
                self.result(False, "NDIP directory not found", severity="critical")
            )
            return results

        # Check core NDIP components
        required = [
            "gateway",
            "validation",
            "normalization",
            "classification",
            "warehouse",
            "distribution",
        ]
        missing = [c for c in required if not (ndip_dir / c).exists()]

        if missing:
            results.append(
                self.result(
                    False,
                    f"NDIP missing components: {', '.join(missing)}",
                    severity="critical",
                )
            )
        else:
            results.append(self.result(True, "NDIP structure is complete"))

        return results
