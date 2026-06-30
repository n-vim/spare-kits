"""Text utilities."""

from __future__ import annotations

import re


def slugify(value: str) -> str:
    """Convert text into a lowercase URL-friendly slug."""

    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    return re.sub(r"-+", "-", cleaned).strip("-")
