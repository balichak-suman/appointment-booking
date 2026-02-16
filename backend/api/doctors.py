from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db, Doctor
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(tags=["Doctors"])

@router.get("")
def get_doctors(
    skip: int = 0,
    limit: int = 100,
    specialization: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Doctor)
    if specialization:
        query = query.filter(Doctor.specialization == specialization)
    
    total = query.count()
    doctors_db = query.offset(skip).limit(limit).all()
    
    formatted_doctors = []
    for d in doctors_db:
        formatted_doctors.append({
            "id": d.id,
            "name": d.name,
            "specialization": d.specialization,
            "experience": d.experience,
            "patients": d.patients,
            "appointments": d.appointments,
            "rating": d.rating,
            "status": d.status,
            "email": d.email,
            "phone": d.phone,
            "working_hours_start": d.working_hours_start,
            "working_hours_end": d.working_hours_end,
            "working_days": d.working_days
        })

    return {
        "success": True,
        "data": formatted_doctors
    }

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    email: str
    phone: Optional[str] = None
    experience: int = 0
    working_hours_start: str = "09:00"
    working_hours_end: str = "17:00"
    working_days: str = "Monday,Tuesday,Wednesday,Thursday,Friday"
    google_calendar_id: Optional[str] = None

@router.post("")
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    try:
        # Check if email already exists
        existing_doctor = db.query(Doctor).filter(Doctor.email == doctor.email).first()
        if existing_doctor:
            raise HTTPException(status_code=400, detail="Doctor with this email already exists")

        new_doctor = Doctor(
            name=doctor.name,
            specialization=doctor.specialization,
            email=doctor.email,
            phone=doctor.phone,
            experience=doctor.experience,
            working_hours_start=doctor.working_hours_start,
            working_hours_end=doctor.working_hours_end,
            working_days=doctor.working_days,
            google_calendar_id=doctor.google_calendar_id,
            status="Available"
        )
        
        db.add(new_doctor)
        db.commit()
        db.refresh(new_doctor)
        return {"success": True, "data": new_doctor, "message": "Doctor created successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        print(f"Error creating doctor: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    try:
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
            
        # Optional: Check for active appointments? For now, we allow deletion.
        # Ideally we should handle associated appointments (set doctor_id to null or delete)
        # Assuming simple deletion is what's requested.
        
        db.delete(doctor)
        db.commit()
        return {"success": True, "message": "Doctor deleted successfully"}
    except Exception as e:
        db.rollback()
        print(f"Error deleting doctor: {e}")
        raise HTTPException(status_code=500, detail=str(e))
