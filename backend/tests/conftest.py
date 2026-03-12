"""Shared test fixtures."""

import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_alerts():
    with open(FIXTURES_DIR / "sample_alerts.json", encoding="utf-8") as f:
        return json.load(f)
