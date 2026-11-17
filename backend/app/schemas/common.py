"""Shared Pydantic helpers for request and response models."""

from datetime import date

from pydantic import BaseModel, ConfigDict


class APIModel(BaseModel):
    """Base schema: reject unknown fields and read SQLAlchemy rows."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        from_attributes=True,
    )


def empty_to_none(value: object) -> object:
    """Treat a blank string as a missing optional value."""
    if isinstance(value, str) and value.strip() == "":
        return None
    return value


def ensure_date_order(
    start: date | None,
    end: date | None,
    start_label: str,
    end_label: str,
) -> None:
    """Raise when an end date falls before its start date."""
    if start is not None and end is not None and end < start:
        raise ValueError(f"{end_label} must be on or after {start_label}")


def ensure_coordinate_pair(latitude: float | None, longitude: float | None) -> None:
    """Require latitude and longitude to be set together."""
    if (latitude is None) != (longitude is None):
        raise ValueError("latitude and longitude must both be provided or both omitted")
