from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

from backend.routes import auth, inventory, bills, analytics
from backend.db.session import engine, Base

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title='Smart Vendor AI')

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

app.include_router(auth.router, prefix='/api/v1/auth', tags=['auth'])
app.include_router(inventory.router, prefix='/api/v1/inventory', tags=['inventory'])
app.include_router(bills.router, prefix='/api/v1/bills', tags=['bills'])
app.include_router(analytics.router, prefix='/api/v1/analytics', tags=['analytics'])

@app.get('/')
def root():
    return {'status':'ok'}
