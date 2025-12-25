#!/usr/bin/env python3
"""
Test script to verify project setup and database connection
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vehicle_service.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line
from booking.models import (
    User, ServiceCenter, Vehicle, Mechanic, ServiceCategory,
    Booking, Invoice, Inventory, Feedback, MechanicRequest
)

def test_setup():
    """Test all components of the project"""
    print("=" * 60)
    print("Vehicle Service Booking System - Setup Test")
    print("=" * 60)
    print()
    
    errors = []
    warnings = []
    
    # Test 1: Database Connection
    print("1. Testing Database Connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        print("   ✅ Database connection: OK")
    except Exception as e:
        error_msg = f"   ❌ Database connection failed: {e}"
        print(error_msg)
        errors.append(error_msg)
    print()
    
    # Test 2: Models Import
    print("2. Testing Models...")
    models = [
        ('User', User),
        ('ServiceCenter', ServiceCenter),
        ('Vehicle', Vehicle),
        ('Mechanic', Mechanic),
        ('ServiceCategory', ServiceCategory),
        ('Booking', Booking),
        ('Invoice', Invoice),
        ('Inventory', Inventory),
        ('Feedback', Feedback),
        ('MechanicRequest', MechanicRequest),
    ]
    
    for name, model in models:
        try:
            count = model.objects.count()
            print(f"   ✅ {name}: OK ({count} records)")
        except Exception as e:
            error_msg = f"   ❌ {name}: Error - {e}"
            print(error_msg)
            errors.append(error_msg)
    print()
    
    # Test 3: Service Categories
    print("3. Testing Service Categories...")
    try:
        categories = ServiceCategory.objects.count()
        if categories == 0:
            warning_msg = "   ⚠️  No service categories found. Run: python manage.py populate_data"
            print(warning_msg)
            warnings.append(warning_msg)
        else:
            print(f"   ✅ Service categories: {categories} found")
    except Exception as e:
        error_msg = f"   ❌ Service categories error: {e}"
        print(error_msg)
        errors.append(error_msg)
    print()
    
    # Test 4: Settings
    print("4. Testing Settings...")
    from django.conf import settings
    try:
        print(f"   ✅ DEBUG: {settings.DEBUG}")
        print(f"   ✅ Database Engine: {settings.DATABASES['default']['ENGINE'].split('.')[-1]}")
        print(f"   ✅ Allowed Hosts: {settings.ALLOWED_HOSTS}")
    except Exception as e:
        error_msg = f"   ❌ Settings error: {e}"
        print(error_msg)
        errors.append(error_msg)
    print()
    
    # Test 5: URLs
    print("5. Testing URL Configuration...")
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        url_count = len([p for p in resolver.url_patterns])
        print(f"   ✅ URL patterns: {url_count} found")
    except Exception as e:
        error_msg = f"   ❌ URL configuration error: {e}"
        print(error_msg)
        errors.append(error_msg)
    print()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    if errors:
        print(f"❌ Errors found: {len(errors)}")
        for error in errors:
            print(f"   - {error}")
    else:
        print("✅ No errors found!")
    
    if warnings:
        print(f"\n⚠️  Warnings: {len(warnings)}")
        for warning in warnings:
            print(f"   - {warning}")
    
    print()
    if not errors:
        print("✅ Project is ready to run!")
        print("\nTo start the server:")
        print("   python3 manage.py runserver")
    else:
        print("❌ Please fix the errors above before running the project.")
    
    return len(errors) == 0

if __name__ == "__main__":
    success = test_setup()
    sys.exit(0 if success else 1)

