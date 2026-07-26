import json
import logging
from datetime import datetime, timedelta

from financial_news_engine.dtos import UniversalNews
from ndip.utils.db_connector import execute, fetch, fetchrow

logger = logging.getLogger(__name__)


class NewsWarehouse:
    def __init__(self):
        self.table = "news_articles"

    async def store(self, article: UniversalNews) -> bool:
        query = f"""
            INSERT INTO {self.table} (
                article_id, provider, provider_article_id, headline, summary, body,
                url, author, country, region, language, published_at, updated_at,
                category, subcategory, importance, tags, confidence, metadata
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19)
            ON CONFLICT (article_id) DO UPDATE SET
                headline = EXCLUDED.headline,
                summary = EXCLUDED.summary,
                body = EXCLUDED.body,
                updated_at = EXCLUDED.updated_at,
                category = EXCLUDED.category,
                subcategory = EXCLUDED.subcategory,
                importance = EXCLUDED.importance,
                tags = EXCLUDED.tags,
                confidence = EXCLUDED.confidence,
                metadata = EXCLUDED.metadata
        """
        try:
            await execute(
                query,
                article.article_id,
                article.provider,
                article.provider_article_id,
                article.headline,
                article.summary,
                article.body,
                article.url,
                article.author,
                article.country,
                article.region,
                article.language,
                article.published_at,
                article.updated_at or article.published_at,
                article.category,
                article.subcategory,
                article.importance,
                article.tags,
                article.confidence,
                json.dumps(article.metadata),
            )
            return True
        except Exception as e:
            logger.error(f"News store error: {e}")
            return False

    async def get_latest(self, limit: int = 20) -> list[dict]:
        query = f"SELECT * FROM {self.table} ORDER BY published_at DESC LIMIT $1"
        rows = await fetch(query, limit)
        return [dict(row) for row in rows]

    async def get_high_impact(self, limit: int = 20) -> list[dict]:
        query = f"SELECT * FROM {self.table} WHERE importance IN ('Critical', 'High') ORDER BY published_at DESC LIMIT $1"
        rows = await fetch(query, limit)
        return [dict(row) for row in rows]

    async def get_breaking(self, hours: int = 6) -> list[dict]:
        cutoff = datetime.now() - timedelta(hours=hours)
        query = f"SELECT * FROM {self.table} WHERE published_at >= $1 AND importance = 'Critical' ORDER BY published_at DESC"
        rows = await fetch(query, cutoff)
        return [dict(row) for row in rows]

    async def get_by_asset(self, asset: str, limit: int = 20) -> list[dict]:
        query = f"SELECT * FROM {self.table} WHERE metadata->>'assets' LIKE $1 OR metadata->>'currencies' LIKE $1 ORDER BY published_at DESC LIMIT $2"
        rows = await fetch(query, f"%{asset}%", limit)
        return [dict(row) for row in rows]

    async def get_article(self, article_id: str) -> dict | None:
        query = f"SELECT * FROM {self.table} WHERE article_id = $1"
        row = await fetchrow(query, article_id)
        return dict(row) if row else None
