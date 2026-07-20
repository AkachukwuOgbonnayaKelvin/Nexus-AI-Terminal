import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException

from economic_events_engine.warehouse import EconomicWarehouse

logger = logging.getLogger(__name__)


class EconomicService:
    def __init__(self):
        self.warehouse = EconomicWarehouse()
        self.router = APIRouter(prefix="/economic", tags=["Macroeconomic Statistics"])
        self._register_routes()

    def _register_routes(self):
        @self.router.get("/today")
        async def get_today(
            country: Optional[str] = None, importance: Optional[str] = None
        ):
            events = await self.warehouse.get_today_events(country, importance)
            return {"status": "success", "count": len(events), "data": events}

        @self.router.get("/upcoming")
        async def get_upcoming(hours: int = 48, country: Optional[str] = None):
            events = await self.warehouse.get_upcoming_events(hours, country)
            return {"status": "success", "count": len(events), "data": events}

        @self.router.get("/series/{series_id}")
        async def get_series(series_id: str, limit: int = 10):
            events = await self.warehouse.get_series(series_id, limit)
            return {"status": "success", "count": len(events), "data": events}

        @self.router.get("/series/{series_id}/latest")
        async def get_latest(series_id: str):
            event = await self.warehouse.get_latest_value(series_id)
            if not event:
                raise HTTPException(status_code=404, detail="No data found for series")
            return {"status": "success", "data": event}

        @self.router.get("/series/{series_id}/history")
        async def get_history(series_id: str, start: str, end: str):
            try:
                start_dt = datetime.fromisoformat(start)
                end_dt = datetime.fromisoformat(end)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS).",
                )
            events = await self.warehouse.get_historical_series(
                series_id, start_dt, end_dt
            )
            return {"status": "success", "count": len(events), "data": events}

        @self.router.get("/country/{country}")
        async def get_by_country(country: str, limit: int = 20):
            events = await self.warehouse.get_events_by_country(country, limit)
            return {"status": "success", "count": len(events), "data": events}

        @self.router.get("/high-impact")
        async def get_high_impact(limit: int = 20):
            events = await self.warehouse.get_high_impact_events(limit)
            return {"status": "success", "count": len(events), "data": events}

        @self.router.get("/between")
        async def get_between(start: str, end: str):
            try:
                start_dt = datetime.fromisoformat(start)
                end_dt = datetime.fromisoformat(end)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS).",
                )
            events = await self.warehouse.get_events_between(start_dt, end_dt)
            return {"status": "success", "count": len(events), "data": events}

        @self.router.get("/series")
        async def list_series():
            series = await self.warehouse.get_all_series()
            return {"status": "success", "count": len(series), "data": series}

    def get_router(self):
        return self.router
