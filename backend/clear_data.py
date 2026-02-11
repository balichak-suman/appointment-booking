"""
Script to clear patients and appointments from the database
"""
from database import SessionLocal, Patient, Appointment

def clear_data():
    db = SessionLocal()
    try:
        print("🔄 Clearing patients and appointments...")
        
        # Delete all appointments
        deleted_appointments = db.query(Appointment).delete()
        print(f"✅ Deleted {deleted_appointments} appointments.")
        
        # Delete all patients
        deleted_patients = db.query(Patient).delete()
        print(f"✅ Deleted {deleted_patients} patients.")
        
        db.commit()
        print("\n✨ Database cleaned! Doctors records were kept.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error during clearing: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    clear_data()
