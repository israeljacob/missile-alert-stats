"""Pikud HaOref alert data provider.

Loads alerts from a local JSON file scraped by scraper.py, with
date-range filtering. Falls back to mock data when USE_MOCK_DATA is set.

Run `python scraper.py month` to refresh the data.
"""

import json
import os
from datetime import datetime
from pathlib import Path

SCRAPED_DATA_PATH = Path(__file__).parent / "alerts_history.json"
MOCK_DATA_PATH = Path(__file__).parent / "tests" / "fixtures" / "sample_alerts.json"

# In-memory cache for the loaded file
_cache: dict[str, tuple[float, list]] = {}
CACHE_TTL = 300  # 5 minutes


def _get_cached(key: str) -> list | None:
    if key in _cache:
        ts, data = _cache[key]
        if datetime.now().timestamp() - ts < CACHE_TTL:
            return data
        del _cache[key]
    return None


def _set_cache(key: str, data: list) -> None:
    _cache[key] = (datetime.now().timestamp(), data)


def _load_mock_data() -> list[dict]:
    with open(MOCK_DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def _load_scraped_data() -> list[dict]:
    if not SCRAPED_DATA_PATH.exists():
        raise FileNotFoundError(
            f"{SCRAPED_DATA_PATH} not found. Run 'python scraper.py month' first."
        )
    with open(SCRAPED_DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


async def fetch_alerts(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[dict]:
    """Load alerts from scraped data or mock data, filtered by date range.

    Args:
        date_from: Start date for the query range.
        date_to: End date for the query range.

    Returns:
        List of alert dicts with alertDate, title, data, category fields.
    """
    if os.environ.get("USE_MOCK_DATA", "").lower() in ("true", "1", "yes"):
        return _load_mock_data()

    cache_key = f"{date_from}:{date_to}"
    cached = _get_cached(cache_key)
    if cached is not None:
        return cached

    alerts = _load_scraped_data()

    # Filter by date range
    if date_from and date_to:
        filtered = []
        for a in alerts:
            try:
                # Handle ISO format: 2026-03-12T09:41:00
                alert_dt = datetime.fromisoformat(a["alertDate"])
                if date_from <= alert_dt <= date_to:
                    filtered.append(a)
            except (KeyError, ValueError):
                continue
        alerts = filtered

    _set_cache(cache_key, alerts)
    return alerts
