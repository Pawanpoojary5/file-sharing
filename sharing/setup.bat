@echo off
REM WiFi Network Sharing Platform - Quick Start Script for Windows

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║         WiFi Network Sharing Platform - Quick Start           ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✓ Dependencies installed
echo.

REM Create migrations
echo Creating database migrations...
python manage.py makemigrations
if errorlevel 1 (
    echo ❌ Failed to create migrations
    pause
    exit /b 1
)

echo ✓ Migrations created
echo.

REM Apply migrations
echo Applying migrations to database...
python manage.py migrate
if errorlevel 1 (
    echo ❌ Failed to apply migrations
    pause
    exit /b 1
)

echo ✓ Database initialized
echo.

REM Create superuser
echo.
echo Creating superuser account...
echo Please enter the following information:
python manage.py createsuperuser
if errorlevel 1 (
    echo ⚠ Failed to create superuser, but this is optional
)

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                  Setup Complete!                              ║
echo ╠═══════════════════════════════════════════════════════════════╣
echo ║                                                               ║
echo ║  Your application is ready to run!                           ║
echo ║                                                               ║
echo ║  To start the development server, run:                       ║
echo ║  python manage.py runserver                                  ║
echo ║                                                               ║
echo ║  Then visit:                                                  ║
echo ║  - Website: http://localhost:8000                            ║
echo ║  - Admin:   http://localhost:8000/admin                      ║
echo ║                                                               ║
echo ║  For more information, see SETUP_GUIDE.md                    ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

pause
