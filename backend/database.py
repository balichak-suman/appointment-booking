"""
Database Configuration - PostgreSQL Only
"""

from sqlalchemy import create_engine, Column, Integer, String, Date, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

from medical_backend.settings import DATABASE_URL

# Create engine
engine = create_engine(DATABASE_URL)
print(f"🗄️  Using PostgreSQL database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}")

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Database Models
class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    experience = Column(Integer)
    patients = Column(Integer, default=0)
    appointments = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    status = Column(String, default="Available")
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    
    # WhatsApp Integration fields
    google_calendar_id = Column(String, nullable=True)
    working_hours_start = Column(String, default="09:00")
    working_hours_end = Column(String, default="17:00")
    slot_duration_minutes = Column(Integer, default=30)
    working_days = Column(String, default="Monday,Tuesday,Wednesday,Thursday,Friday")  # Comma-separated
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    blood_group = Column(String)
    condition = Column(String)
    last_visit = Column(Date)
    status = Column(String, default="Active")
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    address = Column(String)
    
    # WhatsApp Integration
    whatsapp_number = Column(String, nullable=True)  # For WhatsApp booking
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    doctor_name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(String, nullable=False)
    type = Column(String, default="Scheduled")  # Scheduled, Walk-in, Emergency, Follow-up
    status = Column(String, default="Scheduled")  # Scheduled, Completed, Cancelled, Rescheduled
    reason = Column(String)
    department = Column(String)
    
    # Additional fields for tracking
    patient_id = Column(Integer, nullable=True)  # Link to patient
    doctor_id = Column(Integer, nullable=True)   # Link to doctor
    patient_phone = Column(String, nullable=True)  # For WhatsApp notifications
    booking_source = Column(String, default="Dashboard")  # Dashboard, WhatsApp, Phone
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

# Database utility functions
def get_db_info():
    """Get database information"""
    return {
        "type": "PostgreSQL",
        "url": DATABASE_URL.replace(DATABASE_URL.split("@")[-1].split("/")[0] if "@" in DATABASE_URL else "", "***") if "@" in DATABASE_URL else DATABASE_URL,
        "status": "Connected"
    }
