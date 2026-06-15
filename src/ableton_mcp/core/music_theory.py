"""Music theory utilities for MIDI note generation and manipulation.

Provides functions for note name conversion, chord building, scale generation,
and quantization—all without external dependencies.
"""

# MIDI note numbers
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_TO_MIDI = {name: i % 12 for i, name in enumerate(NOTE_NAMES)}
MIDI_TO_NOTE = {i % 12: name for i, name in enumerate(NOTE_NAMES)}


def note_name_to_midi(note_name: str) -> int | None:
    """Convert note name to MIDI number.

    Args:
        note_name: Note name (e.g., "C4", "A#5", "Db3")

    Returns:
        MIDI note number (0-127) or None if invalid.

    Examples:
        >>> note_name_to_midi("C4")
        60
        >>> note_name_to_midi("A4")
        69
        >>> note_name_to_midi("C#5")
        73
    """
    if not note_name or len(note_name) < 2:
        return None

    # Parse note and octave
    note_part = note_name[:-1].upper()
    try:
        octave = int(note_name[-1])
    except ValueError:
        return None

    # Handle sharps/flats
    if note_part.endswith("#"):
        base_note = note_part[:-1]
        semitone_offset = 1
    elif note_part.endswith("B"):
        base_note = note_part[:-1]
        semitone_offset = -1
    else:
        base_note = note_part
        semitone_offset = 0

    if base_note not in NOTE_TO_MIDI:
        return None

    midi_num = (octave + 1) * 12 + NOTE_TO_MIDI[base_note] + semitone_offset
    if 0 <= midi_num <= 127:
        return midi_num
    return None


def midi_to_note_name(midi_num: int) -> str | None:
    """Convert MIDI number to note name.

    Args:
        midi_num: MIDI note number (0-127)

    Returns:
        Note name (e.g., "C4", "A#5") or None if invalid.

    Examples:
        >>> midi_to_note_name(60)
        'C4'
        >>> midi_to_note_name(69)
        'A4'
    """
    if not (0 <= midi_num <= 127):
        return None
    octave = (midi_num // 12) - 1
    note = MIDI_TO_NOTE[midi_num % 12]
    return f"{note}{octave}"


def build_chord(root_midi: int, chord_type: str) -> list[int] | None:
    """Build a chord from a root MIDI note.

    Args:
        root_midi: Root note MIDI number (0-127)
        chord_type: Chord type (major, minor, dim, aug, maj7, min7, dom7, sus2, sus4)

    Returns:
        List of MIDI note numbers for the chord, or None if invalid.

    Examples:
        >>> build_chord(60, "major")  # C major
        [60, 64, 67]
        >>> build_chord(60, "minor")  # C minor
        [60, 63, 67]
        >>> build_chord(60, "maj7")  # C major 7
        [60, 64, 67, 71]
    """
    if not (0 <= root_midi <= 127):
        return None

    # Interval patterns (semitones from root)
    chord_intervals = {
        "major": [0, 4, 7],
        "minor": [0, 3, 7],
        "dim": [0, 3, 6],
        "aug": [0, 4, 8],
        "maj7": [0, 4, 7, 11],
        "min7": [0, 3, 7, 10],
        "dom7": [0, 4, 7, 10],
        "maj6": [0, 4, 7, 9],
        "min6": [0, 3, 7, 9],
        "sus2": [0, 2, 7],
        "sus4": [0, 5, 7],
    }

    if chord_type not in chord_intervals:
        return None

    intervals = chord_intervals[chord_type]
    chord = []
    for interval in intervals:
        note = root_midi + interval
        if 0 <= note <= 127:
            chord.append(note)
    return chord if chord else None


def build_scale(root_midi: int, scale_type: str) -> list[int] | None:
    """Build a scale from a root MIDI note.

    Args:
        root_midi: Root note MIDI number (0-127)
        scale_type: Scale type (major, minor, pentatonic_major, pentatonic_minor, blues,
                               dorian, phrygian, lydian, mixolydian, harmonic_minor)

    Returns:
        List of MIDI note numbers for the scale (octave spanning), or None if invalid.

    Examples:
        >>> build_scale(60, "major")  # C major scale
        [60, 62, 64, 65, 67, 69, 71, 72]
    """
    if not (0 <= root_midi <= 127):
        return None

    # Interval patterns (semitones from root)
    scale_intervals = {
        "major": [0, 2, 4, 5, 7, 9, 11, 12],
        "minor": [0, 2, 3, 5, 7, 8, 10, 12],
        "pentatonic_major": [0, 2, 4, 7, 9, 12],
        "pentatonic_minor": [0, 3, 5, 7, 10, 12],
        "blues": [0, 3, 5, 6, 7, 10, 12],
        "dorian": [0, 2, 3, 5, 7, 9, 10, 12],
        "phrygian": [0, 1, 3, 5, 7, 8, 10, 12],
        "lydian": [0, 2, 4, 6, 7, 9, 11, 12],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10, 12],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11, 12],
        "chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    }

    if scale_type not in scale_intervals:
        return None

    intervals = scale_intervals[scale_type]
    scale = []
    for interval in intervals:
        note = root_midi + interval
        if 0 <= note <= 127:
            scale.append(note)
    return scale if scale else None


def quantize_beat(time_beats: float, grid: float) -> float:
    """Quantize a time value to a grid.

    Args:
        time_beats: Time in beats (float)
        grid: Grid size in beats (0.25, 0.5, 1.0, etc.)

    Returns:
        Quantized time in beats.

    Examples:
        >>> quantize_beat(1.23, 0.25)
        1.25
        >>> quantize_beat(1.1, 1.0)
        1.0
    """
    if grid == 0:
        return time_beats
    return round(time_beats / grid) * grid


