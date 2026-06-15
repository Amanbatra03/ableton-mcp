"""OSC client with request/response pattern."""
import asyncio
import logging
from typing import Any

from pythonosc import udp_client

from ableton_mcp.config import settings
from ableton_mcp.core.errors import NotConnectedError
from ableton_mcp.core.errors import TimeoutError as AbletonTimeoutError

from .dispatcher import OSCDispatcher

logger = logging.getLogger(__name__)


class OSCBridge:
    """Bridges OSC send/receive with async request/response pattern."""

    def __init__(
        self,
        host: str = settings.ableton_ip,
        send_port: int = settings.ableton_send_port,
        recv_port: int = settings.ableton_recv_port,
        timeout: float = settings.osc_timeout_seconds,
    ):
        """Initialize the OSC bridge.

        Args:
            host: Ableton OSC host (IP address)
            send_port: AbletonOSC send port (default 11000)
            recv_port: AbletonOSC receive port (default 11001)
            timeout: Timeout for waiting on replies (seconds)
        """
        self.host = host
        self.send_port = send_port
        self.recv_port = recv_port
        self.timeout = timeout
        self._client = udp_client.SimpleUDPClient(host, send_port)
        self._dispatcher = OSCDispatcher(host, recv_port)
        self._connected = False

    async def start(self) -> None:
        """Start the OSC receive server."""
        await self._dispatcher.start()
        self._connected = True
        logger.info(f"OSC bridge started: send to {self.host}:{self.send_port}, recv on port {self.recv_port}")

    async def stop(self) -> None:
        """Stop the OSC receive server."""
        await self._dispatcher.stop()
        self._dispatcher.clear_pending()
        self._connected = False

    def send(self, address: str, args: Any | list[Any] | None = None) -> None:
        """Send an OSC message without waiting for a reply.

        Args:
            address: OSC address
            args: Arguments to send (can be a single value or list)

        Raises:
            NotConnectedError: If the bridge hasn't been started
        """
        if not self._connected:
            raise NotConnectedError("OSC bridge not started. Call start() first.")

        try:
            if args is None:
                self._client.send_message(address, [])
            elif isinstance(args, list):
                self._client.send_message(address, args)
            else:
                self._client.send_message(address, args)
        except Exception as e:
            logger.error(f"Error sending OSC message to {address}: {e}")
            raise NotConnectedError(f"Failed to send OSC message: {e}")

    async def send_and_receive(
        self, address: str, args: Any | list[Any] | None = None, reply_address: str | None = None
    ) -> Any:
        """Send an OSC message and wait for a reply.

        Args:
            address: OSC address to send to
            args: Arguments to send
            reply_address: Address to listen for reply on (defaults to address + "_result")

        Returns:
            The reply value from Ableton

        Raises:
            NotConnectedError: If not connected to Ableton
            AbletonTimeoutError: If the reply doesn't arrive within the timeout
        """
        if not self._connected:
            raise NotConnectedError("OSC bridge not started. Call start() first.")

        if reply_address is None:
            reply_address = address.rstrip("/") + "/result"

        future = self._dispatcher.await_reply(reply_address)
        self.send(address, args)

        try:
            result = await asyncio.wait_for(future, timeout=self.timeout)
            return result
        except asyncio.TimeoutError:
            logger.error(f"OSC timeout waiting for {reply_address}")
            raise AbletonTimeoutError(f"No reply from Ableton on {reply_address} within {self.timeout}s")

    async def ping(self) -> float:
        """Test connection to Ableton and return the current tempo.

        Raises:
            NotConnectedError: If Ableton is not responding

        Returns:
            Current tempo in BPM
        """
        try:
            tempo = await self.send_and_receive("/live/song/get/tempo", reply_address="/live/song/get/tempo/result")
            return float(tempo)
        except (AbletonTimeoutError, NotConnectedError) as e:
            raise NotConnectedError(f"Ableton Live is not responding: {e}")
