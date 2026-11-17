"""Liveness endpoint for the API and its database."""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def read_health(db: Session = Depends(get_db)) -> HealthResponse:
    """Return application status after confirming the database accepts a query.

    Database failures propagate to the application error handler, which
    responds with HTTP 503.
    """
    db.execute(text("SELECT 1"))
    settings = get_settings()
    return HealthResponse(
        status="ok",
        database="ok",
        environment=settings.environment,
    )
