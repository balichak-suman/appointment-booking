"""
Database Setup and Sample Data Seeder
Run this script to create tables and populate with sample data
"""

from database import SessionLocal, init_db, Doctor, Patient, Appointment
from datetime import datetime, timedelta
import random

def seed_doctors(db, count=247):
    """Seed doctors table with sample data"""
    specializations = [
        "Cardiology", "Neurology", "Pediatrics", "Orthopedics", "Dermatology",
        "Oncology", "Radiology", "Psychiatry", "General Medicine", "Surgery"
    ]
    
    first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "Robert", "Lisa", "James", "Maria"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    
    print(f"🔄 Seeding {count} doctors...")
    
    for i in range(1, count + 1):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        name = f"Dr. {first_name} {last_name}"
        
        doctor = Doctor(
            name=name,
            specialization=random.choice(specializations),
            experience=random.randint(2, 30),
            patients=random.randint(50, 200),
            appointments=random.randint(100, 500),
            rating=round(random.uniform(3.5, 5.0), 1),
            status=random.choice(["Available", "Busy", "On Leave"]),
            email=f"doctor{i}@preclinic.com",
            phone=f"+1-555-{random.randint(1000, 9999)}"
        )
        db.add(doctor)
    
    db.commit()
    print(f"✅ Successfully seeded {count} doctors!")

def seed_patients(db, count=4178):
    """Seed patients table with sample data"""
    first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "Robert", "Lisa", "James", "Maria", 
                   "William", "Elizabeth", "Richard", "Jennifer", "Charles"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", 
                  "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]
    
    conditions = ["Diabetes", "Hypertension", "Asthma", "Arthritis", "Heart Disease",
                 "None", "Allergy", "Migraine", "Back Pain"]
    
    blood_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    
    print(f"🔄 Seeding {count} patients...")
    
    for i in range(1, count + 1):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        
        last_visit = datetime.now() - timedelta(days=random.randint(1, 365))
        
        patient = Patient(
            name=name,
            age=random.randint(18, 85),
            gender=random.choice(["Male", "Female"]),
            blood_group=random.choice(blood_groups),
            condition=random.choice(conditions),
            last_visit=last_visit.date(),
            status=random.choice(["Active", "Inactive"]),
            email=f"patient{i}@email.com",
            phone=f"+1-555-{random.randint(1000, 9999)}",
            address=f"{random.randint(100, 9999)} Main St, City, State"
        )
        db.add(patient)
        
        # Commit in batches to improve performance
        if i % 100 == 0:
            db.commit()
            print(f"  ⏳ Seeded {i}/{count} patients...")
    
    db.commit()
    print(f"✅ Successfully seeded {count} patients!")

def seed_appointments(db, count=6314):
    """Seed appointments table with sample data"""
    statuses = ["Scheduled", "Completed", "Cancelled", "Rescheduled", "In Progress"]
    types = ["Walk-in", "Scheduled", "Emergency", "Follow-up"]
    departments = ["Cardiology", "Neurology", "Pediatrics", "Orthopedics", "General Medicine"]
    reasons = ["Checkup", "Follow-up", "Consultation", "Emergency", "Routine"]
    
    print(f"🔄 Seeding {count} appointments...")
    
    for i in range(1, count + 1):
        appointment_date = datetime.now() + timedelta(days=random.randint(-30, 30))
        appointment_time = f"{random.randint(8, 17)}:{random.choice(['00', '15', '30', '45'])}"
        
        appointment = Appointment(
            patient_name=f"Patient {random.randint(1, 4178)}",
            doctor_name=f"Dr. {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones'])}",
            date=appointment_date.date(),
            time=appointment_time,
            type=random.choice(types),
            status=random.choice(statuses),
            reason=random.choice(reasons),
            department=random.choice(departments)
        )
        db.add(appointment)
        
        # Commit in batches
        if i % 100 == 0:
            db.commit()
            print(f"  ⏳ Seeded {i}/{count} appointments...")
    
    db.commit()
    print(f"✅ Successfully seeded {count} appointments!")

def main():
    """Main function to initialize database and seed data"""
    print("=" * 60)
    print("🏥 Medical Dashboard - Database Setup")
    print("=" * 60)
    
    # Initialize database (create tables)
    print("\n📊 Creating database tables...")
    init_db()
    print("✅ Tables created successfully!")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_doctors = db.query(Doctor).count()
        existing_patients = db.query(Patient).count()
        existing_appointments = db.query(Appointment).count()
        
        print(f"\n📈 Current database status:")
        print(f"  - Doctors: {existing_doctors}")
        print(f"  - Patients: {existing_patients}")
        print(f"  - Appointments: {existing_appointments}")
        
        if existing_doctors > 0 or existing_patients > 0 or existing_appointments > 0:
            response = input("\n⚠️  Database already contains data. Do you want to add more? (y/n): ")
            if response.lower() != 'y':
                print("❌ Seeding cancelled.")
                return
        
        print("\n🌱 Starting data seeding process...")
        
        # Seed data
        if existing_doctors == 0:
            seed_doctors(db, 247)
        
        if existing_patients == 0:
            seed_patients(db, 4178)
        
        if existing_appointments == 0:
            seed_appointments(db, 6314)
        
        print("\n" + "=" * 60)
        print("🎉 Database setup completed successfully!")
        print("=" * 60)
        print("\n📊 Final database status:")
        print(f"  - Doctors: {db.query(Doctor).count()}")
        print(f"  - Patients: {db.query(Patient).count()}")
        print(f"  - Appointments: {db.query(Appointment).count()}")
        print("\n✅ You can now start the API server!")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
