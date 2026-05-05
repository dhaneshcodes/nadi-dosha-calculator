@echo off
echo ========================================================
echo    Nadi Dosha Calculator - NEW Server
echo ========================================================
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting NEW server (with calculation API)...
echo This replaces proxy-server.py
echo.
echo Server will start at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo Press Ctrl+C to stop the server
echo.
echo ========================================================
python server.py

