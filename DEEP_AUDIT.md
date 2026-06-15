# Deep Technical Audit: Ableton MCP Server

## 1. OSC Address Coverage Analysis

### Available Addresses in `addresses.py` (26 entries)

Mapped by category and implementation status:

#### Song/Transport (11 addresses)
| Address | Implemented | Status |
|---------|-------------|--------|
| `/live/song/get/tempo` | ✓ get_tempo | OK |
| `/live/song/set/tempo` | ✓ set_tempo | OK |
| `/live/song/get/time_signature` | ❌ | Missing tool |
| `/live/song/set/time_signature` | ❌ | Missing tool |
| `/live/song/start_playing` | ✓ start_playback | OK |
| `/live/song/continue_playing` | ✓ continue_playback | OK |
| `/live/song/stop_playing` | ✓ stop_playback | OK |
| `/live/song/get/playing` | ❌ | Missing tool |
| `/live/song/get/song_time` | ❌ | Missing tool |
| `/live/song/set/song_time` | ❌ | Missing tool |
| `/live/song/get/loop` | ❌ | Missing tool |
| `/live/song/set/loop` | ❌ | Missing tool |
| `/live/song/undo` | ✓ undo | OK |
| `/live/song/redo` | ✓ redo | OK |
| `/live/song/stop_all_clips` | ✓ stop_all_clips | OK |
| `/live/song/set/metronome` | ✓ toggle_metronome | OK |
| `/live/song/get/metronome` | ❌ | Missing tool |

**Coverage: 7/17 (41%)**

#### Track (10 addresses)
| Address | Implemented | Status |
|---------|-------------|--------|
| `/live/track/get/mute` | ❌ | Have set but not get |
| `/live/track/set/mute` | ✓ mute_track | OK |
| `/live/track/get/solo` | ❌ | Have set but not get |
| `/live/track/set/solo` | ✓ solo_track | OK |
| `/live/track/get/arm` | ❌ | Have set but not get |
| `/live/track/set/arm` | ✓ set_track_arm | OK |
| `/live/track/get/volume` | ✓ get_track_volume | OK |
| `/live/track/set/volume` | ✓ set_track_volume | OK |
| `/live/track/get/panning` | ❌ | Have set but not get |
| `/live/track/set/panning` | ✓ set_track_pan | OK |
| `/live/track/get/name` | ❌ | Missing tool |
| `/live/track/set/name` | ✓ set_track_name | OK |
| `/live/track/get/device_count` | ❌ | Missing tool |
| `/live/track/get/clip_slot_count` | ❌ | Missing tool |

**Coverage: 5/14 (36%), but read-write parity broken (5 tools can set but not get)**

#### Clip/Clip Slot (8 addresses)
| Address | Implemented | Status |
|---------|-------------|--------|
| `/live/clip_slot/fire` | ✓ fire_clip | OK |
| `/live/clip_slot/stop` | ✓ stop_clip | OK |
| `/live/clip_slot/create_clip` | ✓ create_midi_clip | OK |
| `/live/clip/get/notes` | ❌ | Missing tool |
| `/live/clip/add/notes` | ✓ add_midi_note | OK |
| `/live/clip/remove/notes` | ❌ | Missing tool |
| `/live/clip/set/loop` | ❌ | Missing tool |
| `/live/clip/get/loop` | ❌ | Missing tool |
| `/live/clip/get/length` | ❌ | Missing tool |
| `/live/clip/get/name` | ❌ | Missing tool |
| `/live/clip/set/name` | ✓ set_clip_name | OK |

**Coverage: 5/11 (45%)**

#### Device (4 addresses)
| Address | Implemented | Status |
|---------|-------------|--------|
| `/live/device/get/name` | ❌ | Missing tool |
| `/live/device/get/parameters` | ❌ | Missing tool |
| `/live/device/get/parameter/value` | ✓ get_device_parameter | OK |
| `/live/device/set/parameter/value` | ✓ set_device_parameter | OK |

