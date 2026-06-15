# Mixing Capabilities Analysis: What's Missing

## Current Mixing Tools (Limited)

### What EXISTS (3 tools):
```
1. set_track_volume(track_index, volume)           ✓ Can do
2. set_track_pan(track_index, pan)                 ✓ Can do
3. set_device_parameter(track, device, param, val) ✓ Can do (but...)
```

### What's BROKEN:
```
3. set_device_parameter() requires you to know:
   - Which track index is which instrument
   - Which device is on that track
   - Which parameter index is "Dry/Wet" vs "Decay"
   
   Example: "Set reverb dry/wet to 30%"
   Currently: ❌ Can't do this
   Error: "Unknown track, unknown device, unknown parameter"
```

---

## What Mixing Actually Requires

### **Tier 1: Observation (Can't see state)**

```python
# Claude needs to see:
tracks = list_tracks()  # ❌ Missing
# Returns: [TrackInfo(name="Drums", volume=0.8, pan=-0.1, mute=False, ...)]

devices = get_devices(track_index=0)  # ❌ Missing
# Returns: [DeviceInfo(name="EQ Eight", index=0, param_count=8), ...]

params = get_device_parameters(track=0, device=0)  # ❌ Missing
# Returns: [
#   ParamInfo(name="Dry/Wet", index=0, min=0.0, max=1.0, current=0.5),
#   ParamInfo(name="Decay", index=1, min=0.01, max=5.0, current=0.5),
#   ...
# ]

volume = get_track_volume(0)  # ✓ Exists (only 1 read tool!)
levels = get_track_meter(0)   # ❌ Missing
```

**Status: 10% implemented**

---

### **Tier 2: Intelligent Control (Can't target by name)**

```python
# What Claude wants to do:
set_device_parameter_by_name(
    track=0, 
    device="EQ Eight",
    parameter="High Shelf Gain",
    value=3.0  # dB
)  # ❌ Missing — have to use indices instead

# Current workaround (broken):
set_device_parameter(track=0, device=0, param=6, value=0.3)
# ^ Hopes param index 6 is "High Shelf Gain" but has no way to know
```

**Status: 0% implemented (requires Tier 1 first)**

---

### **Tier 3: Mixing Workflows (Can't do multi-step mixes)**

```python
# Example: "Create a balanced mix"
# This requires:

1. list_tracks() → see what's in the session
2. get_track_volume(each) → see current levels
3. Analyze loudness of each track
4. Suggest which to bring down/up
5. set_track_volume(drums_track, 0.7)
6. set_track_volume(bass_track, 0.6)
7. set_track_volume(vocals_track, 0.8)
8. Verify with get_track_volume() for each
9. Apply subtle EQ to problem instruments
10. Add reverb sends for cohesion

# Currently: CAN'T DO ANY OF THIS
# Missing tools: 1, 2, 3 (critical), 9, 10
```

**Status: 10% possible (only steps 5-7 have tools)**

---

## What's Needed for Mixing Automation

### **Phase 1: Observation Layer** (CRITICAL)
```python
# Tools needed:
1. list_tracks() 
   → Returns: [TrackInfo(name, volume, pan, mute, solo, arm, device_names, clip_count)]

2. get_devices(track_index)
   → Returns: [DeviceInfo(name, type, index, parameter_count)]

3. get_device_parameters(track_index, device_index)
   → Returns: [ParamInfo(name, index, min, max, current_value, unit)]

4. get_track_pan(track_index)  ← Missing! Can SET but not GET

5. get_track_name(track_index)  ← Missing! Can SET but not GET

6. get_track_mute(track_index)  ← Missing! Can SET but not GET

7. get_track_solo(track_index)  ← Missing! Can SET but not GET
```

**Impact: Enables "what's in this session?"**

---

### **Phase 2: Intelligent Control** (DEPENDS ON PHASE 1)
```python
# Tools needed:
1. set_device_parameter_by_name(track, device_name, param_name, value)
   # Example: set_device_parameter_by_name(0, "EQ Eight", "High Shelf Gain", 3.0)

2. add_device_to_track(track_index, device_name)
   # Example: add_device_to_track(0, "Compressor")

3. remove_device(track_index, device_index)

4. toggle_device(track_index, device_index, enabled)

5. load_device_preset(track_index, device_index, preset_name)
```

**Impact: Enables "set EQ on drums to bright preset"**

---

