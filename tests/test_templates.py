from pathlib import Path

import pytest

from sparekit.exceptions import DestinationExistsError, TemplateNotFoundError
from sparekit.models import ProjectOptions
from sparekit.templates import get_template_path, list_templates, render_template


def make_options(tmp_path: Path, **overrides: object) -> ProjectOptions:
    data = {
        "template": "cli-tool",
        "project_name": "demo-app",
        "destination": tmp_path,
        "package_name": "demo_app",
        "author": "Tester",
        "description": "Demo project",
        "python_version": "3.11",
        "include_docker": False,
        "include_github_actions": False,
        "force": False,
    }
    data.update(overrides)
    return ProjectOptions(**data)  # type: ignore[arg-type]


def test_list_templates_contains_defaults() -> None:
    names = {template.name for template in list_templates()}
    assert {
        "fastapi-api",
        "flask-api",
        "cli-tool",
        "python-package",
        "streamlit-app",
        "automation-script",
        "telegram-bot",
        "data-science",
    }.issubset(names)


def test_get_template_path_missing() -> None:
    with pytest.raises(TemplateNotFoundError):
        get_template_path("missing-template")


def test_render_cli_template(tmp_path: Path) -> None:
    destination = render_template(make_options(tmp_path))
    assert (destination / "README.md").exists()
    assert (destination / "src" / "demo_app" / "cli.py").exists()
    assert "Demo project" in (destination / "README.md").read_text(encoding="utf-8")


def test_render_optional_folders(tmp_path: Path) -> None:
    destination = render_template(
        make_options(
            tmp_path,
            template="fastapi-api",
            project_name="demo-api",
            package_name="demo_api",
            include_docker=True,
            include_github_actions=True,
        )
    )
    assert (destination / "Dockerfile").exists()
    assert (destination / ".github" / "workflows" / "ci.yml").exists()


def test_render_refuses_existing_without_force(tmp_path: Path) -> None:
    render_template(make_options(tmp_path))
    with pytest.raises(DestinationExistsError):
        render_template(make_options(tmp_path))


def test_render_force_overwrites(tmp_path: Path) -> None:
    destination = render_template(make_options(tmp_path))
    marker = destination / "marker.txt"
    marker.write_text("old", encoding="utf-8")
    render_template(make_options(tmp_path, force=True))
    assert not marker.exists()


def test_bundled_template_paths_are_clean() -> None:
    root = Path("src/sparekit/templates")
    bad_paths = [
        path
        for path in root.rglob("*")
        if any(char in path.name for char in "{}()")
    ]
    assert bad_paths == []
