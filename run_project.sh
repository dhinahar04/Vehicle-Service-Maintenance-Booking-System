#!/bin/bash

# Vehicle Service Booking System - Run Script
# This script sets up and runs the project

echo "=========================================="
echo "Vehicle Service Booking System"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the project root."
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check dependencies
echo "Checking dependencies..."
if ! python3 -c "import django" 2>/dev/null; then
    echo "⚠️  Django not found. Installing dependencies..."
    pip3 install -r requirements.txt
else
    echo "✅ Dependencies OK"
fi
echo ""

# Check database
echo "Checking database..."
if [ ! -f "db.sqlite3" ]; then
    echo "⚠️  Database not found. Running migrations..."
    python3 manage.py migrate
    python3 manage.py populate_data
    echo "✅ Database created and populated"
else
    echo "✅ Database exists"
    # Check if migrations are needed
    if python3 manage.py migrate --check 2>&1 | grep -q "have unapplied"; then
        echo "⚠️  Running migrations..."
        python3 manage.py migrate
    fi
fi
echo ""

# Check .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found."
    echo "   The project will use SQLite database (default)."
    echo "   To use MongoDB, create .env file with MONGODB_URI"
    echo ""
else
    echo "✅ .env file found"
    # Check if MongoDB is configured
    if grep -q "MONGODB_URI" .env && ! grep -q "MONGODB_URI=$" .env; then
        echo "✅ MongoDB connection configured"
    else
        echo "⚠️  MongoDB not configured, using SQLite"
    fi
    echo ""
fi

# Run Django system check
echo "Running system check..."
if python3 manage.py check 2>&1 | grep -q "System check identified no issues"; then
    echo "✅ System check passed"
else
    echo "⚠️  System check found issues (check output above)"
fi
echo ""

# Start server
echo "=========================================="
echo "Starting Django development server..."
echo "=========================================="
echo ""
echo "🌐 Server will be available at: http://127.0.0.1:8000/"
echo "📝 Admin panel: http://127.0.0.1:8000/admin/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 manage.py runserver

