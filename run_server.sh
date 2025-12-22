#!/bin/bash

echo "Starting Vehicle Service Booking System..."
echo ""
echo "Make sure you have:"
echo "1. Installed Python 3.8+"
echo "2. Installed dependencies: pip install -r requirements.txt"
echo "3. Run migrations: python manage.py migrate"
echo "4. Created superuser: python manage.py createsuperuser"
echo ""
echo "Starting server..."

python manage.py runserver



