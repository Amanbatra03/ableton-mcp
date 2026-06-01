# Ableton Live MCP Server

> An MCP (Model Context Protocol) server that exposes Ableton Live controls as AI-callable tools — enabling any MCP-compatible LLM (Claude, GPT-4, etc.) to compose, arrange, and mix music through natural language.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![MCP](https://img.shields.io/badge/MCP-FastMCP-blueviolet)
![OSC](https://img.shields.io/badge/Protocol-OSC-orange)
![Ableton](https://img.shields.io/badge/Ableton-Live-black)

---

## Overview

This project bridges the gap between **Large Language Models** and **Digital Audio Workstations**. Using the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), it exposes Ableton Live's core controls as structured tools that any AI assistant can call.

Ask an AI: *"Create a 4-bar MIDI clip on track 0, add a C major chord on beat 1, and set the tempo to 128 BPM"* — the LLM will orchestrate multiple tool calls to make it happen, in real-time, inside Ableton Live.

---

## How It Works

```
LLM (Claude / GPT-4)
        │
        │  Tool calls via MCP protocol
        ▼
  MCP Server (server.py)
        │
        │  OSC messages via UDP
        ▼
  AbletonOSC (Ableton Live plugin)
        │
        ▼
  Ableton Live DAW
```

1. The MCP server registers tool definitions that any MCP-compatible client can discover
2. When the LLM calls a tool, the server sends an OSC message to AbletonOSC running inside Ableton Live
3. Ableton Live executes the action in real time

---

## Available Tools

| Tool | Parameters | Description |
|---|---|---|
| `set_tempo` | `bpm: float` | Set project tempo (e.g., 128.0 BPM) |
| `start_playback` | — | Start playback |
| `stop_playback` | — | Stop playback |
| `toggle_metronome` | `on: bool` | Turn metronome on/off |
| `set_track_volume` | `track_index, volume (0.0–1.0)` | Set volume on any track |
| `mute_track` | `track_index, mute: bool` | Mute or unmute a track |
| `fire_clip` | `track_index, clip_index` | Launch a clip slot |
| `create_midi_track` | `name: str` | Create a new MIDI track |
| `create_midi_clip` | `track_index, clip_index, length_beats` | Create an empty MIDI clip |
| `add_midi_note` | `track_index, clip_index, pitch, start, duration, velocity` | Add a note to a MIDI clip |
| `set_track_name` | `track_index, name: str` | Rename a track |
| `set_device_parameter` | `track_index, device_index, param_index, value` | Adjust any instrument/effect parameter |

---

## Example: AI Composing a Chord

When you prompt an MCP-compatible AI assistant with:

> "Create a 4-beat MIDI clip on track 0, slot 0. Add a C major chord (C4, E4, G4) at beat 0 with quarter-note duration. Then start playback."

The AI will chain these tool calls:

```python
create_midi_clip(track_index=0, clip_index=0, length_beats=4.0)
add_midi_note(track_index=0, clip_index=0, pitch=60, start_time=0, duration=1.0, velocity=100)  # C4
add_midi_note(track_index=0, clip_index=0, pitch=64, start_time=0, duration=1.0, velocity=100)  # E4
add_midi_note(track_index=0, clip_index=0, pitch=67, start_time=0, duration=1.0, velocity=100)  # G4
start_playback()
```

---

## Setup

### Prerequisites
- Python 3.11+
- Ableton Live (any edition)
- [AbletonOSC](https://github.com/ideoforms/AbletonOSC) installed as an Ableton MIDI Remote Script
- An MCP-compatible AI client (Claude Desktop, etc.)

### Installation

```bash
pip install mcp python-osc
```

### Running the Server

```bash
python server.py
```

The server listens for MCP tool calls and forwards OSC messages to Ableton Live at `127.0.0.1:11000` (AbletonOSC default).

### Connecting to Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ableton": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

---

## Why MCP?

MCP (Model Context Protocol) is an open standard by Anthropic that lets AI models safely and reliably call external tools. Unlike raw function calling, MCP:
- Provides structured tool discovery
- Handles type validation on inputs
- Works across any MCP-compatible client (Claude, IDE plugins, custom agents)

This project was built to demonstrate how MCP can connect AI to real-world creative software — not just APIs.

---

## Skills Demonstrated

- **MCP Server Development** — Building structured AI tool interfaces with FastMCP
- **LLM Tool Orchestration** — Designing tools that compose well for multi-step AI reasoning
- **OSC Protocol** — Real-time UDP message communication with DAW software
- **AI + Creative Tools** — Applying agentic AI patterns to music production workflows
