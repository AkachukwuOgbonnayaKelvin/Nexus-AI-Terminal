import logging
from typing import List, Optional

from central_bank_engine.dtos import UniversalCentralBankEvent
from providers.provider_manager import ProviderManager

logger = logging.getLogger(__name__)


class CentralBankCollector:
    def __init__(self, provider_manager: ProviderManager):
        self.pm = provider_manager

    async def collect_today(self) -> List[UniversalCentralBankEvent]:
        events = []
        provider_names = self.pm.get_providers(capability="central_bank")
        logger.info(f"Found providers: {provider_names}")
        for name in provider_names:
            provider = self.pm.get_provider(name)
            if not provider or not hasattr(provider, "get_today_events"):
                continue
            if not self.pm.health.is_healthy(name):
                logger.warning(f"Provider {name} unhealthy, skipping")
                continue
            try:
                raw = provider.get_today_events()
                if raw:
                    adapter = self.pm.get_adapter(name)
                    if adapter:
                        for item in raw:
                            adapted = adapter.adapt(item, name)
                            events.append(adapted)
                    else:
                        logger.warning(f"No adapter for {name}")
                else:
                    logger.info(f"Provider {name} returned no events")
            except Exception as e:
                logger.error(f"Error from {name}: {e}")
                self.pm.failover.record_failure(name)
        return events

    async def get_latest_rate(self, bank: str = "Federal Reserve") -> Optional[UniversalCentralBankEvent]:
        provider_names = self.pm.get_providers(capability="central_bank")
        for name in provider_names:
            provider = self.pm.get_provider(name)
            if not provider or not hasattr(provider, "get_fed_funds_rate"):
                continue
            if not self.pm.health.is_healthy(name):
                continue
            try:
                raw = provider.get_fed_funds_rate()
                if raw:
                    adapter = self.pm.get_adapter(name)
                    if adapter:
                        return adapter.adapt(raw, name)
            except Exception as e:
                logger.error(f"Error getting rate from {name}: {e}")
        return None
