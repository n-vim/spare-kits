"""Utility helpers for safe file generation."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from sparekit.exceptions import UnsafePathError

_TOKEN_PATTERN = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}")


def normalize_package_name(name: str) -> str:
    """Convert a display project name into a valid Python package name."""

    value = re.sub(r"[^a-zA-Z0-9_]+", "_", name.strip().lower())
    value = re.sub(r"_+", "_", value).strip("_")
    if not value:
        return "app"
    if value[0].isdigit():
        return f"app_{value}"
    return value


def normalize_distribution_name(name: str) -> str:
    """Convert a project name into a Python distribution/package name."""

    value = re.sub(r"[^a-zA-Z0-9.-]+", "-", name.strip().lower())
    value = re.sub(r"-+", "-", value).strip("-.")
    return value or "app"


def render_string(text: str, context: dict[str, object]) -> str:
    """Render simple {{ variable }} placeholders without executing code."""

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        value = context.get(key, match.group(0))
        return str(value)

    return _TOKEN_PATTERN.sub(replace, text)


def is_binary_file(path: Path) -> bool:
    """Best-effort binary detection for template copying."""

    try:
        chunk = path.read_bytes()[:2048]
    except OSError:
        return False
    return b"\\0" in chunk


def ensure_safe_child(base: Path, child: Path) -> None:
    """Ensure child resolves inside base, preventing path traversal."""

    base_resolved = base.resolve()
    child_resolved = child.resolve()
    if base_resolved != child_resolved and base_resolved not in child_resolved.parents:
        raise UnsafePathError(f"Refusing to write outside destination: {child}")


def copy_tree(src: Path, dst: Path) -> None:
    """Copy src tree into dst, preserving existing folders."""

    for item in src.rglob("*"):
        relative = item.relative_to(src)
        target = dst / relative
        ensure_safe_child(dst, target)
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
