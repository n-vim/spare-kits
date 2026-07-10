"""Business logic for {{ project_name }}."""

from __future__ import annotations


def build_greeting(name: str, excited: bool = False) -> str:
    """Build a greeting message."""

    message = f"Hello, {name}!"
    return message.upper() if excited else message


def count_words(text: str) -> int:
    """Count words in a string."""

    return len([part for part in text.split() if part.strip()])
