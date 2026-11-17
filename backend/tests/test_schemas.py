"""Validation coverage for the Pydantic schemas."""

from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas import EventCreate, LocationCreate, SourceCreate


def test_event_rejects_end_before_start() -> None:
    with pytest.raises(ValidationError):
        EventCreate(
            title="Example",
            start_date=date(1945, 8, 15),
            end_date=date(1945, 8, 14),
            historical_period="World War II",
            event_category="surrender",
            geographic_region="Japan",
        )


def test_event_rejects_a_single_coordinate() -> None:
    with pytest.raises(ValidationError):
        EventCreate(
            title="Example",
            start_date=date(1945, 8, 15),
            historical_period="World War II",
            event_category="surrender",
            geographic_region="Japan",
            latitude=35.68,
        )


def test_location_accepts_a_coordinate_pair() -> None:
    location = LocationCreate(name="Hiroshima", latitude=34.385, longitude=132.455)
    assert location.name == "Hiroshima"


def test_source_rejects_a_url_without_a_scheme() -> None:
    with pytest.raises(ValidationError):
        SourceCreate(title="Example archive", url="example.com/record")
