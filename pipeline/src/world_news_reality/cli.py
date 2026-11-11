"""Command line entry point: ``wnr``."""

from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError

from world_news_reality import __version__
from world_news_reality.config import load_metrics_config
from world_news_reality.schemas import export_schemas

app = typer.Typer(no_args_is_help=True, add_completion=False, help="World News Reality pipeline.")
config_app = typer.Typer(no_args_is_help=True, help="Inspect and validate configuration.")
schemas_app = typer.Typer(no_args_is_help=True, help="Data contracts shared with the website.")
app.add_typer(config_app, name="config")
app.add_typer(schemas_app, name="schemas")

MetricsPath = Annotated[
    Path,
    typer.Option("--metrics", exists=True, dir_okay=False, help="Path to metrics.yaml."),
]
SchemasDir = Annotated[
    Path,
    typer.Option("--out", file_okay=False, help="Directory for the generated schemas."),
]


@app.command()
def version() -> None:
    """Print the package version."""
    typer.echo(__version__)


@config_app.command("check")
def config_check(metrics: MetricsPath = Path("config/metrics.yaml")) -> None:
    """Validate the metrics file and print the method version."""
    try:
        config = load_metrics_config(metrics)
    except ValidationError as error:
        typer.echo(f"{metrics}: invalid\n{error}", err=True)
        raise typer.Exit(code=1) from error
    typer.echo(f"{metrics}: ok (method {config.method_version})")


@schemas_app.command("export")
def schemas_export(out: SchemasDir = Path("schemas")) -> None:
    """Regenerate the JSON Schemas from the models."""
    for path in export_schemas(out):
        typer.echo(f"wrote {path.as_posix()}")
