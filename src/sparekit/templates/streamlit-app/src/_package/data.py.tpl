"""Data helpers for the Streamlit app."""

from __future__ import annotations


def sample_metrics() -> dict[str, int]:
    """Return demo metrics for the dashboard."""

    return {"Users": 128, "Projects": 12, "Deployments": 34}
