"""
Clean Database Initialization
Creates empty tables without any sample data
"""

from database import Base, engine, SessionLocal, Doctor, Patient, Appointment
import sys

def init_clean_database():
    """Initialize database with empty tables only"""
    print("=" * 60)
    print("🗄️  CLEAN DATABASE INITIALIZATION")
    print("=" * 60)
    
    try:
        # Drop all existing tables
        print("\n🗑️  Dropping existing tables...")
        Base.metadata.drop_all(bind=engine)
        print("✅ Existing tables dropped")
        
        # Create fresh tables
        print("\n📋 Creating fresh tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        
        # Verify tables are empty
        db = SessionLocal()
        try:
            doctor_count = db.query(Doctor).count()
            patient_count = db.query(Patient).count()
            appointment_count = db.query(Appointment).count()
            
            print("\n" + "=" * 60)
            print("✅ DATABASE INITIALIZED SUCCESSFULLY!")
            print("=" * 60)
            print(f"\n📊 Current Database Status:")
            print(f"   • Doctors: {doctor_count}")
            print(f"   • Patients: {patient_count}")
            print(f"   • Appointments: {appointment_count}")
            print("\n✨ Database is clean and ready to use!")
            print("=" * 60)
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_clean_database()
