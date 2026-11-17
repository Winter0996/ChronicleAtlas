"""Response schema for the health endpoint."""

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """Application and database availability."""

    model_config = ConfigDict(extra="forbid")

    status: str
    database: str
    environment: str
