"""Pytest fixtures. The test database URL is set before the app is imported."""

from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path

_TEST_DB = Path(__file__).resolve().parent / "_test_chronicle.db"
os.environ["DATABASE_URL"] = f"sqlite:///{_TEST_DB.as_posix()}"
os.environ["ENVIRONMENT"] = "test"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import app.models  # noqa: F401, E402
from app.core.database import SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models.base import Base  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_database() -> Generator[None, None, None]:
    """Give each test an empty schema in the shared SQLite file."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Yield a session that rolls back and closes if the test fails."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """HTTP client that runs the application lifespan."""
    with TestClient(app) as test_client:
        yield test_client


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Release the SQLite file created for the test run."""
    del session, exitstatus
    engine.dispose()
    if _TEST_DB.exists():
        _TEST_DB.unlink()
