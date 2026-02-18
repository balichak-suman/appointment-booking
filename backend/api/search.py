from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db, Appointment, Patient, Doctor
from typing import List, Dict, Any

router = APIRouter(tags=["Search"])

@router.get("")
def search_all(
    q: str = Query(..., min_length=2, description="Search query"),
    db: Session = Depends(get_db)
):
    results = []
    
    # helper to format results
    def format_result(item_type, id, title, subtitle, link):
        return {
            "type": item_type,
            "id": id,
            "title": title,
            "subtitle": subtitle,
            "link": link
        }

    # Search Patients
    patients = db.query(Patient).filter(
        or_(
            Patient.name.ilike(f"%{q}%"),
            Patient.email.ilike(f"%{q}%"),
            Patient.phone.ilike(f"%{q}%")
        )
    ).limit(5).all()
    
    for p in patients:
        results.append(format_result(
            "patient", 
            p.id, 
            p.name, 
            f"Phone: {p.phone or 'N/A'}", 
            f"/patients?id={p.id}"
        ))

    # Search Doctors
    doctors = db.query(Doctor).filter(
        or_(
            Doctor.name.ilike(f"%{q}%"),
            Doctor.specialization.ilike(f"%{q}%")
        )
    ).limit(5).all()
    
    for d in doctors:
        results.append(format_result(
            "doctor", 
            d.id, 
            d.name, 
            d.specialization, 
            f"/doctors?id={d.id}"
        ))

    # Search Appointments
    appointments = db.query(Appointment).filter(
        or_(
            Appointment.patient_name.ilike(f"%{q}%"),
            Appointment.doctor_name.ilike(f"%{q}%"),
            Appointment.reason.ilike(f"%{q}%")
        )
    ).limit(5).all()
    
    for a in appointments:
        results.append(format_result(
            "appointment", 
            a.id, 
            f"{a.patient_name} with {a.doctor_name}", 
            f"{a.date} at {a.time} ({a.status})", 
            f"/appointments?id={a.id}"
        ))
        
    return results
