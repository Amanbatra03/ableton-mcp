"""Clip control tools (create, fire, add notes, etc.)."""
from mcp.server.fastmcp import FastMCP

from ableton_mcp.core.errors import NotConnectedError
from ableton_mcp.osc import OSCBridge
from ableton_mcp.osc import addresses as addr
from ableton_mcp.tools import utils


def set_bridge(bridge: OSCBridge) -> None:
    """Set the OSC bridge instance for this module."""
    utils.set_bridge(bridge)


def register_tools(mcp: FastMCP) -> None:
    """Register all clip tools with the MCP server."""

    @mcp.tool()
    async def create_midi_clip(track_index: int, clip_index: int, length_beats: float = 4.0) -> str:
        """Create an empty MIDI clip in a specific slot.

        Args:
            track_index: The index of the track.
            clip_index: The index of the clip slot.
            length_beats: Length of the clip in beats (default 4.0).
        """
        try:
            if length_beats <= 0:
                return f"Error: Clip length must be positive, got {length_beats}"
            bridge = await utils.get_bridge()
            bridge.send(addr.CLIP_SLOT_CREATE_CLIP, [track_index, clip_index, length_beats])
            return f"Created {length_beats}-beat MIDI clip at track {track_index}, slot {clip_index}"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def fire_clip(track_index: int, clip_index: int) -> str:
        """Launch (fire) a specific clip slot.

        Args:
            track_index: The index of the track (starting at 0).
            clip_index: The index of the clip slot (starting at 0).
        """
        try:
            bridge = await utils.get_bridge()
            bridge.send(addr.CLIP_SLOT_FIRE, [track_index, clip_index])
            return f"Fired clip at track {track_index}, slot {clip_index}"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def stop_clip(track_index: int, clip_index: int) -> str:
        """Stop a playing clip.

        Args:
            track_index: The index of the track (starting at 0).
            clip_index: The index of the clip slot (starting at 0).
        """
        try:
            bridge = await utils.get_bridge()
            bridge.send(addr.CLIP_SLOT_STOP, [track_index, clip_index])
            return f"Stopped clip at track {track_index}, slot {clip_index}"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def add_midi_note(
        track_index: int,
        clip_index: int,
        pitch: int,
        start_time: float,
        duration: float,
        velocity: int = 100,
    ) -> str:
        """Add a MIDI note to an existing clip.

        Args:
            track_index: The index of the track.
            clip_index: The index of the clip slot.
            pitch: MIDI note number (0-127, e.g., 60 is Middle C).
            start_time: Start position in beats.
            duration: Duration in beats.
            velocity: Note velocity (0-127, default 100).
        """
        try:
            if not 0 <= pitch <= 127:
                return f"Error: MIDI pitch must be 0-127, got {pitch}"
            if not 0 <= velocity <= 127:
                return f"Error: Velocity must be 0-127, got {velocity}"
            if start_time < 0:
                return f"Error: Start time must be non-negative, got {start_time}"
            if duration <= 0:
                return f"Error: Duration must be positive, got {duration}"

            bridge = await utils.get_bridge()
            bridge.send(addr.CLIP_ADD_NOTES, [track_index, clip_index, pitch, start_time, duration, velocity, 0])
            return f"Added note {pitch} to clip at track {track_index}, slot {clip_index}"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def set_clip_name(track_index: int, clip_index: int, name: str) -> str:
        """Set the name of a clip.

        Args:
            track_index: The index of the track.
            clip_index: The index of the clip slot.
            name: The new name for the clip.
        """
        try:
            bridge = await utils.get_bridge()
            bridge.send(addr.CLIP_SET_NAME, [track_index, clip_index, name])
            return f"Clip at track {track_index}, slot {clip_index} renamed to '{name}'"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def stop_all_clips() -> str:
        """Stop all currently playing clips in the session."""
        try:
            bridge = await utils.get_bridge()
            bridge.send(addr.SONG_STOP_ALL_CLIPS)
            return "All clips stopped"
        except NotConnectedError as e:
            return f"Error: {e}"
