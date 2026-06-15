"""Device parameter mappings for common Ableton Live devices.

Maps device names and parameter names to their OSC indices for intelligent control.
This enables set_device_parameter_by_name() to work despite AbletonOSC limitations.
"""

# Device parameter indices for common Ableton Live devices
# Format: {device_name: {parameter_name: parameter_index}}

DEVICE_PARAMETERS = {
    "EQ Eight": {
        # EQ Eight has 8 bands, each with Freq, Gain, Q
        "Band 1 Frequency": 0,
        "Band 1 Gain": 1,
        "Band 1 Q": 2,
        "Band 1 Type": 3,
        "Band 2 Frequency": 4,
        "Band 2 Gain": 5,
        "Band 2 Q": 6,
        "Band 2 Type": 7,
        # Simplified common names
        "Low Shelf Gain": 1,  # Band 1 Gain (typically low shelf)
        "High Shelf Gain": 5,  # Band 2 Gain (typically high shelf)
        "Mid Gain": 9,  # Common for band 3
        "Brightness": 5,  # High shelf gain
        "Warmth": 1,  # Low shelf gain
        "Presence": 13,  # Band 4 gain (presence peak)
    },
    "Compressor": {
        "Threshold": 0,
        "Ratio": 1,
        "Attack": 2,
        "Release": 3,
        "Makeup Gain": 4,
        "Look Ahead": 5,
        "Knee": 6,
        "Dry/Wet": 7,
        "Sidechain": 8,
        "Sidechain Range": 9,
    },
    "Reverb": {
        "In": 0,
        "Decay": 1,
        "Predealy": 2,
        "Dry/Wet": 3,
        "Room": 4,
        "Damp": 5,
        "Width": 6,
        "Mix": 3,  # Common name for Dry/Wet
        "Size": 4,  # Common name for Room
    },
    "Delay": {
        "Feedback": 0,
        "Time": 1,
        "Offset": 2,
        "Dry/Wet": 3,
        "Filter": 4,
        "Pan": 5,
        "Mix": 3,  # Common name
        "Delay Time": 1,
    },
    "Saturator": {
        "Drive": 0,
        "Tone": 1,
        "Split": 2,
        "Dry/Wet": 3,
        "Soft Knee": 4,
        "Mode": 5,
        "Oversampling": 6,
        "Gain": 7,
    },
    "Vocoder": {
        "Formant": 0,
        "Spectral Time": 1,
        "Sidechain": 2,
        "Gate Threshold": 3,
        "Unvoiced": 4,
        "Transpose": 5,
        "Wet": 6,
        "Dry": 7,
    },
    "AutoFilter": {
        "LFO Frequency": 0,
        "LFO Amount": 1,
        "LFO Phase": 2,
        "Filter Frequency": 3,
        "Filter Resonance": 4,
        "Filter Type": 5,
        "Envelope Amount": 6,
        "Envelope Attack": 7,
        "Envelope Release": 8,
        "Dry/Wet": 9,
    },
    "Overdrive": {
        "Drive": 0,
        "Tone": 1,
        "Output": 2,
        "Dry/Wet": 3,
        "Mode": 4,
    },
    "Operator": {
        # Complex - only common params
        "Oscillator": 0,
        "Filter": 1,
        "LFO": 2,
        "Envelope": 3,
        "Mix": 4,
    },
    "Wavetable": {
        "Oscillator": 0,
        "Filter": 1,
        "Envelope": 2,
        "LFO": 3,
        "Unison": 4,
        "Transpose": 5,
        "Fine": 6,
    },
    "Sampler": {
        "Sample": 0,
        "Pitch": 1,
        "Filter": 2,
        "Envelope": 3,
        "Dry/Wet": 4,
    },
}

# Device type classification
DEVICE_TYPES = {
    "EQ Eight": "Audio Effect",
    "Compressor": "Audio Effect",
    "Reverb": "Audio Effect",
    "Delay": "Audio Effect",
    "Saturator": "Audio Effect",
    "Vocoder": "Audio Effect",
    "AutoFilter": "Audio Effect",
    "Overdrive": "Audio Effect",
    "Operator": "Instrument",
    "Wavetable": "Instrument",
    "Sampler": "Instrument",
}

# Common mixing presets for devices
DEVICE_PRESETS = {
    "EQ Eight": {
        "Bright": {"High Shelf Gain": 0.8, "High Shelf Frequency": 0.8},
        "Warm": {"Low Shelf Gain": 0.7, "Low Shelf Frequency": 0.3},
        "Flat": {"Band 1 Gain": 0.5, "Band 2 Gain": 0.5},
        "Dark": {"High Shelf Gain": 0.2},
    },
    "Compressor": {
        "Gentle": {"Ratio": 0.3, "Attack": 0.3, "Release": 0.5},
        "Moderate": {"Ratio": 0.5, "Attack": 0.2, "Release": 0.4},
        "Aggressive": {"Ratio": 0.8, "Attack": 0.1, "Release": 0.3},
        "Punch": {"Ratio": 0.6, "Attack": 0.05, "Release": 0.2},
    },
    "Reverb": {
        "Small": {"Room": 0.3, "Decay": 0.4},
        "Medium": {"Room": 0.5, "Decay": 0.6},
        "Large": {"Room": 0.8, "Decay": 0.8},
        "Hall": {"Room": 0.9, "Decay": 0.7},
    },
}


def get_device_parameter_index(device_name: str, parameter_name: str) -> int | None:
    """Resolve device and parameter names to OSC index.

    Args:
        device_name: Device name (e.g., "EQ Eight", "Compressor")
        parameter_name: Parameter name (e.g., "Dry/Wet", "Attack")

    Returns:
        Parameter index (0-N) or None if not found.
    """
    if device_name not in DEVICE_PARAMETERS:
        return None

    device_params = DEVICE_PARAMETERS[device_name]
    if parameter_name not in device_params:
        return None

    return device_params[parameter_name]


def get_device_type(device_name: str) -> str | None:
    """Get device type (Audio Effect, Instrument, MIDI Effect).

    Args:
        device_name: Device name

    Returns:
        Device type or None if unknown.
    """
    return DEVICE_TYPES.get(device_name)


def get_preset_values(device_name: str, preset_name: str) -> dict | None:
    """Get preset parameter values.

    Args:
        device_name: Device name
        preset_name: Preset name (e.g., "Bright", "Warm")

    Returns:
        Dict of {parameter_name: value} or None if not found.
    """
    if device_name not in DEVICE_PRESETS:
        return None

    return DEVICE_PRESETS[device_name].get(preset_name)


def list_device_parameters(device_name: str) -> list[str] | None:
    """List all available parameters for a device.

    Args:
        device_name: Device name

    Returns:
        List of parameter names or None if device unknown.
    """
    if device_name not in DEVICE_PARAMETERS:
        return None

    return list(DEVICE_PARAMETERS[device_name].keys())


def list_device_presets(device_name: str) -> list[str] | None:
    """List all available presets for a device.

    Args:
        device_name: Device name

    Returns:
        List of preset names or None if device unknown.
    """
    if device_name not in DEVICE_PRESETS:
        return None

    return list(DEVICE_PRESETS[device_name].keys())
