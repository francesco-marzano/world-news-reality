"""Properties of the configuration model, checked on generated inputs."""

from typing import Any

import pytest
import yaml
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

from world_news_reality.config import MetricsConfig

shares = st.floats(min_value=0.0, max_value=1.0, allow_nan=False)
categories = st.lists(
    st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1, max_size=12), unique=True, max_size=5
)


@st.composite
def valid_configs(draw: st.DrawFn) -> dict[str, Any]:
    min_story_countries = draw(st.integers(min_value=2, max_value=10))
    bs_min_countries = draw(st.integers(min_value=min_story_countries, max_value=60))
    grace_hours = draw(st.integers(min_value=0, max_value=72))
    return {
        "method_version": ".".join(str(draw(st.integers(0, 99))) for _ in range(3)),
        "window_hours": draw(st.integers(min_value=1, max_value=168)),
        "dup_threshold": draw(shares),
        "min_story_countries": min_story_countries,
        "bs_min_countries": bs_min_countries,
        "bs_min_own_countries": draw(st.integers(min_value=1, max_value=bs_min_countries)),
        "bs_max_it_outlets": draw(st.integers(min_value=0, max_value=20)),
        "panel_health_min": draw(shares),
        "grace_hours": grace_hours,
        "gdelt_timeout_hours": draw(st.integers(min_value=max(1, grace_hours), max_value=72)),
        "location_min_share": draw(shares),
        "relevance_normalization": draw(st.sampled_from(["log", "rank"])),
        "excluded_categories": draw(categories),
    }


@given(valid_configs())
def test_every_consistent_config_is_accepted(raw: dict[str, Any]) -> None:
    config = MetricsConfig.model_validate(raw)

    assert config.bs_min_own_countries <= config.bs_min_countries


@given(valid_configs())
def test_yaml_round_trip_preserves_the_config(raw: dict[str, Any]) -> None:
    config = MetricsConfig.model_validate(raw)

    reloaded = MetricsConfig.model_validate(yaml.safe_load(yaml.safe_dump(config.model_dump())))

    assert reloaded == config


@given(valid_configs(), st.integers(min_value=1, max_value=50))
def test_own_countries_above_countries_is_always_rejected(raw: dict[str, Any], extra: int) -> None:
    raw["bs_min_own_countries"] = raw["bs_min_countries"] + extra

    with pytest.raises(ValidationError):
        MetricsConfig.model_validate(raw)


@given(
    valid_configs(),
    st.sampled_from(["dup_threshold", "panel_health_min", "location_min_share"]),
    st.one_of(st.floats(max_value=-1e-9), st.floats(min_value=1.0 + 1e-9), st.just(float("nan"))),
)
def test_shares_outside_zero_one_are_always_rejected(
    raw: dict[str, Any], field: str, value: float
) -> None:
    raw[field] = value

    with pytest.raises(ValidationError):
        MetricsConfig.model_validate(raw)
