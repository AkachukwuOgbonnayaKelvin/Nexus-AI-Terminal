"""
API Schemas

Request and response schemas for the API.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class SnapshotResponse(BaseModel):
    """
    API response for snapshot requests.
    """

    success: bool
    snapshot_id: str
    generated_at: datetime
    data: dict[str, Any]
    health: dict[str, Any]
    version: str = "1.0.0"


class HealthResponse(BaseModel):
    """
    API response for health checks.
    """

    status: str
    service: str
    timestamp: datetime
    details: dict[str, Any]


class ErrorResponse(BaseModel):
    """
    API response for errors.
    """

    success: bool = False
    error: str
    code: str
    timestamp: datetime
