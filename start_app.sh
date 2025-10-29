#!/bin/bash

echo "Starting Land Cover Classification System..."
echo ""

echo "Starting Backend Server..."
python app.py &
BACKEND_PID=$!

sleep 3

echo "Starting Frontend Server..."
cd frontend
npm start &
FRONTEND_PID=$!

echo ""
echo "Both servers are running..."
echo "Backend: http://localhost:5000 (PID: $BACKEND_PID)"
echo "Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
