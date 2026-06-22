@echo off
REM vidgrab installer for Windows

echo Installing vidgrab...
echo.

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3.11+ is required but not installed.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python %PYTHON_VERSION% detected
echo.

REM Check ffmpeg
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: ffmpeg is required but not found in PATH
    echo.
    echo Install it with:
    echo   winget install ffmpeg
    echo.
    set /p continue="Continue anyway? (y/n): "
    if not "!continue!"=="y" (
        if not "!continue!"=="Y" (
            exit /b 1
        )
    )
)

echo.
echo Installing vidgrab via pip...
pip install --upgrade vidgrab

echo.
echo. Installation complete!
echo.
echo Test it:
echo   vidgrab --help
echo.
echo Download a video:
echo   vidgrab https://youtu.be/dQw4w9WgXcQ
echo.
pause
