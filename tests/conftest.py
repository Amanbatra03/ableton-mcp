"""Pytest configuration and fixtures."""
import asyncio
import pytest
from pythonosc import dispatcher, osc_server


@pytest.fixture
async def fake_osc_server():
    """Create a fake OSC server for testing (no real Ableton needed)."""
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
