"""Automatic update checker for missile alert statistics."""

import json
import threading
import time
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "alerts_history.json"
STATE_FILE = BASE_DIR / "last_check_time.json"

def _load_last_check_time() -> datetime:
    if STATE_FILE.exists():
        try:
            return datetime.fromisoformat(STATE_FILE.read_text().strip())
        except Exception:
            pass
    return datetime.min

def _save_last_check_time(dt: datetime) -> None:
    STATE_FILE.write_text(dt.isoformat())

def _latest_alert_date(data: list) -> str | None:
    dates = [item.get("alertDate") for item in data if item.get("alertDate")]
    return max(dates) if dates else None

def check_for_updates() -> None:
    """Check for newer alerts data and update alerts_history.json if found."""
    last_check = _load_last_check_time()
    # Load existing data if any
    existing_data = json.loads(DATA_FILE.read_text(encoding="utf-8")) if DATA_FILE.exists() else []
    existing_max_date = _latest_alert_date(existing_data)

    # Scrape new data using the scraper module
    from scraper import scrape_alerts
    print("[BackgroundUpdater] Checking for updates...")
    new_data = scrape_alerts(mode="month")
    new_max_date = _latest_alert_date(new_data)

    if new_max_date and (existing_max_date is None or new_max_date > existing_max_date):
        print("[BackgroundUpdater] Newer data found, updating alerts_history.json")
        DATA_FILE.write_text(json.dumps(new_data, ensure_ascii=False, indent=2))
        _save_last_check_time(datetime.now())
    else:
        print("[BackgroundUpdater] No newer data found")

def _run_scheduler() -> None:
    """Run check_for_updates every 15 minutes, handling errors."""
    while True:
        try:
            check_for_updates()
        except Exception as e:
            print(f"[BackgroundUpdater] Error during update check: {e}")
        time.sleep(900)  # 15 minutes

# Start the scheduler thread as daemon
_thread = threading.Thread(target=_run_scheduler, daemon=True)
_thread.start()