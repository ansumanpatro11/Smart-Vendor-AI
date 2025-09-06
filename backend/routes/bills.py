from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from backend.db import get_db
from backend import models, schemas, auth
from decimal import Decimal
from backend.services.whisper_service import transcribe_audio
from backend.services.llm_parser import parse_bill_text
from typing import List

router = APIRouter()

def _create_bill_from_items(db: Session, user_id: int, items: List[dict], total_amount: float):
    new_bill = models.Bill(user_id=user_id, total_amount=Decimal(total_amount))
    db.add(new_bill)
    db.flush()
    for it in items:
        product_id = it["product_id"]
        qty = int(it["quantity"])
        ppu = Decimal(it["price_per_unit"])
        subtotal = qty * ppu

        prod = db.query(models.Product).filter(models.Product.product_id==product_id).first()
        if not prod:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
        if prod.stock_quantity < qty:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {prod.name}")
        prod.stock_quantity -= qty

        bi = models.BillItem(bill_id=new_bill.bill_id, product_id=product_id, quantity=qty, price_per_unit=ppu, subtotal=subtotal)
        db.add(bi)
    db.commit()
    db.refresh(new_bill)
    return new_bill

@router.post("/", response_model=schemas.BillOut)
def create_bill(bill: schemas.BillCreate, db: Session = Depends(get_db), token: dict = Depends(auth.get_current_user)):
    try:
        return _create_bill_from_items(db, bill.user_id, [i.dict() for i in bill.items], bill.total_amount)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/speech", response_model=schemas.BillOut)
async def create_bill_from_speech(user_id: int = Form(...), audio: UploadFile = File(...), db: Session = Depends(get_db), token: dict = Depends(auth.get_current_user)):
    # 1) Transcribe
    import tempfile, shutil
    with tempfile.NamedTemporaryFile(delete=False, suffix=audio.filename[-4:]) as tmp:
        shutil.copyfileobj(audio.file, tmp)
        tmp_path = tmp.name
    transcript = transcribe_audio(tmp_path)

    # 2) Parse with LLM (structured)
    parsed = await parse_bill_text(transcript, db)
    if not parsed or not parsed.items:
        raise HTTPException(status_code=400, detail="Failed to parse bill items from speech")

    # 3) Build items list by mapping product names -> IDs (parser already maps if found)
    items = []
    total = float(parsed.total_amount) if parsed.total_amount else 0.0
    for it in parsed.items:
        items.append({
            "product_id": it.product_id,
            "quantity": it.quantity,
            "price_per_unit": it.price_per_unit
        })
        if total == 0.0:
            total += it.quantity * it.price_per_unit

    # 4) Persist
    return _create_bill_from_items(db, user_id, items, total)
