# Contributing to Ableton MCP

This guide outlines how to develop, test, and contribute to the Ableton MCP server.

## Development Setup

### 1. Install Dependencies

```bash
# Clone the repository
git clone https://github.com/Amanbatra03/ableton-mcp
cd ableton-mcp

# Install with uv (recommended)
uv sync --all-extras

# Or with pip
pip install -e ".[dev]"
```

### 2. Verify Installation

```bash
# Run linting
ruff check src/ tests/

# Run type checking
pyright src/

# Run tests (no Ableton required)
pytest tests/ -v -m "not live"
```

## Code Quality

### Linting

All code must pass **ruff** linting (PEP 8, import order, etc.):

```bash
uv run ruff check src/ tests/
uv run ruff format src/ tests/  # Auto-fix
```

### Type Hints

All functions should have type hints. Run **pyright** for type checking:

```bash
uv run pyright src/
```

### Testing

Write tests for new features. Place them in `tests/`:

```bash
# Run all tests (skip live ones)
uv run pytest tests/ -v -m "not live"

# Run a specific test file
uv run pytest tests/test_mixing_workflows.py -v

# Run with live Ableton (requires running instance)
uv run pytest tests/ -m "live"
```

## Adding New Tools

### 1. Create a Tool Module

Add a new file in `src/ableton_mcp/tools/` (e.g., `my_feature.py`):

```python
"""Phase X: My feature description."""
from mcp.server.fastmcp import FastMCP
from ableton_mcp.osc import OSCBridge
from ableton_mcp.tools import utils

def set_bridge(bridge: OSCBridge) -> None:
    """Set the OSC bridge instance."""
    utils.set_bridge(bridge)

def register_tools(mcp: FastMCP) -> None:
    """Register all tools with the MCP server."""
    
    @mcp.tool()
    async def my_tool(param: str) -> str:
        """Tool description."""
        try:
            await utils.get_bridge()
            # Implementation
            return json.dumps({"status": "success"}, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)
```

### 2. Register in Server

Update `src/ableton_mcp/server.py`:

```python
from ableton_mcp.tools import my_feature

# In create_app():
my_feature.set_bridge(bridge)
my_feature.register_tools(mcp)
```

### 3. Add Tests

Create tests in `tests/test_my_feature.py`:

```python
import pytest

class TestMyFeature:
    def test_my_tool(self):
        """Test my_tool."""
        # Your test here
        pass
```

## Adding Device Support

Expand device mappings in `src/ableton_mcp/core/device_mappings.py`:

```python
DEVICE_PARAMETERS = {
    "New Device": {
        "Parameter 1": 0,
        "Parameter 2": 1,
        # ... more parameters
    },
}

DEVICE_TYPES = {
    "New Device": "Audio Effect",  # or "Instrument"
}

DEVICE_PRESETS = {
    "New Device": {
        "Preset Name": {"Parameter 1": 0.5},
    },
}
```

## Commit Guidelines

Use conventional commits:

```
feat: add new feature
fix: fix a bug
refactor: restructure code
docs: update documentation
test: add or update tests
chore: dependency updates, config changes
```

Example:

```
feat(devices): add Pedal device parameter mappings
- Add Pedal device with Drive, Tone, Output parameters
- Add presets for light/heavy distortion
- Update device coverage to 24 devices
```

## Pull Request Process

1. Create a feature branch: `git checkout -b feat/my-feature`
2. Make changes and test locally
3. Run full CI suite: `ruff check`, `pyright`, `pytest`
4. Commit with conventional message
5. Push and create PR against `main`
6. Ensure CI passes

## Architecture Notes

- **Phase 0**: Basic transport/track/clip control (26 tools)
- **Phase 1**: Observation/monitoring (9 tools)
- **Phase 2**: Intelligent device control (1 tool + mappings)
- **Phase 3**: Metering framework (6 tools)
- **Phase 4**: Batch workflows (7 tools)

When adding new features, decide which phase they belong to and follow the established patterns.

## Performance Considerations

- **OSC round-trips**: ~200ms per request. Batch operations where possible.
- **Lazy initialization**: OSC bridge starts on first tool use, not server startup.
- **Timeouts**: 2s default for OSC operations (configurable via `.env`).

## Troubleshooting

### "ModuleNotFoundError: No module named 'ableton_mcp'"

Install in editable mode:

```bash
uv pip install -e .
```

### "pythonosc: No module named"

Install dev dependencies:

```bash
uv sync --all-extras
```

### Type checking fails

Run pyright with verbose output:

```bash
pyright src/ --outputjson
```

## Questions?

- Check existing issues/discussions on GitHub
- Review FINAL_SUMMARY.md for architecture overview
- Look at PHASE2_FINDINGS.md for AbletonOSC API details
