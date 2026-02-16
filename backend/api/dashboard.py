from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Doctor, Patient, Appointment
from datetime import datetime, date

router = APIRouter(tags=["Dashboard"])

@router.get("/summary")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Generate dashboard data from database counts for TODAY only"""
    try:
        # Get today's date
        today = date.today()
        
        # Get actual counts from database
        total_doctors = db.query(Doctor).count()
        total_patients = db.query(Patient).count()
        
        # Filter appointments by today's date
        total_appointments = db.query(Appointment).filter(Appointment.appointment_date == today).count()
        
        # Calculate statistics from actual data (TODAY only)
        available_doctors = db.query(Doctor).filter(Doctor.status == "Available").count()
        completed = db.query(Appointment).filter(Appointment.appointment_date == today, Appointment.status == "Completed").count()
        cancelled = db.query(Appointment).filter(Appointment.appointment_date == today, Appointment.status == "Cancelled").count()
        rescheduled = db.query(Appointment).filter(Appointment.appointment_date == today, Appointment.status == "Rescheduled").count()
        booked = db.query(Appointment).filter(Appointment.appointment_date == today, Appointment.status == "Booked").count()
        checked_in = db.query(Appointment).filter(Appointment.appointment_date == today, Appointment.status == "Checked In").count()
        in_consultation = db.query(Appointment).filter(Appointment.appointment_date == today, Appointment.status == "In Consultation").count()
        no_show = db.query(Appointment).filter(Appointment.appointment_date == today, Appointment.status == "No Show").count()
        
        # Doctor Summary (Group by doctor) - TODAY only
        doctors = db.query(Doctor).all()
        doctor_summary = []
        for doc in doctors:
            doc_appts = db.query(Appointment).filter(Appointment.doctor_id == doc.id, Appointment.appointment_date == today).count()
            doc_completed = db.query(Appointment).filter(Appointment.doctor_id == doc.id, Appointment.appointment_date == today, Appointment.status == "Completed").count()
            doc_waiting = db.query(Appointment).filter(Appointment.doctor_id == doc.id, Appointment.appointment_date == today, Appointment.status.in_(["Booked", "Checked In"])).count()
            
            doctor_summary.append({
                "doctorId": doc.id,
                "doctor": {
                    "name": doc.name,
                    "department": doc.specialization
                },
                "totalAppointments": doc_appts,
                "completed": doc_completed,
                "waiting": doc_waiting
            })

        return {
            "success": True,
            "data": {
                "summary": {
                    "total": total_appointments,
                    "completed": completed,
                    "cancelled": cancelled,
                    "booked": booked,
                    "checkedIn": checked_in,
                    "inConsultation": in_consultation,
                    "noShow": no_show,
                    "doctors": total_doctors,
                    "patients": total_patients
                },
                "doctorSummary": doctor_summary
            }
        }
    except Exception as e:
        print(f"Error generating dashboard data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
