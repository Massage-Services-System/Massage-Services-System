@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Install Python 3.10 or newer and select Add Python to PATH.
  pause
  exit /b 1
)
if not exist .venv\Scripts\python.exe (
  python -m venv .venv
  if errorlevel 1 goto :fail
)
.venv\Scripts\python.exe -c "import fastapi, uvicorn, sqlalchemy, tzdata" >nul 2>nul
if errorlevel 1 (
  .venv\Scripts\python.exe -m pip install -r requirements.txt
  if errorlevel 1 goto :fail
)
if not exist .env copy .env.example .env >nul
echo.
echo Massage Services System: http://127.0.0.1:8000
echo Swagger: http://127.0.0.1:8000/docs
echo Keep this window open. Ctrl+C stops the server.
start "" http://127.0.0.1:8000
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
if errorlevel 1 goto :fail
exit /b 0
:fail
echo.
echo Startup failed. Check the error above and your internet connection.
pause
exit /b 1

