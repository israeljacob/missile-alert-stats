"""Event matching and duration calculation logic for alert statistics."""

from datetime import datetime

ALERT_START_TITLES = {"ירי רקטות וטילים", "חדירת כלי טיס עוין"}
ALERT_END_TITLES = {"האירוע הסתיים", "ירי רקטות וטילים -  האירוע הסתיים"}


def parse_alert_date(date_str: str) -> datetime:
    """Parse alert date string in either ISO or space-separated format."""
    return datetime.fromisoformat(date_str)


def calculate_stats(alerts: list[dict], area: str) -> dict:
    """Calculate event statistics for a specific area or across all areas.

    Returns dict with events_count, total_shelter_seconds, and events list.
    When area is "_ALL", returns the average of each area's statistics.
    """
    if area == "_ALL":
        # Get all unique areas from alerts
        areas = sorted(set(a.get("data") for a in alerts if a.get("data")))
        if not areas:
            return {"events_count": 0, "total_shelter_seconds": 0, "events": []}

        # Calculate stats for each area
        all_events_counts = []
        all_total_seconds = []
        all_events = []

        for a in areas:
            area_stats = calculate_stats(alerts, a)
            all_events_counts.append(area_stats["events_count"])
            all_total_seconds.append(area_stats["total_shelter_seconds"])
            all_events.extend(area_stats["events"])

        # Return averages
        return {
            "events_count": sum(all_events_counts) / len(all_events_counts),
            "total_shelter_seconds": sum(all_total_seconds) / len(all_total_seconds),
            "events": all_events,
        }

    # Filter alerts for the given area and sort by timestamp
    area_alerts = [a for a in alerts if a.get("data") == area]
    area_alerts.sort(key=lambda a: a["alertDate"])

    events = []
    i = 0
    while i < len(area_alerts):
        alert = area_alerts[i]
        if alert.get("title") in ALERT_START_TITLES:
            start_time = parse_alert_date(alert["alertDate"])
            # Scan forward for matching end event
            end_time = None
            for j in range(i + 1, len(area_alerts)):
                if area_alerts[j].get("title") in ALERT_END_TITLES:
                    end_time = parse_alert_date(area_alerts[j]["alertDate"])
                    break
            if end_time is not None:
                duration = (end_time - start_time).total_seconds()
                events.append({
                    "start": alert["alertDate"],
                    "end": area_alerts[j]["alertDate"],
                    "duration_seconds": duration,
                    "type": alert["title"],
                })
        i += 1

    total_seconds = sum(e["duration_seconds"] for e in events)
    return {
        "events_count": len(events),
        "total_shelter_seconds": total_seconds,
        "events": events,
    }
