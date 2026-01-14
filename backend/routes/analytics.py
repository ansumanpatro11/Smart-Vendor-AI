from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from backend.services.sarvam_service import transcribe_file
from backend.services.text_to_sql import run_nl_analytics_query
from backend.db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text

router = APIRouter()

@router.post('/speech')
async def analytics_from_speech(audio: UploadFile = File(...), db: Session = Depends(get_db)):
    import tempfile, shutil
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
        shutil.copyfileobj(audio.file, tmp)
        tmp_path = tmp.name
    textq = transcribe_file(tmp_path)
    if not textq:
        raise HTTPException(status_code=400, detail='Could not transcribe')
    result = run_nl_analytics_query(textq)
    # Return rows as list for table display instead of full JSON
    if result.get('success') and result.get('rows'):
        return result['rows']
    return result

@router.post('/text')
def analytics_from_text(query: str = Form(...)):
    return run_nl_analytics_query(query)

@router.get('/views/{view_name}')
def get_view(view_name: str, db: Session = Depends(get_db)):
    engine = db.get_bind()
    if view_name not in ('top_selling_products','most_profitable_products','monthly_sales_summary'):
        raise HTTPException(status_code=404, detail='unknown view')
    with engine.connect() as conn:
        res = conn.execute(text(f'SELECT * FROM {view_name}'))
        rows = [dict(r._mapping) for r in res]
    return rows
