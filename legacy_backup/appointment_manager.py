import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
import random
import string

DATA_DIR = "data"
APPOINTMENTS_FILE = os.path.join(DATA_DIR, "appointments.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(APPOINTMENTS_FILE):
    with open(APPOINTMENTS_FILE, 'w') as f:
        json.dump([], f)

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
    
    def load_appointments(self) -> List[Dict[str, Any]]:
        """Load appointments from file"""
        try:
            with open(APPOINTMENTS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_appointments(self, appointments: List[Dict[str, Any]]):
        """Save appointments to file"""
        with open(APPOINTMENTS_FILE, 'w') as f:
            json.dump(appointments, f, indent=2)
    
    def create_appointment(self, user_id: str, user_name: str, doctor_id: str, doctor_name: str, 
                          specialization: str, date: str, time: str) -> Dict[str, Any]:
        """Create a new appointment with doctor information"""
        appointments = self.load_appointments()
        
        appointment_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))
        
        new_appointment = {
            "id": appointment_id,
            "userId": user_id,
            "userName": user_name,
            "doctorId": doctor_id,
            "doctorName": doctor_name,
            "specialization": specialization,
            "date": date,
            "time": time,
            "status": "confirmed",
            "createdAt": datetime.utcnow().isoformat() + "Z"
        }
        
        appointments.append(new_appointment)
        self.save_appointments(appointments)
        
        return new_appointment
    
    def check_availability(self, doctor_id: str, date: str, time: str) -> bool:
        """Check if a doctor is available at specific date and time"""
        appointments = self.load_appointments()
        for apt in appointments:
            if (apt.get("doctorId") == doctor_id and 
                apt["date"] == date and 
                apt["time"] == time and 
                apt["status"] == "confirmed"):
                return False
        return True
    
    def get_doctor_appointments(self, doctor_id: str, date: str) -> List[Dict[str, Any]]:
        """Get all appointments for a doctor on a specific date"""
        appointments = self.load_appointments()
        return [apt for apt in appointments 
                if apt.get("doctorId") == doctor_id and 
                apt["date"] == date and 
                apt["status"] == "confirmed"]
    
    def cancel_appointment(self, appointment_id: str) -> bool:
        """Cancel an appointment"""
        appointments = self.load_appointments()
        for apt in appointments:
            if apt["id"] == appointment_id:
                apt["status"] = "cancelled"
                self.save_appointments(appointments)
                return True
        return False
    
    def get_user_appointments(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all appointments for a user"""
        appointments = self.load_appointments()
        return [apt for apt in appointments 
                if apt["userId"] == user_id and 
                apt["status"] == "confirmed"]

appointment_manager = AppointmentManager()
