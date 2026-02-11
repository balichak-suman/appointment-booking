import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# USER: PASTE YOUR RENDER DATABASE URL HERE
RENDER_DB_URL = "postgresql://hospital_db_z7qv_user:aqbJ8NMDmipesRbzvgF0vTFdVfshbkau@dpg-d66c1scr85hc73dcvmog-a.oregon-postgres.render.com/hospital_db_z7qv"

print(f"Connecting to: {RENDER_DB_URL}")
engine = create_engine(RENDER_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Doctor model inline to avoid importing from database.py (which connects to local DB)
class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    experience = Column(Integer, default=5)
    patients = Column(Integer, default=0)
    appointments = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    status = Column(String, default="Available")
    email = Column(String, nullable=False) # Changed from unique=True to avoid constraint issues if re-seeding differently
    phone = Column(String)
    
    # WhatsApp Integration fields
    google_calendar_id = Column(String, nullable=True)
    working_hours_start = Column(String, default="09:00")
    working_hours_end = Column(String, default="17:00")
    slot_duration_minutes = Column(Integer, default=30)
    working_days = Column(String, default="Monday,Tuesday,Wednesday,Thursday,Friday")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

def seed_doctors():
    db = SessionLocal()
    try:
        # Check if doctors exist
        # Create tables if they don't exist (safety)
        Base.metadata.create_all(bind=engine)
        
        count = db.query(Doctor).count()
        if count > 0:
            print(f"Database already has {count} doctors. Skipping seed.")
            return

        print("Seeding doctors...")
        
        doctors = [
            Doctor(
                name="Dr. Sarah Smith",
                specialization="Cardiologist",
                email="sarah@hospital.com",
                working_hours_start="09:00",
                working_hours_end="17:00",
                working_days="Monday,Wednesday,Friday",
                slot_duration_minutes=30,
                status="Available",
                google_calendar_id="primary" 
            ),
            Doctor(
                name="Dr. John Doe",
                specialization="Dermatologist",
                email="john@hospital.com",
                working_hours_start="10:00",
                working_hours_end="16:00",
                working_days="Tuesday,Thursday",
                slot_duration_minutes=45,
                status="Available",
                google_calendar_id="primary"
            ),
            Doctor(
                name="Dr. Emily White",
                specialization="General Physician",
                email="emily@hospital.com",
                working_hours_start="08:00",
                working_hours_end="14:00",
                working_days="Monday,Tuesday,Wednesday,Thursday,Friday",
                slot_duration_minutes=15,
                status="Available",
                google_calendar_id="primary"
            )
        ]
        
        db.add_all(doctors)
        db.commit()
        print("✅ Successfully seeded 3 doctors to Render DB!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    confirm = input("This will add data to your RENDER database. Type 'yes' to proceed: ")
    if confirm.lower() == 'yes':
        seed_doctors()
    else:
        print("Cancelled.")
