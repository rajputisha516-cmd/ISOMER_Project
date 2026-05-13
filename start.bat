@echo off
REM Isomer - AI Surveillance System Startup Script (Windows)

setlocal enabledelayedexpansion

echo.
echo 🚀 Starting Isomer AI Surveillance System...
echo.

REM Check Python
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ Python not found. Please install Python 3.8+
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ Node.js not found. Please install Node.js 16+
    exit /b 1
)

echo 📝 Starting Backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
pip install -q -r requirements.txt

REM Start backend
start "Isomer Backend" python app.py

echo ✅ Backend started (check command window)
echo ⏳ Waiting for backend to be ready...

timeout /t 5 /nobreak

REM Check if backend is running
curl http://localhost:5000/api/health >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ Backend failed to start
    exit /b 1
)

echo ✅ Backend is ready!

cd ..

echo.
echo 📦 Starting Frontend...
cd frontend

REM Install dependencies if needed
if not exist "node_modules" (
    echo Installing Node dependencies...
    call npm install
)

REM Start frontend
start "Isomer Frontend" cmd /k npm run dev

echo ✅ Frontend starting...

cd ..

echo.
echo ✅ Isomer System Started Successfully!
echo.
echo Dashboard: http://localhost:3000
echo Backend API: http://localhost:5000
echo.
echo Both services are running in separate windows.
echo Close the command windows to stop the services.
echo.

pause
