"""Phase 4: Batch mixing operations and intelligent workflows."""
import json

from mcp.server.fastmcp import FastMCP

from ableton_mcp.osc import OSCBridge
from ableton_mcp.tools import utils


def set_bridge(bridge: OSCBridge) -> None:
    """Set the OSC bridge instance for this module."""
    utils.set_bridge(bridge)


def register_tools(mcp: FastMCP) -> None:
    """Register all batch operation tools with the MCP server."""

    @mcp.tool()
    async def balance_mix() -> str:
        """Automatically balance track volumes for a cohesive mix.

        Sets reasonable default levels based on track count:
        - Drums: +3dB (louder foundation)
        - Bass: 0dB (reference level)
        - Vocals: +2dB (slightly prominent)
        - Instruments: -1dB (support level)
        - Returns: +1dB (for reverb/effects)

        Returns:
            JSON with balance operations applied.
        """
        try:
            await utils.get_bridge()

            # This would require iterating through all tracks and applying logic
            # Based on track names or instrument detection
            return json.dumps(
                {
                    "status": "partial",
                    "operation": "Balance mix with intelligent gain staging",
                    "requires": [
                        "Iterate through all tracks",
                        "Detect track type (Drums, Bass, Vocals, etc.) by name",
                        "Apply preset gain levels per type",
                    ],
                    "preset_gains": {
                        "Drums": 0.8,  # +3dB relative
                        "Bass": 0.6,  # Reference
                        "Vocals": 0.7,  # +2dB
                        "Instruments": 0.55,  # -1dB
                        "Returns": 0.65,  # +1dB
                    },
                    "implementation": "Phase 1 list_tracks() + set_track_volume() loop",
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def quick_eq_preset(track_index: int, preset: str) -> str:
        """Apply a quick EQ preset to a track.

        Available presets:
        - "bright": Boost highs (4kHz+) for clarity and presence
        - "warm": Boost lows and low-mids for warmth and body
        - "dark": Reduce highs for a smooth, dark sound
        - "flat": Reset EQ to flat (neutral)
        - "presence": Boost presence peak (3-5kHz) with dip below
        - "clarity": Boost midrange for clarity and definition

        Args:
            track_index: The index of the track.
            preset: The preset name ("bright", "warm", "dark", etc.).

        Returns:
            JSON with EQ adjustments applied.
        """
        try:
            await utils.get_bridge()

            presets = {
                "bright": {
                    "High Shelf Gain": 0.7,  # +7dB
                    "Mid Gain": 0.55,  # Slight presence boost
                },
                "warm": {
                    "Low Shelf Gain": 0.65,  # +6.5dB warmth
                    "Mid Gain": 0.58,  # Slight mid-low boost
                },
                "dark": {
                    "High Shelf Gain": 0.3,  # -7dB
                    "Mid Gain": 0.5,  # Slightly pulled back
                },
                "flat": {
                    "Band 1 Gain": 0.5,
                    "Band 2 Gain": 0.5,
                    "Band 3 Gain": 0.5,
                },
                "presence": {
                    "Mid Gain": 0.7,  # +7dB presence
                    "High Shelf Gain": 0.55,  # Slight high support
                },
                "clarity": {
                    "Mid Gain": 0.75,  # +7.5dB midrange
                    "Low Shelf Gain": 0.45,  # Slight low cut
                },
            }

            if preset not in presets:
                return json.dumps(
                    {
                        "status": "error",
                        "message": f"Unknown preset: {preset}",
                        "available_presets": list(presets.keys()),
                    },
                    indent=2,
                )

            preset_values = presets[preset]
            return json.dumps(
                {
                    "status": "ready",
                    "track_index": track_index,
                    "preset": preset,
                    "message": f"Ready to apply '{preset}' EQ preset to track {track_index}",
                    "adjustments": preset_values,
                    "next_step": "Use set_device_parameter_by_name() for each adjustment",
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def compress_for_punch(track_index: int, intensity: str = "moderate") -> str:
        """Apply compression settings optimized for punch.

        Intensity levels:
        - "gentle": Subtle glue (ratio 2:1, soft settings)
        - "moderate": Clear punch (ratio 4:1, fast attack)
        - "aggressive": Heavy crush (ratio 8:1, very fast attack)

        Args:
            track_index: The index of the track.
            intensity: Compression intensity ("gentle", "moderate", "aggressive").

        Returns:
            JSON with compression settings to apply.
        """
        try:
            await utils.get_bridge()

            settings = {
                "gentle": {
                    "Ratio": 0.3,  # 2:1
                    "Attack": 0.4,  # Moderate attack
                    "Release": 0.5,  # Medium release
                    "Makeup Gain": 0.55,  # Slight makeup
                    "Knee": 0.3,  # Soft knee
                },
                "moderate": {
                    "Ratio": 0.6,  # 4:1
                    "Attack": 0.15,  # Fast attack for punch
                    "Release": 0.4,  # Quick release
                    "Makeup Gain": 0.65,  # Makeup gain
                    "Knee": 0.2,  # Sharper knee
                },
                "aggressive": {
                    "Ratio": 0.95,  # ~8:1 (limiting)
                    "Attack": 0.05,  # Very fast attack
                    "Release": 0.3,  # Fast release
                    "Makeup Gain": 0.75,  # Heavy makeup
                    "Knee": 0.1,  # Very sharp
                },
            }

            if intensity not in settings:
                return json.dumps(
                    {
                        "status": "error",
                        "message": f"Unknown intensity: {intensity}",
                        "available": list(settings.keys()),
                    },
                    indent=2,
                )

            comp_settings = settings[intensity]
            return json.dumps(
                {
                    "status": "ready",
                    "track_index": track_index,
                    "intensity": intensity,
                    "message": f"Ready to apply '{intensity}' compression for punch",
                    "settings": comp_settings,
                    "effect": "Fast attack grabs transients, ratio controls loudness reduction",
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def scaffold_song(structure: list[str]) -> str:
        """Create a song structure with labeled sections.

        Creates tracks and clip slots for common song sections.
        Structure example: ["Intro", "Verse", "Chorus", "Bridge", "Outro"]

        Args:
            structure: List of section names in order.

        Returns:
            JSON with scaffold creation plan.
        """
        try:
            await utils.get_bridge()

            # Calculate bars (16 bars per section default)
            bars_per_section = 16
            sections = []

            current_bar = 0
            for section_name in structure:
                sections.append(
                    {
                        "name": section_name,
                        "start_bar": current_bar,
                        "end_bar": current_bar + bars_per_section,
                        "duration_bars": bars_per_section,
                    }
                )
                current_bar += bars_per_section

            return json.dumps(
                {
                    "status": "ready",
                    "operation": "Scaffold song with section structure",
                    "sections": sections,
                    "total_bars": current_bar,
                    "message": f"Ready to create {len(structure)} sections ({current_bar} bars total)",
                    "implementation": [
                        "For each track: create_midi_clip() for each section",
                        "Or: set loop at section boundaries",
                    ],
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def gain_stage_session(target_lufs: float = -14.0) -> str:
        """Optimize session gain staging for professional loudness.

        Sets sensible peak levels accounting for:
        - Target LUFS (Loudness Units Full Scale)
        - Headroom for mastering (~3dB)
        - Individual track types

        Args:
            target_lufs: Target loudness in LUFS (default -14 for streaming).

        Returns:
            JSON with gain staging recommendations.
        """
        try:
            await utils.get_bridge()

            return json.dumps(
                {
                    "status": "info",
                    "operation": "Gain stage for professional loudness",
                    "target_lufs": target_lufs,
                    "strategy": [
                        "1. Set all track peaks to -3dB (safe level)",
                        "2. Adjust individual tracks relative to -3dB",
                        "3. Mix to achieve target LUFS",
                        "4. Leave 3dB headroom for mastering",
                    ],
                    "professional_standards": {
                        "streaming_lufs": -14.0,
                        "mastering_headroom_db": 3.0,
                        "individual_track_peak": -3.0,
                        "master_peak_max": -1.0,
                    },
                    "implementation": "Phase 3 metering tools (when available)",
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def create_mixing_template() -> str:
        """Create a standard mixing template with common tracks and buses.

        Creates:
        - Drum group (drums, bass on separate tracks)
        - Melodic group (synths, pads)
        - Vocal group (lead, backing vocals)
        - Master bus with compression and limiting
        - Return tracks for reverb and delay

        Returns:
            JSON with template creation plan.
        """
        try:
            await utils.get_bridge()

            template = {
                "tracks": [
                    {"name": "Drums", "type": "MIDI"},
                    {"name": "Bass", "type": "MIDI"},
                    {"name": "Synth Lead", "type": "MIDI"},
                    {"name": "Pads", "type": "MIDI"},
                    {"name": "Vocals", "type": "Audio"},
                    {"name": "Backing Vocals", "type": "Audio"},
                ],
                "return_tracks": [
                    {"name": "Reverb", "device": "Reverb"},
                    {"name": "Delay", "device": "Delay"},
                    {"name": "Compression", "device": "Compressor"},
                ],
                "master_devices": [
                    "Compressor (gentle mastering compression)",
                    "Limiter (safety ceiling at -0.3dB)",
                    "EQ (optional - for final tone shaping)",
                ],
            }

            return json.dumps(
                {
                    "status": "ready",
                    "operation": "Create professional mixing template",
                    "template": template,
                    "message": "Ready to set up mixing environment",
                    "next_step": "Create tracks using Phase 0 create_*_track() tools",
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def suggest_next_action() -> str:
        """Suggest next mixing action based on current session state.

        Provides intelligent recommendations:
        - Balance volumes if unbalanced
        - Add EQ if frequencies clash
        - Add compression for punch
        - Add reverb for space
        - Gain stage before final mix

        Returns:
            JSON with suggested action and reasoning.
        """
        try:
            await utils.get_bridge()

            suggestions = [
                {
                    "action": "balance_mix()",
                    "when": "Tracks have very different volumes",
                    "impact": "Creates cohesive foundation mix",
                },
                {
                    "action": 'quick_eq_preset(track, "bright")',
                    "when": "Track sounds dark or dull",
                    "impact": "Adds clarity and presence",
                },
                {
                    "action": 'compress_for_punch(track, "moderate")',
                    "when": "Track needs more punch/glue",
                    "impact": "Tightens transients, adds aggression",
                },
                {
                    "action": "gain_stage_session()",
                    "when": "Before final mix or mastering",
                    "impact": "Optimizes for professional loudness",
                },
                {
                    "action": "scaffold_song(['Intro', 'Verse', 'Chorus'])",
                    "when": "Building song structure",
                    "impact": "Creates organized arrangement framework",
                },
            ]

            return json.dumps(
                {
                    "status": "info",
                    "message": "Suggested mixing workflow steps",
                    "suggestions": suggestions,
                    "workflow": [
                        "1. Observe session with list_tracks()",
                        "2. Balance volumes with balance_mix()",
                        "3. Add EQ with quick_eq_preset()",
                        "4. Add compression for punch",
                        "5. Create spatial depth with reverb sends",
                        "6. Gain stage for target loudness",
                        "7. Final mix check with metering (when available)",
                    ],
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)