### **Phase 3: Metering & Analysis** (DEPENDS ON PHASES 1-2)
```python
# Tools needed:
1. get_track_meter(track_index, duration=1.0)
   → Returns: MeterInfo(peak, rms, frequency_spectrum, headroom)

2. get_master_meter()
   → Returns: MeterInfo(peak, rms, headroom, clipping)

3. analyze_loudness(track_index)
   → Returns: LoudnessInfo(lufs, loudness_range, peaks)

4. get_clip_detection(track_index)
   → Returns: bool (is track clipping?)

5. spectrum_analysis(track_index)
   → Returns: {freq: magnitude, ...} (what frequencies are present?)
```

**Impact: Enables "drums are too quiet, vocals are clipping, bass is muddy"**

---

### **Phase 4: Mixing Workflows** (DEPENDS ON PHASES 1-3)
```python
# Tools needed:
1. balance_mix()
   # Automatically: measure loudness of each track, normalize to -14 LUFS

2. quick_eq_preset(track_index, preset: "bright" | "dark" | "flat")
   # Apply common EQ curves

3. add_reverb_send_chain(track_index, reverb_size)
   # Create return track + reverb device + set send levels

4. compress_track(track_index, ratio, threshold, makeup_gain)
   # Add compressor with smart settings

5. eq_for_clarity()
   # Automatically detect muddy frequencies and remove them

6. gain_stage_session()
   # Normalize track volumes for optimal headroom
```

**Impact: Enables "give me a balanced, professional-sounding mix"**

---

### **Phase 5: Expert Mixing** (DEPENDS ON PHASES 1-4 + MUSIC THEORY)
```python
# Tools needed:
1. freq_aware_eq(track_index, intent: "reduce_muddiness" | "add_sparkle" | "warm_up")
   # Uses music theory to know which freqs to target

2. creative_reverb_design(track_index, preset: "chamber" | "hall" | "spring")

3. parallel_compression(track_index, ratio=4, makeup_gain=3)
   # New return track with compressed signal

4. multiband_compression(track_index, bands=[...])
   # Compress only certain frequency ranges

5. mid_side_processing(track_index, mid_solo=False, side_compress=True)
   # Separate mid from sides, process differently
```

**Impact: Enables "use parallel compression with 4:1 ratio on drums"**

---

## Current State: Mixing Capability Assessment

### **Can Claude Currently Help with Mixing?**

| Task | Possible? | Tools Needed |
|------|-----------|--------------|
| Set all track volumes | 🟡 Partially | ✓ Have `set_track_volume()` but ❌ need `list_tracks()` to find them |
| Pan drums left | ✓ Yes | ✓ Have `set_track_pan()` |
| Add EQ | 🟡 Partially | ✓ Have `set_device_parameter()` but ❌ must know param indices |
| "Make drums brighter" | ❌ No | ❌ Can't find drums, can't find EQ, can't find brightness param |
| "Balance the mix" | ❌ No | ❌ Can't see levels, can't measure, can't iterate |
| "Add reverb" | ❌ No | ❌ Can't create return track, can't create device, can't set sends |
| "Fix clipping vocals" | ❌ No | ❌ Can't measure clipping, can't add compressor |
| "Warm up the bass" | ❌ No | ❌ Can't find bass, can't identify frequencies, no EQ knowledge |

**Overall: 5% of mixing tasks possible, 95% blocked**

---

## Example: What "Mixing Support" Would Look Like

### **TODAY (Without Phase 1-5):**
```
User: "Make the drums punchier and warmer"

Claude: 
"I need to:
1. Find the drums track
2. Check if EQ is there, if not add one
3. Boost the low mids (warmth) and compress the transients (punch)
4. Reduce harshness around 3kHz

But I can't do any of this because:
- No way to list tracks or find 'drums'
- No way to see what devices exist
- No way to know parameter names/indices
- No way to add devices
- No API for device parameter names"

Result: ❌ FAIL
```

### **WITH Phases 1-3 (Observation + Control + Metering):**
```
User: "Make the drums punchier and warmer"

Claude:
1. list_tracks() → Finds track "Drums" (index=0)
2. get_devices(0) → Sees "Compressor" (index=0), "EQ Eight" (index=1)
3. get_track_meter(0) → Sees peak=-6dB, sustain is low (not punchy)
4. get_device_parameters(0, 1) → Finds EQ params (Gain Band 1, 2, 3...)
5. set_device_parameter_by_name(0, "EQ Eight", "Low Mid Gain", 2.0) → Warmth
6. set_device_parameter_by_name(0, "Compressor", "Ratio", 4.0) → Punch
7. set_device_parameter_by_name(0, "Compressor", "Attack", 0.001) → Fast attack
8. get_track_meter(0) → Verifies punch increased

Result: ✓ SUCCESS
```

