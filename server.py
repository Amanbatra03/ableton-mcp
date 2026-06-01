import asyncio
from mcp.server.fastmcp import FastMCP
from pythonosc import udp_client

# AbletonOSC default configuration
ABLETON_IP = "127.0.0.1"
ABLETON_PORT = 11000

# Create the MCP server
mcp = FastMCP("Ableton")

# Initialize OSC client
client = udp_client.SimpleUDPClient(ABLETON_IP, ABLETON_PORT)

@mcp.tool()
def set_tempo(bpm: float) -> str:
    """Set the tempo of the Ableton Live project.
    
    Args:
        bpm: The tempo in beats per minute (e.g., 120.0).
    """
    client.send_message("/live/song/set/tempo", bpm)
    return f"Tempo set to {bpm} BPM"

@mcp.tool()
def start_playback() -> str:
    """Start playback in Ableton Live."""
    client.send_message("/live/song/continue_playing", [])
    return "Playback started"

@mcp.tool()
def stop_playback() -> str:
    """Stop playback in Ableton Live."""
    client.send_message("/live/song/stop_playing", [])
    return "Playback stopped"

@mcp.tool()
def toggle_metronome(on: bool) -> str:
    """Toggle the metronome on or off.
    
    Args:
        on: True to turn on, False to turn off.
    """
    client.send_message("/live/song/set/metronome", 1 if on else 0)
    return f"Metronome {'on' if on else 'off'}"

@mcp.tool()
def set_track_volume(track_index: int, volume: float) -> str:
    """Set the volume of a specific track.
    
    Args:
        track_index: The index of the track (starting at 0).
        volume: Volume level from 0.0 to 1.0.
    """
    client.send_message("/live/track/set/volume", [track_index, volume])
    return f"Track {track_index} volume set to {volume}"

@mcp.tool()
def mute_track(track_index: int, mute: bool) -> str:
    """Mute or unmute a specific track.
    
    Args:
        track_index: The index of the track (starting at 0).
        mute: True to mute, False to unmute.
    """
    client.send_message("/live/track/set/mute", [track_index, 1 if mute else 0])
    return f"Track {track_index} {'muted' if mute else 'unmuted'}"

@mcp.tool()
def fire_clip(track_index: int, clip_index: int) -> str:
    """Launch a specific clip slot.
    
    Args:
        track_index: The index of the track (starting at 0).
        clip_index: The index of the clip slot (starting at 0).
    """
    client.send_message("/live/clip_slot/fire", [track_index, clip_index])
    return f"Fired clip at track {track_index}, slot {clip_index}"

@mcp.tool()
def create_midi_track(name: str = "New MIDI Track") -> str:
    """Create a new MIDI track.
    
    Args:
        name: The name for the new track.
    """
    client.send_message("/live/song/create_midi_track", -1) # -1 appends to the end
    return f"Created new MIDI track: {name}"

@mcp.tool()
def create_midi_clip(track_index: int, clip_index: int, length_beats: float = 4.0) -> str:
    """Create an empty MIDI clip in a specific slot.
    
    Args:
        track_index: The index of the track.
        clip_index: The index of the clip slot.
        length_beats: Length of the clip in beats (default 4.0).
    """
    client.send_message("/live/clip_slot/create_clip", [track_index, clip_index, length_beats])
    return f"Created {length_beats}-beat MIDI clip at track {track_index}, slot {clip_index}"

@mcp.tool()
def add_midi_note(track_index: int, clip_index: int, pitch: int, start_time: float, duration: float, velocity: int = 100) -> str:
    """Add a MIDI note to an existing clip.
    
    Args:
        track_index: The index of the track.
        clip_index: The index of the clip slot.
        pitch: MIDI note number (0-127, e.g., 60 is Middle C).
        start_time: Start position in beats.
        duration: Duration in beats.
        velocity: Note velocity (0-127).
    """
    client.send_message("/live/clip/add/notes", [track_index, clip_index, pitch, start_time, duration, velocity, 0])
    return f"Added note {pitch} to clip at track {track_index}, slot {clip_index}"

@mcp.tool()
def set_track_name(track_index: int, name: str) -> str:
    """Rename a track.
    
    Args:
        track_index: The index of the track.
        name: The new name for the track.
    """
    client.send_message("/live/track/set/name", [track_index, name])
    return f"Track {track_index} renamed to '{name}'"

@mcp.tool()
def set_device_parameter(track_index: int, device_index: int, parameter_index: int, value: float) -> str:
    """Set a specific parameter of a device (effect/instrument).
    
    Args:
        track_index: The index of the track.
        device_index: The index of the device on that track.
        parameter_index: The index of the parameter to change.
        value: The new value for the parameter.
    """
    client.send_message("/live/device/set/parameter/value", [track_index, device_index, parameter_index, value])
    return f"Set device {device_index} parameter {parameter_index} to {value} on track {track_index}"

if __name__ == "__main__":
    mcp.run()
