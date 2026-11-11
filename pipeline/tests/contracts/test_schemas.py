"""The committed JSON Schemas are the contract with the website: they must match the models."""

import json
from pathlib import Path

import pytest

from world_news_reality.schemas import SCHEMA_MODELS, render_schema


@pytest.mark.parametrize("filename", sorted(SCHEMA_MODELS))
def test_committed_schema_matches_model(repo_root: Path, filename: str) -> None:
    committed = (repo_root / "schemas" / filename).read_text(encoding="utf-8")

    assert committed == render_schema(SCHEMA_MODELS[filename]), (
        f"schemas/{filename} is stale: run `just schemas` and review the diff"
    )


def test_no_orphan_schema_files(repo_root: Path) -> None:
    on_disk = {path.name for path in (repo_root / "schemas").glob("*.json")}

    assert on_disk == set(SCHEMA_MODELS)


@pytest.mark.parametrize("filename", sorted(SCHEMA_MODELS))
def test_schema_forbids_unknown_fields(repo_root: Path, filename: str) -> None:
    schema = json.loads((repo_root / "schemas" / filename).read_text(encoding="utf-8"))

    assert schema["additionalProperties"] is False
