import os
import sys
import traceback
import speech_recognition as sr

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from ai.brain import Brain
from ai.planner import Planner
from ai.memory import MemoryManager

from speech.whisper_engine import WhisperEngine
from speech.piper_engine import PiperEngine

from tools.registry import ToolRegistry
from tools.memory_tool import MemoryTool
from tools.tickets import TicketTool
from tools.emergency import EmergencyTool
from tools.email import EmailTool
from tools.whatsapp import WhatsAppTool
from tools.knowledge import KnowledgeTool

from core.executor import Executor

from config import (
    MIC_DEVICE_INDEX,
    TEMP_AUDIO,
    MAX_CONVERSATION_LENGTH
)


class Agent:

    def __init__(self):

        print("=" * 50)
        print("        LiftGuard AI Starting")
        print("=" * 50)

        # -------------------------
        # AI
        # -------------------------

        self.brain = Brain()
        self.planner = Planner()

        # -------------------------
        # Speech
        # -------------------------

        self.whisper = WhisperEngine()
        self.piper = PiperEngine()

        # -------------------------
        # Memory
        # -------------------------

        self.memory = MemoryManager()

        # -------------------------
        # Registry
        # -------------------------

        self.registry = ToolRegistry()

        # Register built-in tools
        self.registry.register(MemoryTool())
        self.registry.register(TicketTool())
        self.registry.register(EmergencyTool())
        self.registry.register(KnowledgeTool())
        self.registry.register(EmailTool())
        self.registry.register(WhatsAppTool())

        # -------------------------
        # Executor
        # -------------------------

        self.executor = Executor(
            self.registry
        )

        # -------------------------
        # Speech Recognition
        # -------------------------

        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.5

        print("\nRegistered Tools:")
        print(self.registry.list_tools())

        print("\nLiftGuard AI Ready!\n")

            # ------------------------------------
    # LISTEN
    # ------------------------------------

    def listen(self):

        with sr.Microphone(
            device_index=MIC_DEVICE_INDEX
        ) as source:

            print("\nListening...")

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = self.recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        with open(TEMP_AUDIO, "wb") as f:

            f.write(
                audio.get_wav_data()
            )

        return TEMP_AUDIO

    # ------------------------------------
    # TRANSCRIBE
    # ------------------------------------

    def transcribe(self):

        text = self.whisper.transcribe(
            TEMP_AUDIO
        )

        print("\nUSER:", text)

        return text

    # ------------------------------------
    # PLAN
    # ------------------------------------

    def create_plan(self, user_text):

        plan = self.planner.plan(
            user_text
        )

        return plan

    # ------------------------------------
    # EXECUTE
    # ------------------------------------

    def execute_plan(self, plan):

        if not plan.get("steps"):

            return

        results = self.executor.execute(
            plan
        )

        return results

    # ------------------------------------
    # BUILD PROMPT
    # ------------------------------------

    def build_prompt(self, user_text, results=None):

        conversation = self.memory.get_conversation()
        user_info = self.memory.get_all_user_info()

        history = ""

        for message in conversation[-10:]:

            history += (
                f"{message['role']}: "
                f"{message['message']}\n"
            )

        known_facts = ""
        if user_info:
            known_facts = "Known User Information:\n"
            for k, v in user_info.items():
                known_facts += f"- {k}: {v}\n"

        tool_results = ""
        if results:
            tool_results = f"\nSystem Tools just executed. Their results:\n{results}\n"

        prompt = f"""
You are LiftGuard AI, a helpful voice assistant. You must always respond in English.
Keep your answers brief and concise.

{known_facts}
Conversation History:

{history}

User:

{user_text}
{tool_results}
Assistant:
"""

        return prompt

    # ------------------------------------
    # GENERATE RESPONSE
    # ------------------------------------

    def generate_reply(self, user_text, results=None):

        prompt = self.build_prompt(
            user_text, results
        )

        reply = self.brain.ask(
            prompt
        )

        return reply

    # ------------------------------------
    # SAVE CONVERSATION
    # ------------------------------------

    def save_conversation(
        self,
        user_text,
        reply
    ):

        self.memory.add_message(
            "User",
            user_text
        )

        self.memory.add_message(
            "Assistant",
            reply
        )

    # ------------------------------------
    # RUN
    # ------------------------------------

    def run(self):

        print("=" * 50)
        print("LiftGuard AI Running")
        print("=" * 50)

        while True:

            try:

                audio_path = self.listen()

                user_text = self.transcribe()

                if not user_text.strip():
                    continue

                if user_text.lower() in [
                    "exit",
                    "quit",
                    "stop"
                ]:

                    self.piper.speak(
                        "Goodbye!"
                    )

                    break

                plan = self.create_plan(
                    user_text
                )

                if not isinstance(plan, dict):
                    raise ValueError("Planner did not return an execution plan.")

                from ai.extractor import Extractor

                extractor = Extractor()

                for step in plan.get("steps", []):
                    tool = step.get("tool")
                    
                    extracted_args = extractor.extract(tool, user_text)
                    if "arguments" not in step or not isinstance(step["arguments"], dict):
                        step["arguments"] = {}
                    
                    for k, v in extracted_args.items():
                        if k not in step["arguments"]:
                            step["arguments"][k] = v

                results = self.execute_plan(
                    plan
                )

                reply = self.generate_reply(
                    user_text, results
                )

                self.save_conversation(
                    user_text,
                    reply
                )

                self.piper.speak(
                    reply
                )

            except sr.WaitTimeoutError:

                print("No speech detected.")

            except KeyboardInterrupt:
                print("\nStopping LiftGuard AI...")
                break

            except Exception as e:
                print("ERROR:", e)
                traceback.print_exc()

    