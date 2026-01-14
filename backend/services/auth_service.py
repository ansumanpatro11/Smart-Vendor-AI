from sqlalchemy.orm import Session
from backend.models.models import User
from backend.services.pw import hash_password, verify_password
from backend.services.jwt_util import create_access_token
from fastapi import HTTPException

class AuthService:
    def register(self, user, db: Session):
        existing = db.query(User).filter(User.email==user.email).first()
        if existing:
            raise HTTPException(status_code=400, detail='Email already exists')
        new = User(name=user.name, email=user.email, password_hash=hash_password(user.password))
        db.add(new); db.commit(); db.refresh(new)
        token = create_access_token({'user_id': new.user_id, 'email': new.email})
        return {'access_token': token}

    def login(self, email: str, password: str, db: Session):
        user = db.query(User).filter(User.email==email).first()
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail='Invalid credentials')
        token = create_access_token({'user_id': user.user_id, 'email': user.email})
        return {'access_token': token}
