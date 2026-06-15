"""Device control tools (effects, instruments, parameters)."""
from mcp.server.fastmcp import FastMCP

from ableton_mcp.core.errors import NotConnectedError
from ableton_mcp.osc import OSCBridge
from ableton_mcp.osc import addresses as addr

_bridge: OSCBridge | None = None


def set_bridge(bridge: OSCBridge) -> None:
    """Set the OSC bridge instance for this module."""
    global _bridge
    _bridge = bridge


async def _ensure_bridge() -> OSCBridge:
    """Ensure bridge is available."""
    if _bridge is None:
        raise NotConnectedError("OSC bridge not initialized")
    return _bridge


def register_tools(mcp: FastMCP) -> None:
    """Register all device tools with the MCP server."""

    @mcp.tool()
    async def set_device_parameter(track_index: int, device_index: int, parameter_index: int, value: float) -> str:
        """Set a specific parameter of a device (effect/instrument).

        Args:
            track_index: The index of the track.
            device_index: The index of the device on that track.
            parameter_index: The index of the parameter to change.
            value: The new value for the parameter (typically 0.0 to 1.0).
        """
        try:
            if not 0.0 <= value <= 1.0:
                return f"Error: Parameter value must be between 0.0 and 1.0, got {value}"
            bridge = await _ensure_bridge()
            bridge.send(addr.DEVICE_SET_PARAMETER_VALUE, [track_index, device_index, parameter_index, value])
            return f"Set device {device_index} parameter {parameter_index} to {value} on track {track_index}"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def get_device_parameter(track_index: int, device_index: int, parameter_index: int) -> str:
        """Get the current value of a device parameter.

        Args:
            track_index: The index of the track.
            device_index: The index of the device on that track.
            parameter_index: The index of the parameter.
        """
        try:
            bridge = await _ensure_bridge()
            value = await bridge.send_and_receive(
                addr.DEVICE_GET_PARAMETER_VALUE,
                [track_index, device_index, parameter_index],
                reply_address=addr.DEVICE_GET_PARAMETER_VALUE + "/result",
            )
            return f"Device {device_index} parameter {parameter_index} value: {value}"
        except Exception as e:
            return f"Error: {e}"
