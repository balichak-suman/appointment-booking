import os
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

# Import models from the main database module
from database import SessionLocal, Appointment, Doctor, Patient

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
                          specialization: str, date: str, time: str, reason: str = "WhatsApp Booking") -> Dict[str, Any]:
        """Create a new appointment in PostgreSQL"""
        db = SessionLocal()
        try:
            # Format date string to date object
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            
            # Clean doctor_id (remove 'dr_' prefix if exists)
            numeric_doctor_id = None
            if doctor_id and isinstance(doctor_id, str) and doctor_id.startswith('dr_'):
                try:
                    numeric_doctor_id = int(doctor_id.replace('dr_', ''))
                except: pass
            elif doctor_id:
                try:
                    numeric_doctor_id = int(doctor_id)
                except: pass

            # 1. Create/Update Patient Record
            patient = db.query(Patient).filter(Patient.phone == user_id).first()
            if not patient:
                # Need unique email for the dashboard model
                patient = Patient(
                    name=user_name,
                    phone=user_id,
                    whatsapp_number=user_id,
                    email=f"{user_id}@whatsapp.com",
                    last_visit=date_obj,
                    status="Active",
                    age=30, # Default for model
                    gender="Not Specified" # Default for model
                )
                db.add(patient)
            else:
                patient.last_visit = date_obj
                patient.name = user_name # Keep name updated
            
            db.flush() # Get patient ID
            
            # 2. Create Appointment
            new_apt = Appointment(
                patient_name=user_name,
                doctor_name=doctor_name,
                date=date_obj,
                time=time,
                type="Scheduled",
                status="Scheduled",
                reason=reason,
                department=specialization,
                doctor_id=numeric_doctor_id,
                patient_id=patient.id, # Link to patient
                patient_phone=user_id,
                booking_source="WhatsApp"
            )
            
            db.add(new_apt)
            db.commit()
            db.refresh(new_apt)
            
            return {
                "id": str(new_apt.id),
                "userId": user_id,
                "userName": user_name,
                "doctorId": doctor_id,
                "doctorName": doctor_name,
                "specialization": specialization,
                "date": date,
                "time": time,
                "status": "confirmed"
            }
        finally:
            db.close()
    
    def check_availability(self, doctor_id: str, date: str, time: str) -> bool:
        """Check if a doctor is available in PostgreSQL"""
        db = SessionLocal()
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            
            numeric_doctor_id = None
            if doctor_id and isinstance(doctor_id, str) and doctor_id.startswith('dr_'):
                try:
                    numeric_doctor_id = int(doctor_id.replace('dr_', ''))
                except: pass
            
            query = db.query(Appointment).filter(
                Appointment.date == date_obj,
                Appointment.time == time,
                Appointment.status == "Scheduled"
            )
            
            if numeric_doctor_id:
                query = query.filter(Appointment.doctor_id == numeric_doctor_id)
            else:
                query = query.filter(Appointment.doctor_name == doctor_id) # Fallback
                
            existing = query.first()
            return existing is None
        finally:
            db.close()
    
    def get_user_appointments(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all appointments for a user from PostgreSQL"""
        db = SessionLocal()
        try:
            appointments = db.query(Appointment).filter(
                Appointment.patient_phone == user_id,
                Appointment.status == "Scheduled"
            ).all()
            
            return [
                {
                    "id": str(apt.id),
                    "doctorName": apt.doctor_name,
                    "doctorId": f"dr_{str(apt.doctor_id).zfill(3)}" if apt.doctor_id else None,
                    "specialization": apt.department,
                    "date": str(apt.date),
                    "time": apt.time,
                    "status": "confirmed"
                } for apt in appointments
            ]
        finally:
            db.close()

    def cancel_appointment(self, appointment_id: str) -> bool:
        """Cancel an appointment in PostgreSQL"""
        db = SessionLocal()
        try:
            apt = db.query(Appointment).filter(Appointment.id == int(appointment_id)).first()
            if apt:
                apt.status = "Cancelled"
                apt.updated_at = datetime.utcnow()
                db.commit()
                return True
            return False
        except:
            return False
        finally:
            db.close()

appointment_manager = AppointmentManager()