---

## Blocking Dependencies

### To Enable Mixing Help, MUST HAVE:

```
Phase 5 (Expert Mixing)
  ↓ Requires
Phase 4 (Mixing Workflows)
  ↓ Requires
Phase 3 (Metering)
  ↓ Requires
Phase 2 (Intelligent Control)
  ↓ Requires
Phase 1 (Observation)
  ↓ Requires
CRITICAL: list_tracks() + get_devices() + get_device_parameters()
```

**You cannot skip Phase 1.** Without it, mixing is impossible.

---

## Implementation Roadmap for Mixing

### **Week 1: Phase 1 (Observation)**
```python
# New tools (6 tools)
list_tracks()                          # See all tracks
get_track_info(index)                  # Track properties
get_devices(track_index)               # List devices
get_device_parameters(track, device)   # Parameter details
get_track_mute/solo/pan/name()         # Read-write parity

# New models (5 types)
TrackInfo
DeviceInfo
ParameterInfo
MeterInfo
SessionOverview
```

**Result: Claude can see the session**

---

### **Week 2: Phase 2 (Intelligent Control)**
```python
# New tools (5 tools)
set_device_parameter_by_name(track, device, param, val)
add_device_to_track(track, device_name)
remove_device(track, device_index)
toggle_device(track, device_index, enabled)
load_device_preset(track, device_index, preset_name)
```

**Result: Claude can control mixing intelligently**

---

### **Week 3: Phase 3 (Metering)**
```python
# New tools (5 tools)
get_track_meter(track_index)
get_master_meter()
analyze_loudness(track_index)
get_clip_detection(track_index)
spectrum_analysis(track_index)
```

**Result: Claude can measure and analyze sound**

---

### **Week 4: Phase 4 (Workflows)**
```python
# New tools (6 tools)
balance_mix()
quick_eq_preset(track, preset)
add_reverb_send_chain(track, size)
compress_track(track, ratio, threshold, makeup)
eq_for_clarity()
gain_stage_session()

# New models (3 types)
MixProfile
EQCurve
CompressorSettings
```

**Result: Claude can do complete mixing workflows**

---

### **Week 5: Phase 5 (Expert Mixing)**
```python
# New tools (5 tools)
freq_aware_eq(track, intent)
creative_reverb_design(track, preset)
parallel_compression(track, ratio, makeup)
multiband_compression(track, bands)
mid_side_processing(track, mid_solo, side_compress)

# New knowledge base
Music theory module (frequency ranges, effects, mixing techniques)
Mixing recipes database
```

**Result: Claude becomes a mixing engineer**

---

## Summary: Can Claude Help with Mixing?

### Current State:
```
✓ Volume & pan control
❌ Everything else
```

### To Enable Full Mixing Support:

1. **MUST DO Phase 1** (Observation):
   - `list_tracks()`, `get_devices()`, `get_device_parameters()`
   - Enables: "What's in this session?"
   
2. **SHOULD DO Phase 2** (Intelligent Control):
   - `set_device_parameter_by_name()`, `add_device_to_track()`
   - Enables: "Adjust EQ to brighten drums"

3. **NICE Phase 3** (Metering):
   - `get_track_meter()`, `analyze_loudness()`
   - Enables: "Drums are too quiet, fix it"

4. **NICE Phase 4** (Workflows):
   - `balance_mix()`, `add_reverb_send_chain()`
   - Enables: "Create a balanced mix"

5. **POLISH Phase 5** (Expert):
   - Music theory + advanced techniques
   - Enables: "Use parallel compression on vocals"

---

## Rough Effort Estimates

| Phase | Tools | Models | Hours | Enables |
|-------|-------|--------|-------|---------|
| **1** | 6 | 5 | 8h | Session observation |
| **2** | 5 | 2 | 6h | Intelligent mixing control |
| **3** | 5 | 2 | 8h | Measurement & analysis |
| **4** | 6 | 3 | 10h | Automated mixing workflows |
| **5** | 5 | - | 8h | Expert techniques |

**Total: 40 hours to full mixing automation**

---

## Bottom Line

**Can Claude help with mixing today?** 🟡 Barely (5% of tasks)

**Can Claude become a mixing engineer?** ✅ Yes, but needs:
1. Phase 1 (Observation) — **6-8 hours** ← **START HERE**
2. Phase 2 (Control) — 6 hours
3. Phase 3 (Metering) — 8 hours
4. Phase 4 (Workflows) — 10 hours
5. Phase 5 (Expertise) — 8 hours

**Critical Path:** Phase 1 is the blocker. Everything depends on it.
