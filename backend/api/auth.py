from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["Auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    # Mock authentication for demo purposes
    if request.username == "root" and request.password == "root":
        return {
            "success": True,
            "data": {
                "token": "mock-jwt-token-root",
                "user": {
                    "id": 0,
                    "username": "root",
                    "role": "admin",
                    "name": "Super Admin"
                }
            }
        }
    elif request.username == "admin" and request.password == "admin123":
        return {
            "success": True,
            "data": {
                "token": "mock-jwt-token-admin",
                "user": {
                    "id": 1,
                    "username": "admin",
                    "role": "admin",
                    "name": "Admin User"
                }
            }
        }
    elif request.username == "staff" and request.password == "staff123":
        return {
            "success": True,
            "data": {
                "token": "mock-jwt-token-staff",
                "user": {
                    "id": 2,
                    "username": "staff",
                    "role": "staff",
                    "name": "Staff Member"
                }
            }
        }
    elif request.username == "dr.sarah" and request.password == "doctor123":
        return {
            "success": True,
            "data": {
                "token": "mock-jwt-token-doctor",
                "user": {
                    "id": 3,
                    "username": "dr.sarah",
                    "role": "doctor",
                    "name": "Dr. Sarah"
                }
            }
        }
    
    raise HTTPException(status_code=401, detail="Invalid credentials")
