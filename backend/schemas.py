from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ProductCreate(BaseModel):
    name: str
    category: Optional[str] = None
    price: float
    cost_price: Optional[float] = 0.0
    stock_quantity: int

class ProductOut(BaseModel):
    product_id: int
    name: str
    category: Optional[str]
    price: float
    cost_price: Optional[float]
    stock_quantity: int

    class Config:
        orm_mode = True

class BillItemIn(BaseModel):
    product_id: int
    quantity: int
    price_per_unit: float

class BillCreate(BaseModel):
    user_id: int
    items: List[BillItemIn]
    total_amount: float

class BillOut(BaseModel):
    bill_id: int
    user_id: int
    total_amount: float
    created_at: datetime

    class Config:
        orm_mode = True
