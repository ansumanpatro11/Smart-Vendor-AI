from passlib.context import CryptContext
pwd = CryptContext(schemes=['bcrypt'], deprecated='auto')
def hash_password(pw: str):
    return pwd.hash(pw)
def verify_password(plain: str, hashed: str):
    return pwd.verify(plain, hashed)