**Coverage: 2/4 (50%)**

#### Track Creation (3 addresses)
| Address | Implemented | Status |
|---------|-------------|--------|
| `/live/song/create_midi_track` | ✓ create_midi_track | OK |
| `/live/song/create_audio_track` | ✓ create_audio_track | OK |
| `/live/song/create_return_track` | ❌ | Missing tool |

**Coverage: 2/3 (67%)**

#### Scene (1 address)
| Address | Implemented | Status |
|---------|-------------|--------|
| `/live/song/fire_scene` | ❌ | Missing tool |

**Coverage: 0/1 (0%)**

#### Health Check (2 addresses)
| Address | Implemented | Status |
|---------|-------------|--------|
| `/live/test` | ✓ ping (indirect) | OK |
| `/live/test/result` | ✓ ping (indirect) | OK |

**Coverage: 1/2 (50%)**

### **Overall OSC Address Coverage: 22/50 (44%)**

### Missing AbletonOSC Features Not in addresses.py

These are likely available in AbletonOSC but not documented in our registry:

1. **Mixer/Sends:**
   - `/live/track/get/sends` / `/live/track/set/send`
   - `/live/master/get/volume` / `/live/master/set/volume`
   - `/live/mixer/get/crossfader` / `/live/mixer/set/crossfader`

2. **Arrangement:**
   - `/live/arrangement/get/length`
   - `/live/arrangement/set/loop`
   - `/live/arrangement/fire_cue` (jump to locator)

3. **Locators/Cues:**
   - `/live/song/create_cue_point`
   - `/live/song/delete_cue_point`

4. **Browser/Device Loading:**
   - `/live/browser/get/items`
   - `/live/browser/select_item`

5. **Clip/Track Properties:**
   - `/live/clip/get/warping`
   - `/live/clip/set/color`
   - `/live/track/get/color`
   - `/live/clip/get/current_position` (playhead in clip)

---

## 2. Structural Issues Found

### 2.1 **No Pydantic Models** 
Current: All tools return strings like `"Track 0 volume: 0.5"`
Problem: Claude can't parse/reason about structured data
Needed: `TrackInfo`, `ClipInfo`, `DeviceInfo`, `SessionOverview` models

**Impact:** LLM responses are weakly typed, hard to validate, not composable

### 2.2 **Missing Batch/Composite Tools**
Individual tools are granular (set_tempo, start_playback, etc.)
Problem: Common workflows require 5-10 tool calls in sequence
Example: Creating a drum rack = create_track + create_clip + add_note(×12)

**Impact:** High turn count, brittle compositions, slow workflows

### 2.3 **No Error Recovery**
Tools return strings like `"Error: {e}"` with no recovery path
Problem: If OSC bridge fails, all subsequent tools will fail silently
Needed: Automatic reconnect, health checks, graceful degradation

**Impact:** Fragile, requires manual restart

### 2.4 **Missing Input Validation**
Some validation added (MIDI range, tempo bounds) but inconsistent
Problem: No validation for:
- Track indices (max track count unknown at tool runtime)
- Clip indices (max clip slots unknown)
- Device indices (device count unknown until queried)
- Device parameter indices (parameter count unknown)

**Impact:** Invalid OSC messages sent to Ableton, silent failures

### 2.5 **Asymmetric Read-Write Tools**
| Operation | Set | Get |
|-----------|-----|-----|
| Track mute | ✓ | ❌ |
| Track solo | ✓ | ❌ |
| Track arm | ✓ | ❌ |
| Track pan | ✓ | ❌ |
| Clip loop | ❌ | ❌ |
| Song loop | ❌ | ❌ |
| Song position | ❌ | ❌ |

**Impact:** Can't verify changes, can't write conditional logic

### 2.6 **No Session State Caching**
Each tool independently queries Ableton
Problem: Repeated calls to `get_tempo()` hit the OSC round-trip 3x
Better: Cache with TTL, invalidate on change

