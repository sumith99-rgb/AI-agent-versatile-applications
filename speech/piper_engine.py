import uuid
import wave
import os

from playsound import playsound
from piper import PiperVoice

from config import PIPER_MODEL


class PiperEngine:

    def __init__(self):

        print("Loading Piper...")

        self.voice = PiperVoice.load(
            PIPER_MODEL
        )

        print("Piper Loaded!")

    def speak(self, text):

        print("\nAI:", text)

        filename = f"temp/{uuid.uuid4().hex}.wav"

        with wave.open(filename, "wb") as wav_file:

            self.voice.synthesize_wav(
                text,
                wav_file
            )

        playsound(filename)

        try:
            os.remove(filename)

        except:
            pass