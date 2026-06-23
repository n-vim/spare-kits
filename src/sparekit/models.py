"""Typed models for templates and project generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class TemplateInfo:
    """Metadata describing one available starter template."""

    name: str
    title: str
    description: str
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProjectOptions:
    """Options used while rendering a project template."""

    template: str
    project_name: str
    destination: Path
    package_name: str
    author: str = "Nitish Vimal"
    description: str = "Generated with SpareKit"
    python_version: str = "3.11"
    include_docker: bool = True
    include_github_actions: bool = True
    force: bool = False
    variables: dict[str, Any] = field(default_factory=dict)
    template_root: Path | None = None

    def context(self) -> dict[str, Any]:
        """Return rendering variables available inside template files."""

        base = {
            "project_name": self.project_name,
            "package_name": self.package_name,
            "author": self.author,
            "description": self.description,
            "python_version": self.python_version,
            "include_docker": self.include_docker,
            "include_github_actions": self.include_github_actions,
        }
        return {**base, **self.variables}
