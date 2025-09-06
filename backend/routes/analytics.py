from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Body
from sqlalchemy.orm import Session
from backend.db import get_db
from backend import auth
from backend.services.whisper_service import transcribe_audio
from backend.services.text_to_sql import run_nl_analytics_query

router = APIRouter()

@router.post("/speech")
async def analytics_from_speech(audio: UploadFile = File(...), db: Session = Depends(get_db), token: dict = Depends(auth.get_current_user)):
    import tempfile, shutil
    with tempfile.NamedTemporaryFile(delete=False, suffix=audio.filename[-4:]) as tmp:
        shutil.copyfileobj(audio.file, tmp)
        tmp_path = tmp.name
    text = transcribe_audio(tmp_path)
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Could not transcribe speech")

    result = run_nl_analytics_query(text)
    return {"query": text, "result": result}

@router.post("/text")
async def analytics_from_text(payload: dict = Body(...), db: Session = Depends(get_db), token: dict = Depends(auth.get_current_user)):
    q = payload.get('query')
    if not q:
        raise HTTPException(status_code=400, detail="Query missing")
    result = run_nl_analytics_query(q)
    return {"query": q, "result": result}