def transpose_notes(midi_notes: list[int], semitones: int) -> list[int]:
    """Transpose a list of MIDI notes.

    Args:
        midi_notes: List of MIDI note numbers
        semitones: Number of semitones to transpose (positive = up, negative = down)

    Returns:
        List of transposed MIDI notes (clamped to 0-127).

    Examples:
        >>> transpose_notes([60, 64, 67], 2)
        [62, 66, 69]
    """
    transposed = []
    for note in midi_notes:
        new_note = note + semitones
        if 0 <= new_note <= 127:
            transposed.append(new_note)
    return transposed


def find_nearest_scale_note(midi_num: int, scale: list[int]) -> int | None:
    """Find the nearest note in a scale.

    Args:
        midi_num: MIDI note number to snap
        scale: List of MIDI note numbers (scale)

    Returns:
        Nearest MIDI note in the scale, or None if scale is empty.

    Examples:
        >>> scale = [60, 62, 64, 65, 67, 69, 71, 72]  # C major
        >>> find_nearest_scale_note(61, scale)
        60
        >>> find_nearest_scale_note(63, scale)
        64
    """
    if not scale:
        return None
    return min(scale, key=lambda x: abs(x - midi_num))


def generate_drum_pattern(style: str, bars: int = 1) -> list[tuple[float, int, int]] | None:
    """Generate a drum pattern.

    Args:
        style: Drum pattern style (kick, snare, hihat, house, techno, breakbeat)
        bars: Number of bars (4 beats each)

    Returns:
        List of (time_beats, pitch, velocity) tuples, or None if invalid style.

    Examples:
        >>> pattern = generate_drum_pattern("house", 1)
        >>> len(pattern) > 0
        True
    """
    beat_length = 4 * bars

    patterns = {
        "kick": [
            (0.0, 36, 100),  # Beat 1
            (2.0, 36, 100),  # Beat 3
            (3.5, 36, 80),   # Off-beat
        ],
        "snare": [
            (1.0, 38, 90),   # Beat 2
            (3.0, 38, 90),   # Beat 4
        ],
        "hihat": [
            (i * 0.5, 42, 70) for i in range(beat_length * 2)
        ],
        "house": [
            (0.0, 36, 100),
            (1.0, 38, 90),
            (2.0, 36, 100),
            (3.0, 38, 90),
        ] * bars,
        "techno": [
            (i * 0.25, 36, 100) for i in range(beat_length * 4)
        ],
        "breakbeat": [
            (0.0, 36, 100),
            (0.75, 36, 80),
            (1.0, 38, 90),
            (2.0, 36, 100),
            (3.0, 38, 90),
        ] * bars,
    }

    return patterns.get(style)


def humanize_notes(
    notes: list[tuple[float, int, int]],
    timing_variance: float = 0.02,
    velocity_variance: int = 5,
) -> list[tuple[float, int, int]]:
    """Add humanization to notes (subtle timing and velocity variations).

    Args:
        notes: List of (time_beats, pitch, velocity) tuples
        timing_variance: Max timing variation in beats (0.02 = 20ms at 120 BPM)
        velocity_variance: Max velocity variation (0-100)

    Returns:
        Humanized notes with small random variations.
    """
    import random

    humanized = []
    for time, pitch, velocity in notes:
        # Add subtle timing variation
        var_time = time + random.uniform(-timing_variance, timing_variance)
        # Add subtle velocity variation
        var_vel = max(1, min(127, velocity + random.randint(-velocity_variance, velocity_variance)))
        humanized.append((var_time, pitch, var_vel))
    return humanized


# Common chord progressions
PROGRESSIONS = {
    "i_v_vi_iv": ["i", "V", "vi", "IV"],  # Pop progression
    "i_vi_iv_v": ["I", "vi", "IV", "V"],  # Sensitive females
    "i_v_vi_iii_iv": ["I", "V", "vi", "iii", "IV"],  # Extended pop
    "ii_v_i": ["ii", "V", "I"],  # Jazz standard
    "vi_iv_i_v": ["vi", "IV", "I", "V"],  # Minor variation
}


def build_progression(root_midi: int, progression_name: str) -> list[list[int]] | None:
    """Build a chord progression.

    Args:
        root_midi: Root note MIDI number
        progression_name: Progression name (i_v_vi_iv, ii_v_i, etc.)

    Returns:
        List of chords (each chord is a list of MIDI notes), or None if invalid.

    Examples:
        >>> progression = build_progression(60, "i_v_vi_iv")
        >>> len(progression)
        4
    """
    if progression_name not in PROGRESSIONS:
        return None

    # Map progression names to chord types
    progression_chords = PROGRESSIONS[progression_name]
    chords = []

    for chord_name in progression_chords:
        # Simple mapping: Roman numerals to intervals
        intervals = {
            "i": 0,
            "ii": 2,
            "iii": 4,
            "iv": 5,
            "v": 7,
            "vi": 9,
            "vii": 11,
            "I": 0,
            "II": 2,
            "III": 4,
            "IV": 5,
            "V": 7,
            "VI": 9,
            "VII": 11,
        }

        if chord_name not in intervals:
            return None

        root = root_midi + intervals[chord_name]
        chord_type = "minor" if chord_name.islower() else "major"
        chord = build_chord(root, chord_type)
        if chord:
            chords.append(chord)

    return chords if chords else None
