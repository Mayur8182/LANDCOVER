@echo off
echo ============================================================
echo Land Cover Classification System - Startup
echo ============================================================
echo.
echo Project: My First Project
echo Project ID: gleaming-tube-445109-t2
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Check if GEE is authenticated
echo.
echo Checking Google Earth Engine authentication...
python -c "import ee; ee.Initialize(project='gleaming-tube-445109-t2')" 2>nul
if errorlevel 1 (
    echo.
    echo Google Earth Engine not authenticated!
    echo.
    echo Please run: python setup_gee.py
    echo.
    echo This will:
    echo   1. Authenticate with your Google account
    echo   2. Initialize with project: gleaming-tube-445109-t2
    echo   3. Test Sentinel-2 and MODIS access
    echo.
    pause
    exit /b 1
)

echo GEE authenticated successfully!
echo.

REM Start backend
echo Starting Backend Server...
start "Land Cover Backend" cmd /k "cd /d %CD% && venv\Scripts\activate && python app.py"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo Starting Frontend Server...
start "Land Cover Frontend" cmd /k "cd /d %CD%\frontend && npm start"

echo.
echo ============================================================
echo Both servers are starting...
echo ============================================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo The browser will open automatically in a few seconds.
echo.
echo To stop servers: Close both command windows
echo.
echo ============================================================
pause
