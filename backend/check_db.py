from database import SessionLocal, Doctor

db = SessionLocal()
doctors = db.query(Doctor).all()
print(f"Sub-step: Checking doctors in DB...")
print(f"Total Doctors: {len(doctors)}")
for d in doctors:
    print(f"- {d.name} ({d.specialization})")

if not doctors:
    print("❌ NO DOCTORS FOUND! Please run seed_doctors.py")
else:
    print("✅ Doctors exist.")
db.close()
