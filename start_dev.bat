@echo off
echo ============================================================
echo  Starting DevUpward Full Stack (Backend + Bot + Frontend)
echo ============================================================

if not exist .env (
    echo [!] Copying .env.example to .env...
    copy .env.example .env
)

echo [*] Launching Python Backend in new window...
start cmd /k "call backend\venv\Scripts\activate.bat && python backend\app\main.py"

echo [*] Launching React Frontend...
cd frontend
npm run dev
