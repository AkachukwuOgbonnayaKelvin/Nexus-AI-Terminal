"""Provider Manager – orchestrates provider selection with failover."""

from typing import Dict, List, Optional

from providers.dtos.transport import UniversalTransport
from providers.interfaces.base_adapter import BaseAdapter
from providers.interfaces.base_provider import BaseProvider
from providers.provider_failover import ProviderFailover
from providers.provider_health import ProviderHealth
from providers.provider_metrics import ProviderMetrics


class ProviderManager:
    """Orchestrates all providers."""

    def __init__(self):
        self.providers: Dict[str, BaseProvider] = {}
        self.adapters: Dict[str, BaseAdapter] = {}
        self.health = ProviderHealth()
        self.failover = ProviderFailover()
        self.metrics = ProviderMetrics()
        self._capabilities: Dict[str, List[str]] = {}

    def register_provider(
        self,
        name: str,
        provider: BaseProvider,
        adapter: BaseAdapter,
        capabilities: List[str] = None,
    ) -> None:
        """Register a provider with its adapter."""
        self.providers[name] = provider
        self.adapters[name] = adapter
        self.health.register(name, provider)
        self.metrics.register(name)
        self._capabilities[name] = capabilities or []

        try:
            if not provider.connect():
                self.health.set_status(name, False)
                print(f"⚠️ Provider {name} failed to connect")
            else:
                print(f"✅ Provider {name} connected")
        except Exception as e:
            self.health.set_status(name, False)
            print(f"⚠️ Provider {name} connection error: {e}")

    def get_provider(self, name: str) -> Optional[BaseProvider]:
        return self.providers.get(name)

    def get_adapter(self, name: str) -> Optional[BaseAdapter]:
        return self.adapters.get(name)

    def get_providers(self, capability: str) -> List[str]:
        return [name for name, caps in self._capabilities.items() if capability in caps]

    def get_price(
        self, symbol: str, asset_class: Optional[str] = None
    ) -> Optional[UniversalTransport]:
        priority_order = self.health.get_priority_order(asset_class)

        for provider_name in priority_order:
            provider = self.providers.get(provider_name)
            adapter = self.adapters.get(provider_name)

            if not provider or not adapter:
                continue

            if not self.health.is_healthy(provider_name):
                self.failover.record_failure(provider_name)
                continue

            if not provider.supports_symbol(symbol):
                continue

            raw_data = provider.get_price(symbol)
            if raw_data is None:
                self.failover.record_failure(provider_name)
                continue

            transport = adapter.adapt(raw_data, provider_name)
            if transport:
                self.metrics.record_success(provider_name)
                return transport

        self.metrics.record_error("all_providers_failed", symbol)
        return None

    def get_multiple(self, symbols: List[str]) -> List[UniversalTransport]:
        results = []
        for symbol in symbols:
            data = self.get_price(symbol)
            if data:
                results.append(data)
        return results

    def health_check_all(self) -> Dict[str, bool]:
        results = {}
        for name, provider in self.providers.items():
            results[name] = self.health.is_healthy(name)
        return results