**Impact:** Slow, high OSC traffic

### 2.7 **No Event Subscription/Monitoring**
Tools are imperative only (send command, get response)
Problem: Can't react to Ableton events (clip launched, tempo changed, etc.)
AbletonOSC supports: `/live/clip_slot/add_listener`, `/live/clip_slot/start_listen`

**Impact:** No reactive patterns, polling-only

### 2.8 **Limited MCP Protocol Usage**
Currently using: `@mcp.tool()` decorators only
Not using: MCP Resources, Prompts, Sampling
Needed: 
- `@mcp.resource()` for session state (subscribable)
- `@mcp.prompt()` for workflows (reusable instruction sets)

**Impact:** Not using MCP to its full potential, poor discoverability

---

## 3. Configuration & Environment Issues

### 3.1 **No Validation of AbletonOSC Installation**
`ping()` will fail at runtime if AbletonOSC isn't installed
Better: Validate on startup, give clear instructions

### 3.2 **No Multi-Live Version Support**
Hardcoded for Live 11.3.20, ignores Live 12
Better: Auto-detect, support both versions' APIs

### 3.3 **No Hot-Reload for Configuration**
Changes to `.env` require server restart
Better: Watch file, reload on change

### 3.4 **No Logging Configuration**
Settings has `debug: bool` but no log file option
Better: Structured logging, JSON output for parsing

---

## 4. Performance Issues

### 4.1 **No Connection Pooling**
Each OSC message creates a new UDP socket on send
Better: Reuse socket, batch messages

### 4.2 **Blocking await for Each Tool**
`await bridge.send_and_receive()` blocks for timeout (2 sec)
Problem: If Ableton is slow, 10 tools = 20 seconds
Better: Parallel OSC calls where possible, request batching

### 4.3 **Lazy Initialization Adds Latency**
First tool call triggers bridge startup (500ms+)
Better: Eager init in MCP startup, or background task

### 4.4 **No Response Caching**
`get_tempo()` called twice = 2 round trips
Better: Cache with short TTL, invalidate on writes

---

## 5. Missing MCP Protocol Features

### 5.1 **No Resources**
MCP supports subscribable resources:
```python
@mcp.resource("ableton://session/overview")
async def session() -> str: ...
```
Benefits: Claude can subscribe, auto-refresh, better UX

### 5.2 **No Prompts**
MCP supports reusable instruction templates:
```python
@mcp.prompt("arrange_song")
async def arrange(template: str) -> str: ...
```
Use case: "Use the arrange_song prompt to scaffold a song"

### 5.3 **No Sampling**
MCP supports sampling resources for context:
```python
@mcp.resource("...", refresh_interval=5)
```
Use case: Auto-refresh session state every 5 seconds

### 5.4 **No Server Metadata**
Missing `instructions` and other server capabilities

---

## 6. Testing Gaps

### 6.1 **No Integration Tests**
Created `tests/test_osc_bridge.py` but marked `@pytest.mark.live`
Problem: Can't run without live Ableton + AbletonOSC
Solution: Mock OSC server, test against fake responses

### 6.2 **No End-to-End Tests**
No tests of the full flow (MCP server → tool call → OSC → Ableton)

### 6.3 **No Error Case Tests**
No tests for:
- Ableton not responding
- Invalid track index
- Device parameter out of range
- OSC timeout

---

## 7. Documentation Gaps

### 7.1 **No README**
No installation, usage, or troubleshooting guide

### 7.2 **No Tool Reference**
Should auto-generate from docstrings

### 7.3 **No Architecture Documentation**
How does the OSC bridge work? What about the lazy init?

### 7.4 **No Example Prompts**
No "RECIPES.md" of prompt patterns

### 7.5 **No Troubleshooting Guide**
No "OSC not responding? Try this..."

---

## 8. Security & Robustness

