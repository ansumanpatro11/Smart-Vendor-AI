import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.db import Base, engine
from backend.routes import auth, bills, inventory, analytics

load_dotenv()

# create tables (dev only)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Vendor AI - Backend (SQL + GenAI)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(bills.router, prefix="/api/v1/bills", tags=["bills"])
app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["inventory"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

@app.get('/')
def root():
    return {"status":"ok", "msg":"Smart Vendor AI backend running"}
