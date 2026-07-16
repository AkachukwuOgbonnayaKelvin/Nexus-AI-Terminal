"""News Gateway Service – API for querying news."""

import logging

from fastapi import APIRouter, HTTPException

from financial_news_engine.warehouse import NewsWarehouse

logger = logging.getLogger(__name__)


class NewsGateway:
    def __init__(self):
        self.warehouse = NewsWarehouse()
        self.router = APIRouter(prefix="/news", tags=["Financial News"])
        self._register_routes()

    def _register_routes(self):
        @self.router.get("/latest")
        async def get_latest(limit: int = 20):
            articles = await self.warehouse.get_latest(limit)
            return {"status": "success", "count": len(articles), "data": articles}

        @self.router.get("/high-impact")
        async def get_high_impact(limit: int = 20):
            articles = await self.warehouse.get_high_impact(limit)
            return {"status": "success", "count": len(articles), "data": articles}

        @self.router.get("/breaking")
        async def get_breaking(hours: int = 6):
            articles = await self.warehouse.get_breaking(hours)
            return {"status": "success", "count": len(articles), "data": articles}

        @self.router.get("/asset/{asset}")
        async def get_by_asset(asset: str, limit: int = 20):
            articles = await self.warehouse.get_by_asset(asset, limit)
            return {"status": "success", "count": len(articles), "data": articles}

        @self.router.get("/article/{article_id}")
        async def get_article(article_id: str):
            # We need to implement get_article in warehouse
            # For now, we'll just query the latest and filter
            articles = await self.warehouse.get_latest(100)
            for a in articles:
                if a["article_id"] == article_id:
                    return {"status": "success", "data": a}
            raise HTTPException(status_code=404, detail="Article not found")

    def get_router(self):
        return self.router
