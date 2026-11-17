"""Request and response schemas for organizations."""

from datetime import date, datetime

from pydantic import Field, field_validator, model_validator

from app.schemas.common import APIModel, empty_to_none, ensure_date_order


class OrganizationCreate(APIModel):
    """Fields required to record an organization."""

    name: str = Field(min_length=1, max_length=300)
    organization_type: str | None = Field(default=None, max_length=100)
    description: str | None = None
    founded_date: date | None = None
    dissolved_date: date | None = None

    @field_validator("organization_type", "description", mode="before")
    @classmethod
    def blank_optional(cls, value: object) -> object:
        return empty_to_none(value)

    @model_validator(mode="after")
    def check_dates(self) -> "OrganizationCreate":
        ensure_date_order(
            self.founded_date,
            self.dissolved_date,
            "founded_date",
            "dissolved_date",
        )
        return self


class OrganizationUpdate(APIModel):
    """Partial update for an organization."""

    name: str | None = Field(default=None, min_length=1, max_length=300)
    organization_type: str | None = Field(default=None, max_length=100)
    description: str | None = None
    founded_date: date | None = None
    dissolved_date: date | None = None

    @field_validator("organization_type", "description", mode="before")
    @classmethod
    def blank_optional(cls, value: object) -> object:
        return empty_to_none(value)

    @model_validator(mode="after")
    def check_dates(self) -> "OrganizationUpdate":
        ensure_date_order(
            self.founded_date,
            self.dissolved_date,
            "founded_date",
            "dissolved_date",
        )
        return self


class OrganizationRead(OrganizationCreate):
    """Organization returned to API clients."""

    id: int
    created_at: datetime
    updated_at: datetime
