import os
import traceback
os.environ['PYTHONPATH'] = '.'
from core.agent import Agent

class TestAgent(Agent):
    def listen(self):
        return 'temp/audio.wav'

    def transcribe(self):
        return 'Hello'


try:
    a = TestAgent()
    a.memory = a.memory  # preserve
    a.run()
except Exception:
    traceback.print_exc()
