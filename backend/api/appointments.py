from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Appointment, Doctor
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(tags=["Appointments"])

@router.get("")
def get_appointments(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    date: Optional[str] = None,
    doctorId: Optional[str] = None,
    db: Session = Depends(get_db)
):
    print(f">>> GET APPOINTMENTS CALLED params: status={status}, date={date}, doctorId={doctorId}")
    query = db.query(Appointment)
    
    if status and status != "All Statuses":
        if ',' in status:
            status_list = [s.strip() for s in status.split(',')]
            query = query.filter(Appointment.status.in_(status_list))
        else:
            query = query.filter(Appointment.status == status)
    
    if date:
        from datetime import datetime
        try:
            # Frontend sends YYYY-MM-DD
            filter_date = datetime.strptime(date, "%Y-%m-%d").date()
            query = query.filter(Appointment.date == filter_date)
        except ValueError:
            pass # Ignore invalid date format

    if doctorId:
        query = query.filter(Appointment.doctor_id == int(doctorId))
    
    total = query.count()
    appointments_db = query.offset(skip).limit(limit).all()
    
    # Format to camelCase for frontend
    formatted_appointments = []
    for apt in appointments_db:
        formatted_appointments.append({
            "id": apt.id,
            "patient": {
                "name": apt.patient_name,
                "mobile": apt.patient_phone or "N/A"
            },
            "doctor": {
                "name": apt.doctor_name,
                "department": apt.department
            },
            "appointmentDate": str(apt.date),
            "slotStartTime": apt.time,
            "type": apt.type,
            "status": apt.status,
            "reasonForVisit": apt.reason,
            "source": apt.booking_source or "Dashboard"
        })
    
    return {
        "success": True,
        "data": formatted_appointments
    }

class StatusUpdate(BaseModel):
    status: str



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

from database import get_db, Appointment, Doctor

# ... existing code ...

class AppointmentCreate(BaseModel):
    patient_name: str
    patient_phone: str
    doctor_id: int
    date: str
    time: str
    reason: Optional[str] = None
    status: str = "Booked"

@router.post("")
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    try:
        # Fetch doctor details automatically
        doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        from datetime import datetime
        
        new_appointment = Appointment(
            patient_name=appointment.patient_name,
            patient_phone=appointment.patient_phone,
            doctor_id=appointment.doctor_id,
            doctor_name=doctor.name,
            department=doctor.specialization,
            date=datetime.strptime(appointment.date, "%Y-%m-%d").date(),
            time=appointment.time,
            reason=appointment.reason,
            status=appointment.status,
            type="Scheduled",
            booking_source="Dashboard"
        )

        # Validate appointment time is not in the past
        appointment_datetime = datetime.combine(new_appointment.date, datetime.strptime(new_appointment.time, "%H:%M").time())
        if appointment_datetime < datetime.now():
            raise HTTPException(status_code=400, detail="Cannot book appointments in the past")
        
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)

        # Sync to Google Calendar
        try:
            from whatsapp_bot.google_calendar_service import google_calendar_service
            # Use doctor's specific calendar ID if available, otherwise fallback to 'primary'
            calendar_id = doctor.google_calendar_id if doctor.google_calendar_id else 'primary'
            
            google_calendar_service.create_appointment(
                calendar_id=calendar_id,
                patient_name=new_appointment.patient_name,
                patient_phone=new_appointment.patient_phone,
                doctor_name=new_appointment.doctor_name,
                date=str(new_appointment.date),
                time=new_appointment.time
            )
            print(f"Appointment synced to Google Calendar ({calendar_id})")
        except Exception as e:
            print(f"Failed to sync to Google Calendar: {e}")
            # We do NOT rollback the DB transaction here because the appointment IS created in our system.
            # In a production system, we might want a background job to retry sync.
            
        # Send WhatsApp Confirmation Template
        try:
            from whatsapp_bot.whatsapp_client import whatsapp_client
            from whatsapp_bot.templates import WhatsAppTemplates

            if new_appointment.patient_phone:
                components = WhatsAppTemplates.get_confirmation_components(
                    patient_name=new_appointment.patient_name,
                    doctor_name=new_appointment.doctor_name,
                    date=new_appointment.date,
                    time=new_appointment.time
                )
                whatsapp_client.send_template(
                    to=new_appointment.patient_phone,
                    template_name=WhatsAppTemplates.APPOINTMENT_CONFIRMATION,
                    components=components
                )
                print(f"WhatsApp confirmation sent to {new_appointment.patient_phone}")
        except Exception as e:
            print(f"Failed to send WhatsApp confirmation: {e}")

        return {"success": True, "data": new_appointment, "message": "Appointment created successfully"}
    except Exception as e:
        db.rollback()
        print(f"Error creating appointment: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{appointment_id}/remind")
def send_appointment_reminder(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    if not appointment.patient_phone:
        raise HTTPException(status_code=400, detail="Patient has no phone number")
        
    try:
        from whatsapp_bot.whatsapp_client import whatsapp_client
        from whatsapp_bot.templates import WhatsAppTemplates
        
        components = WhatsAppTemplates.get_reminder_components(
            patient_name=appointment.patient_name,
            doctor_name=appointment.doctor_name,
            time=f"{appointment.date} at {appointment.time}"
        )
        
        whatsapp_client.send_template(
            to=appointment.patient_phone,
            template_name=WhatsAppTemplates.APPOINTMENT_REMINDER,
            components=components
        )
        
        return {"success": True, "message": "Reminder sent successfully"}
    except Exception as e:
        print(f"Error sending reminder: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send reminder: {str(e)}")
