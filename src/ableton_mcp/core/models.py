"""Pydantic models for structured Ableton responses."""
from typing import Optional

from pydantic import BaseModel, Field


class ParameterInfo(BaseModel):
    """Information about a device parameter."""

    name: str = Field(description="Parameter name (e.g., 'Dry/Wet', 'Attack')")
    index: int = Field(description="Parameter index for OSC control")
    min_value: float = Field(description="Minimum parameter value")
    max_value: float = Field(description="Maximum parameter value")
    current_value: float = Field(description="Current parameter value")
    unit: Optional[str] = Field(default=None, description="Parameter unit (e.g., 'dB', 'ms', '%')")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Dry/Wet",
                "index": 0,
                "min_value": 0.0,
                "max_value": 1.0,
                "current_value": 0.5,
                "unit": "%",
            }
        }


class DeviceInfo(BaseModel):
    """Information about a device on a track."""

    name: str = Field(description="Device name (e.g., 'EQ Eight', 'Compressor')")
    index: int = Field(description="Device index on the track")
    device_type: str = Field(description="Device type (e.g., 'Audio Effect', 'MIDI Effect', 'Instrument')")
    parameter_count: int = Field(description="Number of parameters")
    enabled: bool = Field(default=True, description="Whether device is enabled")
    parameters: list[ParameterInfo] = Field(default_factory=list, description="List of parameters (optional, requires get_device_parameters)")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "EQ Eight",
                "index": 0,
                "device_type": "Audio Effect",
                "parameter_count": 8,
                "enabled": True,
                "parameters": [],
            }
        }


class TrackInfo(BaseModel):
    """Information about a track."""

    index: int = Field(description="Track index in session")
    name: str = Field(description="Track name")
    track_type: str = Field(description="Track type: 'Audio', 'MIDI', or 'Return'")
    volume: float = Field(description="Volume level (0.0 to 1.0, where 0.0 is -inf dB)")
    pan: float = Field(description="Pan position (-1.0 = left, 0.0 = center, 1.0 = right)")
    mute: bool = Field(description="Whether track is muted")
    solo: bool = Field(description="Whether track is soloed")
    arm: bool = Field(description="Whether track is armed for recording")
    device_count: int = Field(description="Number of devices on track")
    clip_slot_count: int = Field(description="Number of clip slots")
    devices: list[DeviceInfo] = Field(default_factory=list, description="List of devices (requires get_devices())")

    class Config:
        json_schema_extra = {
            "example": {
                "index": 0,
                "name": "Drums",
                "track_type": "MIDI",
                "volume": 0.8,
                "pan": 0.0,
                "mute": False,
                "solo": False,
                "arm": False,
                "device_count": 2,
                "clip_slot_count": 12,
                "devices": [],
            }
        }


class ClipInfo(BaseModel):
    """Information about a clip."""

    track_index: int = Field(description="Track index containing the clip")
    clip_index: int = Field(description="Clip slot index")
    name: str = Field(description="Clip name")
    length: float = Field(description="Clip length in beats")
    is_playing: bool = Field(description="Whether clip is currently playing")
    loop_start: Optional[float] = Field(default=None, description="Loop start position in beats")
    loop_end: Optional[float] = Field(default=None, description="Loop end position in beats")
    note_count: int = Field(default=0, description="Number of MIDI notes (for MIDI clips)")

    class Config:
        json_schema_extra = {
            "example": {
                "track_index": 0,
                "clip_index": 0,
                "name": "Drums - Verse",
                "length": 16.0,
                "is_playing": False,
                "loop_start": 0.0,
                "loop_end": 16.0,
                "note_count": 32,
            }
        }


class SessionOverview(BaseModel):
    """Complete overview of the current session."""

    track_count: int = Field(description="Total number of tracks")
    tracks: list[TrackInfo] = Field(description="List of all tracks")
    tempo: float = Field(description="Current tempo in BPM")
    time_signature_numerator: int = Field(description="Time signature numerator (e.g., 4 in 4/4)")
    time_signature_denominator: int = Field(description="Time signature denominator (e.g., 4 in 4/4)")
    is_playing: bool = Field(description="Whether playback is active")
    song_time: float = Field(description="Current song time in beats")
    song_length: Optional[float] = Field(default=None, description="Total song length in beats")
    loop_enabled: bool = Field(description="Whether loop is enabled")
    loop_start: Optional[float] = Field(default=None, description="Loop start position")
    loop_end: Optional[float] = Field(default=None, description="Loop end position")

    class Config:
        json_schema_extra = {
            "example": {
                "track_count": 8,
                "tracks": [],
                "tempo": 120.0,
                "time_signature_numerator": 4,
                "time_signature_denominator": 4,
                "is_playing": False,
                "song_time": 0.0,
                "song_length": 128.0,
                "loop_enabled": True,
                "loop_start": 0.0,
                "loop_end": 32.0,
            }
        }


class MeterInfo(BaseModel):
    """Audio metering information for a track."""

    peak_db: float = Field(description="Peak level in dB")
    rms_db: float = Field(description="RMS (average) level in dB")
    headroom_db: float = Field(description="Headroom to 0dB (positive number)")
    is_clipping: bool = Field(description="Whether signal is clipping")

    class Config:
        json_schema_extra = {
            "example": {
                "peak_db": -3.5,
                "rms_db": -15.2,
                "headroom_db": 3.5,
                "is_clipping": False,
            }
        }
