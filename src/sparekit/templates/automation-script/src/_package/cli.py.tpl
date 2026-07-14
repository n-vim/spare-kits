"""Automation CLI."""

from __future__ import annotations

import typer
from rich.console import Console

from {{ package_name }}.tasks import run_cleanup_task

app = typer.Typer(help="{{ description }}")
console = Console()


@app.command()
def run(dry_run: bool = typer.Option(False, "--dry-run", help="Preview work only.")) -> None:
    """Run automation tasks."""

    result = run_cleanup_task(dry_run=dry_run)
    console.print(f"{result.name}: {result.message}")


if __name__ == "__main__":
    app()
