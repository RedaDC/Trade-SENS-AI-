@echo off
echo ==========================================
echo   Starting TradeSense Backend
echo ==========================================

cd /d "%~dp0"

if not exist ".venv" (
    echo Virtual environment not found! Creating one...
    python -m venv .venv
    call .venv\Scripts\activate
    echo Installing dependencies...
    pip install -r backend\requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo Error installing dependencies!
        pause
        exit /b 1
    )
) else (
    call .venv\Scripts\activate
    echo Virtual environment activated.
)

:: Initialize database if it doesn't exist
if not exist "backend\instance\tradesense.db" (
    echo Initializing database...
    python -m backend.init_db
)

echo Starting Flask Server...
python -m backend.app
