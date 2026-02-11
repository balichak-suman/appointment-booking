from datetime import datetime, timedelta
from typing import List, Dict, Optional
from database import SessionLocal, Doctor, Appointment

class DoctorService:
    def __init__(self):
        # We'll fetch from DB dynamically instead of caching forever
        pass
    
    def get_all_doctors(self) -> List[Dict]:
        """Get list of all doctors from DB"""
        db = SessionLocal()
        try:
            doctors = db.query(Doctor).all()
            return [self._format_doctor(d) for d in doctors]
        finally:
            db.close()
    
    def _format_doctor(self, doc: Doctor) -> Dict:
        """Format DB doctor object to dictionary expected by bot"""
        return {
            'id': f"dr_{str(doc.id).zfill(3)}",
            'db_id': doc.id,
            'name': doc.name,
            'specialization': doc.specialization,
            'status': doc.status,
            'working_hours': {
                'start': doc.working_hours_start,
                'end': doc.working_hours_end
            },
            'working_days': doc.working_days.split(',') if doc.working_days else [],
            'slot_duration_minutes': doc.slot_duration_minutes,
            'google_calendar_id': doc.google_calendar_id,
            'break_time': {'start': '13:00', 'end': '14:00'} # Default
        }
    
    def get_doctor_by_id(self, doctor_id: str) -> Optional[Dict]:
        """Get doctor by ID from DB"""
        db = SessionLocal()
        try:
            # Extract numeric ID if format is dr_001
            try:
                numeric_id = int(doctor_id.replace("dr_", ""))
            except:
                numeric_id = doctor_id
                
            doc = db.query(Doctor).filter(Doctor.id == numeric_id).first()
            return self._format_doctor(doc) if doc else None
        finally:
            db.close()
    
    def get_doctors_by_specialization(self, specialization: str) -> List[Dict]:
        """Get doctors by specialization from DB"""
        db = SessionLocal()
        try:
            doctors = db.query(Doctor).filter(Doctor.specialization == specialization).all()
            return [self._format_doctor(d) for d in doctors]
        finally:
            db.close()
    
    def get_all_specializations(self) -> List[str]:
        """Get unique list of specializations from DB"""
        db = SessionLocal()
        try:
            specializations = db.query(Doctor.specialization).distinct().all()
            return sorted([s[0] for s in specializations if s[0]])
        finally:
            db.close()
    
    def get_available_slots(self, doctor_id: str, date_str: str, booked_appointments: List[Dict] = None) -> List[str]:
        """Get available time slots for a doctor on a specific date using DB data"""
        doctor = self.get_doctor_by_id(doctor_id)
        if not doctor:
            return []
        
        try:
            appointment_date = datetime.strptime(date_str, "%Y-%m-%d")
            day_name = appointment_date.strftime("%A")
            
            # Check if doctor works on this day
            if day_name not in doctor['working_days']:
                return []
            
            # Fetch booked appointments from DB if not provided
            if booked_appointments is None:
                db = SessionLocal()
                try:
                    numeric_id = int(doctor_id.replace("dr_", ""))
                    apts = db.query(Appointment).filter(
                        Appointment.doctor_id == numeric_id,
                        Appointment.date == appointment_date.date(),
                        Appointment.status == "Scheduled"
                    ).all()
                    booked_appointments = [{'time': a.time} for a in apts]
                finally:
                    db.close()

            # Get current time for filtering
            now = datetime.now()
            is_today = appointment_date.date() == now.date()
            
            # Generate slots
            work_start = datetime.strptime(doctor['working_hours']['start'], "%H:%M")
            work_end = datetime.strptime(doctor['working_hours']['end'], "%H:%M")
            slot_duration = timedelta(minutes=doctor['slot_duration_minutes'])
            
            break_start = datetime.strptime(doctor['break_time']['start'], "%H:%M")
            break_end = datetime.strptime(doctor['break_time']['end'], "%H:%M")
            
            slots = []
            current_time = work_start
            
            while current_time < work_end:
                # Skip break
                if break_start <= current_time < break_end:
                    current_time += slot_duration
                    continue
                
                time_str = current_time.strftime("%H:%M")
                
                # Skip past slots
                if is_today:
                    if current_time.hour < now.hour or (current_time.hour == now.hour and current_time.minute <= now.minute):
                        current_time += slot_duration
                        continue
                
                # Check bookings
                if not any(a['time'] == time_str for a in booked_appointments):
                    slots.append(time_str)
                
                current_time += slot_duration
                
            return slots
        except Exception as e:
            print(f"Error getting slots: {e}")
            return []

doctor_service = DoctorService()
