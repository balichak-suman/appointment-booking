import json
import os
from database import SessionLocal, Doctor

def seed_doctors_from_json():
    config_path = os.path.join(os.path.dirname(__file__), "doctors_config.json")
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found")
        return

    with open(config_path, 'r') as f:
        data = json.load(f)
        doctors_json = data.get('doctors', [])

    db = SessionLocal()
    try:
        # Get existing doctor names to avoid duplicates
        existing_names = [d.name for d in db.query(Doctor).all()]
        
        added_count = 0
        for doc_data in doctors_json:
            if doc_data['name'] not in existing_names:
                # Map JSON fields to database fields
                # Ensure id is numeric (dr_001 -> 1)
                numeric_id = int(doc_data['id'].replace("dr_", ""))
                
                new_doctor = Doctor(
                    id=numeric_id,
                    name=doc_data['name'],
                    specialization=doc_data['specialization'],
                    email=doc_data['name'].lower().replace(" ", ".") + "@hospital.com",
                    status="Available",
                    working_hours_start=doc_data['working_hours']['start'],
                    working_hours_end=doc_data['working_hours']['end'],
                    working_days=",".join(doc_data['working_days']),
                    slot_duration_minutes=doc_data['slot_duration_minutes'],
                    google_calendar_id=doc_data.get('google_calendar_id')
                )
                db.add(new_doctor)
                added_count += 1
        
        db.commit()
        print(f"✅ Successfully seeded {added_count} doctors into PostgreSQL.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding doctors: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_doctors_from_json()
