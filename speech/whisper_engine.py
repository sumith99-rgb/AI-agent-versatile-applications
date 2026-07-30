import requests
import os

from config import (
    GROQ_API_KEY,
    WHISPER_MODEL
)

class WhisperEngine:

    def __init__(self):
        print("Loading Whisper Engine (Groq Cloud)...")
        if not GROQ_API_KEY or GROQ_API_KEY == "PASTE_YOUR_GROQ_API_KEY_HERE":
            print("WARNING: GROQ_API_KEY is not set in config.py!")
            self.api_key = None
        else:
            self.api_key = GROQ_API_KEY
        print("Whisper Loaded!")

    def transcribe(self, audio_path):
        if not self.api_key:
            return "API Key missing."

        url = "https://api.groq.com/openai/v1/audio/transcriptions"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            with open(audio_path, "rb") as audio_file:
                files = {
                    "file": (os.path.basename(audio_path), audio_file, "audio/wav")
                }
                data = {
                    "model": WHISPER_MODEL
                }

                # We use a 10 second timeout
                response = requests.post(url, headers=headers, files=files, data=data, timeout=10)

                if response.status_code != 200:
                    print(f"Groq API Error: {response.status_code} - {response.text}")
                    return "Sorry, I couldn't understand that."

                result = response.json()
                text = result.get("text", "")
                return text.strip()

        except requests.exceptions.Timeout:
            print("Groq API Error: Request timed out.")
            return "Transcription timed out."
        except Exception as e:
            print("Groq API Error:", e)
            return "Transcription failed."