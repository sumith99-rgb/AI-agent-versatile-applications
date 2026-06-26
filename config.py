"""
=========================================
        LiftGuard AI Configuration
=========================================
"""

# -------------------------------
# OLLAMA
# -------------------------------

OLLAMA_MODEL = "deepseek-v2:16b"

OLLAMA_URL = "http://localhost:11434/api/generate"

# -------------------------------
# MICROPHONE
# -------------------------------

MIC_DEVICE_INDEX = 2

# -------------------------------
# WHISPER
# -------------------------------

WHISPER_MODEL = "base"

WHISPER_DEVICE = "cpu"

WHISPER_COMPUTE_TYPE = "int8"

# -------------------------------
# PIPER
# -------------------------------

PIPER_MODEL = r"C:\Users\sumit\piper-voices\en_US-lessac-medium.onnx"

# -------------------------------
# MEMORY
# -------------------------------

MEMORY_FILE = "memory.json"

MAX_CONVERSATION_LENGTH = 5000

# -------------------------------
# TEMP FILES
# -------------------------------

TEMP_AUDIO = "temp/audio.wav"

TEMP_TTS = "temp/response.wav"