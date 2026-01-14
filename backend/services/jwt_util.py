import os, time
from jose import jwt
from dotenv import load_dotenv
load_dotenv()
SECRET = os.getenv('JWT_SECRET','devsecret')
ALGO = 'HS256'
def create_access_token(data: dict, expires=60*60*24*7):
    to_encode = data.copy(); to_encode.update({'exp': int(time.time())+expires}); return jwt.encode(to_encode, SECRET, algorithm=ALGO)
