"""Central registry of AbletonOSC addresses."""

# Song / Transport
SONG_GET_TEMPO = "/live/song/get/tempo"
SONG_SET_TEMPO = "/live/song/set/tempo"
SONG_GET_TIME_SIGNATURE = "/live/song/get/time_signature"
SONG_SET_TIME_SIGNATURE = "/live/song/set/time_signature"
SONG_START_PLAYING = "/live/song/start_playing"
SONG_CONTINUE_PLAYING = "/live/song/continue_playing"
SONG_STOP_PLAYING = "/live/song/stop_playing"
SONG_GET_PLAYING = "/live/song/get/playing"
SONG_GET_SONG_TIME = "/live/song/get/song_time"
SONG_SET_SONG_TIME = "/live/song/set/song_time"
SONG_GET_LOOP = "/live/song/get/loop"
SONG_SET_LOOP = "/live/song/set/loop"
SONG_UNDO = "/live/song/undo"
SONG_REDO = "/live/song/redo"
SONG_STOP_ALL_CLIPS = "/live/song/stop_all_clips"
SONG_SET_METRONOME = "/live/song/set/metronome"
SONG_GET_METRONOME = "/live/song/get/metronome"

# Track
TRACK_SET_MUTE = "/live/track/set/mute"
TRACK_GET_MUTE = "/live/track/get/mute"
TRACK_SET_SOLO = "/live/track/set/solo"
TRACK_GET_SOLO = "/live/track/get/solo"
TRACK_SET_ARM = "/live/track/set/arm"
TRACK_GET_ARM = "/live/track/get/arm"
TRACK_SET_VOLUME = "/live/track/set/volume"
TRACK_GET_VOLUME = "/live/track/get/volume"
TRACK_SET_PANNING = "/live/track/set/panning"
TRACK_GET_PANNING = "/live/track/get/panning"
TRACK_SET_NAME = "/live/track/set/name"
TRACK_GET_NAME = "/live/track/get/name"
TRACK_GET_DEVICE_COUNT = "/live/track/get/device_count"
TRACK_GET_CLIP_SLOT_COUNT = "/live/track/get/clip_slot_count"

# Clip Slot
CLIP_SLOT_FIRE = "/live/clip_slot/fire"
CLIP_SLOT_STOP = "/live/clip_slot/stop"
CLIP_SLOT_CREATE_CLIP = "/live/clip_slot/create_clip"

# Clip
CLIP_GET_NOTES = "/live/clip/get/notes"
CLIP_ADD_NOTES = "/live/clip/add/notes"
CLIP_REMOVE_NOTES = "/live/clip/remove/notes"
CLIP_SET_LOOP = "/live/clip/set/loop"
CLIP_GET_LOOP = "/live/clip/get/loop"
CLIP_GET_LENGTH = "/live/clip/get/length"
CLIP_GET_NAME = "/live/clip/get/name"
CLIP_SET_NAME = "/live/clip/set/name"

# Song creation
SONG_CREATE_MIDI_TRACK = "/live/song/create_midi_track"
SONG_CREATE_AUDIO_TRACK = "/live/song/create_audio_track"
SONG_CREATE_RETURN_TRACK = "/live/song/create_return_track"

# Device
DEVICE_GET_NAME = "/live/device/get/name"
DEVICE_GET_PARAMETERS = "/live/device/get/parameters"
DEVICE_SET_PARAMETER_VALUE = "/live/device/set/parameter/value"
DEVICE_GET_PARAMETER_VALUE = "/live/device/get/parameter/value"

# Scene
SONG_FIRE_SCENE = "/live/song/fire_scene"

# Test/Health Check
LIVE_TEST = "/live/test"
LIVE_TEST_RESULT = "/live/test/result"
