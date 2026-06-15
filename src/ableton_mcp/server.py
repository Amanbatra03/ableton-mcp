"""Main MCP server for Ableton Live automation."""
import logging

from mcp.server.fastmcp import FastMCP

from ableton_mcp.config import settings
from ableton_mcp.osc import OSCBridge
from ableton_mcp.tools import clips, devices, mixer, tracks, transport

logger = logging.getLogger(__name__)

if settings.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


def create_app() -> FastMCP:
    """Create and configure the MCP server application."""
    mcp = FastMCP(
        "Ableton",
        instructions="Control Ableton Live via OSC. The OSC bridge will start automatically on first use.",
    )

    bridge = OSCBridge(
        host=settings.ableton_ip,
        send_port=settings.ableton_send_port,
        recv_port=settings.ableton_recv_port,
        timeout=settings.osc_timeout_seconds,
    )

    transport.set_bridge(bridge)
    tracks.set_bridge(bridge)
    clips.set_bridge(bridge)
    devices.set_bridge(bridge)
    mixer.set_bridge(bridge)

    transport.register_tools(mcp)
    tracks.register_tools(mcp)
    clips.register_tools(mcp)
    devices.register_tools(mcp)
    mixer.register_tools(mcp)

    logger.info("Ableton MCP server initialized")

    return mcp


app = create_app()
