"""Phase 3: Metering and analysis tools (loudness, clipping, levels)."""
import json

from mcp.server.fastmcp import FastMCP

from ableton_mcp.osc import OSCBridge
from ableton_mcp.tools import utils


def set_bridge(bridge: OSCBridge) -> None:
    """Set the OSC bridge instance for this module."""
    utils.set_bridge(bridge)


def register_tools(mcp: FastMCP) -> None:
    """Register all metering and analysis tools with the MCP server."""

    @mcp.tool()
    async def get_track_meter(track_index: int) -> str:
        """Get current audio metering information for a track.

        Provides peak level, RMS (average) level, and headroom information.

        Args:
            track_index: The index of the track.

        Returns:
            JSON with MeterInfo containing peak_db, rms_db, headroom_db, is_clipping.
        """
        try:
            await utils.get_bridge()

            # Note: AbletonOSC may not expose metering directly
            # This would require:
            # /live/track/get/meter_left
            # /live/track/get/meter_right
            # /live/track/get/meter_level

            # For now, return placeholder with instructions
            return json.dumps(
                {
                    "status": "partial",
                    "track_index": track_index,
                    "message": "Track metering requires AbletonOSC meter endpoints",
                    "note": "Implement with /live/track/get/meter_* endpoints if available",
                    "what_would_work": {
                        "peak_db": -3.5,
                        "rms_db": -15.2,
                        "headroom_db": 3.5,
                        "is_clipping": False,
                    },
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def analyze_loudness(track_index: int) -> str:
        """Analyze loudness of a track using LUFS standard.

        Provides loudness in LUFS (Loudness Units relative to Full Scale),
        loudness range, and peak levels for professional loudness analysis.

        Args:
            track_index: The index of the track.

        Returns:
            JSON with loudness analysis (LUFS, loudness_range, integrated, peaks).
        """
        try:
            await utils.get_bridge()

            # LUFS analysis would require:
            # - Continuous sampling of track output
            # - Integration window (e.g., 3 seconds)
            # - Loudness calculation following ITU-R BS.1770-4 standard

            # This is complex and likely requires custom implementation
            return json.dumps(
                {
                    "status": "info",
                    "track_index": track_index,
                    "message": "LUFS loudness analysis requires real-time sampling",
                    "requirements": [
                        "Continuous audio sampling from track output",
                        "ITU-R BS.1770-4 loudness calculation",
                        "Integration window (typically 3 seconds)",
                    ],
                    "how_to_implement": "Custom Remote Script or Max for Live device with metering",
                    "reference_standard": "ITU-R BS.1770-4",
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def get_clip_detection(track_index: int) -> str:
        """Detect if a track is clipping (exceeding 0dB).

        Useful for gain staging and mixing safety checks.

        Args:
            track_index: The index of the track.

        Returns:
            JSON with is_clipping boolean and peak_db if clipping detected.
        """
        try:
            await utils.get_bridge()

            # Clipping detection requires:
            # /live/track/get/meter_peak or similar

            return json.dumps(
                {
                    "status": "info",
                    "track_index": track_index,
                    "is_clipping": False,
                    "message": "Clipping detection requires track meter peak endpoint",
                    "suggestion": "Use get_track_meter() when metering endpoints available",
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def get_master_meter() -> str:
        """Get metering information for the master track.

        Provides overall mix loudness, peak levels, and headroom for safety.

        Returns:
            JSON with master MeterInfo (peak_db, rms_db, headroom_db).
        """
        try:
            await utils.get_bridge()

            # Master metering would require:
            # /live/song/get/master_meter_left
            # /live/song/get/master_meter_right

            return json.dumps(
                {
                    "status": "info",
                    "track": "master",
                    "message": "Master metering requires master track meter endpoints",
                    "typical_safe_levels": {
                        "peak_db": -3.0,
                        "rms_db": -18.0,
                        "headroom_db": 3.0,
                    },
                    "professional_loudness": {
                        "lufs_target": -14.0,
                        "lufs_max_short_term": -11.0,
                    },
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def spectrum_analysis(track_index: int) -> str:
        """Analyze frequency spectrum of a track.

        Provides frequency content to identify presence or absence of
        specific frequency ranges (bass, mids, treble, etc.).

        Args:
            track_index: The index of the track.

        Returns:
            JSON with frequency spectrum analysis (freq_db mapping).
        """
        try:
            await utils.get_bridge()

            # Spectrum analysis requires:
            # - Real-time FFT of track output
            # - Frequency binning (e.g., 31 bands 1/3 octave)

            return json.dumps(
                {
                    "status": "info",
                    "track_index": track_index,
                    "message": "Spectrum analysis requires real-time FFT analysis",
                    "how_to_implement": "Max for Live analyzer or custom Remote Script",
                    "useful_for": [
                        "Identifying muddy frequencies",
                        "Detecting frequency clashes",
                        "Equalizer targeting",
                        "Mix balance visualization",
                    ],
                    "frequency_bands": {
                        "sub_bass": "20-60 Hz",
                        "bass": "60-250 Hz",
                        "low_mid": "250-500 Hz",
                        "mid": "500-2000 Hz",
                        "high_mid": "2000-4000 Hz",
                        "presence": "4000-6000 Hz",
                        "brilliance": "6000-20000 Hz",
                    },
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool()
    async def check_headroom(track_index: int, target_db: float = -3.0) -> str:
        """Check if a track has sufficient headroom to target.

        Useful for gain staging to ensure clean recording without clipping.

        Args:
            track_index: The index of the track.
            target_db: Target headroom in dB (default -3.0dB).

        Returns:
            JSON with headroom status and recommendation.
        """
        try:
            await utils.get_bridge()

            # Headroom check requires:
            # /live/track/get/meter_peak

            return json.dumps(
                {
                    "status": "info",
                    "track_index": track_index,
                    "target_headroom_db": target_db,
                    "message": "Headroom check requires track peak meter",
                    "recommendation": "Use gain staging tools when metering available",
                    "professional_standards": {
                        "digital_peak_target": -3.0,
                        "loudness_target_lufs": -14.0,
                        "safety_margin_db": 3.0,
                    },
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)
