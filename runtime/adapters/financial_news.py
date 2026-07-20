# ruff: noqa: E402
import logging
import sys

from pathlib import Path

from runtime.base_engine import BaseRawEngine

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from financial_news_engine.acquisition import NewsCollector
from financial_news_engine.classification import NewsClassifier
from financial_news_engine.entities import EntityExtractor
from financial_news_engine.providers.tier3_backup.newsapi import (
    NewsAPIAdapter,
    NewsAPIConnector,
)
from financial_news_engine.providers.tier3_backup.rss import RSSAdapter, RSSConnector
from financial_news_engine.warehouse import NewsWarehouse
from providers.provider_manager import ProviderManager

logger = logging.getLogger(__name__)


class FinancialNewsEngineAdapter(BaseRawEngine):
    def __init__(self):
        self._initialized = False
        self.pm = None
        self.collector = None
        self.warehouse = None
        self.classifier = None
        self.extractor = None

    @property
    def name(self) -> str:
        return "financial_news"

    @property
    def enabled(self) -> bool:
        return True

    @property
    def interval_seconds(self) -> int:
        return 60

    async def initialize(self):
        if not self._initialized:
            logger.info("Initializing Financial News Engine")
            self.pm = ProviderManager()
            newsapi = NewsAPIConnector()
            newsapi_adapter = NewsAPIAdapter()
            self.pm.register_provider(
                "newsapi", newsapi, newsapi_adapter, capabilities=["news"]
            )
            rss = RSSConnector()
            rss_adapter = RSSAdapter()
            self.pm.register_provider("rss", rss, rss_adapter, capabilities=["news"])
            self.collector = NewsCollector(self.pm)
            self.warehouse = NewsWarehouse()
            self.classifier = NewsClassifier()
            self.extractor = EntityExtractor()
            self._initialized = True

    async def run(self):
        if not self._initialized:
            await self.initialize()
        logger.info("Running Financial News Engine")
        articles = await self.collector.collect_today()
        stored = 0
        for article in articles:
            classification = self.classifier.classify(article.headline, article.summary)
            article.category = classification["category"]
            article.importance = classification["importance"]
            entities = self.extractor.extract(
                f"{article.headline} {article.summary or ''} {article.body or ''}"
            )
            article.currencies = entities.get("currencies", [])
            article.assets = entities.get("assets", [])
            article.central_banks = entities.get("central_banks", [])
            if await self.warehouse.store(article):
                stored += 1
        return {"stored": stored, "collected": len(articles)}

    async def shutdown(self):
        logger.info("Shutting down Financial News Engine")
        self._initialized = False

    def health(self):
        return {
            "status": "healthy" if self._initialized else "not_initialized",
            "engine": "financial_news",
        }

    def metrics(self):
        return {"engine": "financial_news", "last_run": "N/A", "articles": 0}
