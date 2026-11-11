from pathlib import Path
from typing import Any

import pytest
import yaml
from pydantic import ValidationError

from world_news_reality.config import MetricsConfig, load_metrics_config


def test_published_defaults_are_valid(repo_root: Path) -> None:
    config = load_metrics_config(repo_root / "config" / "metrics.yaml")

    assert config.bs_min_countries == 8
    assert config.bs_min_own_countries == 4
    assert config.bs_max_it_outlets == 1
    assert config.excluded_categories == ("sport",)


def test_unknown_key_is_rejected(valid_metrics: dict[str, Any]) -> None:
    valid_metrics["bs_min_countires"] = 8  # a typo must not fall back to a default

    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        MetricsConfig.model_validate(valid_metrics)


def test_missing_key_is_rejected(valid_metrics: dict[str, Any]) -> None:
    del valid_metrics["grace_hours"]

    with pytest.raises(ValidationError, match="grace_hours"):
        MetricsConfig.model_validate(valid_metrics)


@pytest.mark.parametrize(
    ("override", "message"),
    [
        ({"bs_min_own_countries": 9}, "bs_min_own_countries cannot exceed"),
        ({"min_story_countries": 9}, "bs_min_countries cannot be lower"),
        ({"gdelt_timeout_hours": 5}, "gdelt_timeout_hours cannot be shorter"),
        ({"excluded_categories": ["sport", "sport"]}, "duplicates"),
    ],
)
def test_inconsistent_thresholds_are_rejected(
    valid_metrics: dict[str, Any], override: dict[str, Any], message: str
) -> None:
    with pytest.raises(ValidationError, match=message):
        MetricsConfig.model_validate(valid_metrics | override)


@pytest.mark.parametrize("version", ["1.0", "v1.0.0", "1.0.0-rc1", ""])
def test_method_version_must_be_plain_semver(valid_metrics: dict[str, Any], version: str) -> None:
    with pytest.raises(ValidationError, match="method_version"):
        MetricsConfig.model_validate(valid_metrics | {"method_version": version})


def test_config_is_immutable(valid_metrics: dict[str, Any]) -> None:
    config = MetricsConfig.model_validate(valid_metrics)

    with pytest.raises(ValidationError, match="frozen"):
        config.grace_hours = 0  # type: ignore[misc]


def test_load_reads_utf8_yaml(tmp_path: Path, valid_metrics: dict[str, Any]) -> None:
    path = tmp_path / "metrics.yaml"
    path.write_text(yaml.safe_dump(valid_metrics), encoding="utf-8")

    assert load_metrics_config(path) == MetricsConfig.model_validate(valid_metrics)
