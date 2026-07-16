import logging

from ndip.utils.db_connector import fetchrow

logger = logging.getLogger(__name__)


async def health_check() -> dict:
    """Check health of the engine and its dependencies."""
    status = "healthy"
    errors = []
    # Check database connectivity
    try:
        await fetchrow("SELECT 1")
    except Exception as e:
        status = "degraded"
        errors.append(f"Database error: {e}")
    return {
        "status": status,
        "errors": errors,
        "engine": "macro_statistics",
        "version": "1.0",
    }
