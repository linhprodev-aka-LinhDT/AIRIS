from __future__ import annotations

from fastapi.testclient import TestClient

from src.api.app import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["demo_mode"] is True


def test_schools_endpoint_returns_demo_data() -> None:
    response = client.get("/api/schools")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["schools"], list)
    assert len(payload["schools"]) >= 1
    assert payload["schools"][0]["school_id"]


def test_events_endpoint_omits_identity_fields() -> None:
    response = client.get("/api/events")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["events"], list)
    if payload["events"]:
        event = payload["events"][0]
        assert "track_id" not in event or event["track_id"] is None
        assert "student_id" not in event
        assert "face" not in event


def test_statistics_endpoint_reuses_demo_aggregate_data() -> None:
    response = client.get("/api/statistics")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total_events"] >= 0
    assert "daily" in payload
    assert "hourly" in payload


def test_heatmap_endpoint_has_density_ranges() -> None:
    response = client.get("/api/heatmap")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["zones"], list)
    assert payload["zones"]
    first = payload["zones"][0]
    assert "smoke_density" in first
    assert "level" in first
