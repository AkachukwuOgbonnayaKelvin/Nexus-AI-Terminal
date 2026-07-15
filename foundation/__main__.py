"""Foundation layer testing entry point."""

from foundation.config import config
from foundation.settings import settings


def main() -> None:
    """Test foundation layer."""
    print("=" * 60)
    print("NEXUS AI TERMINAL - FOUNDATION LAYER")
    print("=" * 60)

    print(f"\nApplication: {config.APP_NAME}")
    print(f"Version: {config.APP_VERSION}")
    print(f"Environment: {config.APP_ENV}")
    print(f"Debug: {config.DEBUG}")
    print(f"API: {config.API_HOST}:{config.API_PORT}")

    print("\nSettings:")
    print(f"  Log Level: {settings.log_level}")
    print(f"  Cache TTL: {settings.cache_ttl_seconds}s")
    print(f"  Confidence Threshold: {settings.confidence_threshold}")

    print("\nFoundation layer loaded successfully!")


if __name__ == "__main__":
    main()
