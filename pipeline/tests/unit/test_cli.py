from pathlib import Path
from typing import Any

import yaml
from typer.testing import CliRunner

from world_news_reality import __version__
from world_news_reality.cli import app

runner = CliRunner()


def test_version_prints_package_version() -> None:
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == __version__


def test_config_check_accepts_published_defaults(repo_root: Path) -> None:
    metrics = repo_root / "config" / "metrics.yaml"

    result = runner.invoke(app, ["config", "check", "--metrics", str(metrics)])

    assert result.exit_code == 0
    assert "ok (method" in result.stdout


def test_config_check_fails_on_invalid_file(tmp_path: Path, valid_metrics: dict[str, Any]) -> None:
    metrics = tmp_path / "metrics.yaml"
    metrics.write_text(yaml.safe_dump(valid_metrics | {"dup_threshold": 1.5}), encoding="utf-8")

    result = runner.invoke(app, ["config", "check", "--metrics", str(metrics)])

    assert result.exit_code == 1
    assert "dup_threshold" in result.stderr


def test_schemas_export_writes_files(tmp_path: Path) -> None:
    result = runner.invoke(app, ["schemas", "export", "--out", str(tmp_path)])

    assert result.exit_code == 0
    assert (tmp_path / "metrics-config.schema.json").is_file()
