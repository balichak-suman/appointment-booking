from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Patient
from typing import List, Optional

router = APIRouter(tags=["Patients"])

@router.get("")
def get_patients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Patient)
    total = query.count()
    patients_db = query.offset(skip).limit(limit).all()
    
    # Format to camelCase for frontend
    formatted_patients = []
    for p in patients_db:
        formatted_patients.append({
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "gender": p.gender,
            "bloodGroup": p.blood_group,
            "condition": p.condition,
            "lastVisit": str(p.last_visit) if p.last_visit else None,
            "status": p.status,
            "email": p.email,
            "phone": p.phone,
            "address": p.address
        })
    
    return {
        "total": total,
        "patients": formatted_patients
    }

@router.post("/")
def create_patient(patient_data: dict, db: Session = Depends(get_db)):
    try:
        new_patient = Patient(**patient_data)
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)
        return new_patient
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
