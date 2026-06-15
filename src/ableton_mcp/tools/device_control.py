"""Intelligent device control tools (parameter by name, device management)."""
import json

from mcp.server.fastmcp import FastMCP

from ableton_mcp.core.device_mappings import get_device_parameter_index, list_device_parameters
from ableton_mcp.osc import OSCBridge
from ableton_mcp.osc import addresses as addr
from ableton_mcp.tools import utils


def set_bridge(bridge: OSCBridge) -> None:
    """Set the OSC bridge instance for this module."""
    utils.set_bridge(bridge)


def register_tools(mcp: FastMCP) -> None:
    """Register all intelligent device control tools with the MCP server."""

    @mcp.tool()
    async def set_device_parameter_by_name(
        track_index: int, device_name: str, parameter_name: str, value: float
    ) -> str:
        """Set a device parameter by name (intelligent control).

        This is the key Phase 2 tool - allows setting parameters by name
        instead of index using device parameter mappings for common devices.

        Supported devices: EQ Eight, Compressor, Reverb, Delay, Saturator, Vocoder, AutoFilter, Overdrive, Operator, Wavetable, Sampler

        Example: set_device_parameter_by_name(0, "EQ Eight", "High Shelf Gain", 0.7)

        Args:
            track_index: The index of the track.
            device_name: The name of the device (e.g., "EQ Eight", "Compressor").
            parameter_name: The name of the parameter (e.g., "Dry/Wet", "Attack").
            value: The new value for the parameter (0.0 to 1.0).

        Returns:
            Success message or error message.
        """
        try:
            if not 0.0 <= value <= 1.0:
                return f"Error: Parameter value must be between 0.0 and 1.0, got {value}"

            bridge = await utils.get_bridge()

            # Step 1: Look up parameter index in device mappings
            param_index = get_device_parameter_index(device_name, parameter_name)

            if param_index is None:
                available_params = list_device_parameters(device_name)
                if available_params is None:
                    return json.dumps(
                        {
                            "status": "error",
                            "message": f"Device '{device_name}' not found in parameter mappings",
                            "available_devices": [
                                "EQ Eight",
                                "Compressor",
                                "Reverb",
                                "Delay",
                                "Saturator",
                                "Vocoder",
                                "AutoFilter",
                                "Overdrive",
                                "Operator",
                                "Wavetable",
                                "Sampler",
                            ],
                        },
                        indent=2,
                    )
                else:
                    return json.dumps(
                        {
                            "status": "error",
                            "message": f"Parameter '{parameter_name}' not found on {device_name}",
                            "available_parameters": available_params,
                        },
                        indent=2,
                    )

            # Step 2: Get device count on this track
            device_count = await bridge.send_and_receive(
                addr.TRACK_GET_DEVICE_COUNT, [track_index], reply_address=addr.TRACK_GET_DEVICE_COUNT + "/result"
            )

            device_count_int = int(device_count)

            # Step 3: Find the device by name on the track
            device_index = None
            for idx in range(device_count_int):
                try:
                    d_name = await bridge.send_and_receive(
                        addr.DEVICE_GET_NAME,
                        [track_index, idx],
                        reply_address=addr.DEVICE_GET_NAME + "/result",
                    )
                    if str(d_name).strip() == device_name.strip():
                        device_index = idx
                        break
                except Exception:
                    continue

            if device_index is None:
                return f"Error: Device '{device_name}' not found on track {track_index}"

            # Step 4: Set the parameter using the resolved index
            bridge.send(addr.DEVICE_SET_PARAMETER_VALUE, [track_index, device_index, param_index, value])

            return json.dumps(
                {
                    "status": "success",
                    "message": f"Set {device_name} parameter '{parameter_name}' to {value}",
                    "track_index": track_index,
                    "device_index": device_index,
                    "parameter_index": param_index,
                    "parameter_name": parameter_name,
                    "value": value,
                },
                indent=2,
            )

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)}, indent=2)

    @mcp.tool()
    async def add_device_to_track(track_index: int, device_name: str) -> str:
        """Add a device (effect or instrument) to a track.

        Args:
            track_index: The index of the track.
            device_name: The name of the device to add (e.g., "Compressor", "EQ Eight", "Reverb").

        Returns:
            Success message with the new device index, or error message.
        """
        try:
            bridge = await utils.get_bridge()

            # Get current device count
            device_count = await bridge.send_and_receive(
                addr.TRACK_GET_DEVICE_COUNT, [track_index], reply_address=addr.TRACK_GET_DEVICE_COUNT + "/result"
            )

            # AbletonOSC doesn't expose a direct "add device by name" endpoint
            # This would require browser navigation or Live API
            return json.dumps(
                {
                    "status": "not_implemented",
                    "message": f"Adding device '{device_name}' to track {track_index}",
                    "warning": "AbletonOSC does not expose device browser/creation API",
                    "current_device_count": int(device_count),
                    "suggestion": "Consider using Live's Python API or Max for Live for device loading",
                },
                indent=2,
            )

        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    async def remove_device(track_index: int, device_index: int) -> str:
        """Remove a device from a track.

        Args:
            track_index: The index of the track.
            device_index: The index of the device to remove.

        Returns:
            Success message or error message.
        """
        try:
            await utils.get_bridge()

            # AbletonOSC doesn't expose device removal
            # This would require Live API access
            return json.dumps(
                {
                    "status": "not_implemented",
                    "message": f"Removing device at index {device_index} from track {track_index}",
                    "warning": "AbletonOSC does not expose device deletion API",
                    "suggestion": "This operation requires Live's Python API or Max for Live",
                },
                indent=2,
            )

        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    async def toggle_device(track_index: int, device_index: int, enabled: bool) -> str:
        """Enable or disable a device.

        Args:
            track_index: The index of the track.
            device_index: The index of the device.
            enabled: True to enable, False to disable.

        Returns:
            Success message or error message.
        """
        try:
            await utils.get_bridge()

            # AbletonOSC doesn't expose a direct device enable/disable endpoint
            # This would require finding the device's "active" or "enabled" parameter
            return json.dumps(
                {
                    "status": "not_implemented",
                    "message": f"{'Enabling' if enabled else 'Disabling'} device {device_index} on track {track_index}",
                    "warning": "AbletonOSC does not expose device enabled state control",
                    "suggestion": "This may be available via device parameter if AbletonOSC exposes parameter enumeration",
                },
                indent=2,
            )

        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    async def load_device_preset(track_index: int, device_index: int, preset_name: str) -> str:
        """Load a preset on a device.

        Args:
            track_index: The index of the track.
            device_index: The index of the device.
            preset_name: The name of the preset to load (e.g., "Bright", "Warm").

        Returns:
            Success message or error message.
        """
        try:
            await utils.get_bridge()

            # AbletonOSC doesn't expose preset loading by name
            return json.dumps(
                {
                    "status": "not_implemented",
                    "message": f"Loading preset '{preset_name}' on device {device_index} of track {track_index}",
                    "warning": "AbletonOSC does not expose preset browser/loading API",
                    "suggestion": "Presets can be loaded manually or via Live's Python API",
                },
                indent=2,
            )

        except Exception as e:
            return f"Error: {e}"
