import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os

class DoctorService:
    def __init__(self):
        self.doctors = []
        self.load_doctors()
    
    def load_doctors(self):
        """Load doctor configurations from JSON file"""
        config_path = os.path.join(os.path.dirname(__file__), 'doctors_config.json')
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
                self.doctors = data.get('doctors', [])
                print(f"Loaded {len(self.doctors)} doctors")
        except FileNotFoundError:
            print("doctors_config.json not found. No doctors loaded.")
            self.doctors = []
    
    def get_all_doctors(self) -> List[Dict]:
        """Get list of all doctors"""
        return self.doctors
    
    def get_doctor_by_id(self, doctor_id: str) -> Optional[Dict]:
        """Get doctor by ID"""
        for doctor in self.doctors:
            if doctor['id'] == doctor_id:
                return doctor
        return None
    
    def get_doctors_by_specialization(self, specialization: str) -> List[Dict]:
        """Get doctors by specialization"""
        return [d for d in self.doctors if d['specialization'].lower() == specialization.lower()]
    
    def get_all_specializations(self) -> List[str]:
        """Get unique list of specializations"""
        return list(set(d['specialization'] for d in self.doctors))
    
    def is_doctor_available(self, doctor_id: str, date_str: str, time_str: str) -> bool:
        """Check if doctor is available at given date and time"""
        doctor = self.get_doctor_by_id(doctor_id)
        if not doctor:
            return False
        
        try:
            # Parse date and time
            appointment_date = datetime.strptime(date_str, "%Y-%m-%d")
            appointment_time = datetime.strptime(time_str, "%H:%M").time()
            
            # Check if day is in working days
            day_name = appointment_date.strftime("%A")
            if day_name not in doctor['working_days']:
                return False
            
            # Check if time is within working hours
            work_start = datetime.strptime(doctor['working_hours']['start'], "%H:%M").time()
            work_end = datetime.strptime(doctor['working_hours']['end'], "%H:%M").time()
            
            if not (work_start <= appointment_time < work_end):
                return False
            
            # Check if time is during break
            break_start = datetime.strptime(doctor['break_time']['start'], "%H:%M").time()
            break_end = datetime.strptime(doctor['break_time']['end'], "%H:%M").time()
            
            if break_start <= appointment_time < break_end:
                return False
            
            return True
            
        except Exception as e:
            print(f"Error checking availability: {e}")
            return False
    
    def get_available_slots(self, doctor_id: str, date_str: str, booked_appointments: List[Dict] = None) -> List[str]:
        """Get available time slots for a doctor on a specific date"""
        doctor = self.get_doctor_by_id(doctor_id)
        if not doctor:
            return []
        
        try:
            appointment_date = datetime.strptime(date_str, "%Y-%m-%d")
            day_name = appointment_date.strftime("%A")
            
            # Check if doctor works on this day
            if day_name not in doctor['working_days']:
                print(f"Doctor {doctor['name']} doesn't work on {day_name}")
                return []
            
            # Get current time for filtering past slots
            from datetime import datetime as dt
            import pytz
            timezone = pytz.timezone('Asia/Kolkata')  # Use your timezone
            current_datetime = dt.now(timezone)
            is_today = appointment_date.date() == current_datetime.date()
            
            # Generate all possible slots
            work_start = datetime.strptime(doctor['working_hours']['start'], "%H:%M")
            work_end = datetime.strptime(doctor['working_hours']['end'], "%H:%M")
            
            # Check for break time (optional)
            has_break = 'break_time' in doctor
            if has_break:
                break_start = datetime.strptime(doctor['break_time']['start'], "%H:%M")
                break_end = datetime.strptime(doctor['break_time']['end'], "%H:%M")
            
            slot_duration = timedelta(minutes=doctor['slot_duration_minutes'])
            
            slots = []
            current_time = work_start
            
            while current_time < work_end:
                # Skip break time if exists
                if has_break and (break_start <= current_time < break_end):
                    current_time += slot_duration
                    continue
                
                time_str = current_time.strftime("%H:%M")
                
                # Skip past time slots if booking for today
                if is_today:
                    slot_hour, slot_minute = map(int, time_str.split(':'))
                    if (slot_hour < current_datetime.hour or 
                        (slot_hour == current_datetime.hour and slot_minute <= current_datetime.minute)):
                        current_time += slot_duration
                        continue
                
                # Check if slot is already booked
                is_booked = False
                if booked_appointments:
                    for apt in booked_appointments:
                        if apt.get('time') == time_str:
                            is_booked = True
                            break
                
                if not is_booked:
                    slots.append(time_str)
                
                current_time += slot_duration
            
            print(f"Generated {len(slots)} slots for {doctor['name']} on {date_str} ({day_name})")
            return slots
            
        except Exception as e:
            print(f"Error getting available slots: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_specializations(self) -> List[str]:
        """Get list of unique specializations"""
        specializations = list(set(doctor['specialization'] for doctor in self.doctors))
        return sorted(specializations)
    
    def get_doctors_by_specialization(self, specialization: str) -> List[Dict]:
        """Get all doctors with a specific specialization"""
        return [doctor for doctor in self.doctors if doctor['specialization'] == specialization]
    
    def format_doctor_list(self) -> str:
        """Format doctor list for display"""
        if not self.doctors:
            return "No doctors available."
        
        result = "📋 *Available Doctors:*\n\n"
        for i, doctor in enumerate(self.doctors, 1):
            result += f"{i}. *{doctor['name']}* - {doctor['specialization']}\n"
            days = ", ".join(doctor['working_days'][:3])  # Show first 3 days
            if len(doctor['working_days']) > 3:
                days += "..."
            result += f"   Available: {days}\n\n"
        
        return result
    
    def format_specializations(self) -> str:
        """Format specializations for display"""
        specs = self.get_all_specializations()
        if not specs:
            return "No specializations available."
        
        result = "🏥 *Select Specialization:*\n\n"
        for i, spec in enumerate(sorted(specs), 1):
            result += f"{i}. {spec}\n"
        
        return result

# Singleton instance
doctor_service = DoctorService()
