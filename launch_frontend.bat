@echo off
echo ==========================================
echo   Lancement du Frontend TradeSense
echo ==========================================

cd frontend

echo [1/2] Installation des dependances (npm install)...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo Erreur: npm install a echoue. Verifiez que Node.js est bien installe.
    pause
    exit /b %ERRORLEVEL%
)

echo [2/2] Demarrage du serveur de developpement...
npm run dev
