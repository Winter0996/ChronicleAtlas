"""Request and response schemas for sources."""

from datetime import date, datetime

from pydantic import Field, field_validator

from app.schemas.common import APIModel, empty_to_none


class SourceCreate(APIModel):
    """Fields accepted when recording a source."""

    title: str = Field(min_length=1, max_length=500)
    author: str | None = Field(default=None, max_length=300)
    publisher: str | None = Field(default=None, max_length=300)
    publication_date: date | None = None
    url: str | None = Field(default=None, max_length=2048)
    source_type: str | None = Field(default=None, max_length=100)
    notes: str | None = None

    @field_validator("author", "publisher", "url", "source_type", "notes", mode="before")
    @classmethod
    def blank_optional(cls, value: object) -> object:
        return empty_to_none(value)

    @field_validator("url")
    @classmethod
    def require_http_url(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError("url must start with http:// or https://")
        return value


class SourceUpdate(APIModel):
    """Partial update for a source."""

    title: str | None = Field(default=None, min_length=1, max_length=500)
    author: str | None = Field(default=None, max_length=300)
    publisher: str | None = Field(default=None, max_length=300)
    publication_date: date | None = None
    url: str | None = Field(default=None, max_length=2048)
    source_type: str | None = Field(default=None, max_length=100)
    notes: str | None = None

    @field_validator("author", "publisher", "url", "source_type", "notes", mode="before")
    @classmethod
    def blank_optional(cls, value: object) -> object:
        return empty_to_none(value)

    @field_validator("url")
    @classmethod
    def require_http_url(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError("url must start with http:// or https://")
        return value


class SourceRead(SourceCreate):
    """Source returned to API clients."""

    id: int
    created_at: datetime
    updated_at: datetime
