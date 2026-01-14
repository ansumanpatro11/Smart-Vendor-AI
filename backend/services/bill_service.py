import tempfile, shutil, os
from decimal import Decimal
from backend.services.sarvam_service import transcribe_file
from backend.services.gemini_service import parse_bill_text_and_map
from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.models.models import Bill, BillItem, Product

class BillService:
    async def create_from_speech(self, user_id, audio, db: Session):
        # save audio to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
            shutil.copyfileobj(audio.file, tmp)
            tmp_path = tmp.name
        # transcribe via Sarvam AI
        text = transcribe_file(tmp_path)
        if not text:
            raise HTTPException(status_code=400, detail='Could not transcribe audio')
        # parse and create bill
        return await self._create_from_text(user_id, text, db)

    async def create_from_text(self, user_id, text, db: Session):
        return await self._create_from_text(user_id, text, db)

    async def _create_from_text(self, user_id, text, db: Session):
        # parse with Gemini and map to product IDs (expects list of items with product_id, quantity, price_per_unit)
        parsed = parse_bill_text_and_map(text, db)
        items = parsed.get('items', [])
        total = parsed.get('total', 0)

        if not items:
            raise HTTPException(status_code=400, detail='No items parsed from bill text')

        try:
            # create bill record
            bill = Bill(user_id=user_id, total_amount=Decimal(total))
            db.add(bill)
            db.flush()  # populates bill.bill_id

            # create bill items and update stock
            for it in items:
                pid = it.get('product_id')
                qty = int(it.get('quantity') or it.get('qty') or 0)
                price = Decimal(it.get('price_per_unit') or it.get('price') or 0)
                product = db.query(Product).filter(Product.product_id == pid).with_for_update().first()
                if not product:
                    db.rollback()
                    raise HTTPException(status_code=404, detail=f'Product {pid} not found')
                if product.stock_quantity < qty:
                    db.rollback()
                    raise HTTPException(status_code=400, detail=f'Insufficient stock for {product.name}')
                product.stock_quantity = product.stock_quantity - qty
                subtotal = qty * price
                bi = BillItem(bill_id=bill.bill_id, product_id=pid, quantity=qty, price_per_unit=price, subtotal=subtotal)
                db.add(bi)

            db.commit()
            db.refresh(bill)
            return {'status':'ok', 'bill_id': bill.bill_id, 'total': float(bill.total_amount)}
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
