# Phase 0 Audit: What's Missing for Complete Ableton Automation

## Critical Issues Found

### 1. **CRITICAL: Startup/Shutdown Hooks Not Connected**
- **Issue**: `server.py` defines `startup()` and `shutdown()` functions but sets them on `mcp._on_startup` / `mcp._on_shutdown` which don't exist in FastMCP API
- **Impact**: OSC bridge is NEVER started, so all tools will fail at runtime
- **Tools affected**: ALL async tools (26 tools)
- **Solution needed**: Implement proper lifecycle hooks using MCP's actual API (likely `mcp.system_prompt()` or startup middleware)

### 2. **Missing Query/Read Tools (Session State Blind)**
Without these, Claude can't observe Ableton → can't make intelligent decisions:

| Tool | Purpose | Status |
|------|---------|--------|
| `list_tracks()` | Get all track names/indices | ❌ MISSING |
| `get_track_info(index)` | Get track properties (name, mute, solo, volume, pan, arm, devices) | ❌ MISSING |
| `get_devices(track_index)` | List devices on a track | ❌ MISSING |
| `get_device_parameters(track_index, device_index)` | Get device param names + ranges | ❌ MISSING |
| `get_clip_notes(track_index, clip_index)` | Read MIDI notes in a clip | ❌ MISSING |
| `get_session_overview()` | Full session snapshot (tracks, clips, tempo, key, time sig) | ❌ MISSING |
| `get_arrangement_view()` | Get arrangement/locators/cues | ❌ MISSING |

### 3. **Missing Data Models (String Responses Only)**
All tools return strings like `"Track 0 volume set to 0.5"`. For agentic workflows, need structured JSON:

| Model | Status |
|-------|--------|
| `TrackInfo` (name, type, volume, pan, mute, solo, arm, device_count) | ❌ MISSING |
| `ClipInfo` (name, length, is_playing, notes_count) | ❌ MISSING |
| `DeviceInfo` (name, parameters) | ❌ MISSING |
| `NoteInfo` (pitch, start_time, duration, velocity) | ❌ MISSING |
| `SessionOverview` (tracks, clips, tempo, time_sig, key, locators) | ❌ MISSING |

### 4. **Missing Control Tools**

| Tool | Purpose | Status |
|------|---------|--------|
| `delete_track(index)` | Remove a track | ❌ MISSING |
| `delete_clip(track_index, clip_index)` | Remove a clip | ❌ MISSING |
| `duplicate_track(index)` | Clone a track | ❌ MISSING |
| `duplicate_clip(track_index, clip_index)` | Clone a clip | ❌ MISSING |
| `set_time_signature(numerator, denominator)` | Set time sig | ❌ MISSING (can read but not write) |
| `get_time_signature()` | Read time sig | ❌ MISSING |
| `set_loop(start, end)` | Control loop | ❌ MISSING |
| `get_loop()` | Read loop | ❌ MISSING |
| `set_song_position(beats)` | Jump to bar/beat | ❌ MISSING |
| `get_song_position()` | Get current playhead position | ❌ MISSING |
| `create_return_track(name)` | Add return/send track | ❌ MISSING |
| `fire_scene(index)` | Launch a scene | ❌ MISSING |
| `create_scene()` | Add a scene | ❌ MISSING |
| `create_locator(time, name)` | Add a cue/locator | ❌ MISSING |
| `set_mixer_send(track_index, send_index, value)` | Control send level | ❌ MISSING |
| `get_mixer_send(track_index, send_index)` | Read send level | ❌ MISSING |

### 5. **Missing Generation & Analysis**

| Feature | Status |
|---------|--------|
| Music theory helpers (note names, MIDI conversion, scales, chords) | ❌ MISSING |
| `generate_drum_pattern(style, bars)` | ❌ MISSING |
| `add_chord(root, quality)` | ❌ MISSING |
| `add_progression(chords)` | ❌ MISSING |
| `humanize_clip(timing_amount, velocity_amount)` | ❌ MISSING |
| `transpose_clip(semitones)` | ❌ MISSING |
| `quantize_clip(grid)` | ❌ MISSING |
| `analyze_arrangement()` - detect sections | ❌ MISSING |
| `suggest_arrangement()` - AI suggestions | ❌ MISSING |

### 6. **Missing Batch Operations**

| Tool | Status |
|------|--------|
| `scaffold_song(["intro", "verse", "chorus"])` | ❌ MISSING |
| `build_drum_rack_track(name, bars)` | ❌ MISSING |
| `apply_mix_template(template_name)` | ❌ MISSING |
| `clone_section(from_bar, to_bar, target_bar)` | ❌ MISSING |

### 7. **Missing Event Monitoring**

| Tool | Status |
|------|--------|
| `poll_events()` - get fired clips, tempo changes, etc | ❌ MISSING |
| `wait_for_beat(beat_number)` - block until transport reaches beat | ❌ MISSING |

### 8. **Missing MCP Resources**
MCP has two ways to expose data: Tools (imperative) and Resources (declarative, subscribable):

| Resource | Status |
|----------|--------|
| `ableton://session/overview` | ❌ MISSING |
| `ableton://track/{index}` | ❌ MISSING |
| `ableton://clip/{track}/{clip}` | ❌ MISSING |

### 9. **Missing Documentation & CI**

| Item | Status |
|------|--------|
| README with install steps | ❌ MISSING |
| INSTALL.md for AbletonOSC setup | ❌ MISSING |
| Auto-generated TOOLS.md | ❌ MISSING |
| RECIPES.md with example prompts | ❌ MISSING |
| GitHub Actions CI (ruff, tests) | ❌ MISSING |
| server.json (MCP Registry manifest) | ❌ MISSING |

## Summary

**Current state: 26 tools (transport, tracks, clips, devices)**

**For complete automation, need at least 60+ tools across:**
- Session queries (8+ tools)
- Track management (15+ tools)
- Clip editing (12+ tools)
- Device control (8+ tools)
- Arrangement/scenes (10+ tools)
- Generation/analysis (10+ tools)
- Batch workflows (4+ tools)
- Monitoring (2+ tools)

**Blocker**: Startup hook issue means ZERO tools actually work right now. This must be fixed first.

## Recommended Action

1. **Fix startup/shutdown hooks** (blocker)
2. **Add core models** (TrackInfo, ClipInfo, etc.) - enables structured responses
3. **Add list/get tools** for session state queries - enables observation
4. **Add missing control tools** - completes the basic control set
5. **Add generation/analysis** - enables creative workflows
6. **Add batch operations** - reduces turn count for complex workflows
7. **Add monitoring** - enables reactive patterns
8. **Add MCP resources** - differentiator for indexing/discovery
9. **Documentation + CI** - publication readiness
