#!/usr/bin/env python3
"""Test Financial News Engine (NEWS-001)."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from financial_news_engine.acquisition import NewsCollector
from financial_news_engine.classification import NewsClassifier
from financial_news_engine.entities import EntityExtractor
from financial_news_engine.providers.tier3_backup.newsapi import (
    NewsAPIAdapter,
    NewsAPIConnector,
)
from financial_news_engine.providers.tier3_backup.rss import RSSAdapter, RSSConnector
from financial_news_engine.warehouse import NewsWarehouse
from ndip.utils.db_connector import close_pool
from providers.provider_manager import ProviderManager


async def main():
    print("=" * 60)
    print("TESTING FINANCIAL NEWS ENGINE (NEWS-001)")
    print("=" * 60)

    pm = ProviderManager()

    newsapi = NewsAPIConnector()
    newsapi_adapter = NewsAPIAdapter()
    pm.register_provider("newsapi", newsapi, newsapi_adapter, capabilities=["news"])

    rss = RSSConnector()
    rss_adapter = RSSAdapter()
    pm.register_provider("rss", rss, rss_adapter, capabilities=["news"])

    collector = NewsCollector(pm)
    warehouse = NewsWarehouse()
    classifier = NewsClassifier()
    extractor = EntityExtractor()

    print("\nCollecting news...")
    articles = await collector.collect_today()

    print(f"Collected {len(articles)} articles")
    stored = 0
    for article in articles:
        # Classify
        classification = classifier.classify(article.headline, article.summary)
        article.category = classification["category"]
        article.importance = classification["importance"]
        # Extract entities
        full_text = f"{article.headline} {article.summary or ''} {article.body or ''}"
        entities = extractor.extract(full_text)
        article.currencies = entities.get("currencies", [])
        article.assets = entities.get("assets", [])
        article.central_banks = entities.get("central_banks", [])
        # Store
        result = await warehouse.store(article)
        if result:
            stored += 1
            print(
                f"  ✅ {article.headline[:50]}... ({article.category}) [{article.importance}]"
            )

    print(f"\nStored {stored} articles")

    print("\nLatest high-impact news:")
    high = await warehouse.get_high_impact()
    for h in high:
        print(f"  {h['headline'][:60]}... - {h['importance']}")

    await close_pool()
    print("\n✅ Test complete.")


if __name__ == "__main__":
    asyncio.run(main())
