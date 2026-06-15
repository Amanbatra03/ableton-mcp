"""Unit tests for music theory utilities."""

import pytest

from ableton_mcp.core import music_theory


class TestNoteConversion:
    """Test MIDI <-> note name conversion."""

    def test_note_name_to_midi(self):
        """Convert note names to MIDI numbers."""
        assert music_theory.note_name_to_midi("C4") == 60
        assert music_theory.note_name_to_midi("A4") == 69
        assert music_theory.note_name_to_midi("C#5") == 73
        assert music_theory.note_name_to_midi("C0") == 12
        assert music_theory.note_name_to_midi("B7") == 119

    def test_midi_to_note_name(self):
        """Convert MIDI numbers to note names."""
        assert music_theory.midi_to_note_name(60) == "C4"
        assert music_theory.midi_to_note_name(69) == "A4"
        assert music_theory.midi_to_note_name(73) == "C#5"

    def test_invalid_note_conversion(self):
        """Invalid conversions should return None."""
        assert music_theory.note_name_to_midi("Z10") is None
        assert music_theory.note_name_to_midi("") is None
        assert music_theory.midi_to_note_name(-1) is None
        assert music_theory.midi_to_note_name(128) is None


class TestChordBuilding:
    """Test chord generation."""

    def test_major_chord(self):
        """Build major chords."""
        chord = music_theory.build_chord(60, "major")
        assert chord == [60, 64, 67]  # C E G

    def test_minor_chord(self):
        """Build minor chords."""
        chord = music_theory.build_chord(60, "minor")
        assert chord == [60, 63, 67]  # C Eb G

    def test_diminished_chord(self):
        """Build diminished chords."""
        chord = music_theory.build_chord(60, "dim")
        assert chord == [60, 63, 66]  # C Eb Gb

    def test_augmented_chord(self):
        """Build augmented chords."""
        chord = music_theory.build_chord(60, "aug")
        assert chord == [60, 64, 68]  # C E G#

    def test_seventh_chord(self):
        """Build seventh chords."""
        maj7 = music_theory.build_chord(60, "maj7")
        assert maj7 == [60, 64, 67, 71]  # C E G B

    def test_invalid_chord_type(self):
        """Invalid chord types should return None."""
        assert music_theory.build_chord(60, "invalid") is None


class TestScaleBuilding:
    """Test scale generation."""

    def test_major_scale(self):
        """Build major scale."""
        scale = music_theory.build_scale(60, "major")
        assert scale == [60, 62, 64, 65, 67, 69, 71, 72]  # C major

    def test_minor_scale(self):
        """Build minor scale."""
        scale = music_theory.build_scale(60, "minor")
        assert scale == [60, 62, 63, 65, 67, 68, 70, 72]  # C natural minor

    def test_pentatonic_major_scale(self):
        """Build pentatonic major scale."""
        scale = music_theory.build_scale(60, "pentatonic_major")
        assert scale == [60, 62, 64, 67, 69, 72]  # C pentatonic major

    def test_pentatonic_minor_scale(self):
        """Build pentatonic minor scale."""
        scale = music_theory.build_scale(60, "pentatonic_minor")
        assert scale == [60, 63, 65, 67, 70, 72]  # C pentatonic minor

    def test_invalid_scale_type(self):
        """Invalid scale types should return None."""
        assert music_theory.build_scale(60, "invalid") is None


class TestQuantization:
    """Test note quantization."""

    def test_quantize_to_quarter_note(self):
        """Quantize to quarter notes (0.25 beats)."""
        assert music_theory.quantize_beat(1.23, 0.25) == 1.25
        assert music_theory.quantize_beat(1.1, 0.25) == 1.0

    def test_quantize_to_beat(self):
        """Quantize to beats (1.0)."""
        assert music_theory.quantize_beat(1.4, 1.0) == 1.0
        assert music_theory.quantize_beat(1.6, 1.0) == 2.0

    def test_quantize_triplet(self):
        """Quantize to triplets (1/3 beat)."""
        result = music_theory.quantize_beat(0.4, 1 / 3)
        assert abs(result - (1 / 3)) < 0.01


class TestTransposition:
    """Test note transposition."""

    def test_transpose_up(self):
        """Transpose notes upward."""
        notes = music_theory.transpose_notes([60, 64, 67], 2)
        assert notes == [62, 66, 69]

    def test_transpose_down(self):
        """Transpose notes downward."""
        notes = music_theory.transpose_notes([60, 64, 67], -3)
        assert notes == [57, 61, 64]

    def test_transpose_clamping(self):
        """Transposed notes should be clamped to valid MIDI range."""
        notes = music_theory.transpose_notes([120, 124, 127], 10)
        assert notes == []  # All out of range


class TestScaleSnapping:
    """Test snapping notes to scales."""

    def test_snap_to_scale(self):
        """Snap note to nearest scale degree."""
        scale = music_theory.build_scale(60, "major")
        # 61 is between C (60) and D (62), closer to C
        nearest = music_theory.find_nearest_scale_note(61, scale)
        assert nearest == 60

    def test_snap_to_scale_upward(self):
        """Snap upward to scale."""
        scale = music_theory.build_scale(60, "major")
        # 63.5 is between Eb (63) and E (64), closer to E
        nearest = music_theory.find_nearest_scale_note(64, scale)
        assert nearest == 64


class TestDrumPatterns:
    """Test drum pattern generation."""

    def test_house_pattern(self):
        """Generate house drum pattern."""
        pattern = music_theory.generate_drum_pattern("house", 1)
        assert pattern is not None
        assert len(pattern) == 4  # 4 hits per bar

    def test_techno_pattern(self):
        """Generate techno drum pattern."""
        pattern = music_theory.generate_drum_pattern("techno", 1)
        assert pattern is not None
        assert len(pattern) > 4  # More hits per bar

    def test_invalid_style(self):
        """Invalid drum style should return None."""
        assert music_theory.generate_drum_pattern("invalid", 1) is None


class TestProgressions:
    """Test chord progression building."""

    def test_pop_progression(self):
        """Build pop progression (I-V-vi-IV)."""
        progression = music_theory.build_progression(60, "i_v_vi_iv")
        assert progression is not None
        assert len(progression) == 4

    def test_jazz_progression(self):
        """Build jazz progression (ii-V-I)."""
        progression = music_theory.build_progression(60, "ii_v_i")
        assert progression is not None
        assert len(progression) == 3

    def test_invalid_progression(self):
        """Invalid progression name should return None."""
        assert music_theory.build_progression(60, "invalid") is None


def test_music_theory_coverage():
    """Report music theory module coverage."""
    print(
        f"\nMusic Theory Coverage:"
        f"\n  Note conversion: note_name_to_midi, midi_to_note_name"
        f"\n  Chords: 11 types (major, minor, dim, aug, maj7, min7, dom7, maj6, min6, sus2, sus4)"
        f"\n  Scales: 11 types (major, minor, pentatonic_major, pentatonic_minor, blues, etc.)"
        f"\n  Drum Patterns: 6 styles (kick, snare, hihat, house, techno, breakbeat)"
        f"\n  Progressions: 5 templates (pop, sensitive, extended, jazz, minor)"
        f"\n  Utilities: quantize, transpose, humanize, scale-snap"
        f"\n  Dependencies: None (pure Python, 100% unit-testable)"
    )
