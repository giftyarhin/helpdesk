#!/bin/bash

# Helpdesk System - Quick Setup Script for macOS/Linux

echo "================================"
echo "Helpdesk System Setup"
echo "================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check MySQL
if ! command -v mysql &> /dev/null
then
    echo "❌ MySQL is not installed. Please install MySQL first."
    exit 1
fi

echo "✓ MySQL found"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

echo "✓ Virtual environment created and activated"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✓ Dependencies installed"
echo ""

# Copy .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your actual configuration!"
    echo ""
fi

# Create directories
echo "Creating required directories..."
mkdir -p static media

echo "✓ Directories created"
echo ""

echo "================================"
echo "Database Setup"
echo "================================"
echo ""
echo "Please create your MySQL database manually:"
echo ""
echo "1. Log into MySQL:"
echo "   mysql -u root -p"
echo ""
echo "2. Run these commands:"
echo "   CREATE DATABASE helpdesk_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
echo "   CREATE USER 'helpdesk_user'@'localhost' IDENTIFIED BY 'your_password';"
echo "   GRANT ALL PRIVILEGES ON helpdesk_db.* TO 'helpdesk_user'@'localhost';"
echo "   FLUSH PRIVILEGES;"
echo "   EXIT;"
echo ""
read -p "Press Enter once you've created the database..."

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "✓ Migrations complete"
echo ""

# Create superuser
echo "Creating admin user..."
python manage.py createsuperuser

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your SendGrid API key and other settings"
echo "2. Run: python manage.py runserver"
echo "3. Visit: http://localhost:8000"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "source venv/bin/activate"
echo ""
