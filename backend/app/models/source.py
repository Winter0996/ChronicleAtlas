"""Source records for works that document historical events."""

from datetime import date

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.associations import event_sources
from app.models.base import Base, TimestampMixin


class Source(TimestampMixin, Base):
    """A book, article, archive, website, or other cited work.

    ``source_type`` is a free-text label such as ``book`` or ``archive``.
    Bibliographic fields other than the title may be unknown.
    """

    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    author: Mapped[str | None] = mapped_column(String(300))
    publisher: Mapped[str | None] = mapped_column(String(300))
    publication_date: Mapped[date | None] = mapped_column()
    url: Mapped[str | None] = mapped_column(String(2048))
    source_type: Mapped[str | None] = mapped_column(String(100))
    notes: Mapped[str | None] = mapped_column(Text())

    events: Mapped[list["Event"]] = relationship(
        secondary=event_sources,
        back_populates="sources",
    )
