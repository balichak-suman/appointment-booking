from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from medical_backend.settings import CORS_ORIGINS
from medical_backend.urls import api_router
from database import init_db

app = FastAPI(title="Medical Dashboard API", version="3.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Centralized Router (urls.py)
app.include_router(api_router)

@app.on_event("startup")
def startup_event():
    init_db()
    print("✅ Database initialized successfully!")

@app.get("/")
def read_root():
    return {
        "message": "Medical Dashboard API - Modular Edition",
        "status": "Running",
        "database": "PostgreSQL (hospital)"
    }
