"""Person records for individuals connected to historical events."""

from datetime import date

from sqlalchemy import CheckConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.associations import event_people
from app.models.base import Base, TimestampMixin


class Person(TimestampMixin, Base):
    """A historical person who can be linked to one or more events."""

    __tablename__ = "people"
    __table_args__ = (
        CheckConstraint(
            "death_date IS NULL OR birth_date IS NULL OR death_date >= birth_date",
            name="ck_people_life_dates",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    biography: Mapped[str | None] = mapped_column(Text())
    birth_date: Mapped[date | None] = mapped_column()
    death_date: Mapped[date | None] = mapped_column()

    events: Mapped[list["Event"]] = relationship(
        secondary=event_people,
        back_populates="people",
    )
