@echo off
title SPK-SBCC 3T - Server
echo ========================================================
echo   MENJALANKAN SISTEM SPK-SBCC 3T
echo ========================================================
echo.
echo [1/3] Memeriksa/menginstal dependensi Python...
python -m pip install fastapi uvicorn google-generativeai python-dotenv

echo.
echo [2/3] Membuka browser ke alamat http://127.0.0.1:8000...
timeout /t 3 /nobreak >nul
start "" "http://127.0.0.1:8000"

echo.
echo [3/3] Menjalankan Server FastAPI Backend...
echo (Tekan Ctrl+C untuk menghentikan server)
echo.
python -m uvicorn app.main:app --reload --port 8000
pause
