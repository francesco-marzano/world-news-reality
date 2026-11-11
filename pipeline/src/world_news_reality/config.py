"""Method parameters, loaded from ``config/metrics.yaml``.

Every field changes published numbers. The model is strict on purpose: an unknown
key or an out-of-range value stops the run instead of silently using a default.
"""

from pathlib import Path
from typing import Annotated, Literal, Self

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

Share = Annotated[float, Field(ge=0.0, le=1.0)]
SEMVER_PATTERN = r"^\d+\.\d+\.\d+$"


class MetricsConfig(BaseModel):
    """Parameters of the blind-spot method. See PROJECT_BRIEF.md, section 3."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    method_version: str = Field(pattern=SEMVER_PATTERN)

    window_hours: int = Field(ge=1, le=168)
    dup_threshold: Share
    min_story_countries: int = Field(ge=2)

    bs_min_countries: int = Field(ge=2)
    bs_min_own_countries: int = Field(ge=1)
    bs_max_it_outlets: int = Field(ge=0)
    panel_health_min: Share
    grace_hours: int = Field(ge=0, le=72)
    gdelt_timeout_hours: int = Field(ge=1, le=72)

    location_min_share: Share
    relevance_normalization: Literal["log", "rank"]
    excluded_categories: tuple[str, ...]

    @model_validator(mode="after")
    def _thresholds_are_consistent(self) -> Self:
        if self.bs_min_own_countries > self.bs_min_countries:
            msg = "bs_min_own_countries cannot exceed bs_min_countries"
            raise ValueError(msg)
        if self.bs_min_countries < self.min_story_countries:
            msg = "bs_min_countries cannot be lower than min_story_countries"
            raise ValueError(msg)
        if self.gdelt_timeout_hours < self.grace_hours:
            msg = "gdelt_timeout_hours cannot be shorter than grace_hours"
            raise ValueError(msg)
        if len(set(self.excluded_categories)) != len(self.excluded_categories):
            msg = "excluded_categories contains duplicates"
            raise ValueError(msg)
        return self


def load_metrics_config(path: Path) -> MetricsConfig:
    """Read and validate a metrics file. Raises ``ValidationError`` on bad content."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return MetricsConfig.model_validate(raw)
