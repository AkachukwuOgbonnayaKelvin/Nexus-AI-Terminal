"""Validation service implementation."""

from typing import Any, Optional, Type


class ValidationError(Exception):
    """Exception raised for validation errors."""

    pass


def validate(value: Any, expected_type: Optional[Type] = None) -> bool:
    """Validate a value."""
    if expected_type and not isinstance(value, expected_type):
        raise ValidationError(f"Expected {expected_type}, got {type(value)}")
    return True


def is_valid(value: Any) -> bool:
    """Check if a value is valid."""
    return value is not None
