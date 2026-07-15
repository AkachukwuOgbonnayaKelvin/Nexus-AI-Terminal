"""Logging service implementation."""

import logging
import sys

from foundation.config import config
from foundation.settings import settings


def setup_logging() -> None:
    """Configure logging for the platform."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    if settings.log_format == "json":
        # JSON format would be implemented here
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(config.LOGS_DIR / "platform.log")
            if settings.log_to_file
            else logging.NullHandler(),
        ],
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
