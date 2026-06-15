"""Music generation tools for advanced MIDI composition."""

import json

from mcp.server.fastmcp import FastMCP

from ableton_mcp.core import music_theory
from ableton_mcp.osc import OSCBridge
from ableton_mcp.tools import utils


def set_bridge(bridge: OSCBridge) -> None:
    """Set the OSC bridge instance for this module."""
    utils.set_bridge(bridge)


def register_tools(mcp: FastMCP) -> None:
    """Register music generation tools with the MCP server."""

    @mcp.tool()
    async def note_name_to_midi(note_name: str) -> str:
        """Convert musical note name to MIDI number.

        Args:
            note_name: Note name (e.g., "C4", "A#5", "Db3")

        Returns:
            JSON with MIDI number or error.
        """
        try:
            await utils.get_bridge()
            midi_num = music_theory.note_name_to_midi(note_name)
            if midi_num is None:
                return json.dumps(
                    {"status": "error", "message": f"Invalid note name: {note_name}"},
                    indent=2,
                )
            return json.dumps(
                {
                    "status": "success",
                    "note_name": note_name,
                    "midi_number": midi_num,
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def midi_to_note_name(midi_number: int) -> str:
        """Convert MIDI number to musical note name.

        Args:
            midi_number: MIDI note number (0-127)

        Returns:
            JSON with note name or error.
        """
        try:
            await utils.get_bridge()
            note_name = music_theory.midi_to_note_name(midi_number)
            if note_name is None:
                return json.dumps(
                    {"status": "error", "message": f"Invalid MIDI number: {midi_number}"},
                    indent=2,
                )
            return json.dumps(
                {
                    "status": "success",
                    "midi_number": midi_number,
                    "note_name": note_name,
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def build_chord(root_note: str, chord_type: str) -> str:
        """Build a chord from root note and type.

        Available chord types:
        - major, minor, dim, aug
        - maj7, min7, dom7
        - maj6, min6
        - sus2, sus4

        Args:
            root_note: Root note name (e.g., "C4", "A#3")
            chord_type: Chord type (e.g., "major", "minor")

        Returns:
            JSON with chord notes and MIDI numbers.
        """
        try:
            await utils.get_bridge()
            root_midi = music_theory.note_name_to_midi(root_note)
            if root_midi is None:
                return json.dumps(
                    {"status": "error", "message": f"Invalid root note: {root_note}"},
                    indent=2,
                )

            chord = music_theory.build_chord(root_midi, chord_type)
            if chord is None:
                return json.dumps(
                    {"status": "error", "message": f"Invalid chord type: {chord_type}"},
                    indent=2,
                )

            note_names = [music_theory.midi_to_note_name(n) for n in chord]
            return json.dumps(
                {
                    "status": "success",
                    "root_note": root_note,
                    "chord_type": chord_type,
                    "midi_numbers": chord,
                    "note_names": note_names,
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def build_scale(root_note: str, scale_type: str) -> str:
        """Build a scale from root note and type.

        Available scale types:
        - major, minor
        - pentatonic_major, pentatonic_minor
        - blues
        - dorian, phrygian, lydian, mixolydian
        - harmonic_minor
        - chromatic

        Args:
            root_note: Root note name (e.g., "C4")
            scale_type: Scale type (e.g., "major", "minor")

        Returns:
            JSON with scale notes and MIDI numbers.
        """
        try:
            await utils.get_bridge()
            root_midi = music_theory.note_name_to_midi(root_note)
            if root_midi is None:
                return json.dumps(
                    {"status": "error", "message": f"Invalid root note: {root_note}"},
                    indent=2,
                )

            scale = music_theory.build_scale(root_midi, scale_type)
            if scale is None:
                return json.dumps(
                    {"status": "error", "message": f"Invalid scale type: {scale_type}"},
                    indent=2,
                )

            note_names = [music_theory.midi_to_note_name(n) for n in scale]
            return json.dumps(
                {
                    "status": "success",
                    "root_note": root_note,
                    "scale_type": scale_type,
                    "midi_numbers": scale,
                    "note_names": note_names,
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def build_chord_progression(root_note: str, progression_type: str) -> str:
        """Build a chord progression.

        Available progressions:
        - i_v_vi_iv (pop progression)
        - i_vi_iv_v (sensitive females)
        - i_v_vi_iii_iv (extended pop)
        - ii_v_i (jazz standard)
        - vi_iv_i_v (minor variation)

        Args:
            root_note: Root note (e.g., "C4")
            progression_type: Progression type (e.g., "i_v_vi_iv")

        Returns:
            JSON with chord progression.
        """
        try:
            await utils.get_bridge()
            root_midi = music_theory.note_name_to_midi(root_note)
            if root_midi is None:
                return json.dumps(
                    {"status": "error", "message": f"Invalid root note: {root_note}"},
                    indent=2,
                )

            progression = music_theory.build_progression(root_midi, progression_type)
            if progression is None:
                return json.dumps(
                    {
                        "status": "error",
                        "message": f"Invalid progression type: {progression_type}",
                    },
                    indent=2,
                )

            # Convert to note names
            chord_names = []
            for chord in progression:
                names = [music_theory.midi_to_note_name(n) for n in chord]
                chord_names.append(names)

            return json.dumps(
                {
                    "status": "success",
                    "root_note": root_note,
                    "progression_type": progression_type,
                    "chords": progression,
                    "chord_names": chord_names,
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def generate_drum_pattern(style: str, bars: int = 1) -> str:
        """Generate a drum pattern.

        Available styles:
        - kick, snare, hihat
        - house (4-on-the-floor)
        - techno (fast kick)
        - breakbeat (syncopated)

        Args:
            style: Drum pattern style
            bars: Number of bars (1-8)

        Returns:
            JSON with drum pattern notes (time, pitch, velocity).
        """
        try:
            await utils.get_bridge()
            bars = min(max(1, bars), 8)  # Clamp 1-8
            pattern = music_theory.generate_drum_pattern(style, bars)
            if pattern is None:
                return json.dumps(
                    {"status": "error", "message": f"Invalid drum style: {style}"},
                    indent=2,
                )

            return json.dumps(
                {
                    "status": "success",
                    "style": style,
                    "bars": bars,
                    "pattern": [
                        {"time_beats": t, "pitch": p, "velocity": v} for t, p, v in pattern
                    ],
                    "message": f"Generated {style} pattern ({len(pattern)} notes, {bars} bars)",
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def transpose_notes(midi_numbers: list[int], semitones: int) -> str:
        """Transpose a list of MIDI notes.

        Args:
            midi_numbers: List of MIDI note numbers (0-127)
            semitones: Semitones to transpose (positive = up, negative = down)

        Returns:
            JSON with transposed MIDI numbers.
        """
        try:
            await utils.get_bridge()
            transposed = music_theory.transpose_notes(midi_numbers, semitones)
            note_names = [music_theory.midi_to_note_name(n) for n in transposed]
            return json.dumps(
                {
                    "status": "success",
                    "original": midi_numbers,
                    "semitones": semitones,
                    "transposed": transposed,
                    "note_names": note_names,
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)
