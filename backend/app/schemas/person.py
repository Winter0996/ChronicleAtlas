"""Request and response schemas for people."""

from datetime import date, datetime

from pydantic import Field, field_validator, model_validator

from app.schemas.common import APIModel, empty_to_none, ensure_date_order


class PersonCreate(APIModel):
    """Fields required to record a person."""

    name: str = Field(min_length=1, max_length=300)
    biography: str | None = None
    birth_date: date | None = None
    death_date: date | None = None

    @field_validator("biography", mode="before")
    @classmethod
    def blank_biography(cls, value: object) -> object:
        return empty_to_none(value)

    @model_validator(mode="after")
    def check_dates(self) -> "PersonCreate":
        ensure_date_order(self.birth_date, self.death_date, "birth_date", "death_date")
        return self


class PersonUpdate(APIModel):
    """Partial update for a person."""

    name: str | None = Field(default=None, min_length=1, max_length=300)
    biography: str | None = None
    birth_date: date | None = None
    death_date: date | None = None

    @field_validator("biography", mode="before")
    @classmethod
    def blank_biography(cls, value: object) -> object:
        return empty_to_none(value)

    @model_validator(mode="after")
    def check_dates(self) -> "PersonUpdate":
        ensure_date_order(self.birth_date, self.death_date, "birth_date", "death_date")
        return self


class PersonRead(PersonCreate):
    """Person returned to API clients."""

    id: int
    created_at: datetime
    updated_at: datetime
