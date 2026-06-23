"""Template source loading for bundled, local, and GitHub templates."""

from __future__ import annotations

import subprocess
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from sparekit.exceptions import TemplateSourceError
from sparekit.templates import bundled_templates_root, normalize_templates_root


@dataclass(frozen=True)
class GitHubSource:
    """Parsed GitHub template source."""

    clone_url: str
    ref: str | None
    subpath: Path


def parse_github_source(source: str) -> GitHubSource:
    """Parse github:owner/repo[@ref][/path] into clone details."""

    value = source.removeprefix("github:").strip().strip("/")
    parts = value.split("/")
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise TemplateSourceError(
            "GitHub source must look like github:owner/repo or github:owner/repo/path."
        )

    owner = parts[0]
    repo_ref = parts[1]
    repo, _, ref = repo_ref.partition("@")
    subpath = Path(*parts[2:]) if len(parts) > 2 else Path()
    return GitHubSource(
        clone_url=f"https://github.com/{owner}/{repo}.git",
        ref=ref or None,
        subpath=subpath,
    )


def _clone_github_source(parsed: GitHubSource, target: Path) -> None:
    command = ["git", "clone", "--depth", "1"]
    if parsed.ref:
        command.extend(["--branch", parsed.ref])
    command.extend([parsed.clone_url, str(target)])

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except FileNotFoundError as error:
        raise TemplateSourceError("Git is required for GitHub template sources.") from error
    except subprocess.CalledProcessError as error:
        message = error.stderr.strip() or error.stdout.strip() or str(error)
        raise TemplateSourceError(f"Could not clone template source: {message}") from error


def _resolve_local_source(source: str) -> Path:
    value = source.removeprefix("local:").strip()
    path = Path(value).expanduser().resolve()
    if not path.exists():
        raise TemplateSourceError(f"Template source path does not exist: {path}")
    if not path.is_dir():
        raise TemplateSourceError(f"Template source must be a directory: {path}")
    return normalize_templates_root(path)


@contextmanager
def open_template_source(source: str | None = None) -> Iterator[Path]:
    """Yield a normalized template root for bundled, local, or GitHub templates."""

    if source is None:
        yield bundled_templates_root()
        return

    source = source.strip()
    if not source:
        yield bundled_templates_root()
        return

    if source.startswith("github:"):
        parsed = parse_github_source(source)
        with tempfile.TemporaryDirectory(prefix="sparekit-templates-") as directory:
            checkout = Path(directory) / "repo"
            _clone_github_source(parsed, checkout)
            root = checkout / parsed.subpath
            if not root.exists():
                raise TemplateSourceError(f"GitHub template subpath does not exist: {parsed.subpath}")
            yield normalize_templates_root(root)
        return

    yield _resolve_local_source(source)
