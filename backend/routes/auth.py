from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.models.models import User
from backend.services.auth_service import AuthService
from backend.models.schemas import UserCreate

router = APIRouter()
service = AuthService()

@router.post('/register')
def register(user: UserCreate, db: Session = Depends(get_db)):
    return service.register(user, db)

@router.post('/token')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return service.login(form_data.username, form_data.password, db)
