import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(file_path: str):
    try:
        with open(file_path, "rb") as f:
            resp = openai.Audio.transcriptions.create(model="whisper-1", file=f)  # adjust if SDK changes
        return getattr(resp, "text", "") if resp else ""
    except Exception as e:
        print("Whisper error:", e)
        return ""
