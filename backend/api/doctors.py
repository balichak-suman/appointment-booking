from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db, Doctor
from typing import List, Optional

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
    doctors = query.offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "data": doctors
    }

@router.post("/")
def create_doctor(doctor_data: dict, db: Session = Depends(get_db)):
    try:
        new_doctor = Doctor(**doctor_data)
        db.add(new_doctor)
        db.commit()
        db.refresh(new_doctor)
        return new_doctor
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
