#!/bin/bash

# WiFi Network Sharing Platform - Quick Start Script for Linux/Mac

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║         WiFi Network Sharing Platform - Quick Start           ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Create migrations
echo "Creating database migrations..."
python3 manage.py makemigrations
if [ $? -ne 0 ]; then
    echo "❌ Failed to create migrations"
    exit 1
fi

echo "✓ Migrations created"
echo ""

# Apply migrations
echo "Applying migrations to database..."
python3 manage.py migrate
if [ $? -ne 0 ]; then
    echo "❌ Failed to apply migrations"
    exit 1
fi

echo "✓ Database initialized"
echo ""

# Create superuser
echo ""
echo "Creating superuser account..."
echo "Please enter the following information:"
python3 manage.py createsuperuser
if [ $? -ne 0 ]; then
    echo "⚠ Failed to create superuser, but this is optional"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                  Setup Complete!                              ║"
echo "╠═══════════════════════════════════════════════════════════════╣"
echo "║                                                               ║"
echo "║  Your application is ready to run!                           ║"
echo "║                                                               ║"
echo "║  To start the development server, run:                       ║"
echo "║  python3 manage.py runserver                                 ║"
echo "║                                                               ║"
echo "║  Then visit:                                                  ║"
echo "║  - Website: http://localhost:8000                            ║"
echo "║  - Admin:   http://localhost:8000/admin                      ║"
echo "║                                                               ║"
echo "║  For more information, see SETUP_GUIDE.md                    ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
