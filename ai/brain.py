import requests

from config import (
    OLLAMA_MODEL,
    OLLAMA_URL
)


class Brain:

    def __init__(self):

        print(f"Brain Loaded ({OLLAMA_MODEL})")

    def ask(self, prompt):

        response = requests.post(

            OLLAMA_URL,

            json={

                "model": OLLAMA_MODEL,

                "prompt": prompt,

                "stream": False,

                "options": {

                    "temperature": 0.7,

                    "num_predict": 200

                }

            }

        )

        data = response.json()

        return data.get(
            "response",
            "Sorry, I couldn't answer."
        ).strip()