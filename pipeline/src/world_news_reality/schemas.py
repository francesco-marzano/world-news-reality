"""JSON Schemas generated from the pydantic models.

The files in ``schemas/`` are the data contract between pipeline and web. They are
generated, never edited by hand: ``wnr schemas export`` writes them and a contract
test fails when they drift from the models.
"""

import json
from pathlib import Path

from pydantic import BaseModel

from world_news_reality.config import MetricsConfig

SCHEMA_MODELS: dict[str, type[BaseModel]] = {
    "metrics-config.schema.json": MetricsConfig,
}


def render_schema(model: type[BaseModel]) -> str:
    """Return the JSON Schema of ``model`` as stable, diff-friendly text."""
    return json.dumps(model.model_json_schema(), indent=2, sort_keys=True) + "\n"


def export_schemas(out_dir: Path) -> list[Path]:
    """Write every schema into ``out_dir`` and return the written paths."""
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for filename, model in SCHEMA_MODELS.items():
        target = out_dir / filename
        target.write_text(render_schema(model), encoding="utf-8", newline="\n")
        written.append(target)
    return written
