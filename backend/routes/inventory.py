from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.services.inventory_service import InventoryService
from backend.models.schemas import ProductCreate

router = APIRouter()
service = InventoryService()

@router.post('/')
def add_product(p: ProductCreate, db: Session = Depends(get_db)):
    return service.add(p, db)

@router.get('/')
def list_products(db: Session = Depends(get_db)):
    return service.list(db)
