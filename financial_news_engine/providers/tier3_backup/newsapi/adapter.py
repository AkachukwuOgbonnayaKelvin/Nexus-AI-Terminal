from datetime import datetime
from typing import Any, Dict

from financial_news_engine.dtos import UniversalNews


class NewsAPIAdapter:
    def adapt(self, raw: Dict[str, Any], provider_name: str) -> UniversalNews:
        published_at = raw.get("publishedAt")
        if published_at:
            published_at = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        else:
            published_at = datetime.now()
        article_id = f"newsapi_{raw.get('source', {}).get('id', 'unknown')}_{published_at.isoformat()}"
        return UniversalNews(
            article_id=article_id,
            provider=provider_name,
            provider_article_id=raw.get("url", article_id),
            headline=raw.get("title", "No Title"),
            summary=raw.get("description", ""),
            body=raw.get("content", ""),
            url=raw.get("url"),
            author=raw.get("author"),
            country=None,
            region=None,
            language="en",
            published_at=published_at,
            updated_at=None,
            category="News",
            subcategory=None,
            importance="Medium",
            entities=[],
            assets=[],
            currencies=[],
            commodities=[],
            central_banks=[],
            governments=[],
            companies=[],
            tags=[],
            raw_payload=raw,
            confidence=0.8,
            metadata={"source": raw.get("source", {})},
        )
