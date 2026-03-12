"""Scrape historical alert data from Pikud HaOref via Playwright.

Uses the alerts-history.oref.org.il iframe endpoint with city-batched
queries to work around the 3000-result cap.
"""

import json
import sys
import time
from pathlib import Path
from urllib.parse import urlencode

from playwright.sync_api import sync_playwright

BATCH_SIZE = 20  # cities per request
OUTPUT_PATH = Path(__file__).parent / "alerts_history.json"

# mode=1: 24h, mode=2: week, mode=3: month
MODE_MAP = {"day": "1", "week": "2", "month": "3"}


def scrape_alerts(mode: str = "month", output_path: Path = OUTPUT_PATH) -> list[dict]:
    """Scrape alerts for all cities.

    Args:
        mode: One of "day", "week", "month".
        output_path: Where to save the JSON output.

    Returns:
        List of all alert dicts.
    """
    mode_val = MODE_MAP.get(mode, "3")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Loading alerts-history page...")
        page.goto(
            "https://www.oref.org.il/heb/alerts-history/",
            wait_until="networkidle",
            timeout=30000,
        )
        page.wait_for_timeout(5000)

        # Find the iframe
        iframe = None
        for f in page.frames:
            if "Pakar.aspx" in f.url:
                iframe = f
                break

        if not iframe:
            print("ERROR: Could not find alerts-history iframe")
            browser.close()
            return []

        # Get city list
        print("Fetching city list...")
        cities_raw = iframe.evaluate(
            """async () => {
                const r = await fetch('/Shared/Ajax/GetCitiesMix.aspx?lang=he');
                return await r.text();
            }"""
        )
        cities = json.loads(cities_raw)
        city_names = [c["label_he"] for c in cities]
        print(f"Found {len(city_names)} cities")

        # Batch queries
        all_alerts = {}  # keyed by rid to deduplicate
        total_batches = (len(city_names) + BATCH_SIZE - 1) // BATCH_SIZE

        for batch_idx in range(0, len(city_names), BATCH_SIZE):
            batch = city_names[batch_idx : batch_idx + BATCH_SIZE]
            batch_num = batch_idx // BATCH_SIZE + 1

            # Build query params
            params = {"lang": "he", "mode": mode_val}
            for i, city in enumerate(batch):
                params[f"city_{i}"] = city

            query = urlencode(params)

            try:
                resp = iframe.evaluate(
                    f"""async () => {{
                        const r = await fetch('/Shared/Ajax/GetAlarmsHistory.aspx?{query}');
                        return await r.text();
                    }}"""
                )
                data = json.loads(resp)
                new_count = 0
                for alert in data:
                    rid = alert.get("rid")
                    if rid and rid not in all_alerts:
                        all_alerts[rid] = alert
                        new_count += 1

                print(
                    f"  Batch {batch_num}/{total_batches}: "
                    f"{len(data)} results, {new_count} new "
                    f"(total: {len(all_alerts)})"
                )

            except Exception as e:
                print(f"  Batch {batch_num}/{total_batches}: ERROR - {e}")

            # Small delay to be polite
            time.sleep(0.3)

        browser.close()

    # Sort by alertDate descending
    alerts_list = sorted(
        all_alerts.values(),
        key=lambda a: a.get("alertDate", ""),
        reverse=True,
    )

    # Normalize: add "title" field from category_desc for compatibility
    for alert in alerts_list:
        if "category_desc" in alert and "title" not in alert:
            alert["title"] = alert["category_desc"]

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(alerts_list, f, ensure_ascii=False, indent=2)

    # Summary
    dates = sorted(set(a["alertDate"][:10] for a in alerts_list))
    print(f"\nDone! {len(alerts_list)} alerts across {len(dates)} days")
    print(f"Date range: {dates[0] if dates else 'N/A'} to {dates[-1] if dates else 'N/A'}")
    print(f"Saved to: {output_path}")

    return alerts_list


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "month"
    if mode not in MODE_MAP:
        print(f"Usage: python scraper.py [day|week|month]")
        sys.exit(1)
    scrape_alerts(mode=mode)
