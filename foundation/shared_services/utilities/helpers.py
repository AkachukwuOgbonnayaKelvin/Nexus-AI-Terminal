"""Utility functions."""

from datetime import datetime


def timestamp_to_datetime(timestamp: float) -> datetime:
    """Convert a timestamp to datetime."""
    return datetime.fromtimestamp(timestamp)


def format_currency(value: float, symbol: str = "$") -> str:
    """Format a currency value."""
    return f"{symbol}{value:,.2f}"


def truncate_string(value: str, max_length: int = 100) -> str:
    """Truncate a string to a maximum length."""
    if len(value) <= max_length:
        return value
    return value[: max_length - 3] + "..."
