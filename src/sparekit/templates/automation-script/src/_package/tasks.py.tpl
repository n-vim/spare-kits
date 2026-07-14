"""Automation tasks."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class TaskResult:
    name: str
    success: bool
    message: str


def run_cleanup_task(dry_run: bool = False) -> TaskResult:
    """Run a demo cleanup task."""

    timestamp = datetime.now(timezone.utc).isoformat()
    mode = "dry run" if dry_run else "executed"
    return TaskResult("cleanup", True, f"Cleanup {mode} at {timestamp}")
