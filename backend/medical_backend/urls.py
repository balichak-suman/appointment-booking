from fastapi import APIRouter
from api.whatsapp import router as whatsapp_router
from api.dashboard import router as dashboard_router
from api.doctors import router as doctors_router
from api.patients import router as patients_router
from api.appointments import router as appointments_router

# Main API Router
api_router = APIRouter()

# We use prefix="" in the sub-routers and define the full path in urls.py 
# to match the frontend's exact URL calls (no trailing slash issues)
api_router.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])
api_router.include_router(doctors_router, prefix="/api/doctors", tags=["Doctors"])
api_router.include_router(patients_router, prefix="/api/patients", tags=["Patients"])
api_router.include_router(appointments_router, prefix="/api/appointments", tags=["Appointments"])
api_router.include_router(whatsapp_router, prefix="", tags=["WhatsApp"])
