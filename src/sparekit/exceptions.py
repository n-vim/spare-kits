"""Custom exceptions used by SpareKit."""

from __future__ import annotations


class SpareKitError(Exception):
    """Base error for all user-facing SpareKit failures."""


class TemplateNotFoundError(SpareKitError):
    """Raised when a requested template does not exist."""


class DestinationExistsError(SpareKitError):
    """Raised when a project destination already exists and force is disabled."""


class UnsafePathError(SpareKitError):
    """Raised when a template attempts to write outside the destination."""


class TemplateSourceError(SpareKitError):
    """Raised when a remote or local template source cannot be loaded."""
