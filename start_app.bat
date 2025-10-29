@echo off
echo Starting Land Cover Classification System...
echo.

echo Starting Backend Server...
start cmd /k "python app.py"

timeout /t 3 /nobreak > nul

echo Starting Frontend Server...
start cmd /k "cd frontend && npm start"

echo.
echo Both servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this window (servers will continue running)
pause > nul
