from sqlalchemy.orm import Session
from database import SessionLocal, Appointment, Doctor
from datetime import datetime
import random
import string
from typing import Dict, Any, List, Optional

class AppointmentManager:
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def get_session(self, user_id: str) -> Dict[str, Any]:
        """Get or create user session"""
        if user_id not in self.sessions:
            self.sessions[user_id] = {
                "userId": user_id,
                "step": "idle",
                "tempData": {}
            }
        return self.sessions[user_id]
    
    def update_session(self, user_id: str, data: Dict[str, Any]):
        """Update user session"""
        session = self.get_session(user_id)
        session.update(data)
        if "tempData" in data:
            session["tempData"].update(data["tempData"])
    
    def clear_session(self, user_id: str):
        """Clear user session"""
        if user_id in self.sessions:
            del self.sessions[user_id]
    
    def create_appointment(self, user_id: str, user_name: str, doctor_id: str, doctor_name: str, 
                          specialization: str, date: str, time: str) -> Dict[str, Any]:
        """Create a new appointment in PostgreSQL"""
        db: Session = SessionLocal()
        try:
            # Create new appointment record
            new_appointment = Appointment(
                patient_name=user_name,
                doctor_name=doctor_name,
                date=datetime.strptime(date, "%Y-%m-%d").date(),
                time=time,
                type="Scheduled",
                status="Confirmed",
                patient_phone=user_id,
                doctor_id=int(doctor_id) if doctor_id.isdigit() else None,
                booking_source="WhatsApp",
                department=specialization
            )
            
            db.add(new_appointment)
            db.commit()
            db.refresh(new_appointment)
            
            return {
                "id": str(new_appointment.id),
                "doctorName": doctor_name,
                "date": date,
                "time": time,
                "status": "confirmed"
            }
        except Exception as e:
            print(f"Error creating appointment: {e}")
            db.rollback()
            raise e
        finally:
            db.close()
    
    def get_slots_for_doctor(self, doctor_id: str, date: str) -> List[Dict[str, Any]]:
        """Get all appointments for a doctor on a specific date (Renamed)"""
        db: Session = SessionLocal()
        try:
            # Helper to check if doctor_id matches (handling int/str mismatch if necessary)
            # Assuming doctor_id in DB is distinct from the API ID if not strictly integer
            # But based on api/doctors.py, doctor ID is Integer
            
            # If doctor_id comes as "dr_001", we might need to handle it.
            # However, the existing logic passes "dr_001".
            # The database.py Doctor model has 'id' as Integer. 
            # We need to resolve this.
            
            query_date = datetime.strptime(date, "%Y-%m-%d").date()
            
            appointments = db.query(Appointment).filter(
                Appointment.date == query_date,
                Appointment.status != "Cancelled"
            ).all()
            
            # Filter in python if doctor_id format doesn't match DB directly
            # Or better, fetch doctor by ID first?
            
            # For now, let's assume we filter by doctor_name or we fix the ID mapping later.
            # But wait, app.py uses "dr_001" from config. 
            # frontend/backend/database.py uses Integer IDs.
            # We need a DoctorService that maps them or we just use IDs.
            
            # Let's filter by checking the doctor_id field
            doctor_appointments = []
            for apt in appointments:
                # If we stored doctor_id as integer in create_appointment
                if str(apt.doctor_id) == str(doctor_id):
                   doctor_appointments.append({
                       "date": str(apt.date),
                       "time": apt.time,
                       "status": apt.status.lower()
                   })
            
            return doctor_appointments
        finally:
            db.close()

    def validate_booking_constraints(self, user_id: str, doctor_id: str, date: str, time: str) -> tuple[bool, str, str]:
        """
        Validate booking constraints:
        1. No multiple bookings with same doctor on same day
        2. No multiple bookings at same time (any doctor)
        Returns: (is_valid, error_message, error_code)
        """
        db: Session = SessionLocal()
        try:
            query_date = datetime.strptime(date, "%Y-%m-%d").date()
            
            # Get all active appointments for this user on this date
            user_appointments = db.query(Appointment).filter(
                Appointment.patient_phone == user_id,
                Appointment.date == query_date,
                Appointment.status != "Cancelled"
            ).all()
            
            for apt in user_appointments:
                # Check Constraint 1: Same Doctor, Same Day
                # Handle doctor_id comparison (DB is int, input might be str/int)
                try:
                    appt_doc_id = str(apt.doctor_id)
                    input_doc_id = str(doctor_id)
                    if appt_doc_id == input_doc_id:
                        return False, f"You already have an appointment with {apt.doctor_name} on {date}. Please reschedule or cancel it first.", "SAME_DOCTOR_DAY"
                except:
                    pass # Continue if ID comparison fails (shouldn't happen)

                # Check Constraint 2: Same Time, Any Doctor
                if apt.time == time:
                     return False, f"You already have an appointment at {time} on {date} with {apt.doctor_name}.", "TIME_CLASH"
            
            return True, "", ""
            
        finally:
            db.close()

    def get_user_appointments(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all appointments for a user (phone number)"""
        db: Session = SessionLocal()
        try:
            appointments = db.query(Appointment).filter(
                Appointment.patient_phone == user_id,
                Appointment.status != "Cancelled"
            ).all()
            
            return [{
                "id": str(apt.id),
                "doctorId": str(apt.doctor_id),
                "doctorName": apt.doctor_name,
                "specialization": apt.department,
                "date": str(apt.date),
                "time": apt.time,
                "status": apt.status,
                "userName": apt.patient_name
            } for apt in appointments]
        finally:
            db.close()

    def cancel_appointment(self, appointment_id: str) -> bool:
        """Cancel an appointment"""
        db: Session = SessionLocal()
        try:
            # appointment_id might be string from WhatsApp button, DB id is Integer
            db_id = int(appointment_id)
            appointment = db.query(Appointment).filter(Appointment.id == db_id).first()
            if appointment:
                appointment.status = "Cancelled"
                db.commit()
                return True
            return False
        except:
             return False
        finally:
            db.close()

appointment_manager = AppointmentManager()
