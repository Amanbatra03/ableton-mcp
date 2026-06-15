"""Tests for OSC bridge functionality."""
import pytest
from ableton_mcp.core.errors import NotConnectedError
from ableton_mcp.osc import OSCBridge


@pytest.mark.asyncio
async def test_bridge_not_connected_error():
    """Test that bridge raises NotConnectedError when not started."""
    bridge = OSCBridge()
    with pytest.raises(NotConnectedError):
        bridge.send("/test", [1, 2, 3])


@pytest.mark.asyncio
async def test_bridge_startup():
    """Test that bridge can start and stop."""
    bridge = OSCBridge()
    await bridge.start()
    assert bridge._connected
    await bridge.stop()
    assert not bridge._connected
