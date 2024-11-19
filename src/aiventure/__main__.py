"""Main entry point for the package."""

import os
from typing import Annotated

import typer
from typer import Typer

from aiventure import __version__


app = Typer(name="AI Venture CLI", no_args_is_help=True)


@app.command()
def run(
    build: Annotated[bool, typer.Option("--build")] = False,
    migrate: Annotated[bool, typer.Option("--migrate")] = False,
) -> None:
    """Run the API."""
    if build:
        os.system("bun run build")

    if migrate:
        os.system("uv run alembic upgrade head")

    os.system("uv run fastapi dev src/aiventure/api.py --reload")


@app.command()
def version() -> None:
    """Show the version of the CLI."""
    typer.secho(f"v{__version__}", fg=typer.colors.YELLOW)


if __name__ == "__main__":
    typer.run(app)
