# Installation Guide

## Prerequisites

- **Ableton Live 11.3+** (any edition)
- **Python 3.11+**
- **AbletonOSC** (Ableton Remote Script)

## Step 1: Install AbletonOSC (Required)

AbletonOSC is the OSC bridge that enables communication between Claude and Ableton Live.

### On Windows

1. Download AbletonOSC from: https://github.com/ideoforms/AbletonOSC
2. Extract the `AbletonOSC/` folder
3. Copy it to:
   ```
   C:\Users\<USERNAME>\AppData\Roaming\Ableton\Live 11.3.20\Preferences\User Remote Scripts\
   ```
4. **Restart Ableton Live**
5. In Live: **Preferences → Link/MIDI → Control Surfaces**
6. Select **AbletonOSC** from the dropdown

### On macOS

1. Download AbletonOSC from: https://github.com/ideoforms/AbletonOSC
2. Extract the `AbletonOSC/` folder
3. Copy it to:
   ```
   ~/Library/Preferences/Ableton/Live\ 11.3.20/User\ Remote\ Scripts/
   ```
4. **Restart Ableton Live**
5. In Live: **Preferences → Link/MIDI → Control Surfaces**
6. Select **AbletonOSC** from the dropdown

### On Linux

1. Download AbletonOSC from: https://github.com/ideoforms/AbletonOSC
2. Extract the `AbletonOSC/` folder
3. Copy it to:
   ```
   ~/.config/Ableton/Live\ 11.3.20/User\ Remote\ Scripts/
   ```
4. **Restart Ableton Live**
5. In Live: **Preferences → Link/MIDI → Control Surfaces**
6. Select **AbletonOSC** from the dropdown

### Verify AbletonOSC is Working

In Ableton Live, you should see in the status bar:
> "AbletonOSC listening on port 11000"

If not, check that the port (11000) is not blocked by a firewall.

## Step 2: Install Ableton MCP

### Option A: From PyPI (Recommended)

```bash
pip install ableton-mcp
```

Then run:

```bash
ableton-mcp
```

### Option B: From Source with uv (Development)

```bash
git clone https://github.com/Amanbatra03/ableton-mcp
cd ableton-mcp

# Install dependencies
uv sync

# Run the server
uv run ableton-mcp
```

### Option C: From Source with pip

```bash
git clone https://github.com/Amanbatra03/ableton-mcp
cd ableton-mcp

# Install in development mode
pip install -e ".[dev]"

# Run the server
python -m ableton_mcp
```

## Step 3: Configure Environment (Optional)

Create a `.env` file in the project root:

```env
# Default values shown
ABLETON_IP=127.0.0.1
ABLETON_SEND_PORT=11000
ABLETON_RECV_PORT=11001
OSC_TIMEOUT_SECONDS=2.0
DEBUG=false
```

## Step 4: Connect with Claude

### Option A: Claude Desktop (Recommended)

1. Install [Claude Desktop](https://claude.ai/download)
2. Open the configuration file:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`
3. Add the MCP server:
   ```json
   {
     "mcpServers": {
       "ableton": {
         "command": "uvx",
         "args": ["ableton-mcp"]
       }
     }
   }
   ```
4. Restart Claude Desktop

### Option B: Claude Code CLI

```bash
claude mcp add --transport stdio ableton -- uvx ableton-mcp
```

### Option C: Manual MCP Registration

If using Claude API or another client, start the server:

```bash
ableton-mcp
```

The server will listen on stdin/stdout for MCP protocol messages.

## Step 5: Verify Installation

1. **Start Ableton Live** with a session open
2. **Open Claude** (Desktop or Code)
3. **Type this test command:**
   ```
   What's the current tempo in Ableton?
   ```
4. **Claude should use the `get_tempo()` tool** and return the tempo value

If it works, you're set! If not, see **Troubleshooting** below.

## Troubleshooting

### "OSCBridge failed to connect"

- **Verify AbletonOSC is installed** and appears in Live's Control Surfaces
- **Check the port**: Default is 11000 (send) and 11001 (receive)
- **Check your firewall**: Ensure UDP ports 11000-11001 are not blocked
- **Restart Ableton Live**: Sometimes the Remote Script needs to be re-initialized

### "ModuleNotFoundError: No module named 'ableton_mcp'"

- **Re-install**: `pip install --upgrade ableton-mcp`
- **Or from source**: `pip install -e .` from the project directory

### "Timeout waiting for OSC response"

- **Ableton Live might be frozen**: Check the application
- **Increase timeout**: Edit `.env` and set `OSC_TIMEOUT_SECONDS=5.0`
- **Check network**: Ensure 127.0.0.1 is accessible (not firewalled)

### Claude doesn't see the Ableton tools

- **Restart Claude**: Close and re-open the application
- **Check MCP registration**: Run `claude mcp list` (if using Claude CLI)
- **Check logs**: Enable `DEBUG=true` in `.env` for verbose output

### Tools call successfully but Ableton doesn't respond

- **AbletonOSC might have crashed**: Check Live's status bar
- **Restart the MCP server**: Stop and re-run `ableton-mcp`
- **Check that Ableton Live is in focus**: Some operations require active window

## Getting Help

- **GitHub Issues**: https://github.com/Amanbatra03/ableton-mcp/issues
- **Documentation**: See `README.md`, `CONTRIBUTING.md`, `FINAL_SUMMARY.md`
- **Example Prompts**: See `README.md` under "Example Commands"

## Next Steps

Once installed, try these commands in Claude:

### Basic Mixing
- "What tracks are in my session?"
- "Make the drums brighter"
- "Balance the mix"
- "Add punch to the vocals"

### Advanced
- "Create a C major chord starting at beat 2"
- "Generate a house drum pattern for 2 bars"
- "Create a pop chord progression starting from C"
- "Make the bass warmer and add some compression"

### Full Workflows
- "Create a mixing template for my song"
- "Scaffold a song with intro, verse, chorus, bridge, and outro"
- "Balance the mix, make drums bright, and add compression for punch"

See `README.md` for more examples and the full tool catalog.
