"""Event records, the central entity in Chronicle Atlas."""

from datetime import date

from sqlalchemy import CheckConstraint, Float, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.associations import (
    event_locations,
    event_organizations,
    event_people,
    event_sources,
)
from app.models.base import Base, TimestampMixin


class Event(TimestampMixin, Base):
    """A historical event with its own summary geography and related records.

    ``geographic_region`` is a broad label such as ``Pacific`` or ``Japan``.
    Specific places belong in linked ``Location`` rows. Optional coordinates
    describe the event itself and must be stored as a pair.
    """

    __tablename__ = "events"
    __table_args__ = (
        CheckConstraint(
            "end_date IS NULL OR end_date >= start_date",
            name="ck_events_date_order",
        ),
        CheckConstraint(
            "latitude IS NULL OR (latitude >= -90 AND latitude <= 90)",
            name="ck_events_latitude",
        ),
        CheckConstraint(
            "longitude IS NULL OR (longitude >= -180 AND longitude <= 180)",
            name="ck_events_longitude",
        ),
        CheckConstraint(
            "(latitude IS NULL) = (longitude IS NULL)",
            name="ck_events_coordinate_pair",
        ),
        Index("ix_events_start_date", "start_date"),
        Index("ix_events_historical_period", "historical_period"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str | None] = mapped_column(Text())
    start_date: Mapped[date] = mapped_column(nullable=False)
    end_date: Mapped[date | None] = mapped_column()
    historical_period: Mapped[str] = mapped_column(String(100), nullable=False)
    event_category: Mapped[str] = mapped_column(String(100), nullable=False)
    geographic_region: Mapped[str] = mapped_column(String(150), nullable=False)
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)

    locations: Mapped[list["Location"]] = relationship(
        secondary=event_locations,
        back_populates="events",
    )
    people: Mapped[list["Person"]] = relationship(
        secondary=event_people,
        back_populates="events",
    )
    organizations: Mapped[list["Organization"]] = relationship(
        secondary=event_organizations,
        back_populates="events",
    )
    sources: Mapped[list["Source"]] = relationship(
        secondary=event_sources,
        back_populates="events",
    )
