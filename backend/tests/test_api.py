"""FastAPI endpoint integration tests."""

import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

# Enable mock mode for all API tests
with patch.dict(os.environ, {"USE_MOCK_DATA": "true"}):
    from main import app

client = TestClient(app)


def test_get_areas():
    response = client.get("/api/areas")
    assert response.status_code == 200
    data = response.json()
    assert "areas" in data
    assert isinstance(data["areas"], list)
    assert len(data["areas"]) > 0
    assert "ירושלים - מערב" in data["areas"]


def test_get_stats_returns_correct_structure():
    with patch.dict(os.environ, {"USE_MOCK_DATA": "true"}):
        response = client.get("/api/stats", params={
            "area": "ירושלים - מערב",
            "range": "custom",
            "from": "2025-07-15",
            "to": "2025-07-16",
        })
    assert response.status_code == 200
    data = response.json()
    assert "events_count" in data
    assert "total_shelter_seconds" in data
    assert "events" in data
    assert isinstance(data["events"], list)


def test_get_stats_1d_range():
    with patch.dict(os.environ, {"USE_MOCK_DATA": "true"}):
        response = client.get("/api/stats", params={
            "area": "ירושלים - מערב",
            "range": "1d",
        })
    assert response.status_code == 200


def test_get_stats_missing_area():
    response = client.get("/api/stats", params={"range": "1d"})
    assert response.status_code == 422  # FastAPI validation error


def test_get_stats_custom_missing_dates():
    with patch.dict(os.environ, {"USE_MOCK_DATA": "true"}):
        response = client.get("/api/stats", params={
            "area": "ירושלים - מערב",
            "range": "custom",
        })
    assert response.status_code == 400
