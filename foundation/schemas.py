"""Platform base schemas.

This module defines base Pydantic schemas used across the platform.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""

    model_config = ConfigDict(extra="ignore")

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)

    def touch(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()


class IDMixin(BaseModel):
    """Mixin for ID fields."""

    id: Optional[str] = Field(default=None, description="Unique identifier")
    name: Optional[str] = Field(default=None, description="Name")


class BaseResponse(BaseModel):
    """Base response schema."""

    status: str = Field(..., description="Response status")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Response data")
    timestamp: datetime = Field(default_factory=datetime.now)


class HealthCheckResponse(BaseResponse):
    """Health check response."""

    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")


class ErrorResponse(BaseResponse):
    """Error response schema."""

    error_code: str = Field(..., description="Error code")
    error_details: Optional[Dict[str, Any]] = Field(
        default=None, description="Error details"
    )
    traceback: Optional[str] = Field(default=None, description="Error traceback")
