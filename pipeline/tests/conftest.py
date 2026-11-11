"""Shared fixtures. Tests never touch the network: pytest-socket blocks it."""

from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture
def valid_metrics() -> dict[str, Any]:
    """A minimal valid configuration, independent of the published defaults."""
    return {
        "method_version": "0.1.0",
        "window_hours": 36,
        "dup_threshold": 0.9,
        "min_story_countries": 2,
        "bs_min_countries": 8,
        "bs_min_own_countries": 4,
        "bs_max_it_outlets": 1,
        "panel_health_min": 0.8,
        "grace_hours": 6,
        "gdelt_timeout_hours": 12,
        "location_min_share": 0.4,
        "relevance_normalization": "log",
        "excluded_categories": ["sport"],
    }
