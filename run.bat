@echo off
echo Starting FastAPI Backend on port 8000...
start "" cmd /c ".\venv\Scripts\uvicorn backend.main:app --port 8000"

echo Starting NiceGUI Frontend on port 8080...
start "" cmd /c ".\venv\Scripts\python frontend\main.py"

echo Both servers have been launched in separate windows!
