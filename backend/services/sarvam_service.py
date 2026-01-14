import os
from sarvamai import SarvamAI
from dotenv import load_dotenv
load_dotenv()

SARVAM_KEY = os.getenv('SARVAM_API_KEY')
client = SarvamAI(api_subscription_key=SARVAM_KEY)

def transcribe_file(path: str, model: str = 'saarika:v2.5', language_code: str = 'en-IN'):
    with open(path, 'rb') as f:
        resp = client.speech_to_text.transcribe(file=f, model=model, language_code=language_code)
    try:
        if isinstance(resp, dict):
            return resp.get('text', '') or resp.get('transcript','') or ''
        return getattr(resp, 'text', '') or str(resp)
    except Exception:
        return str(resp)
