"""Tests for oref_client module."""

import os
from unittest.mock import patch

import httpx
import pytest
import respx

from oref_client import OREF_HEADERS, OREF_HISTORY_URL, fetch_alerts, _cache


@pytest.fixture(autouse=True)
def clear_cache():
    _cache.clear()
    yield
    _cache.clear()


@pytest.fixture(autouse=True)
def no_mock_mode():
    with patch.dict(os.environ, {"USE_MOCK_DATA": "false"}, clear=False):
        yield


@respx.mock
@pytest.mark.asyncio
async def test_correct_headers_sent():
    route = respx.get(OREF_HISTORY_URL).mock(return_value=httpx.Response(200, json=[]))
    await fetch_alerts()
    request = route.calls[0].request
    assert request.headers["referer"] == "https://www.oref.org.il/"
    assert request.headers["x-requested-with"] == "XMLHttpRequest"


@respx.mock
@pytest.mark.asyncio
async def test_returns_alert_list():
    mock_data = [{"alertDate": "2025-07-15 08:30:00", "title": "test", "data": "area", "category": 1}]
    respx.get(OREF_HISTORY_URL).mock(return_value=httpx.Response(200, json=mock_data))
    result = await fetch_alerts()
    assert result == mock_data


@respx.mock
@pytest.mark.asyncio
async def test_empty_response():
    respx.get(OREF_HISTORY_URL).mock(return_value=httpx.Response(200, json={}))
    result = await fetch_alerts()
    assert result == []


@respx.mock
@pytest.mark.asyncio
async def test_http_error_raises():
    respx.get(OREF_HISTORY_URL).mock(return_value=httpx.Response(403))
    with pytest.raises(httpx.HTTPStatusError):
        await fetch_alerts()


@pytest.mark.asyncio
async def test_mock_mode_loads_fixture():
    with patch.dict(os.environ, {"USE_MOCK_DATA": "true"}):
        result = await fetch_alerts()
        assert len(result) > 0
        assert result[0]["title"] in ("ירי רקטות וטילים", "חדירת כלי טיס עוין", "האירוע הסתיים")


@pytest.mark.asyncio
async def test_mock_mode_returns_all_data_regardless_of_dates():
    from datetime import datetime
    with patch.dict(os.environ, {"USE_MOCK_DATA": "true"}):
        result = await fetch_alerts(
            date_from=datetime(2025, 7, 16, 0, 0, 0),
            date_to=datetime(2025, 7, 16, 23, 59, 59),
        )
        # Mock mode returns all fixture data regardless of date range
        assert len(result) == 23
