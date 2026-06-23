"""Template discovery and rendering engine."""

from __future__ import annotations

import json
import shutil
from importlib import resources
from pathlib import Path
from typing import Iterable

from sparekit.exceptions import DestinationExistsError, TemplateNotFoundError
from sparekit.models import ProjectOptions, TemplateInfo
from sparekit.utils import ensure_safe_child, is_binary_file, render_string

TEMPLATE_MANIFEST = "template.json"
SKIP_MARKERS = {TEMPLATE_MANIFEST}
SPECIAL_FOLDER_MARKERS = {"_docker", "_github_actions", "__docker__", "__github_actions__"}
PATH_VARIABLE_MARKERS = {"_package": "package_name", "__package__": "package_name"}


def bundled_templates_root() -> Path:
    """Return the path to bundled templates."""

    return Path(str(resources.files("sparekit") / "templates"))


def templates_root() -> Path:
    """Backward-compatible alias for the bundled templates root."""

    return bundled_templates_root()


def normalize_templates_root(root: Path | None = None) -> Path:
    """Normalize a source path to the directory that contains template folders."""

    candidate = (root or bundled_templates_root()).expanduser().resolve()
    if (candidate / "templates").is_dir():
        return candidate / "templates"
    if (candidate / TEMPLATE_MANIFEST).is_file():
        return candidate.parent
    return candidate


def _read_manifest(template_dir: Path) -> dict[str, object]:
    manifest_path = template_dir / TEMPLATE_MANIFEST
    if not manifest_path.exists():
        return {"title": template_dir.name, "description": "No description available.", "tags": []}
    with manifest_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        return {"title": template_dir.name, "description": "No description available.", "tags": []}
    return data


def list_templates(root: Path | None = None) -> list[TemplateInfo]:
    """List available templates and their metadata."""

    base = normalize_templates_root(root)
    if not base.exists():
        return []

    templates: list[TemplateInfo] = []
    for child in sorted(base.iterdir()):
        if not child.is_dir():
            continue
        data = _read_manifest(child)
        tags = data.get("tags", [])
        if not isinstance(tags, list):
            tags = []
        templates.append(
            TemplateInfo(
                name=child.name,
                title=str(data.get("title", child.name)),
                description=str(data.get("description", "No description available.")),
                tags=tuple(str(tag) for tag in tags),
            )
        )
    return templates


def get_template_info(template_name: str, root: Path | None = None) -> TemplateInfo:
    """Return metadata for one template."""

    template_path = get_template_path(template_name, root)
    data = _read_manifest(template_path)
    tags = data.get("tags", [])
    if not isinstance(tags, list):
        tags = []
    return TemplateInfo(
        name=template_path.name,
        title=str(data.get("title", template_path.name)),
        description=str(data.get("description", "No description available.")),
        tags=tuple(str(tag) for tag in tags),
    )


def get_template_path(template_name: str, root: Path | None = None) -> Path:
    """Resolve a template path or raise TemplateNotFoundError."""

    base = normalize_templates_root(root)
    path = base / template_name
    if not path.is_dir():
        available = ", ".join(template.name for template in list_templates(base)) or "none"
        raise TemplateNotFoundError(
            f"Template '{template_name}' was not found. Available templates: {available}."
        )
    return path


def count_template_files(template_name: str, root: Path | None = None) -> int:
    """Count renderable files in a template."""

    template_path = get_template_path(template_name, root)
    return sum(1 for path in _iter_template_files(template_path) if path.name not in SKIP_MARKERS)


def _should_skip(relative: Path, options: ProjectOptions) -> bool:
    parts = set(relative.parts)
    if relative.name in SKIP_MARKERS:
        return True
    if ("_docker" in parts or "__docker__" in parts) and not options.include_docker:
        return True
    if ("_github_actions" in parts or "__github_actions__" in parts) and not options.include_github_actions:
        return True
    return False


def _clean_special_parts(relative: Path) -> Path:
    parts = [part for part in relative.parts if part not in SPECIAL_FOLDER_MARKERS]
    return Path(*parts)


def _render_path(relative: Path, context: dict[str, object]) -> Path:
    cleaned = _clean_special_parts(relative)
    rendered_parts: list[str] = []
    for part in cleaned.parts:
        variable_name = PATH_VARIABLE_MARKERS.get(part)
        rendered = str(context.get(variable_name, part)) if variable_name else render_string(part, context)
        if rendered.endswith(".tpl"):
            rendered = rendered[:-4]
        rendered_parts.append(rendered)
    return Path(*rendered_parts)


def _iter_template_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file():
            yield path


def render_template(options: ProjectOptions) -> Path:
    """Render a template into a destination directory."""

    template_path = get_template_path(options.template, options.template_root)
    destination = options.destination / options.project_name
    if destination.exists():
        if not options.force:
            raise DestinationExistsError(
                f"Destination already exists: {destination}. Use --force to overwrite."
            )
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)

    context = options.context()
    for source_file in _iter_template_files(template_path):
        relative = source_file.relative_to(template_path)
        if _should_skip(relative, options):
            continue

        rendered_relative = _render_path(relative, context)
        target = destination / rendered_relative
        ensure_safe_child(destination, target)
        target.parent.mkdir(parents=True, exist_ok=True)

        if is_binary_file(source_file):
            shutil.copy2(source_file, target)
            continue

        text = source_file.read_text(encoding="utf-8")
        target.write_text(render_string(text, context), encoding="utf-8")

    return destination
l
