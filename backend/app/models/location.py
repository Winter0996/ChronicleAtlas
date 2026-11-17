"""Location records for places connected to historical events."""

from sqlalchemy import CheckConstraint, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.associations import event_locations
from app.models.base import Base, TimestampMixin


class Location(TimestampMixin, Base):
    """A named place that can be linked to one or more events.

    ``region`` is a free-text label such as a country, prefecture, or theater.
    Coordinates are optional and, when present, must be stored as a pair.
    """

    __tablename__ = "locations"
    __table_args__ = (
        CheckConstraint(
            "latitude IS NULL OR (latitude >= -90 AND latitude <= 90)",
            name="ck_locations_latitude",
        ),
        CheckConstraint(
            "longitude IS NULL OR (longitude >= -180 AND longitude <= 180)",
            name="ck_locations_longitude",
        ),
        CheckConstraint(
            "(latitude IS NULL) = (longitude IS NULL)",
            name="ck_locations_coordinate_pair",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(300), nullable=False)
    region: Mapped[str | None] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(Text())
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)

    events: Mapped[list["Event"]] = relationship(
        secondary=event_locations,
        back_populates="locations",
    )
