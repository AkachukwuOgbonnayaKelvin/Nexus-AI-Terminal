"""
API Routes

Exposes endpoints for the workspace.
"""

import logging
from typing import Dict, Any
from datetime import datetime

from .schemas import SnapshotResponse, HealthResponse
from workspace.snapshot_service import SnapshotService

logger = logging.getLogger(__name__)

# Global service instance (using Python 3.10+ union syntax)
_snapshot_service: SnapshotService | None = None


def get_service() -> SnapshotService:
    """Get or create the snapshot service."""
    global _snapshot_service
    if _snapshot_service is None:
        _snapshot_service = SnapshotService()
    return _snapshot_service


# Mock routes (to be replaced with actual framework)
class Router:
    """Mock router for demonstration."""

    @staticmethod
    def get_snapshot() -> Dict[str, Any]:
        """
        GET /api/global-intelligence/snapshot
        """
        service = get_service()
        snapshot = service.get_last_snapshot()

        if snapshot is None:
            snapshot = service.build_snapshot()

        return SnapshotResponse(
            success=True,
            snapshot_id=snapshot.snapshot_id,
            generated_at=snapshot.generated_at,
            data=snapshot.dict(),
            health=snapshot.health,
        ).dict()

    @staticmethod
    def get_health() -> Dict[str, Any]:
        """
        GET /api/health
        """
        service = get_service()
        health = service.health_check()

        return HealthResponse(
            status="HEALTHY",
            service="Nexus-AI-Terminal-API",
            timestamp=datetime.utcnow(),
            details=health,
        ).dict()

    @staticmethod
    def get_regime() -> Dict[str, Any]:
        """
        GET /api/global-intelligence/regime
        """
        service = get_service()
        snapshot = service.get_last_snapshot()

        if snapshot is None:
            snapshot = service.build_snapshot()

        return {
            "success": True,
            "regime": snapshot.market_regime,
            "timestamp": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def get_assets() -> Dict[str, Any]:
        """
        GET /api/global-intelligence/assets
        """
        service = get_service()
        snapshot = service.get_last_snapshot()

        if snapshot is None:
            snapshot = service.build_snapshot()

        return {
            "success": True,
            "assets": snapshot.asset_intelligence,
            "timestamp": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def get_macro() -> Dict[str, Any]:
        """
        GET /api/global-intelligence/macro
        """
        service = get_service()
        snapshot = service.get_last_snapshot()

        if snapshot is None:
            snapshot = service.build_snapshot()

        return {
            "success": True,
            "macro": snapshot.macro_intelligence,
            "timestamp": datetime.utcnow().isoformat(),
        }


# Export router
router = Router()
