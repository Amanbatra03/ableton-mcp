"""Main MCP server for Ableton Live automation."""
import logging

from mcp.server.fastmcp import FastMCP

from ableton_mcp.config import settings
from ableton_mcp.osc import OSCBridge
from ableton_mcp.tools import clips, devices, tracks, transport

logger = logging.getLogger(__name__)

if settings.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


def create_app() -> FastMCP:
    """Create and configure the MCP server application."""
    mcp = FastMCP("Ableton", instructions="Control Ableton Live via OSC")

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

    transport.register_tools(mcp)
    tracks.register_tools(mcp)
    clips.register_tools(mcp)
    devices.register_tools(mcp)

    async def startup() -> None:
        """Called when the server starts."""
        try:
            await bridge.start()
            logger.info("Ableton MCP server started")
        except Exception as e:
            logger.error(f"Failed to start OSC bridge: {e}")
            raise

    async def shutdown() -> None:
        """Called when the server shuts down."""
        try:
            await bridge.stop()
            logger.info("Ableton MCP server stopped")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

    mcp._on_startup = startup
    mcp._on_shutdown = shutdown

    return mcp


app = create_app()
