"""Utility helpers for tools."""
import asyncio
import logging

from ableton_mcp.core.errors import NotConnectedError
from ableton_mcp.osc import OSCBridge

logger = logging.getLogger(__name__)

_bridge: OSCBridge | None = None
_init_lock = asyncio.Lock()


def set_bridge(bridge: OSCBridge) -> None:
    """Set the global bridge instance."""
    global _bridge
    _bridge = bridge


async def get_bridge() -> OSCBridge:
    """Get and initialize the bridge if needed.

    This handles lazy initialization to ensure the OSC server is started
    even if the MCP server's startup hooks don't work as expected.
    """
    global _bridge
    if _bridge is None:
        raise NotConnectedError("OSC bridge not initialized")

    # Lazy start: if bridge hasn't been started yet, start it now
    if not _bridge._connected:
        try:
            async with _init_lock:
                # Double-check after acquiring lock
                if not _bridge._connected:
                    await _bridge.start()
                    logger.info("OSC bridge started (lazy initialization)")
        except Exception as e:
            raise NotConnectedError(f"Failed to start OSC bridge: {e}")

    return _bridge
