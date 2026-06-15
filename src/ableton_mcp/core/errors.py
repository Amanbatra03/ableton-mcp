"""Custom exceptions for Ableton MCP server."""


class AbletonError(Exception):
    """Base exception for Ableton-related errors."""

    pass


class NotConnectedError(AbletonError):
    """Raised when Ableton Live is not responding."""

    pass


class TimeoutError(AbletonError):
    """Raised when an OSC message times out waiting for a reply."""

    pass


class InvalidValueError(AbletonError):
    """Raised when an invalid value is provided (e.g., out-of-range MIDI note)."""

    pass
