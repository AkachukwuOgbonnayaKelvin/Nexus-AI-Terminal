"""Platform configuration management.

This module handles loading and managing configuration from environment variables,
configuration files, and defaults.
"""

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file)


class Config:
    """Master configuration class for the platform."""

    # Application
    APP_NAME: str = os.getenv("APP_NAME", "Nexus AI Terminal")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Paths
    ROOT_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = ROOT_DIR / "data"
    LOGS_DIR: Path = ROOT_DIR / "logs"
    REPORTS_DIR: Path = ROOT_DIR / "qa" / "reports"

    # Database
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "10"))
    DATABASE_MAX_OVERFLOW: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "20"))

    # Redis
    REDIS_URL: str | None = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))

    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_WORKERS: int = int(os.getenv("API_WORKERS", "4"))

    # Authentication
    SECRET_KEY: str | None = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

    # Market Data
    MARKET_DATA_PROVIDER: str = os.getenv("MARKET_DATA_PROVIDER", "alpha_vantage")
    MARKET_DATA_API_KEY: str | None = os.getenv("MARKET_DATA_API_KEY")
    MARKET_DATA_TIMEOUT: int = int(os.getenv("MARKET_DATA_TIMEOUT", "30"))

    # NDIP
    NDIP_BATCH_SIZE: int = int(os.getenv("NDIP_BATCH_SIZE", "1000"))
    NDIP_QUEUE_MAXSIZE: int = int(os.getenv("NDIP_QUEUE_MAXSIZE", "10000"))

    @classmethod
    def to_dict(cls) -> dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "app_name": cls.APP_NAME,
            "app_version": cls.APP_VERSION,
            "app_env": cls.APP_ENV,
            "debug": cls.DEBUG,
            "database_url": cls.DATABASE_URL,
            "redis_url": cls.REDIS_URL,
            "api_host": cls.API_HOST,
            "api_port": cls.API_PORT,
            "market_data_provider": cls.MARKET_DATA_PROVIDER,
        }

    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration."""
        required = [
            ("SECRET_KEY", cls.SECRET_KEY, "Secret key is required for authentication"),
            ("DATABASE_URL", cls.DATABASE_URL, "Database URL is required"),
        ]

        for name, value, message in required:
            if not value:
                raise ValueError(f"{name}: {message}")

        return True


# Singleton instance
config = Config()
