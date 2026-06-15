"""OSC message dispatcher with request/response correlation."""
import asyncio
import logging
from typing import Any, Awaitable, Callable, Dict

from pythonosc import dispatcher, osc_server

logger = logging.getLogger(__name__)


class OSCDispatcher:
    """Manages OSC message receiving and correlates replies with requests."""

    def __init__(self, host: str = "127.0.0.1", port: int = 11001):
        """Initialize the OSC dispatcher.

        Args:
            host: IP address to bind to
            port: UDP port to listen on
        """
        self.host = host
        self.port = port
        self._dispatcher = dispatcher.Dispatcher()
        self._server: osc_server.AsyncIOOSCUDPServer | None = None
        self._futures: Dict[str, asyncio.Future[Any]] = {}
        self._default_handler_set = False

    def set_default_handler(
        self, handler: Callable[[str, list[Any]], Awaitable[None]]
    ) -> None:
        """Set a default handler for all unmapped OSC addresses.

        Args:
            handler: Async function that receives (address, args)
        """

        def sync_handler(address: str, args: list[Any]) -> None:
            asyncio.create_task(handler(address, args))

        self._dispatcher.set_default_handler(sync_handler)
        self._default_handler_set = True

    def map_handler(
        self, address: str, handler: Callable[[str, list[Any]], Awaitable[None]]
    ) -> None:
        """Map an OSC address to an async handler.

        Args:
            address: OSC address pattern
            handler: Async function that receives (address, args)
        """

        def sync_handler(unused_addr: str, args: list[Any]) -> None:
            asyncio.create_task(handler(address, args))

        self._dispatcher.map(address, sync_handler)

    async def handle_reply(self, address: str, args: list[Any]) -> None:
        """Handle an incoming OSC reply by fulfilling the waiting future.

        Args:
            address: OSC address of the reply
            args: Arguments from the OSC message
        """
        if address in self._futures:
            future = self._futures.pop(address)
            if not future.done():
                # Parse the reply: single value or tuple
                value = args[0] if len(args) == 1 else args
                future.set_result(value)
                logger.debug(f"Resolved {address}: {value}")
        else:
            logger.debug(f"Received unmatched reply on {address}: {args}")

    def register_reply_handler(self, reply_address: str) -> None:
        """Register a handler for a specific reply address.

        Args:
            reply_address: OSC address to listen for
        """
        self.map_handler(reply_address, self.handle_reply)

    def await_reply(self, address: str) -> asyncio.Future[Any]:
        """Register a future to await a reply on the given address.

        Args:
            address: OSC address to await a reply on

        Returns:
            An asyncio.Future that will be fulfilled when the reply arrives
        """
        future: asyncio.Future[Any] = asyncio.Future()
        self._futures[address] = future
        self.register_reply_handler(address)
        return future

    async def start(self) -> None:
        """Start the OSC server."""
        if not self._default_handler_set:
            await self.set_default_handler(self.handle_reply)

        self._server = osc_server.AsyncIOOSCUDPServer(
            (self.host, self.port), self._dispatcher
        )
        transport, protocol = await self._server.create_serve_endpoint()
        logger.info(f"OSC server started on {self.host}:{self.port}")

    async def stop(self) -> None:
        """Stop the OSC server."""
        if self._server:
            self._server.shutdown()
            logger.info("OSC server stopped")

    def clear_pending(self) -> None:
        """Clear all pending futures (on shutdown or error)."""
        for future in self._futures.values():
            if not future.done():
                future.cancel()
        self._futures.clear()
