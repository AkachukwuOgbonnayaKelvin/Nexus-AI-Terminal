"""Provider health monitoring."""

from typing import Dict, List, Optional

from providers.interfaces.base_provider import BaseProvider


class ProviderHealth:
    """Tracks health status of providers."""

    def __init__(self):
        self._status: Dict[str, bool] = {}
        self._priority_map: Dict[str, List[str]] = {}
        self._providers: Dict[str, BaseProvider] = {}

    def register(self, name: str, provider: BaseProvider) -> None:
        self._providers[name] = provider
        self._status[name] = True
        # Build priority map based on tier and priority
        # For now, just store in a list sorted by priority
        if name not in self._priority_map.get("default", []):
            self._priority_map.setdefault("default", []).append(name)
        # Sort by priority (higher first)
        self._priority_map["default"].sort(key=lambda p: getattr(self._providers.get(p), "priority", 0), reverse=True)

    def is_healthy(self, name: str) -> bool:
        if name not in self._providers:
            return False
        try:
            healthy = self._providers[name].health_check()
            self._status[name] = healthy
            return healthy
        except Exception:
            self._status[name] = False
            return False

    def get_priority_order(self, asset_class: Optional[str] = None) -> List[str]:
        """Return provider names in priority order."""
        # For now, return default list
        return self._priority_map.get("default", [])

    def set_status(self, name: str, status: bool) -> None:
        self._status[name] = status
