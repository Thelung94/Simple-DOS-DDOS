@echo off
setlocal enabledelayedexpansion

:: Step 1: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed on this system. Please install Python 3.9+ and try again.
    pause
    exit /b
)

echo [INFO] Python found.

:: Step 2: Create virtual environment if not exists
if not exist env (
    echo [INFO] Creating virtual environment...
    python -m venv env
)

:: Step 3: Activate virtual environment
echo [INFO] Activating virtual environment...
call env\Scripts\activate.bat

:: Step 4: Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

:: Step 5: Install requirements
echo [INFO] Installing required packages...
pip install -r requirements.txt

:: Step 6: Start the app
echo [INFO] Starting the app...
python run.py

pause
