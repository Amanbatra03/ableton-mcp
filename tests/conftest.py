"""Pytest configuration and fixtures."""
import asyncio
import sys
from pathlib import Path

import pytest

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Only import pythonosc if available (required for integration tests)
try:
    from pythonosc import dispatcher, osc_server

    HAS_PYTHONOSC = True
except ImportError:
    HAS_PYTHONOSC = False


@pytest.fixture
async def fake_osc_server():
    """Create a fake OSC server for testing (no real Ableton needed)."""
    if not HAS_PYTHONOSC:
        pytest.skip("pythonosc not installed")
    disp = dispatcher.Dispatcher()
    server = osc_server.AsyncIOOSCUDPServer(("127.0.0.1", 11001), disp)
    transport, protocol = await server.create_serve_endpoint()
    yield server
    server.shutdown()


@pytest.fixture
def event_loop():
    """Create and run an event loop for the test."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
