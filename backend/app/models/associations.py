"""Many-to-many association tables between events and related records.

An event may cite many locations, people, organizations, and sources, and each
of those records may be linked to many events. Deleting an event or a related
record removes only the link rows. The related record itself is kept.
"""

from sqlalchemy import Column, ForeignKey, Index, Table

from app.models.base import Base

event_locations = Table(
    "event_locations",
    Base.metadata,
    Column("event_id", ForeignKey("events.id", ondelete="CASCADE"), primary_key=True),
    Column("location_id", ForeignKey("locations.id", ondelete="CASCADE"), primary_key=True),
    Index("ix_event_locations_location_id", "location_id"),
)

event_people = Table(
    "event_people",
    Base.metadata,
    Column("event_id", ForeignKey("events.id", ondelete="CASCADE"), primary_key=True),
    Column("person_id", ForeignKey("people.id", ondelete="CASCADE"), primary_key=True),
    Index("ix_event_people_person_id", "person_id"),
)

event_organizations = Table(
    "event_organizations",
    Base.metadata,
    Column("event_id", ForeignKey("events.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "organization_id",
        ForeignKey("organizations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Index("ix_event_organizations_organization_id", "organization_id"),
)

event_sources = Table(
    "event_sources",
    Base.metadata,
    Column("event_id", ForeignKey("events.id", ondelete="CASCADE"), primary_key=True),
    Column("source_id", ForeignKey("sources.id", ondelete="CASCADE"), primary_key=True),
    Index("ix_event_sources_source_id", "source_id"),
)
