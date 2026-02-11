from sqlalchemy.orm import Session
from database import SessionLocal, Doctor
from typing import List, Dict, Any, Optional

class DoctorService:
    def get_all_doctors(self) -> List[Dict[str, Any]]:
        """Get all doctors from DB formatted for WhatsApp Bot"""
        db: Session = SessionLocal()
        try:
            doctors_db = db.query(Doctor).all()
            return [self._format_doctor(d) for d in doctors_db]
        finally:
            db.close()
    
    def get_doctors_by_specialization(self, specialization: str) -> List[Dict[str, Any]]:
        """Get doctors by specialization"""
        db: Session = SessionLocal()
        try:
            doctors_db = db.query(Doctor).filter(Doctor.specialization == specialization).all()
            return [self._format_doctor(d) for d in doctors_db]
        finally:
            db.close()
            
    def get_doctor_by_id(self, doctor_id: str) -> Optional[Dict[str, Any]]:
        """Get doctor by ID"""
        db: Session = SessionLocal()
        try:
            # Handle string vs int ID
            # If ID comes as "dr_001", we might need to parse or map it.
            # But the Database IDs are integers.
            # Let's assume we pass IDs as strings of integers "1", "2".
            
            if not str(doctor_id).isdigit():
                return None
                
            d = db.query(Doctor).filter(Doctor.id == int(doctor_id)).first()
            return self._format_doctor(d) if d else None
        finally:
            db.close()
    
    def get_all_specializations(self) -> List[str]:
        """Get unique specializations"""
        db: Session = SessionLocal()
        try:
            # Query distinct specializations
            specs = db.query(Doctor.specialization).distinct().all()
            return [s[0] for s in specs]
        finally:
            db.close()

    def get_available_slots(self, doctor_id: str, date: str, booked_appointments: List = None) -> List[str]:
        """Calculate available slots for a doctor"""
        doctor = self.get_doctor_by_id(doctor_id)
        if not doctor:
            return []
            
        start_time = doctor["working_hours"]["start"]
        end_time = doctor["working_hours"]["end"]
        slot_duration = doctor["slot_duration_minutes"]
        
        # Generate all slots
        time_slots = []
        from datetime import datetime, timedelta
        
        current = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")
        
        while current < end:
            time_slots.append(current.strftime("%H:%M"))
            current += timedelta(minutes=slot_duration)
            
        # Filter booked slots
        if booked_appointments:
            booked_times = {apt['time'] for apt in booked_appointments}
            time_slots = [t for t in time_slots if t not in booked_times]
            
        return time_slots

    def _format_doctor(self, doctor_db: Doctor) -> Dict[str, Any]:
        """Format DB model to dictionary expected by Bot"""
        return {
            "id": str(doctor_db.id),
            "name": doctor_db.name,
            "specialization": doctor_db.specialization,
            "google_calendar_id": doctor_db.google_calendar_id,
            "working_hours": {
                "start": doctor_db.working_hours_start,
                "end": doctor_db.working_hours_end
            },
            "working_days": doctor_db.working_days.split(",") if doctor_db.working_days else [],
            "slot_duration_minutes": doctor_db.slot_duration_minutes
        }

doctor_service = DoctorService()
