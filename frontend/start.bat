@echo off
echo =========================================
echo Clinic Staff Dashboard - Frontend Server
echo =========================================
echo.

cd /d "%~dp0"

echo Checking if node_modules exists...
if not exist "node_modules\" (
    echo Installing dependencies...
    call npm install
    echo.
)

echo Starting frontend server...
echo Server will run on http://localhost:5173
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev
