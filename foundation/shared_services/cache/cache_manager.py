"""Cache service implementation."""

import time
from typing import Any

from foundation.settings import settings


class CacheManager:
    """Simple in-memory cache with TTL."""

    def __init__(self) -> None:
        self._cache: dict[str, dict[str, Any]] = {}
        self._ttl = settings.cache_ttl_seconds

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set a value in the cache."""
        if ttl is None:
            ttl = self._ttl
        self._cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl,
        }

    def get(self, key: str) -> Any | None:
        """Get a value from the cache."""
        entry = self._cache.get(key)
        if not entry:
            return None
        if time.time() > entry["expires_at"]:
            del self._cache[key]
            return None
        return entry["value"]

    def delete(self, key: str) -> None:
        """Delete a value from the cache."""
        self._cache.pop(key, None)

    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()
