"""Request and response schemas for locations."""

from datetime import datetime

from pydantic import Field, field_validator, model_validator

from app.schemas.common import APIModel, empty_to_none, ensure_coordinate_pair


class LocationCreate(APIModel):
    """Fields required to record a place."""

    name: str = Field(min_length=1, max_length=300)
    region: str | None = Field(default=None, max_length=150)
    description: str | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    @field_validator("region", "description", mode="before")
    @classmethod
    def blank_optional(cls, value: object) -> object:
        return empty_to_none(value)

    @model_validator(mode="after")
    def check_coordinates(self) -> "LocationCreate":
        ensure_coordinate_pair(self.latitude, self.longitude)
        return self


class LocationUpdate(APIModel):
    """Partial update for a place."""

    name: str | None = Field(default=None, min_length=1, max_length=300)
    region: str | None = Field(default=None, max_length=150)
    description: str | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    @field_validator("region", "description", mode="before")
    @classmethod
    def blank_optional(cls, value: object) -> object:
        return empty_to_none(value)

    @model_validator(mode="after")
    def check_coordinates(self) -> "LocationUpdate":
        if "latitude" in self.model_fields_set or "longitude" in self.model_fields_set:
            ensure_coordinate_pair(self.latitude, self.longitude)
        return self


class LocationRead(LocationCreate):
    """Location returned to API clients."""

    id: int
    created_at: datetime
    updated_at: datetime
