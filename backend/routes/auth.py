from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend import models, schemas, db, auth as _auth
from backend.db import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register", response_model=dict)
def register(user: schemas.UserCreate, database: Session = Depends(get_db)):
    existing = database.query(models.User).filter(models.User.email==user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_obj = models.User(
        name=user.name,
        email=user.email,
        password_hash=_auth.get_password_hash(user.password),
        role="vendor"
    )
    database.add(user_obj)
    database.commit()
    database.refresh(user_obj)
    token = _auth.create_access_token({"user_id": user_obj.user_id, "email": user_obj.email, "role": user_obj.role})
    return {"access_token": token, "token_type":"bearer"}

@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(get_db)):
    user = database.query(models.User).filter(models.User.email==form_data.username).first()
    if not user or not _auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    token = _auth.create_access_token({"user_id": user.user_id, "email": user.email, "role": user.role})
    return {"access_token": token, "token_type":"bearer"}
