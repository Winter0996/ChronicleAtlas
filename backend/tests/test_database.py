"""Tests for schema creation and event relationships."""

from datetime import date

import pytest
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import engine, init_db
from app.models import (
    Event,
    Location,
    Organization,
    Person,
    Source,
    event_locations,
)
from app.schemas import EventRead


def test_init_db_creates_expected_tables() -> None:
    init_db()
    init_db()

    table_names = set(inspect(engine).get_table_names())
    assert {
        "events",
        "locations",
        "people",
        "organizations",
        "sources",
        "event_locations",
        "event_people",
        "event_organizations",
        "event_sources",
    } <= table_names


def test_event_links_to_related_records(db_session: Session) -> None:
    location = Location(name="Pearl Harbor", region="Hawaii", latitude=21.365, longitude=-157.95)
    person = Person(name="Husband E. Kimmel")
    organization = Organization(
        name="United States Pacific Fleet",
        organization_type="military",
    )
    source = Source(title="At Dawn We Slept", author="Gordon Prange", source_type="book")
    event = Event(
        title="Attack on Pearl Harbor",
        description="Carrier aircraft attacked the United States Pacific Fleet.",
        start_date=date(1941, 12, 7),
        end_date=date(1941, 12, 7),
        historical_period="World War II",
        event_category="battle",
        geographic_region="Pacific",
        latitude=21.365,
        longitude=-157.95,
        locations=[location],
        people=[person],
        organizations=[organization],
        sources=[source],
    )
    db_session.add(event)
    db_session.commit()

    stored = db_session.get(Event, event.id)
    assert stored is not None
    assert stored.locations[0].name == "Pearl Harbor"
    assert stored.people[0].name == "Husband E. Kimmel"
    assert stored.organizations[0].name == "United States Pacific Fleet"
    assert stored.sources[0].title == "At Dawn We Slept"
    EventRead.model_validate(stored)

    event_id = stored.id
    person_id = person.id
    db_session.delete(stored)
    db_session.commit()

    assert db_session.get(Person, person_id) is not None
    remaining_links = db_session.execute(
        text("SELECT COUNT(*) FROM event_people WHERE event_id = :event_id"),
        {"event_id": event_id},
    ).scalar_one()
    assert remaining_links == 0


def test_association_foreign_keys_are_enforced(db_session: Session) -> None:
    with pytest.raises(IntegrityError):
        db_session.execute(event_locations.insert().values(event_id=999, location_id=999))
        db_session.commit()
    db_session.rollback()
