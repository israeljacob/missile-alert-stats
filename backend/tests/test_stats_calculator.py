"""Tests for stats_calculator module."""

from stats_calculator import calculate_stats


def test_pairs_rocket_alert_with_end_event(sample_alerts):
    stats = calculate_stats(sample_alerts, "ירושלים - מערב")
    # 3 rocket alerts for Jerusalem West, but only 2 have matching end events
    # (the 18:00 one has no end)
    assert stats["events_count"] == 2


def test_pairs_hostile_aircraft_with_end_event(sample_alerts):
    stats = calculate_stats(sample_alerts, "חיפה - מערב")
    assert stats["events_count"] == 2
    # First: 10:00 - 10:15 = 900s, Second: 06:00 - 06:20 = 1200s
    assert stats["total_shelter_seconds"] == 900 + 1200


def test_multiple_events_same_area(sample_alerts):
    stats = calculate_stats(sample_alerts, "תל אביב - מרכז העיר")
    assert stats["events_count"] == 2
    # First: 09:00 - 09:10 = 600s, Second: 20:00 - 20:03 = 180s
    assert stats["total_shelter_seconds"] == 600 + 180


def test_missing_end_event_excluded(sample_alerts):
    """Alert at 18:00 for Jerusalem West has no matching end event."""
    stats = calculate_stats(sample_alerts, "ירושלים - מערב")
    starts = [e["start"] for e in stats["events"]]
    assert "2025-07-15 18:00:00" not in starts


def test_area_with_no_events():
    stats = calculate_stats([], "אילת")
    assert stats["events_count"] == 0
    assert stats["total_shelter_seconds"] == 0
    assert stats["events"] == []


def test_overlapping_alerts_different_areas(sample_alerts):
    """Ashkelon and Sderot have near-simultaneous alerts."""
    ashkelon = calculate_stats(sample_alerts, "אשקלון - דרום")
    sderot = calculate_stats(sample_alerts, "שדרות, איבים, ניר עם")
    assert ashkelon["events_count"] == 1
    assert sderot["events_count"] == 1
    # Ashkelon: 16:30 - 16:32:30 = 150s
    assert ashkelon["total_shelter_seconds"] == 150
    # Sderot: 16:31 - 16:32:30 = 90s
    assert sderot["total_shelter_seconds"] == 90


def test_duration_calculation_accuracy(sample_alerts):
    stats = calculate_stats(sample_alerts, "ירושלים - מערב")
    # First event: 08:30:00 - 08:31:30 = 90 seconds
    assert stats["events"][0]["duration_seconds"] == 90
    # Second event: 12:00:00 - 12:02:00 = 120 seconds
    assert stats["events"][1]["duration_seconds"] == 120
    assert stats["total_shelter_seconds"] == 210


def test_event_type_preserved(sample_alerts):
    stats = calculate_stats(sample_alerts, "חיפה - מערב")
    assert stats["events"][0]["type"] == "חדירת כלי טיס עוין"


def test_petach_tikva_events(sample_alerts):
    stats = calculate_stats(sample_alerts, "פתח תקווה")
    assert stats["events_count"] == 2
    # First: 14:00 - 14:05 = 300s, Second: 08:00 - 08:02:30 = 150s
    assert stats["total_shelter_seconds"] == 300 + 150
