"""FastAPI application for missile alert statistics."""

from datetime import datetime, timedelta

import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from areas import AREAS
from oref_client import fetch_alerts
from stats_calculator import calculate_stats

app = FastAPI(title="Missile Alert Statistics")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/areas")
async def get_areas():
    if os.environ.get("USE_MOCK_DATA", "").lower() in ("true", "1", "yes"):
        # In mock mode, only return areas that have data in the fixture
        import json
        from pathlib import Path
        fixture = Path(__file__).parent / "tests" / "fixtures" / "sample_alerts.json"
        with open(fixture, encoding="utf-8") as f:
            alerts = json.load(f)
        mock_areas = sorted(set(a["data"] for a in alerts))
        return {"areas": mock_areas}
    return {"areas": AREAS}


@app.get("/api/stats")
async def get_stats(
    area: str = Query("_ALL", description="Area name in Hebrew or '_ALL' for all areas average"),
    range: str = Query("1d", description="Time range: 1d, 1w, or custom"),
    from_date: str | None = Query(None, alias="from", description="Start date (ISO format) for custom range"),
    to_date: str | None = Query(None, alias="to", description="End date (ISO format) for custom range"),
):
    now = datetime.now()

    if range == "1d":
        date_from = now - timedelta(days=1)
        date_to = now
    elif range == "1w":
        date_from = now - timedelta(weeks=1)
        date_to = now
    elif range == "custom":
        if not from_date or not to_date:
            raise HTTPException(status_code=400, detail="from and to dates required for custom range")
        date_from = datetime.fromisoformat(from_date)
        date_to = datetime.fromisoformat(to_date)
    else:
        raise HTTPException(status_code=400, detail=f"Invalid range: {range}")

    alerts = await fetch_alerts(date_from=date_from, date_to=date_to)
    stats = calculate_stats(alerts, area)
    return stats
