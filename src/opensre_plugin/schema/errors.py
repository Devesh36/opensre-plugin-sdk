"""Schema validation exceptions."""

from __future__ import annotations


class SchemaValidationError(Exception):
    """Raised when a tool input schema violates strict investigation invariants."""

    def __init__(self, *, tool_name: str, path: str, message: str) -> None:
        self.tool_name = tool_name
        self.path = path
        self.message = message
        super().__init__(self.format_message())

    def format_message(self) -> str:
        if self.tool_name:
            location = f"tool {self.tool_name!r} at {self.path!r}"
        else:
            location = f"at {self.path!r}"
        return f"{location}: {self.message}"

    def __str__(self) -> str:
        return self.format_message()
