import requests
import json

from config import (
    GROQ_API_KEY,
    GROQ_LLM_MODEL
)


class Brain:

    def __init__(self):

        print(f"Brain Loaded ({GROQ_LLM_MODEL})")
        
        if GROQ_API_KEY and GROQ_API_KEY != "PASTE_YOUR_GROQ_API_KEY_HERE":
            self.model = GROQ_LLM_MODEL
        else:
            self.model = None
            print("WARNING: GROQ_API_KEY is not set in config.py!")

    def ask(self, prompt, is_json=False):
        
        if not self.model:
            return "Sorry, the Groq API key is not configured. Please paste it in config.py."

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}"
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        
        if is_json:
            payload["response_format"] = {"type": "json_object"}
            
        try:
            # Groq is insanely fast, a 10s timeout is more than enough
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code != 200:
                print(f"Groq API Error: {response.status_code} - {response.text}")
                return "Sorry, I couldn't answer."
                
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

        except requests.exceptions.Timeout:
            print("Groq API Error: Request timed out.")
            return "Sorry, the AI server took too long to respond."
        except Exception as e:
            print("Groq API Error:", e)
            return "Sorry, I couldn't answer."