### 8.1 **No Input Sanitization**
Track names, clip names can be arbitrary strings
Problem: Could contain OSC special characters
Better: Validate/escape strings before sending

### 8.2 **No Rate Limiting**
Can send unlimited OSC messages
Problem: DoS risk, system overload
Better: Rate limiter per tool, queue depth limits

### 8.3 **No Authentication**
MCP server runs unencrypted
Problem: Any local process can control Ableton
Better: Optional token auth, TLS for remote

### 8.4 **No Audit Logging**
No record of who did what
Better: Log all tool calls with user/timestamp

---

## 9. Feature Completeness Matrix

| Category | Implemented | Total | % | Priority |
|----------|-------------|-------|---|----------|
| **Transport** | 7 | 17 | 41% | HIGH |
| **Tracks** | 5 | 14 | 36% | HIGH |
| **Clips** | 5 | 11 | 45% | HIGH |
| **Devices** | 2 | 4 | 50% | HIGH |
| **Creation** | 2 | 3 | 67% | MEDIUM |
| **Scenes** | 0 | 1 | 0% | MEDIUM |
| **Models** | 0 | 5 | 0% | CRITICAL |
| **Batch Tools** | 0 | 6 | 0% | HIGH |
| **Resources** | 0 | 3 | 0% | MEDIUM |
| **Testing** | 1 | 10+ | 10% | HIGH |

---

## 10. Summary: What's Actually Working vs. Missing

### ✅ Working Well
- OSC bridge architecture (bidirectional, timeout handling)
- Lazy initialization (critical fix)
- Modular tool organization
- Basic error handling
- Ruff linting passing
- Input validation for common fields

### ❌ Critical Blockers
1. **Missing `list_tracks()` / `get_track_info()`** — Can't enumerate session
2. **No pydantic models** — Can't structure responses
3. **Missing batch tools** — Can't do multi-step workflows
4. **No event monitoring** — Can't be reactive
5. **Incomplete OSC coverage** — Only 44% of available addresses

### ⚠️ Nice-to-Have But Important
1. MCP Resources for session state
2. Caching for performance
3. Event listeners
4. Integration tests
5. Documentation

---

## 11. Recommended Completion Order

**To enable "completely automated Ableton via Claude":**

1. **Phase 1 (Critical):**
   - Add `list_tracks()` + `get_track_info()` → observe session
   - Add pydantic models (TrackInfo, ClipInfo, etc.) → structure responses
   - Add missing read tools (get_mute, get_solo, get_arm, get_pan) → parity
   - Implement: 5 new tools, 5 new models

2. **Phase 2 (High Value):**
   - Add `get_devices()` + `get_device_parameters()` → introspect devices
   - Add `create_return_track()` + `fire_scene()` → composition
   - Add time signature getters
   - Add loop control (get/set)
   - Implement: 8+ new tools

3. **Phase 3 (Enablement):**
   - Music theory module (`core/music_theory.py`)
   - `generate_drum_pattern()`, `add_chord()`, etc.
   - Implement: 6+ generation tools

4. **Phase 4 (UX):**
   - MCP Resources for session discovery
   - Event listeners (clip launch, tempo change)
   - Batch tools (`scaffold_song()`)
   - Implement: 4+ composite tools + 3 resources

5. **Phase 5 (Polish):**
   - Integration tests + CI
   - Documentation + examples
   - Performance optimization (caching, pooling)
   - Security (sanitization, rate limiting)

---

## 12. Rough ROI Estimate

| Investment | ROI | Unlocks |
|-----------|-----|---------|
| Phase 1 (6h) | **VERY HIGH** | Session observation, enables reasoning |
| Phase 2 (6h) | **HIGH** | Full control surface, arrangement |
| Phase 3 (6h) | **HIGH** | Creative AI workflows |
| Phase 4 (10h) | **MEDIUM** | Polish, discoverability |
| Phase 5 (8h) | **MEDIUM** | Production readiness |

**Total: ~36 hours for production-grade "complete" automation**

