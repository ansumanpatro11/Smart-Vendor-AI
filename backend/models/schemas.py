from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class ProductCreate(BaseModel):
    name: str
    category: Optional[str] = None
    price: float
    cost_price: Optional[float] = 0.0
    stock_quantity: int

class ProductOut(BaseModel):
    product_id: int
    name: str
    price: float
    stock_quantity: int
    class Config:
        orm_mode = True

class BillItemOut(BaseModel):
    product_id: int
    quantity: int
    price_per_unit: float
    subtotal: float

    class Config:
        orm_mode = True

class BillOut(BaseModel):
    bill_id: int
    total_amount: float
    created_at: datetime
    class Config:
        orm_mode = True
