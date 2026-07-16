import logging
from typing import List

from economic_events_engine.dtos import UniversalEconomicEvent
from economic_events_engine.providers.interfaces.base_economic_provider import BaseEconomicProvider
from providers.provider_manager import ProviderManager

logger = logging.getLogger(__name__)


class EconomicCollector:
    def __init__(self, provider_manager: ProviderManager):
        self.pm = provider_manager

    def collect_today(self) -> List[UniversalEconomicEvent]:
        events = []
        provider_names = self.pm.get_providers(capability="economic")
        for name in provider_names:
            provider = self.pm.get_provider(name)
            if not provider or not isinstance(provider, BaseEconomicProvider):
                continue
            if not self.pm.health.is_healthy(name):
                logger.warning(f"Provider {name} is unhealthy, skipping")
                continue
            try:
                raw_events = provider.get_today_events()
                adapter = self.pm.get_adapter(name)
                if adapter:
                    for raw in raw_events:
                        adapted = adapter.adapt(raw, name)
                        events.append(adapted)
            except Exception as e:
                logger.error(f"Failed to collect from {name}: {e}")
                self.pm.failover.record_failure(name)
        return events

    def collect_event(self, series_id: str) -> UniversalEconomicEvent:
        provider_names = self.pm.get_providers(capability="economic")
        for name in provider_names:
            provider = self.pm.get_provider(name)
            if not provider or not isinstance(provider, BaseEconomicProvider):
                continue
            if not self.pm.health.is_healthy(name):
                continue
            try:
                raw = provider.get_event(series_id)
                if raw:
                    adapter = self.pm.get_adapter(name)
                    if adapter:
                        return adapter.adapt(raw, name)
            except Exception:
                continue
        raise ValueError(f"No provider could fetch event {series_id}")
