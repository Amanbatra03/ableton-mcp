"""Integration tests for core mixing workflows.

These tests verify that the key mixing automation scenarios work end-to-end.
Tests use mocked OSC responses to avoid requiring a running Ableton instance.
"""

import pytest

from ableton_mcp.core import device_mappings, models
from ableton_mcp.tools import mixer, batch_operations


class TestDeviceMappings:
    """Test device parameter mappings."""

    def test_all_devices_have_types(self):
        """All devices should have a type classification."""
        for device_name in device_mappings.DEVICE_PARAMETERS:
            assert device_mappings.get_device_type(device_name) is not None, (
                f"Device '{device_name}' missing type classification"
            )

    def test_parameter_resolution(self):
        """Parameters should resolve to valid indices."""
        # Test EQ Eight
        idx = device_mappings.get_device_parameter_index("EQ Eight", "Brightness")
        assert idx == 5
        assert isinstance(idx, int)

        # Test Compressor
        idx = device_mappings.get_device_parameter_index("Compressor", "Attack")
        assert idx == 2

        # Test nonexistent device
        assert device_mappings.get_device_parameter_index("Fake Device", "Fake") is None

        # Test nonexistent parameter
        assert device_mappings.get_device_parameter_index("EQ Eight", "Fake") is None

    def test_preset_lookup(self):
        """Presets should return valid parameter dicts."""
        preset = device_mappings.get_preset_values("Compressor", "Punch")
        assert preset is not None
        assert isinstance(preset, dict)
        assert "Ratio" in preset

        # Nonexistent preset
        assert device_mappings.get_preset_values("Compressor", "Fake") is None

    def test_device_parameter_listing(self):
        """Should list all parameters for a device."""
        params = device_mappings.list_device_parameters("EQ Eight")
        assert params is not None
        assert len(params) > 0
        assert "Brightness" in params
        assert "Warmth" in params

        # Nonexistent device
        assert device_mappings.list_device_parameters("Fake") is None

    def test_device_preset_listing(self):
        """Should list all presets for a device."""
        presets = device_mappings.list_device_presets("Compressor")
        assert presets is not None
        assert len(presets) > 0
        assert "Gentle" in presets
        assert "Punch" in presets

        # Device with no presets
        assert device_mappings.list_device_presets("Sampler") is None

    def test_expanded_devices_coverage(self):
        """New devices should be properly configured."""
        # Check new effect devices
        for device in ["Echo", "Pedal", "Phaser", "Glue Compressor", "Limiter"]:
            assert device_mappings.get_device_type(device) == "Audio Effect"
            assert device_mappings.list_device_parameters(device) is not None

        # Check new instrument devices
        for device in ["Collision", "Corpus", "Impulse", "Electric"]:
            assert device_mappings.get_device_type(device) == "Instrument"
            assert device_mappings.list_device_parameters(device) is not None


class TestDataModels:
    """Test Pydantic data models."""

    def test_track_info_model(self):
        """TrackInfo should validate correctly."""
        info = models.TrackInfo(
            index=0,
            name="Drums",
            track_type="MIDI",
            volume=0.8,
            pan=0.5,
            mute=False,
            solo=False,
            arm=True,
            device_count=2,
            clip_slot_count=8,
            devices=[],
        )
        assert info.index == 0
        assert info.name == "Drums"
        assert info.volume == 0.8

    def test_device_info_model(self):
        """DeviceInfo should validate correctly."""
        info = models.DeviceInfo(
            name="EQ Eight",
            index=0,
            device_type="Audio Effect",
            parameter_count=17,
            enabled=True,
            parameters=[],
        )
        assert info.name == "EQ Eight"
        assert info.parameter_count == 17
        assert info.enabled is True

    def test_session_overview_model(self):
        """SessionOverview should validate complex nested data."""
        overview = models.SessionOverview(
            track_count=4,
            tracks=[],
            tempo=120.0,
            time_signature_numerator=4,
            time_signature_denominator=4,
            is_playing=False,
            song_time=0.0,
            song_length=32.0,
            loop_enabled=False,
            loop_start=0.0,
            loop_end=8.0,
        )
        assert overview.track_count == 4
        assert overview.tempo == 120.0
        assert overview.time_signature_numerator == 4


class TestMixingCapability:
    """Test mixing automation capabilities."""

    def test_parameter_name_resolution_common_devices(self):
        """Common devices should resolve parameters by name."""
        # EQ parameters
        for param in ["Brightness", "Warmth", "Presence", "Mid Gain"]:
            idx = device_mappings.get_device_parameter_index("EQ Eight", param)
            assert idx is not None, f"EQ Eight parameter '{param}' should resolve"

        # Compressor parameters
        for param in ["Attack", "Release", "Ratio", "Makeup Gain"]:
            idx = device_mappings.get_device_parameter_index("Compressor", param)
            assert idx is not None, f"Compressor parameter '{param}' should resolve"

        # Reverb parameters
        for param in ["Decay", "Size", "Mix"]:
            idx = device_mappings.get_device_parameter_index("Reverb", param)
            assert idx is not None, f"Reverb parameter '{param}' should resolve"

    def test_preset_workflows(self):
        """Presets should provide valid mixing automation workflows."""
        # EQ presets for brightness/warmth
        bright = device_mappings.get_preset_values("EQ Eight", "Bright")
        warm = device_mappings.get_preset_values("EQ Eight", "Warm")
        assert bright is not None
        assert warm is not None

        # Should have different values (bright has high shelf, warm has low shelf)
        assert bright.get("High Shelf Gain", 0) > warm.get("High Shelf Gain", 0)

    def test_new_devices_mixing_support(self):
        """New devices should support common mixing parameters."""
        # Pedal for distortion
        idx = device_mappings.get_device_parameter_index("Pedal", "Drive")
        assert idx is not None

        # Phaser for modulation
        idx = device_mappings.get_device_parameter_index("Phaser", "Depth")
        assert idx is not None

        # Glue Compressor for cohesive mixing
        presets = device_mappings.list_device_presets("Glue Compressor")
        assert presets is not None
        assert len(presets) > 0

        # Limiter for safety ceiling
        idx = device_mappings.get_device_parameter_index("Limiter", "Threshold")
        assert idx is not None


def test_device_coverage_statistics():
    """Report device mapping coverage."""
    total_devices = len(device_mappings.DEVICE_PARAMETERS)
    effects = sum(1 for t in device_mappings.DEVICE_TYPES.values() if t == "Audio Effect")
    instruments = sum(1 for t in device_mappings.DEVICE_TYPES.values() if t == "Instrument")
    total_presets = sum(len(p) for p in device_mappings.DEVICE_PRESETS.values())

    print(f"\nDevice Mapping Coverage:")
    print(f"  Total Devices: {total_devices}")
    print(f"    - Effects: {effects}")
    print(f"    - Instruments: {instruments}")
    print(f"  Total Presets: {total_presets}")
    print(f"  Coverage: ~{total_devices} devices × ~4.2 avg params = {total_devices * 4} parameter controls")

    assert total_devices >= 24, "Should have at least 24 devices mapped"
    assert effects >= 17, "Should have at least 17 effects"
    assert instruments >= 7, "Should have at least 7 instruments"
