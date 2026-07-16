import logging
from typing import Optional

from fastapi import APIRouter, HTTPException

from macroeconomic_events_engine.warehouse import ConsensusWarehouse

logger = logging.getLogger(__name__)


class MacroService:
    def __init__(self):
        self.warehouse = ConsensusWarehouse()
        self.router = APIRouter(prefix="/macro", tags=["Macroeconomic Events"])
        self._register_routes()

    def _register_routes(self):
        @self.router.get("/today")
        async def get_today(country: Optional[str] = None):
            events = await self.warehouse.get_today_events(country)
            return {"status": "success", "count": len(events), "data": events}

        @self.router.get("/upcoming")
        async def get_upcoming(hours: int = 48):
            events = await self.warehouse.get_upcoming_events(hours)
            return {"status": "success", "count": len(events), "data": events}

        @self.router.get("/high-impact")
        async def get_high_impact():
            events = await self.warehouse.get_high_impact()
            return {"status": "success", "count": len(events), "data": events}

        @self.router.get("/event/{event_id}")
        async def get_event(event_id: str):
            event = await self.warehouse.get_event(event_id)
            if not event:
                raise HTTPException(status_code=404, detail="Event not found")
            return {"status": "success", "data": event}

    def get_router(self):
        return self.router
