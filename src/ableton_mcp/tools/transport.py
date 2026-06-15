"""Transport control tools (play, stop, tempo, etc.)."""
from mcp.server.fastmcp import FastMCP

from ableton_mcp.core.errors import NotConnectedError
from ableton_mcp.osc import OSCBridge
from ableton_mcp.osc import addresses as addr
from ableton_mcp.tools import utils


def set_bridge(bridge: OSCBridge) -> None:
    """Set the OSC bridge instance for this module."""
    utils.set_bridge(bridge)


def register_tools(mcp: FastMCP) -> None:
    """Register all transport tools with the MCP server."""

    @mcp.tool()
    async def ping() -> str:
        """Test connection to Ableton Live and return current tempo.

        Returns the current tempo in BPM, confirming that Ableton is running
        and the OSC bridge is working.
        """
        try:
            bridge = await utils.get_bridge()
            tempo = await bridge.ping()
            return f"Connected to Ableton Live. Current tempo: {tempo} BPM"
        except NotConnectedError as e:
            return f"Error: Ableton Live is not responding: {e}"

    @mcp.tool()
    async def start_playback() -> str:
        """Start playback in Ableton Live from the beginning."""
        try:
            bridge = await utils.get_bridge()
            bridge.send(addr.SONG_START_PLAYING)
            return "Playback started"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def continue_playback() -> str:
        """Resume playback from the current position."""
        try:
            bridge = await utils.get_bridge()
            bridge.send(addr.SONG_CONTINUE_PLAYING)
            return "Playback continued"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def stop_playback() -> str:
        """Stop playback in Ableton Live."""
        try:
            bridge = await utils.get_bridge()
            bridge.send(addr.SONG_STOP_PLAYING)
            return "Playback stopped"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def set_tempo(bpm: float) -> str:
        """Set the tempo of the Ableton Live project.

        Args:
            bpm: The tempo in beats per minute (e.g., 120.0).
        """
        try:
            if not 20 <= bpm <= 300:
                return f"Error: Tempo must be between 20 and 300 BPM, got {bpm}"
            bridge = await utils.get_bridge()
            bridge.send(addr.SONG_SET_TEMPO, bpm)
            return f"Tempo set to {bpm} BPM"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def get_tempo() -> str:
        """Get the current tempo of the Ableton Live project.

        Returns the current tempo in beats per minute.
        """
        try:
            bridge = await utils.get_bridge()
            tempo = await bridge.send_and_receive(
                addr.SONG_GET_TEMPO, reply_address=addr.SONG_GET_TEMPO + "/result"
            )
            return f"Current tempo: {tempo} BPM"
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    async def toggle_metronome(on: bool) -> str:
        """Toggle the metronome on or off.

        Args:
            on: True to turn on, False to turn off.
        """
        try:
            bridge = await utils.get_bridge()
            bridge.send(addr.SONG_SET_METRONOME, 1 if on else 0)
            return f"Metronome {'enabled' if on else 'disabled'}"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def undo() -> str:
        """Undo the last action in Ableton Live."""
        try:
            bridge = await utils.get_bridge()
            bridge.send(addr.SONG_UNDO)
            return "Undo executed"
        except NotConnectedError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def redo() -> str:
        """Redo the last undone action in Ableton Live."""
        try:
            bridge = await utils.get_bridge()
            bridge.send(addr.SONG_REDO)
            return "Redo executed"
        except NotConnectedError as e:
            return f"Error: {e}"
