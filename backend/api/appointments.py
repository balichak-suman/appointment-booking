from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Appointment
from typing import List, Optional

router = APIRouter(tags=["Appointments"])

@router.get("")
def get_appointments(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    print(">>> GET APPOINTMENTS CALLED")
    query = db.query(Appointment)
    if status:
        query = query.filter(Appointment.status == status)
    
    total = query.count()
    appointments_db = query.offset(skip).limit(limit).all()
    
    # Format to camelCase for frontend
    formatted_appointments = []
    for apt in appointments_db:
        formatted_appointments.append({
            "id": apt.id,
            "patientName": apt.patient_name,
            "doctorName": apt.doctor_name,
            "date": str(apt.date),
            "time": apt.time,
            "type": apt.type,
            "status": apt.status,
            "reason": apt.reason,
            "department": apt.department,
            "patientId": apt.patient_id,
            "doctorId": apt.doctor_id,
            "patientPhone": apt.patient_phone,
            "bookingSource": apt.booking_source
        })
    
    return {
        "success": True,
        "data": formatted_appointments
    }

class StatusUpdate(BaseModel):
    status: str

from pydantic import BaseModel

@router.put("/{appointment_id}/status")
def update_appointment_status(
    appointment_id: int, 
    status_update: StatusUpdate,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appointment.status = status_update.status
    db.commit()
    return {"success": True, "message": "Status updated"}

@router.post("/")
def create_appointment(appointment_data: dict, db: Session = Depends(get_db)):
    try:
        new_appointment = Appointment(**appointment_data)
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)
        return {"success": True, "data": new_appointment}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
