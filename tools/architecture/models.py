"""ACP-001: Architecture Compliance Platform – Shared Models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ARCResult:
    """Result of a single validation."""

    validator: str
    passed: bool
    message: str
    details: Any = None
    severity: str = "medium"  # low, medium, high, critical
    suggested_fix: str | None = None
    file_path: str | None = None
    line_number: int | None = None


@dataclass
class ARCReport:
    """Complete ARC validation report."""

    timestamp: datetime = field(default_factory=datetime.now)
    total_validators: int = 0
    passed: int = 0
    failed: int = 0
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0
    results: list[ARCResult] = field(default_factory=list)
    architecture_score: float = 0.0
    certified: bool = False

    def add_result(self, result: ARCResult) -> None:
        """Add a result and update counts."""
        self.results.append(result)
        if result.passed:
            self.passed += 1
        else:
            self.failed += 1
            if result.severity == "critical":
                self.critical += 1
            elif result.severity == "high":
                self.high += 1
            elif result.severity == "medium":
                self.medium += 1
            else:
                self.low += 1
        self.total_validators += 1

    def calculate_score(self) -> float:
        """Calculate architecture score."""
        if self.total_validators == 0:
            return 0.0
        # Weighted score: critical issues reduce score more
        weight = {
            "critical": 5,
            "high": 3,
            "medium": 1,
            "low": 0.5,
        }
        total_weight = sum(
            weight.get(r.severity, 1) for r in self.results if not r.passed
        )
        max_weight = self.total_validators * 5
        self.architecture_score = max(0, 100 - (total_weight / max_weight * 100))
        return self.architecture_score

    def is_certified(self) -> bool:
        """Check if architecture is certified."""
        self.certified = self.failed == 0
        return self.certified
