@echo off
echo Starting Hospital Management System...

:: Start Backend
start cmd /k "cd backend && pip install -r requirements.txt && echo Starting Backend... && python main.py"

:: Start Frontend
start cmd /k "cd frontend && cmd /c npm install && echo Starting Frontend... && cmd /c npm run dev"

echo System starting...
echo Backend will be at: http://localhost:8000
echo Frontend will be at: http://localhost:5173
pause
