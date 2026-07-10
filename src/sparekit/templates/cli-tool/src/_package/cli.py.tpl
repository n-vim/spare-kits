"""CLI entrypoint for {{ project_name }}."""

from __future__ import annotations

import typer
from rich.console import Console

from {{ package_name }}.core import build_greeting, count_words

app = typer.Typer(help="{{ description }}")
console = Console()


@app.command()
def greet(name: str, excited: bool = typer.Option(False, "--excited", "-e")) -> None:
    """Print a greeting."""

    console.print(build_greeting(name, excited=excited))


@app.command()
def count(text: str) -> None:
    """Count words in text."""

    console.print(count_words(text))


if __name__ == "__main__":
    app()
