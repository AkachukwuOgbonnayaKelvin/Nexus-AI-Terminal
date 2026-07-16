import logging

from ndip.utils.db_connector import fetchrow

logger = logging.getLogger(__name__)


async def health_check() -> dict:
    status = "healthy"
    errors = []
    try:
        await fetchrow("SELECT 1")
    except Exception as e:
        status = "degraded"
        errors.append(f"Database error: {e}")
    return {
        "status": status,
        "errors": errors,
        "engine": "central_bank",
        "version": "1.0",
    }
