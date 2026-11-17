"""Import all models so SQLAlchemy registers their tables on the shared metadata."""

from app.models.associations import (
    event_locations,
    event_organizations,
    event_people,
    event_sources,
)
from app.models.base import Base
from app.models.event import Event
from app.models.location import Location
from app.models.organization import Organization
from app.models.person import Person
from app.models.source import Source

__all__ = [
    "Base",
    "Event",
    "Location",
    "Organization",
    "Person",
    "Source",
    "event_locations",
    "event_organizations",
    "event_people",
    "event_sources",
]
