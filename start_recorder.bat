@echo off
REM Screen Recorder Launcher
REM Double-click this file to start the recorder

echo ========================================
echo    Screen Recorder
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check Add Python to PATH during installation
    echo.
    pause
    exit /b 1
)

REM Check if FFmpeg is available
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: FFmpeg not found in PATH
    echo.
    echo FFmpeg is required for recording.
    echo.
    echo To install FFmpeg no admin needed:
    echo 1. Download from: https://www.gyan.dev/ffmpeg/builds/
    echo 2. Extract the zip file
    echo 3. Add the bin folder to your PATH or place this script in the bin folder
    echo.
    set /p open=Open download page in browser? Y/N: 
    if /i "%open%"=="Y" (
        start https://www.gyan.dev/ffmpeg/builds/
    )
    echo.
    pause
    exit /b 1
)

echo Starting Screen Recorder...
echo.

REM Run the Python script
python screen_recorder.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start recorder
    echo.
    pause
)