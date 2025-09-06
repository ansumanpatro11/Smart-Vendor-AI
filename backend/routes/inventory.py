from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from backend.db import get_db
from backend import models, schemas, auth

router = APIRouter()

@router.post("/", response_model=dict)
def add_product(p: schemas.ProductCreate, db: Session = Depends(get_db), token: dict = Depends(auth.get_current_user)):
    prod = models.Product(name=p.name, category=p.category, price=p.price, cost_price=p.cost_price, stock_quantity=p.stock_quantity)
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return {"product_id": prod.product_id}

@router.get("/", response_model=List[schemas.ProductOut])
def list_products(db: Session = Depends(get_db), token: dict = Depends(auth.get_current_user)):
    prods = db.query(models.Product).order_by(models.Product.stock_quantity.asc()).all()
    return prods

@router.patch("/{product_id}", response_model=dict)
def update_stock(product_id: int, qty: int, db: Session = Depends(get_db), token: dict = Depends(auth.get_current_user)):
    prod = db.query(models.Product).filter(models.Product.product_id==product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    if qty < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be negative")
    prod.stock_quantity = qty
    db.commit()
    return {"status":"ok"}
