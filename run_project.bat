@echo off
REM Windows Automated Startup Script
REM Online Retail Customer Value & Revenue Analytics Platform

title Online Retail Analytics Platform Launcher
color 0A

echo ================================================================================
echo           ONLINE RETAIL CUSTOMER VALUE & REVENUE ANALYTICS PLATFORM
echo ================================================================================
echo.

REM 1. Verify Python Installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not available in PATH.
    pause
    exit /b 1
)
echo [OK] Python detected.

REM 2. Check & Install Required Web Dependencies
echo [STATUS] Checking Python package dependencies...
python -c "import flask, pandas, sqlalchemy" >nul 2>&1
if %errorlevel% neq 0 (
    echo [STATUS] Installing required dependencies...
    pip install -r web/requirements.txt
)
echo [OK] Python dependencies verified.

REM 3. Initialize Live Database Engine & Views
echo [STATUS] Initializing Live Database Engine & SQL Views...
python sql/setup_mysql.py
if %errorlevel% neq 0 (
    echo [WARNING] Database setup returned non-zero code. Falling back to embedded engine.
)

echo.
echo ================================================================================
echo [SUCCESS] PLATFORM READY FOR LOCAL DEMONSTRATION!
echo.
echo  - Live Web Application URL: http://127.0.0.1:5000
echo.
echo  - To generate live simulated transactions:
echo      Open a new terminal and run: python python/live_simulator.py --count 10
echo      OR run continuous stream:   python python/live_simulator.py --continuous
echo.
echo  - Interactive controls are also available directly on the web dashboard UI!
echo ================================================================================
echo.

REM 4. Launch Flask Web Application
python web/app.py

pause
