"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.router import api_router
from app.core.config import get_settings
from app.core.database import init_db

logger = logging.getLogger("chronicle_atlas")


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Create database tables on startup."""
    del application
    init_db()
    logger.info("Database schema is ready")
    yield


def create_app() -> FastAPI:
    """Build the FastAPI application."""
    settings = get_settings()
    logging.basicConfig(level=logging.INFO)
    application = FastAPI(title=settings.app_name, lifespan=lifespan)
    application.include_router(api_router, prefix=settings.api_prefix)

    @application.exception_handler(SQLAlchemyError)
    async def handle_database_error(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        """Hide database internals and report that the dependency is unavailable."""
        logger.exception("Database error on %s", request.url.path, exc_info=exc)
        return JSONResponse(
            status_code=503,
            content={"detail": "Database unavailable"},
        )

    return application


app = create_app()
