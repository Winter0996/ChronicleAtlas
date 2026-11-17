"""Tests for GET /api/health."""

from fastapi.testclient import TestClient


def test_health_reports_ok(client: TestClient) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "database": "ok",
        "environment": "test",
    }


def test_unknown_route_is_not_found(client: TestClient) -> None:
    response = client.get("/api/missing")

    assert response.status_code == 404
