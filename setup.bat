@echo off
REM War Thunder Rangefinder - Easy Setup Script
REM This will install everything you need automatically

echo ================================================
echo   War Thunder Rangefinder - Setup
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8 or higher from python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/3] Python detected!
echo.

echo [2/3] Installing required packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo.
echo [3/3] Setup complete!
echo.
echo ================================================
echo   Installation Successful!
echo ================================================
echo.
echo To run the rangefinder, simply double-click:
echo    run_rangefinder.bat
echo.
echo Or run manually with:
echo    python wt_rangefinder.py
echo.
pause
