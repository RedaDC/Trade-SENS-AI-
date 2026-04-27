@echo off
echo ==========================================
echo   Starting TradeSense Backend
echo ==========================================

cd "c:\Users\Setup Game\app testf"

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

echo Starting Flask Server...
python -m backend.app
