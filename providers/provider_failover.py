"""Provider failover tracking."""

from collections import defaultdict


class ProviderFailover:
    """Tracks provider failures and triggers failover."""

    def __init__(self):
        self._failures: dict[str, int] = defaultdict(int)
        self._max_failures: int = 3

    def record_failure(self, provider_name: str) -> None:
        self._failures[provider_name] += 1

    def reset_failures(self, provider_name: str) -> None:
        self._failures[provider_name] = 0

    def should_failover(self, provider_name: str) -> bool:
        return self._failures.get(provider_name, 0) >= self._max_failures
