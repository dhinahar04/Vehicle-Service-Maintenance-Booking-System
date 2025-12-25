@echo off
REM Vehicle Service Booking System - Run Script for Windows

echo ==========================================
echo Vehicle Service Booking System
echo ==========================================
echo.

REM Check if we're in the right directory
if not exist "manage.py" (
    echo Error: manage.py not found. Please run this script from the project root.
    pause
    exit /b 1
)

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo Python found
echo.

REM Check dependencies
echo Checking dependencies...
python -c "import django" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo Dependencies OK
)
echo.

REM Check database
echo Checking database...
if not exist "db.sqlite3" (
    echo Running migrations...
    python manage.py migrate
    python manage.py populate_data
    echo Database created and populated
) else (
    echo Database exists
)
echo.

REM Check .env file
if not exist ".env" (
    echo .env file not found.
    echo The project will use SQLite database (default).
    echo To use MongoDB, create .env file with MONGODB_URI
    echo.
) else (
    echo .env file found
    echo.
)

REM Run Django system check
echo Running system check...
python manage.py check
echo.

REM Start server
echo ==========================================
echo Starting Django development server...
echo ==========================================
echo.
echo Server will be available at: http://127.0.0.1:8000/
echo Admin panel: http://127.0.0.1:8000/admin/
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver

pause

