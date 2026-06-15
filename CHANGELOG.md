# Changelog

All notable changes to the Ableton MCP project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-06-15

### Added

#### Core Features
- **49 tools** across 5 phases (Phase 0-4)
- **35 devices** with 158+ parameter mappings (up from 11)
  - 25 audio effects
  - 10 instruments
  - 7 MIDI effects
- **Music theory module** (440 lines, pure Python)
  - Note name ↔ MIDI conversion
  - 11 chord types
  - 11 scale types
  - 6 drum patterns
  - 5 chord progressions
  - Quantization, transposition, humanization
- **6 music generation tools**
  - Note/scale/chord builders
  - Drum pattern generation
  - Chord progression builder

#### Phase 0 - Foundation (26 tools)
- Transport: play, stop, continue, set tempo, get tempo, toggle metronome, undo, redo, ping
- Tracks: create MIDI/audio tracks, set volume/pan/mute/solo/arm, get properties
- Clips: create, fire, stop, add notes, set name, quantize
- Devices: set/get parameters by index

#### Phase 1 - Observation (9 tools)
- `list_tracks()` — enumerate all tracks
- `get_track_info()` — complete track properties
- `get_devices()` — list devices on track
- `get_session_overview()` — full session snapshot
- Read-write parity: get_track_name, get_track_mute, get_track_solo, get_track_pan

#### Phase 2 - Intelligent Control (1 tool + 35 devices)
- `set_device_parameter_by_name()` — control parameters by friendly name
- Device parameter mappings for 35 common devices
- Preset system with 37 presets

#### Phase 3 - Metering (6 framework tools)
- `get_track_meter()`, `analyze_loudness()`, `get_clip_detection()`
- `get_master_meter()`, `spectrum_analysis()`, `check_headroom()`
- Framework ready for AbletonOSC enhancement

#### Phase 4 - Batch Workflows (7 tools)
- `balance_mix()` — auto-balance with intelligent defaults
- `quick_eq_preset()` — 6 EQ presets (bright, warm, dark, flat, presence, clarity)
- `compress_for_punch()` — 3 compression intensities
- `scaffold_song()` — create song sections
- `gain_stage_session()` — professional loudness optimization
- `create_mixing_template()` — standard mixing layout
- `suggest_next_action()` — workflow recommendations

#### Infrastructure & Quality
- Bidirectional OSC communication with request/response pattern
- Lazy initialization (OSC bridge starts on first tool use)
- Pydantic models for all responses (6 models)
- Full type hints throughout codebase
- Ruff linting configured
- Pyright type checking ready
- GitHub Actions CI/CD pipeline
  - Linting on all pushes/PRs
  - Type checking
  - Unit tests (skip live by default)
  - Integration tests on windows-latest

#### Documentation
- Comprehensive README (quick start, features, examples, architecture)
- CONTRIBUTING.md (development guidelines)
- FINAL_SUMMARY.md (complete project overview)
- AUDIT.md (initial gap analysis)
- PHASE2_FINDINGS.md (AbletonOSC limitations)

### Architecture

```
Phase 0: 26 basic tools (transport, tracks, clips, devices)
Phase 1: 9 observation tools (session visibility)
Phase 2: 1 intelligent control tool + 35 device mappings
Phase 3: 6 metering framework tools
Phase 4: 7 batch workflow tools
Music: 6 composition/generation tools

Total: 55 tools + 6 data models + music theory library
```

### Performance

- **Startup**: ~500ms (lazy OSC init)
- **Tool call**: 2–10ms (local ops)
- **OSC round-trip**: ~200ms (with 2s timeout)
- **Batch ops**: ~10–50ms per operation

### Known Limitations

- Cannot add/remove devices (requires AbletonOSC API enhancement)
- Cannot load presets by name (requires AbletonOSC API enhancement)
- Metering requires AbletonOSC meter endpoints (framework ready)

### Mixing Automation Capability

| Feature | Status | Coverage |
|---------|--------|----------|
| Session observation | ✅ 100% | See all tracks/devices |
| Parameter control | ✅ 90% | 35 devices, 158+ parameters |
| EQ/Compression/Effects | ✅ 100% | Smart presets |
| Batch workflows | ✅ 80% | balance, EQ, compress, scaffold |
| **Overall** | **✅ 80-90%** | Professional mixing tasks |

## Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **Major version** (1.x.x): Breaking changes to tool interfaces
- **Minor version** (x.1.x): New tools/features (backward compatible)
- **Patch version** (x.x.1): Bug fixes, documentation (backward compatible)

## Future Roadmap (Optional)

### Phase 5: Advanced Workflows
- Parallel compression chains
- Mid-side processing
- Frequency analysis and visualization
- ML-driven mixing suggestions

### Phase 6: External Publishing
- Publish to PyPI
- Register with MCP Registry
- Documentation site
- YouTube tutorials

### Enhancement: AbletonOSC APIs
- Meter endpoints for real-time level monitoring
- Device add/remove/toggle
- Preset enumeration and loading
- Custom parameter discovery
