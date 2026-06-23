"""Command-line interface for SpareKit."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text

from sparekit import __version__
from sparekit.config import find_config, load_config, write_default_config
from sparekit.exceptions import SpareKitError
from sparekit.models import ProjectOptions, TemplateInfo
from sparekit.sources import open_template_source
from sparekit.templates import count_template_files, get_template_info, list_templates, render_template
from sparekit.utils import normalize_package_name

app = typer.Typer(
    name="sparekit",
    help="Create production-ready Python projects from local, bundled, or GitHub starter kits.",
    add_completion=False,
)
console = Console()


def version_callback(value: bool) -> None:
    """Print version and exit."""

    if value:
        console.print(f"sparekit {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show SpareKit version and exit.",
    )
) -> None:
    """SpareKit CLI root command."""


def _print_templates(templates: list[TemplateInfo], title: str = "Available SpareKit Templates") -> None:
    table = Table(title=title)
    table.add_column("Name", style="bold")
    table.add_column("Description")
    table.add_column("Tags")
    for template in templates:
        table.add_row(template.name, template.description, ", ".join(template.tags))
    console.print(table)


def _choose_template(templates: list[TemplateInfo]) -> str:
    if not templates:
        raise SpareKitError("No templates were found in this source.")

    _print_templates(templates, title="Choose a Template")
    names = {template.name for template in templates}
    while True:
        answer = Prompt.ask("Template name or number", default=templates[0].name).strip()
        if answer.isdigit():
            index = int(answer) - 1
            if 0 <= index < len(templates):
                return templates[index].name
        if answer in names:
            return answer
        console.print("[yellow]Please enter a listed template name or number.[/yellow]")


def _search_templates(templates: list[TemplateInfo], query: str) -> list[TemplateInfo]:
    needle = query.lower().strip()
    if not needle:
        return templates
    return [
        template
        for template in templates
        if needle in template.name.lower()
        or needle in template.title.lower()
        or needle in template.description.lower()
        or any(needle in tag.lower() for tag in template.tags)
    ]


@app.command("list")
def list_command(
    source: Optional[str] = typer.Option(
        None,
        "--from",
        "-f",
        help="Template source: local path, local:/path, or github:owner/repo[/path].",
    )
) -> None:
    """Show available project templates."""

    try:
        with open_template_source(source) as template_root:
            _print_templates(list_templates(template_root))
    except SpareKitError as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(1) from error


@app.command("search")
def search_command(
    query: str = typer.Argument(..., help="Search term, e.g. api, bot, data, package."),
    source: Optional[str] = typer.Option(
        None,
        "--from",
        "-f",
        help="Template source: local path, local:/path, or github:owner/repo[/path].",
    ),
) -> None:
    """Search templates by name, description, or tag."""

    try:
        with open_template_source(source) as template_root:
            matches = _search_templates(list_templates(template_root), query)
            if not matches:
                console.print(f"[yellow]No templates matched:[/yellow] {query}")
                raise typer.Exit(1)
            _print_templates(matches, title=f"Search results for '{query}'")
    except SpareKitError as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(1) from error


@app.command("info")
def info_command(
    template: str = typer.Argument(..., help="Template name to inspect."),
    source: Optional[str] = typer.Option(
        None,
        "--from",
        "-f",
        help="Template source: local path, local:/path, or github:owner/repo[/path].",
    ),
) -> None:
    """Show detailed metadata for a template."""

    try:
        with open_template_source(source) as template_root:
            info = get_template_info(template, template_root)
            file_count = count_template_files(template, template_root)
    except SpareKitError as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(1) from error

    message = Text()
    message.append(f"{info.title}\n\n", style="bold")
    message.append("Name: ")
    message.append(f"{info.name}\n", style="cyan")
    message.append(f"Description: {info.description}\n")
    message.append(f"Tags: {', '.join(info.tags) or 'none'}\n")
    message.append(f"Files: {file_count}")
    console.print(Panel.fit(message, title="Template Info"))


@app.command("init")
def init_config(
    path: Path = typer.Option(
        Path("sparekit.yaml"),
        "--path",
        "-p",
        help="Where to write the config file.",
    ),
    force: bool = typer.Option(False, "--force", help="Overwrite existing config file."),
) -> None:
    """Create a default sparekit.yaml config file."""

    if path.exists() and not force:
        console.print(f"[red]Config already exists:[/red] {path}")
        raise typer.Exit(1)
    write_default_config(path)
    console.print(f"[green]Created config:[/green] {path}")


@app.command("create")
def create_project(
    template: Optional[str] = typer.Argument(None, help="Template name, e.g. fastapi-api."),
    name: Optional[str] = typer.Argument(None, help="Project folder/name to create."),
    output: Path = typer.Option(Path.cwd(), "--output", "-o", help="Output directory."),
    package: Optional[str] = typer.Option(None, "--package", help="Python package name."),
    author: Optional[str] = typer.Option(None, "--author", help="Project author."),
    description: Optional[str] = typer.Option(None, "--description", help="Project description."),
    python_version: Optional[str] = typer.Option(None, "--python", help="Python version."),
    docker: Optional[bool] = typer.Option(None, "--docker/--no-docker", help="Include Dockerfile."),
    github_actions: Optional[bool] = typer.Option(
        None,
        "--github-actions/--no-github-actions",
        help="Include GitHub Actions workflow.",
    ),
    source: Optional[str] = typer.Option(
        None,
        "--from",
        "-f",
        help="Template source: local path, local:/path, or github:owner/repo[/path].",
    ),
    force: bool = typer.Option(False, "--force", help="Overwrite the destination if it exists."),
    config: Optional[Path] = typer.Option(None, "--config", help="Path to sparekit.yaml."),
) -> None:
    """Create a new project. Run without arguments for interactive mode."""

    try:
        config_path = config or find_config(Path.cwd())
        config_data = load_config(config_path)

        with open_template_source(source) as template_root:
            templates = list_templates(template_root)
            if template is None:
                template = _choose_template(templates)
            elif template not in {item.name for item in templates}:
                available = ", ".join(item.name for item in templates) or "none"
                raise SpareKitError(
                    f"Template '{template}' was not found. Available templates: {available}."
                )

            interactive = name is None
            if name is None:
                name = Prompt.ask("Project name", default=f"my-{template}").strip()

            default_package = normalize_package_name(name)
            if package is None and interactive:
                package = Prompt.ask("Python package name", default=default_package).strip()
            package = package or default_package

            default_author = str(config_data.get("author", "Nitish Vimal"))
            if author is None and interactive:
                author = Prompt.ask("Author", default=default_author).strip()
            author = author or default_author

            default_description = str(
                config_data.get("description", f"A {template} project generated by SpareKit")
            )
            if description is None and interactive:
                description = Prompt.ask("Description", default=default_description).strip()
            description = description or default_description

            default_python = str(config_data.get("python_version", "3.11"))
            if python_version is None and interactive:
                python_version = Prompt.ask("Python version", default=default_python).strip()
            python_version = python_version or default_python

            default_docker = bool(config_data.get("include_docker", True))
            include_docker = docker if docker is not None else default_docker
            if docker is None and interactive:
                include_docker = Confirm.ask("Include Dockerfile?", default=default_docker)

            default_actions = bool(config_data.get("include_github_actions", True))
            include_github_actions = github_actions if github_actions is not None else default_actions
            if github_actions is None and interactive:
                include_github_actions = Confirm.ask(
                    "Include GitHub Actions CI?", default=default_actions
                )

            options = ProjectOptions(
                template=template,
                project_name=name,
                destination=output,
                package_name=package,
                author=author,
                description=description,
                python_version=python_version,
                include_docker=include_docker,
                include_github_actions=include_github_actions,
                force=force,
                variables=dict(config_data.get("variables", {})),
                template_root=template_root,
            )
            destination = render_template(options)
    except SpareKitError as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(1) from error
    except ValueError as error:
        console.print(f"[red]Invalid config:[/red] {error}")
        raise typer.Exit(1) from error

    message = Text()
    message.append("Project created successfully!\n\n", style="bold green")
    message.append("Path: ")
    message.append(f"{destination}\n\n", style="cyan")
    message.append("Next steps:\n")
    message.append(f"  cd {destination}\n")
    message.append("  python -m venv .venv\n")
    message.append("  source .venv/bin/activate\n")
    message.append("  pip install -e .[dev]")
    console.print(Panel.fit(message, title="SpareKit"))


if __name__ == "__main__":
    app()
