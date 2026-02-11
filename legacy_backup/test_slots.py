from doctor_service import doctor_service
from datetime import datetime

# Test for Dr. Michael Chen on Tuesday (2026-02-10)
doctor_id = 'dr_002'
date = '2026-02-10'

doctor = doctor_service.get_doctor_by_id(doctor_id)
print(f"Doctor: {doctor['name']}")
print(f"Specialization: {doctor['specialization']}")
print(f"Working days: {doctor['working_days']}")
print(f"Date: {date} ({datetime.strptime(date, '%Y-%m-%d').strftime('%A')})")
print()

slots = doctor_service.get_available_slots(doctor_id, date, [])
print(f"Available slots: {len(slots)}")
if slots:
    print(f"First 5 slots: {slots[:5]}")
else:
    print("No slots available")
