"""Provider metrics tracking."""

from collections import defaultdict


class ProviderMetrics:
    """Tracks latency, success rate, errors per provider."""

    def __init__(self):
        self._success: dict[str, int] = defaultdict(int)
        self._errors: dict[str, int] = defaultdict(int)
        self._latency: dict[str, list[float]] = defaultdict(list)

    def register(self, name: str) -> None:
        pass

    def record_success(self, provider_name: str) -> None:
        self._success[provider_name] += 1

    def record_error(self, provider_name: str, symbol: str) -> None:
        self._errors[provider_name] += 1

    def get_stats(self) -> dict[str, dict]:
        stats = {}
        for name in set(list(self._success.keys()) + list(self._errors.keys())):
            stats[name] = {
                "success": self._success.get(name, 0),
                "errors": self._errors.get(name, 0),
            }
        return stats
