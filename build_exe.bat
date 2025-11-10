@echo off
REM Build standalone executable for War Thunder Rangefinder

echo ================================================
echo   Building Standalone Executable
echo ================================================
echo.

echo Installing PyInstaller...
python -m pip install pyinstaller

echo.
echo Building executable...
pyinstaller --onefile ^
    --windowed ^
    --name "WT_Rangefinder" ^
    --icon=NONE ^
    --add-data "requirements.txt;." ^
    wt_rangefinder.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo ================================================
echo   Build Complete!
echo ================================================
echo.
echo Executable created in: dist\WT_Rangefinder.exe
echo.
echo You can now distribute this single .exe file!
echo No Python installation needed to run it.
echo.
pause
