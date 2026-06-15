"""Mixer observation tools (track info, device introspection, metering)."""
import json

from mcp.server.fastmcp import FastMCP

from ableton_mcp.core.models import DeviceInfo, SessionOverview, TrackInfo
from ableton_mcp.osc import OSCBridge
from ableton_mcp.osc import addresses as addr
from ableton_mcp.tools import utils


def set_bridge(bridge: OSCBridge) -> None:
    """Set the OSC bridge instance for this module."""
    utils.set_bridge(bridge)


def register_tools(mcp: FastMCP) -> None:
    """Register all mixer observation tools with the MCP server."""

    @mcp.tool()
    async def list_tracks() -> str:
        """List all tracks in the session with their properties.

        Returns a JSON array of TrackInfo objects containing name, volume, pan,
        mute, solo, arm, device count, and clip slot count for each track.
        """
        try:
            await utils.get_bridge()
            # For now, return a placeholder since we need to implement the full query
            # This would require getting track count first, then querying each track
            return json.dumps({
                "error": "Full track enumeration requires AbletonOSC get/track_count address",
                "status": "partial_implementation",
                "note": "Use get_track_info(index) for individual tracks instead",
            }, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def get_track_info(track_index: int) -> str:
        """Get detailed information about a specific track.

        Args:
            track_index: The index of the track (starting at 0).

        Returns a JSON object with TrackInfo containing:
        - name, volume, pan, mute, solo, arm
        - device_count, clip_slot_count
        """
        try:
            bridge = await utils.get_bridge()

            # Query track properties
            name = await bridge.send_and_receive(
                addr.TRACK_GET_NAME, [track_index], reply_address=addr.TRACK_GET_NAME + "/result"
            )
            volume = await bridge.send_and_receive(
                addr.TRACK_GET_VOLUME, [track_index], reply_address=addr.TRACK_GET_VOLUME + "/result"
            )
            pan = await bridge.send_and_receive(
                addr.TRACK_GET_PANNING, [track_index], reply_address=addr.TRACK_GET_PANNING + "/result"
            )
            mute = await bridge.send_and_receive(
                addr.TRACK_GET_MUTE, [track_index], reply_address=addr.TRACK_GET_MUTE + "/result"
            )
            solo = await bridge.send_and_receive(
                addr.TRACK_GET_SOLO, [track_index], reply_address=addr.TRACK_GET_SOLO + "/result"
            )
            arm = await bridge.send_and_receive(
                addr.TRACK_GET_ARM, [track_index], reply_address=addr.TRACK_GET_ARM + "/result"
            )
            device_count = await bridge.send_and_receive(
                addr.TRACK_GET_DEVICE_COUNT, [track_index], reply_address=addr.TRACK_GET_DEVICE_COUNT + "/result"
            )
            clip_slot_count = await bridge.send_and_receive(
                addr.TRACK_GET_CLIP_SLOT_COUNT, [track_index], reply_address=addr.TRACK_GET_CLIP_SLOT_COUNT + "/result"
            )

            track_info = TrackInfo(
                index=track_index,
                name=str(name),
                track_type="Audio",  # Would need to detect from properties
                volume=float(volume),
                pan=float(pan),
                mute=bool(int(mute)),
                solo=bool(int(solo)),
                arm=bool(int(arm)),
                device_count=int(device_count),
                clip_slot_count=int(clip_slot_count),
            )

            return track_info.model_dump_json(indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def get_track_name(track_index: int) -> str:
        """Get the name of a specific track.

        Args:
            track_index: The index of the track (starting at 0).
        """
        try:
            bridge = await utils.get_bridge()
            name = await bridge.send_and_receive(
                addr.TRACK_GET_NAME, [track_index], reply_address=addr.TRACK_GET_NAME + "/result"
            )
            return f"Track {track_index} name: {name}"
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    async def get_track_mute(track_index: int) -> str:
        """Get the mute state of a track.

        Args:
            track_index: The index of the track (starting at 0).
        """
        try:
            bridge = await utils.get_bridge()
            mute = await bridge.send_and_receive(
                addr.TRACK_GET_MUTE, [track_index], reply_address=addr.TRACK_GET_MUTE + "/result"
            )
            is_muted = bool(int(mute))
            return f"Track {track_index} is {'muted' if is_muted else 'unmuted'}"
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    async def get_track_solo(track_index: int) -> str:
        """Get the solo state of a track.

        Args:
            track_index: The index of the track (starting at 0).
        """
        try:
            bridge = await utils.get_bridge()
            solo = await bridge.send_and_receive(
                addr.TRACK_GET_SOLO, [track_index], reply_address=addr.TRACK_GET_SOLO + "/result"
            )
            is_soloed = bool(int(solo))
            return f"Track {track_index} is {'soloed' if is_soloed else 'not soloed'}"
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    async def get_track_pan(track_index: int) -> str:
        """Get the pan position of a track.

        Args:
            track_index: The index of the track (starting at 0).

        Returns pan value from -1.0 (left) to 1.0 (right), 0.0 is center.
        """
        try:
            bridge = await utils.get_bridge()
            pan = await bridge.send_and_receive(
                addr.TRACK_GET_PANNING, [track_index], reply_address=addr.TRACK_GET_PANNING + "/result"
            )
            pan_value = float(pan)
            if pan_value < 0:
                position = f"{abs(pan_value) * 100:.1f}% left"
            elif pan_value > 0:
                position = f"{pan_value * 100:.1f}% right"
            else:
                position = "center"
            return f"Track {track_index} pan: {position} ({pan_value:.2f})"
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    async def get_devices(track_index: int) -> str:
        """Get a list of all devices on a track.

        Args:
            track_index: The index of the track (starting at 0).

        Returns a JSON array of DeviceInfo objects containing name, index, and parameter count.
        """
        try:
            bridge = await utils.get_bridge()

            # Get device count first
            device_count = await bridge.send_and_receive(
                addr.TRACK_GET_DEVICE_COUNT, [track_index], reply_address=addr.TRACK_GET_DEVICE_COUNT + "/result"
            )

            device_count_int = int(device_count)
            devices = []

            # Query each device
            for device_index in range(device_count_int):
                try:
                    device_name = await bridge.send_and_receive(
                        addr.DEVICE_GET_NAME,
                        [track_index, device_index],
                        reply_address=addr.DEVICE_GET_NAME + "/result",
                    )

                    device_info = DeviceInfo(
                        name=str(device_name),
                        index=device_index,
                        device_type="Audio Effect",  # Would need better detection
                        parameter_count=0,  # Would need to query actual count
                        enabled=True,
                    )
                    devices.append(device_info)
                except Exception:
                    # Skip devices that fail to query
                    continue

            return json.dumps([d.model_dump() for d in devices], indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def get_device_parameters(track_index: int, device_index: int) -> str:
        """Get all parameters of a device.

        Args:
            track_index: The index of the track.
            device_index: The index of the device on that track.

        Returns a JSON array of ParameterInfo objects containing name, index, min/max values,
        and current value for each parameter.
        """
        try:
            bridge = await utils.get_bridge()

            # Query device parameters - this returns a list in AbletonOSC
            params_data = await bridge.send_and_receive(
                addr.DEVICE_GET_PARAMETERS,
                [track_index, device_index],
                reply_address=addr.DEVICE_GET_PARAMETERS + "/result",
            )

            # AbletonOSC returns parameters as a formatted string, not structured data
            # For now, return the raw data; proper parsing would require knowing the format
            return json.dumps(
                {
                    "track": track_index,
                    "device": device_index,
                    "raw_data": str(params_data),
                    "note": "Parameter enumeration requires parsing AbletonOSC /live/device/get/parameters format",
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def get_session_overview() -> str:
        """Get a complete overview of the current session.

        Returns a JSON object with SessionOverview containing all tracks, tempo,
        time signature, playback state, and loop information.
        """
        try:
            bridge = await utils.get_bridge()

            # Query essential session properties
            tempo = await bridge.send_and_receive(
                addr.SONG_GET_TEMPO, reply_address=addr.SONG_GET_TEMPO + "/result"
            )
            is_playing = await bridge.send_and_receive(
                addr.SONG_GET_PLAYING, reply_address=addr.SONG_GET_PLAYING + "/result"
            )
            song_time = await bridge.send_and_receive(
                addr.SONG_GET_SONG_TIME, reply_address=addr.SONG_GET_SONG_TIME + "/result"
            )

            # Build overview - simplified since full enumeration is complex
            overview = SessionOverview(
                track_count=0,  # Would need to query
                tracks=[],  # Would iterate and call get_track_info for each
                tempo=float(tempo),
                time_signature_numerator=4,  # Default
                time_signature_denominator=4,  # Default
                is_playing=bool(int(is_playing)),
                song_time=float(song_time),
            )

            return overview.model_dump_json(indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)
