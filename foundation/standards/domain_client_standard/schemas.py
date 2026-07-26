"""Universal Domain Client Standard Schemas.

This module defines the required structure for domain clients.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ClientRequest(BaseModel):
    """A client request."""

    model_config = ConfigDict(extra="ignore")

    client_id: str = Field(..., description="Client identifier")
    request_type: str = Field(..., description="Request type")
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Request parameters"
    )
    timestamp: datetime = Field(default_factory=datetime.now)


class ClientResponse(BaseModel):
    """A client response."""

    model_config = ConfigDict(extra="ignore")

    success: bool = Field(..., description="Whether the request succeeded")
    data: dict[str, Any] | None = Field(None, description="Response data")
    error: str | None = Field(None, description="Error message if failed")
    timestamp: datetime = Field(default_factory=datetime.now)


class ClientConfig(BaseModel):
    """Client configuration."""

    model_config = ConfigDict(extra="ignore")

    client_type: str = Field(..., description="Type of client")
    timeout_seconds: int = Field(30, description="Request timeout in seconds")
    retry_count: int = Field(3, description="Number of retries")
    retry_delay: int = Field(1, description="Delay between retries in seconds")
    cache_enabled: bool = Field(True, description="Whether caching is enabled")
