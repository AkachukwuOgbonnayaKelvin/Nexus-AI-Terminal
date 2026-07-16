import email.utils
from datetime import datetime
from typing import Any, Dict

from financial_news_engine.dtos import UniversalNews


class RSSAdapter:
    def adapt(self, raw: Dict[str, Any], provider_name: str) -> UniversalNews:
        published_at = raw.get("published")
        if published_at:
            try:
                published_at = datetime.fromtimestamp(email.utils.mktime_tz(email.utils.parsedate_tz(published_at)))
            except Exception:
                published_at = datetime.now()
        else:
            published_at = datetime.now()
        article_id = f"rss_{raw.get('source', 'unknown')}_{published_at.isoformat()}"
        return UniversalNews(
            article_id=article_id,
            provider=provider_name,
            provider_article_id=raw.get("link", article_id),
            headline=raw.get("title", "No Title"),
            summary=raw.get("summary", ""),
            body=raw.get("summary", ""),
            url=raw.get("link"),
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
            confidence=0.7,
            metadata={"source": raw.get("source")},
        )
