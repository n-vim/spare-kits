"""Configuration file support for SpareKit."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG_NAMES = ("sparekit.yaml", "sparekit.yml")


def find_config(start: Path | None = None) -> Path | None:
    """Find a SpareKit config file in the given directory."""

    base = (start or Path.cwd()).resolve()
    for directory in (base, *base.parents):
        for name in DEFAULT_CONFIG_NAMES:
            candidate = directory / name
            if candidate.exists():
                return candidate
    return None


def load_config(path: Path | None) -> dict[str, Any]:
    """Load YAML config, returning an empty dict if path is missing."""

    if path is None:
        return {}
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ValueError(f"Config must be a mapping: {path}")
    return raw


def write_default_config(path: Path) -> None:
    """Create an example SpareKit config file."""

    content = """# SpareKit project defaults
author: Nitish Vimal
python_version: '3.11'
include_docker: true
include_github_actions: true
variables: {}
"""
    path.write_text(content, encoding="utf-8")
