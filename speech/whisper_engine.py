from faster_whisper import WhisperModel

from config import (
    WHISPER_MODEL,
    WHISPER_DEVICE,
    WHISPER_COMPUTE_TYPE
)


class WhisperEngine:

    def __init__(self):

        print("Loading Whisper...")

        self.model = WhisperModel(
            WHISPER_MODEL,
            device=WHISPER_DEVICE,
            compute_type=WHISPER_COMPUTE_TYPE
        )

        print("Whisper Loaded!")

    def transcribe(self, audio_path):

        segments, info = self.model.transcribe(
            audio_path,
            beam_size=5
        )

        text = ""

        for segment in segments:

            text += segment.text + " "

        return text.strip()