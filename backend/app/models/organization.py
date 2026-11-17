"""Organization records for groups connected to historical events."""

from datetime import date

from sqlalchemy import CheckConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.associations import event_organizations
from app.models.base import Base, TimestampMixin


class Organization(TimestampMixin, Base):
    """A government, military unit, institution, or other group.

    ``organization_type`` is a free-text label so new kinds of groups can be
    recorded without a schema change.
    """

    __tablename__ = "organizations"
    __table_args__ = (
        CheckConstraint(
            "dissolved_date IS NULL OR founded_date IS NULL OR dissolved_date >= founded_date",
            name="ck_organizations_active_dates",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    organization_type: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text())
    founded_date: Mapped[date | None] = mapped_column()
    dissolved_date: Mapped[date | None] = mapped_column()

    events: Mapped[list["Event"]] = relationship(
        secondary=event_organizations,
        back_populates="organizations",
    )
