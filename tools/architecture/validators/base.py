"""Base class for all architecture validators."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from tools.architecture.models import ARCResult


class BaseValidator(ABC):
    """Abstract base class for all validators."""

    def __init__(self, root_path: Path):
        self.root = root_path
        self.name = self.__class__.__name__

    @abstractmethod
    def validate(self) -> list[ARCResult]:
        """Run the validation and return results."""

    def get_severity(self) -> str:
        """Return the default severity for this validator."""
        return "medium"

    def result(
        self, passed: bool, message: str, details: Any = None, severity: str = None
    ) -> ARCResult:
        """Create a result."""
        return ARCResult(
            validator=self.name,
            passed=passed,
            message=message,
            details=details,
            severity=severity or self.get_severity(),
        )
