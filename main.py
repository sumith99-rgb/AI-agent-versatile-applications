import speech_recognition as sr
import wave

from speech.whisper_engine import WhisperEngine
from speech.piper_engine import PiperEngine

from ai.brain import Brain
from ai.planner import Planner

from ai.memory import MemoryManager


# ----------------------------
# LOAD MODULES
# ----------------------------

print("Loading Modules...")

whisper = WhisperEngine()

speaker = PiperEngine()

brain = Brain()

planner = Planner()

memory = MemoryManager()

print("All Modules Loaded!")

# ----------------------------
# MICROPHONE
# ----------------------------

recognizer = sr.Recognizer()

print("\n======================================")
print(" LiftGuard AI Started Successfully ")
print("======================================\n")

while True:

    try:

        with sr.Microphone(device_index=2) as source:

            print("Listening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        with open("temp/audio.wav", "wb") as f:
            f.write(audio.get_wav_data())

        user_text = whisper.transcribe(
            "temp/audio.wav"
        )

        if not user_text:
            continue

        print("\nYou:", user_text)

        # -----------------------
        # EXIT
        # -----------------------

        if user_text.lower() in [
            "exit",
            "quit",
            "stop"
        ]:

            speaker.speak(
                "Goodbye!"
            )

            break

        # -----------------------
        # PLANNER
        # -----------------------

        decision = planner.plan(
            user_text
        )

        print("\nPlanner Decision:")
        print(decision)

        # -----------------------
        # TEMP
        # -----------------------

        reply = brain.ask(
            user_text
        )

        speaker.speak(
            reply
        )

    except sr.WaitTimeoutError:

        print("No speech detected.")

    except KeyboardInterrupt:

        print("\nClosing...")

        break

    except Exception as e:

        print("ERROR:", e)