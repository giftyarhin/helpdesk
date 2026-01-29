@echo off
REM Helpdesk System - Quick Setup Script for Windows

echo ================================
echo Helpdesk System Setup
echo ================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo + Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

echo + Virtual environment created and activated
echo.

REM Install dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo + Dependencies installed
echo.

REM Copy .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo ! Please edit .env file with your actual configuration!
    echo.
)

REM Create directories
echo Creating required directories...
if not exist static mkdir static
if not exist media mkdir media

echo + Directories created
echo.

echo ================================
echo Database Setup
echo ================================
echo.
echo Please create your MySQL database manually:
echo.
echo 1. Log into MySQL
echo 2. Run these commands:
echo    CREATE DATABASE helpdesk_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
echo    CREATE USER 'helpdesk_user'@'localhost' IDENTIFIED BY 'your_password';
echo    GRANT ALL PRIVILEGES ON helpdesk_db.* TO 'helpdesk_user'@'localhost';
echo    FLUSH PRIVILEGES;
echo    EXIT;
echo.
pause

REM Run migrations
echo.
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

echo + Migrations complete
echo.

REM Create superuser
echo Creating admin user...
python manage.py createsuperuser

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo Next steps:
echo 1. Edit .env file with your SendGrid API key and other settings
echo 2. Run: python manage.py runserver
echo 3. Visit: http://localhost:8000
echo.
echo To activate the virtual environment in the future, run:
echo venv\Scripts\activate.bat
echo.
pause
