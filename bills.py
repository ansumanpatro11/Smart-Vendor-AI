from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.services.bill_service import BillService

router = APIRouter()
service = BillService()

@router.post('/speech')
async def create_from_speech(
    user_id: int = Form(...),
    audio: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return await service.create_from_speech(user_id, audio, db)


@router.post('/text')
async def create_from_text(
    user_id: int = Form(...),
    text: str = Form(...),
    db: Session = Depends(get_db)
):
    return await service.create_from_text(user_id, text, db)



