"""
API Schemas

Request and response schemas for the API.
"""

from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel


class SnapshotResponse(BaseModel):
    """
    API response for snapshot requests.
    """

    success: bool
    snapshot_id: str
    generated_at: datetime
    data: Dict[str, Any]
    health: Dict[str, Any]
    version: str = "1.0.0"


class HealthResponse(BaseModel):
    """
    API response for health checks.
    """

    status: str
    service: str
    timestamp: datetime
    details: Dict[str, Any]


class ErrorResponse(BaseModel):
    """
    API response for errors.
    """

    success: bool = False
    error: str
    code: str
    timestamp: datetime
