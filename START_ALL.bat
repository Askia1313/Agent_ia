@echo off
echo ============================================================
echo        SYSTEME RAG - DEMARRAGE COMPLET
echo ============================================================
echo.
echo Demarrage du backend Django...
start "Backend Django" cmd /k "cd Backend_ia && python manage.py runserver"

echo Attente de 5 secondes...
timeout /t 5 /nobreak > nul

echo Demarrage du frontend Vue.js...
start "Frontend Vue.js" cmd /k "cd Frontend && npm run dev"

echo.
echo ============================================================
echo                    SYSTEME PRET
echo ============================================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API:      http://localhost:8000/api/question/
echo.
echo Fermez les fenetres pour arreter les serveurs
echo.
pause
