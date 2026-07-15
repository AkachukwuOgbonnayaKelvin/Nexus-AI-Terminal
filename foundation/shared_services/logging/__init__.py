"""Platform logging service.

Provides structured logging with support for JSON format, log levels,
and file/console output.
"""

from .logger import get_logger, setup_logging

__all__ = ["get_logger", "setup_logging"]
