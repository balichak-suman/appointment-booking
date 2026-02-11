import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# DATABASE CONFIGURATION
# ============================================
# Using PostgreSQL only as per your request
# ============================================
# DATABASE CONFIGURATION
# ============================================
# Construct the SQLAlchemy URL
# Construct the SQLAlchemy URL
# Format: postgresql://user:password@host:port/name
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hospital.db")

# Log DB connection (masked)
if "sqlite" in DATABASE_URL:
    print(f"[DB] Using SQLite Database (Local Testing)")
else:
    print(f"[DB] Using PostgreSQL Database")

# ============================================
# API SETTINGS
# ============================================
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8001))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:5174,http://localhost:5175").split(",")

# ============================================
# MEDIA SETTINGS
# ============================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
