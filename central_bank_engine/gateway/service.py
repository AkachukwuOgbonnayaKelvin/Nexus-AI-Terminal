"""Central Bank Gateway Service – API for querying central bank intelligence."""

import logging

from fastapi import APIRouter, HTTPException

from central_bank_engine.warehouse import CentralBankWarehouse

logger = logging.getLogger(__name__)


class CentralBankGateway:
    def __init__(self):
        self.warehouse = CentralBankWarehouse()
        self.router = APIRouter(prefix="/central-bank", tags=["Central Bank Intelligence"])
        self._register_routes()

    def _register_routes(self):
        @self.router.get("/latest")
        async def get_latest(limit: int = 20):
            events = await self.warehouse.get_latest(limit)
            return {"status": "success", "count": len(events), "data": events}

        @self.router.get("/latest-rate")
        async def get_latest_rate(bank: str = "Federal Reserve"):
            rate = await self.warehouse.get_latest_rate(bank)
            if not rate:
                raise HTTPException(status_code=404, detail="Rate not found")
            return {"status": "success", "data": rate}

        @self.router.get("/latest-statement")
        async def get_latest_statement(bank: str = "Federal Reserve"):
            statement = await self.warehouse.get_latest_statement(bank)
            if not statement:
                raise HTTPException(status_code=404, detail="Statement not found")
            return {"status": "success", "data": statement}

        @self.router.get("/meeting-calendar")
        async def get_meeting_calendar(bank: str = "Federal Reserve"):
            events = await self.warehouse.get_meeting_calendar(bank)
            return {"status": "success", "count": len(events), "data": events}

        @self.router.get("/importance/{importance}")
        async def get_by_importance(importance: str, limit: int = 20):
            events = await self.warehouse.get_by_importance(importance, limit)
            return {"status": "success", "count": len(events), "data": events}

    def get_router(self):
        return self.router
