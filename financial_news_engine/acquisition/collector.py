import logging
from typing import List

from financial_news_engine.dtos import UniversalNews
from providers.provider_manager import ProviderManager

logger = logging.getLogger(__name__)


class NewsCollector:
    def __init__(self, provider_manager: ProviderManager):
        self.pm = provider_manager

    async def collect_today(self) -> List[UniversalNews]:
        events = []
        provider_names = self.pm.get_providers(capability="news")
        logger.info(f"Found providers: {provider_names}")
        for name in provider_names:
            provider = self.pm.get_provider(name)
            if not provider or not hasattr(provider, "get_today_news"):
                continue
            # Only skip if unhealthy AND not RSS (RSS is forgiving)
            is_healthy = self.pm.health.is_healthy(name)
            if not is_healthy and name != "rss":
                logger.warning(f"Provider {name} unhealthy, skipping")
                continue
            try:
                raw = provider.get_today_news()
                if raw:
                    adapter = self.pm.get_adapter(name)
                    if adapter:
                        for item in raw:
                            adapted = adapter.adapt(item, name)
                            events.append(adapted)
                    else:
                        logger.warning(f"No adapter for {name}")
                else:
                    logger.info(f"Provider {name} returned no news")
            except Exception as e:
                logger.error(f"Error from {name}: {e}")
                self.pm.failover.record_failure(name)
        return events
