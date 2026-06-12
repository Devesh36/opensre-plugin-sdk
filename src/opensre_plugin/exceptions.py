"""SDK-specific exceptions."""

from __future__ import annotations


class OpensreNotInstalledError(ImportError):
    """Raised when an API requires ``opensre`` but it is not installed."""

    def __init__(self, feature: str = "this operation") -> None:
        super().__init__(
            f"opensre is required for {feature}. "
            "Install with: pip install 'opensre-plugin-sdk[opensre]' or pip install opensre"
        )


class PluginRegistrationError(RuntimeError):
    """Raised when plugin validation or registration fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ManifestError(ValueError):
    """Raised when a plugin manifest is missing or invalid."""
