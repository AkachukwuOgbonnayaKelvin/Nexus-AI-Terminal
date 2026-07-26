"""Universal Hub Standard Schemas.

This module defines the required structure for workspace hubs.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HubConfig(BaseModel):
    """Hub configuration."""

    model_config = ConfigDict(extra="ignore")

    workspace_name: str = Field(..., description="Name of the workspace")
    version: str = Field(..., description="Hub version")
    enabled: bool = Field(default=True, description="Whether the hub is enabled")
    update_interval: int = Field(60, description="Update interval in seconds")
    max_history: int = Field(1000, description="Maximum history entries to keep")


class HubStatus(BaseModel):
    """Hub status."""

    model_config = ConfigDict(extra="ignore")

    status: str = Field(..., description="Status: 'running', 'stopped', 'error'")
    last_update: datetime | None = Field(None, description="Last successful update")
    next_update: datetime | None = Field(None, description="Next scheduled update")
    message: str | None = Field(None, description="Status message")


class HubHealth(BaseModel):
    """Hub health status."""

    model_config = ConfigDict(extra="ignore")

    healthy: bool = Field(..., description="Whether the hub is healthy")
    engine_health: dict[str, bool] = Field(
        default_factory=dict, description="Health status of individual engines"
    )
    data_freshness: float = Field(..., description="Age of data in seconds")
    errors: list[str] = Field(default_factory=list, description="Recent errors")
