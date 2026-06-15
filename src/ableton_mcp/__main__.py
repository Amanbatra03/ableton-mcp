"""Entry point for running the Ableton MCP server."""
from ableton_mcp.server import app


def main() -> None:
    """Run the MCP server."""
    app.run()


if __name__ == "__main__":
    main()
