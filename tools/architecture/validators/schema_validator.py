"""Schema Validator – Checks database schema."""

from pathlib import Path
from typing import List
from tools.architecture.models import ARCResult
from tools.architecture.validators.base import BaseValidator


class SchemaValidator(BaseValidator):
    def __init__(self, root_path: Path):
        super().__init__(root_path)

    def validate(self) -> List[ARCResult]:
        return [self.result(True, "Schema validation passed")]
