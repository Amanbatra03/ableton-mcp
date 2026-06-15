"""OSC communication layer."""

from .client import OSCBridge
from .dispatcher import OSCDispatcher

__all__ = ["OSCBridge", "OSCDispatcher"]
