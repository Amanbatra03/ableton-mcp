"""Track control tools (create, delete, mute, solo, volume, etc.)."""
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
    """Register all track tools with the MCP server."""

    @mcp.tool()
    async def create_midi_track(name: str = "New MIDI Track", at_index: int = -1) -> str:
        """Create a new MIDI track.

        Args:
            name: The name for the new track.
            at_index: Index to insert at (-1 appends to end).
        """
        try:
            bridge = await _ensure_bridge()
            bridge.send(addr.SONG_CREATE_MIDI_TRACK, at_index)

            if name != "New MIDI Track":
                bridge.send(addr.TRACK_SET_NAME, [at_index, name])

            return f"Created new MIDI track: {name}"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def create_audio_track(name: str = "New Audio Track", at_index: int = -1) -> str:
        """Create a new audio track.

        Args:
            name: The name for the new track.
            at_index: Index to insert at (-1 appends to end).
        """
        try:
            bridge = await _ensure_bridge()
            bridge.send(addr.SONG_CREATE_AUDIO_TRACK, at_index)

            if name != "New Audio Track":
                bridge.send(addr.TRACK_SET_NAME, [at_index, name])

            return f"Created new audio track: {name}"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def set_track_volume(track_index: int, volume: float) -> str:
        """Set the volume of a specific track.

        Args:
            track_index: The index of the track (starting at 0).
            volume: Volume level from 0.0 to 1.0.
        """
        try:
            if not 0.0 <= volume <= 1.0:
                return f"Error: Volume must be between 0.0 and 1.0, got {volume}"
            bridge = await _ensure_bridge()
            bridge.send(addr.TRACK_SET_VOLUME, [track_index, volume])
            return f"Track {track_index} volume set to {volume}"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def get_track_volume(track_index: int) -> str:
        """Get the volume of a specific track.

        Args:
            track_index: The index of the track (starting at 0).
        """
        try:
            bridge = await _ensure_bridge()
            volume = await bridge.send_and_receive(
                addr.TRACK_GET_VOLUME, [track_index], reply_address=addr.TRACK_GET_VOLUME + "/result"
            )
            return f"Track {track_index} volume: {volume}"
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    async def mute_track(track_index: int, mute: bool) -> str:
        """Mute or unmute a specific track.

        Args:
            track_index: The index of the track (starting at 0).
            mute: True to mute, False to unmute.
        """
        try:
            bridge = await _ensure_bridge()
            bridge.send(addr.TRACK_SET_MUTE, [track_index, 1 if mute else 0])
            return f"Track {track_index} {'muted' if mute else 'unmuted'}"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def solo_track(track_index: int, solo: bool) -> str:
        """Solo or unsolo a specific track.

        Args:
            track_index: The index of the track (starting at 0).
            solo: True to solo, False to unsolo.
        """
        try:
            bridge = await _ensure_bridge()
            bridge.send(addr.TRACK_SET_SOLO, [track_index, 1 if solo else 0])
            return f"Track {track_index} {'soloed' if solo else 'unsoloed'}"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def set_track_name(track_index: int, name: str) -> str:
        """Rename a track.

        Args:
            track_index: The index of the track.
            name: The new name for the track.
        """
        try:
            bridge = await _ensure_bridge()
            bridge.send(addr.TRACK_SET_NAME, [track_index, name])
            return f"Track {track_index} renamed to '{name}'"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def set_track_pan(track_index: int, pan: float) -> str:
        """Set the pan of a specific track.

        Args:
            track_index: The index of the track (starting at 0).
            pan: Pan value from -1.0 (left) to 1.0 (right), 0.0 is center.
        """
        try:
            if not -1.0 <= pan <= 1.0:
                return f"Error: Pan must be between -1.0 and 1.0, got {pan}"
            bridge = await _ensure_bridge()
            bridge.send(addr.TRACK_SET_PANNING, [track_index, pan])
            return f"Track {track_index} pan set to {pan}"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def set_track_arm(track_index: int, armed: bool) -> str:
        """Arm or disarm a track for recording.

        Args:
            track_index: The index of the track (starting at 0).
            armed: True to arm, False to disarm.
        """
        try:
            bridge = await _ensure_bridge()
            bridge.send(addr.TRACK_SET_ARM, [track_index, 1 if armed else 0])
            return f"Track {track_index} {'armed' if armed else 'disarmed'}"
        except NotConnectedError as e:
            return f"Error: {e}"
