from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Doctor, Patient, Appointment

router = APIRouter(tags=["Dashboard"])

@router.get("")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Generate dashboard data from database counts"""
    try:
        # Get actual counts from database
        total_doctors = db.query(Doctor).count()
        total_patients = db.query(Patient).count()
        total_appointments = db.query(Appointment).count()
        
        # Calculate statistics from actual data
        available_doctors = db.query(Doctor).filter(Doctor.status == "Available").count()
        completed_appointments = db.query(Appointment).filter(Appointment.status == "Completed").count()
        cancelled_appointments = db.query(Appointment).filter(Appointment.status == "Cancelled").count()
        rescheduled_appointments = db.query(Appointment).filter(Appointment.status == "Rescheduled").count()
        
        # Monthly data (empty if no data)
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]
        monthly_data = []
        for month in months:
            monthly_data.append({
                "month": month,
                "completed": 0,
                "ongoing": 0,
                "rescheduled": 0
            })
        
        return {
            "summary": {
                "doctors": {
                    "count": total_doctors,
                    "change": "0%",
                    "period": "in last 7 Days"
                },
                "patients": {
                    "count": total_patients,
                    "change": "0%",
                    "period": "in last 7 Days"
                },
                "appointments": {
                    "count": total_appointments,
                    "change": "0%",
                    "period": "in last 7 Days"
                },
                "revenue": {
                    "amount": "$0",
                    "change": "0%",
                    "period": "in last 7 Days"
                }
            },
            "appointmentStats": {
                "total": total_appointments,
                "cancelled": cancelled_appointments,
                "rescheduled": rescheduled_appointments,
                "completed": completed_appointments,
                "walkIn": 0
            },
            "monthlyData": monthly_data
        }
    except Exception as e:
        print(f"Error generating dashboard data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
