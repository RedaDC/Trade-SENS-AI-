@echo off
echo ==========================================
echo   Starting TradeSense Backend
echo ==========================================

<<<<<<< HEAD
cd /d "%~dp0"
=======
cd "c:\Users\Setup Game\app testf"
>>>>>>> 104744f1a8f354c139261e224ea62ab97bb4c620

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

<<<<<<< HEAD
:: Initialize database if it doesn't exist
if not exist "backend\instance\tradesense.db" (
    echo Initializing database...
    python -m backend.init_db
)

=======
>>>>>>> 104744f1a8f354c139261e224ea62ab97bb4c620
echo Starting Flask Server...
python -m backend.app
