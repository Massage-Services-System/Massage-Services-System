@echo off
setlocal
cd /d "%~dp0"
echo Offline development preview, requires installed Flask, SQLAlchemy and Pydantic.
echo http://127.0.0.1:8000 - keep this window open.
start "" http://127.0.0.1:8000
python -m app.preview
pause

