from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db, Appointment
from datetime import datetime
import pytz
from whatsapp_bot.config import config

router = APIRouter(tags=["Queue"])

@router.get("")
def get_queue(db: Session = Depends(get_db)):
    # Get today's date in local timezone
    tz = pytz.timezone(config.TIMEZONE)
    today = datetime.now(tz).date()
    
    # Get all active appointments for today
    # Filter by date and status (exclude cancelled/completed for queue view if desired, but frontend filters too)
    # Frontend seems to show all in queue list, or maybe just active?
    # Based on Dashboard.jsx, it shows "Current Queue".
    
    query = db.query(Appointment).filter(
        Appointment.date == today,
        Appointment.status.in_(["Booked", "Checked In", "In Consultation"])
    )
    
    appointments = query.all()
    
    formatted_queue = []
    for apt in appointments:
        formatted_queue.append({
            "id": apt.id,
            "patient": {
                "name": apt.patient_name,
                "mobile": apt.patient_phone
            },
            "doctor": {
                "name": apt.doctor_name,
                "department": apt.department
            },
            "slotStartTime": apt.time,
            "status": apt.status,
            "source": apt.booking_source,
            "waitingTime": 0 # Placeholder implementation
        })
        
    return {
        "success": True,
        "data": formatted_queue
    }
