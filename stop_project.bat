@echo off
REM Windows Shutdown Script for Online Retail Analytics Platform

title Online Retail Analytics - Shutdown
color 0C

echo ================================================================================
echo           STOPPING ONLINE RETAIL ANALYTICS SERVICES
echo ================================================================================
echo.

echo [STATUS] Terminating python web server and simulator background processes...
taskkill /FI "WINDOWTITLE eq Online Retail Analytics*" /F >nul 2>&1
for /f "tokens=2 delims=," %%i in ('tasklist /fi "imagename eq python.exe" /fo csv /nh') do (
    echo Terminating Python PID: %%~i
)

echo.
echo [SUCCESS] Local services stopped.
pause
