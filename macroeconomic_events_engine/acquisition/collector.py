import logging

from macroeconomic_events_engine.dtos import UniversalMacroEvent
from providers.provider_manager import ProviderManager

logger = logging.getLogger(__name__)


class MacroCollector:
    def __init__(self, provider_manager: ProviderManager):
        self.pm = provider_manager

    async def collect_today(self) -> list[UniversalMacroEvent]:
        events = []
        provider_names = self.pm.get_providers(capability="macroeconomic_events")
        logger.info(f"Found providers: {provider_names}")
        for name in provider_names:
            logger.info(f"Checking provider: {name}")
            provider = self.pm.get_provider(name)
            if not provider or not hasattr(provider, "get_today_events"):
                logger.warning(f"Provider {name} has no get_today_events method")
                continue
            # Log health
            healthy = self.pm.health.is_healthy(name)
            logger.info(f"Provider {name} healthy: {healthy}")
            if not healthy:
                logger.warning(f"Provider {name} unhealthy, skipping")
                continue
            try:
                raw = provider.get_today_events()
                if raw:
                    adapter = self.pm.get_adapter(name)
                    if adapter:
                        for r in raw:
                            adapted = adapter.adapt(r, name)
                            events.append(adapted)
                    else:
                        logger.warning(f"No adapter for {name}")
                else:
                    logger.info(f"Provider {name} returned no events")
            except Exception as e:
                logger.error(f"Error from {name}: {e}")
                self.pm.failover.record_failure(name)
        return events
