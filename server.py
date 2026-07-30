import os
import requests
from flask import Flask, request, jsonify, render_template, send_file
from gtts import gTTS

from config import GROQ_API_KEY, WHISPER_MODEL
from ai.brain import Brain
from ai.planner import Planner
from ai.memory import MemoryManager
from tools.registry import ToolRegistry
from tools.memory_tool import MemoryTool
from tools.tickets import TicketTool
from tools.emergency import EmergencyTool
from tools.email import EmailTool
from tools.whatsapp import WhatsAppTool
from tools.knowledge import KnowledgeTool
from core.executor import Executor
from ai.extractor import Extractor

app = Flask(__name__)

# Ensure temp directory exists
os.makedirs("temp", exist_ok=True)

# Initialize components
brain = Brain()
planner = Planner()
memory = MemoryManager()
registry = ToolRegistry()
registry.register(MemoryTool())
registry.register(TicketTool())
registry.register(EmergencyTool())
registry.register(KnowledgeTool())
registry.register(EmailTool())
registry.register(WhatsAppTool())
executor = Executor(registry)
extractor = Extractor()


def transcribe_audio(audio_path):
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    with open(audio_path, "rb") as f:
        files = {
            "file": ("recording.webm", f, "audio/webm"),
            "model": (None, WHISPER_MODEL),
        }
        resp = requests.post(url, headers=headers, files=files)
        
    if resp.status_code == 200:
        return resp.json().get("text", "").strip()
    else:
        print(f"STT Error: {resp.text}")
        return ""


def synthesize_speech(text, output_path):
    tts = gTTS(text=text, lang='en', tld='us')
    tts.save(output_path)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/intercom", methods=["POST"])
def intercom():
    if "audio" not in request.files:
        return jsonify({"status": "error", "message": "No audio file provided"})
        
    audio_file = request.files["audio"]
    audio_path = "temp/recording.webm"
    audio_file.save(audio_path)
    
    # 1. Transcribe Audio (STT)
    user_text = transcribe_audio(audio_path)
    if not user_text:
        return jsonify({"status": "error", "message": "Could not understand audio"})
        
    print(f"\nUSER: {user_text}")
    memory.add_message("User", user_text)
    
    # 2. Plan Actions
    plan = planner.plan(user_text)
    
    # 3. Extract args & Execute tools
    for step in plan.get("steps", []):
        tool = step.get("tool")
        extracted_args = extractor.extract(tool, user_text)
        if "arguments" not in step or not isinstance(step["arguments"], dict):
            step["arguments"] = {}
        for k, v in extracted_args.items():
            if k not in step["arguments"]:
                step["arguments"][k] = v
                
    results = None
    if plan.get("steps"):
        results = executor.execute(plan)
        
    # 4. Generate AI Reply
    conversation = memory.get_conversation()
    user_info = memory.get_all_user_info()
    
    history = ""
    for message in conversation[-10:]:
        history += f"{message['role']}: {message['message']}\n"
    
    known_facts = ""
    if user_info:
        known_facts = "Known User Information:\n"
        for k, v in user_info.items():
            known_facts += f"- {k}: {v}\n"
            
    tool_results = ""
    if results:
        tool_results = f"\nSystem Tools just executed. Their results:\n{results}\n"
        
    prompt = f"""
You are LiftGuard AI, a helpful voice assistant inside an elevator. You must always respond in English.
Keep your answers very brief, conversational, and concise.

CRITICAL INSTRUCTION: If a user reports an emergency and the System Tools have NOT executed the emergency tool, it means we don't know their location. You MUST ask the user for the address or location of the lift BEFORE you promise that help is on the way.

{known_facts}
Conversation History:

{history}

User:
{user_text}
{tool_results}
Assistant:
"""
    reply = brain.ask(prompt)
    print(f"AI: {reply}")
    memory.add_message("Assistant", reply)
    
    # 5. Synthesize Speech (TTS)
    tts_path = "temp/response.mp3"
    synthesize_speech(reply, tts_path)
    
    return jsonify({
        "status": "success",
        "user_text": user_text,
        "ai_text": reply,
        "audio_url": "/api/audio"
    })


@app.route("/api/audio")
def get_audio():
    return send_file("temp/response.mp3", mimetype="audio/mpeg")


if __name__ == "__main__":
    print("Starting LiftGuard Web Intercom on http://localhost:5000 ...")
    app.run(host="0.0.0.0", port=5000, debug=True)
