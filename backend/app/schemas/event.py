"""Request and response schemas for events."""

from datetime import date, datetime

from pydantic import Field, field_validator, model_validator

from app.schemas.common import APIModel, empty_to_none, ensure_coordinate_pair, ensure_date_order


class EventCreate(APIModel):
    """Fields required to record an event."""

    title: str = Field(min_length=1, max_length=300)
    description: str | None = None
    start_date: date
    end_date: date | None = None
    historical_period: str = Field(min_length=1, max_length=100)
    event_category: str = Field(min_length=1, max_length=100)
    geographic_region: str = Field(min_length=1, max_length=150)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    @field_validator("description", mode="before")
    @classmethod
    def blank_description(cls, value: object) -> object:
        return empty_to_none(value)

    @model_validator(mode="after")
    def check_ranges(self) -> "EventCreate":
        ensure_date_order(self.start_date, self.end_date, "start_date", "end_date")
        ensure_coordinate_pair(self.latitude, self.longitude)
        return self


class EventUpdate(APIModel):
    """Partial update. Omitted fields are left unchanged by a future endpoint."""

    title: str | None = Field(default=None, min_length=1, max_length=300)
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    historical_period: str | None = Field(default=None, min_length=1, max_length=100)
    event_category: str | None = Field(default=None, min_length=1, max_length=100)
    geographic_region: str | None = Field(default=None, min_length=1, max_length=150)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    @field_validator("description", mode="before")
    @classmethod
    def blank_description(cls, value: object) -> object:
        return empty_to_none(value)

    @model_validator(mode="after")
    def check_ranges(self) -> "EventUpdate":
        ensure_date_order(self.start_date, self.end_date, "start_date", "end_date")
        if "latitude" in self.model_fields_set or "longitude" in self.model_fields_set:
            ensure_coordinate_pair(self.latitude, self.longitude)
        return self


class EventRead(EventCreate):
    """Event returned to API clients."""

    id: int
    created_at: datetime
    updated_at: datetime
