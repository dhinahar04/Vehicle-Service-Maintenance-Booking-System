#!/usr/bin/env python3
"""
MongoDB Setup Helper Script
This script helps you create a .env file with your MongoDB connection string.
"""

import os
import getpass

def setup_mongodb():
    """Interactive setup for MongoDB connection"""
    print("=" * 60)
    print("MongoDB Atlas Connection Setup")
    print("=" * 60)
    print()
    
    # Get MongoDB password
    print("Enter your MongoDB Atlas password for user 'dhinaharmurugesan':")
    password = getpass.getpass("Password: ")
    
    if not password:
        print("Error: Password cannot be empty!")
        return
    
    # Build connection string
    connection_string = f"mongodb+srv://dhinaharmurugesan:{password}@vehiclemanagement.8kw7dqf.mongodb.net/vehicle_management?retryWrites=true&w=majority"
    
    # Get other settings
    print("\nEnter Django Secret Key (or press Enter for default):")
    secret_key = input("Secret Key: ").strip() or "django-insecure-vehicle-service-booking-system-2024"
    
    print("\nDebug mode? (True/False, default: True):")
    debug = input("DEBUG: ").strip().lower() or "true"
    debug = "True" if debug in ['true', '1', 'yes', 'y'] else "False"
    
    # Create .env file content
    env_content = f"""# Django Settings
DJANGO_SECRET_KEY={secret_key}
DJANGO_DEBUG={debug}
DJANGO_ALLOWED_HOSTS=*

# MongoDB Atlas Connection
MONGODB_URI={connection_string}

# Email Settings (Optional - uncomment if needed)
# EMAIL_HOST=smtp.gmail.com
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
"""
    
    # Write .env file
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if os.path.exists(env_path):
        print(f"\n⚠️  .env file already exists at: {env_path}")
        overwrite = input("Do you want to overwrite it? (yes/no): ").strip().lower()
        if overwrite not in ['yes', 'y']:
            print("Cancelled. .env file not modified.")
            return
    
    try:
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        print(f"\n✅ Success! .env file created at: {env_path}")
        print("\nNext steps:")
        print("1. Make sure MongoDB Atlas Network Access allows your IP")
        print("2. Test connection: python manage.py migrate")
        print("3. Populate data: python manage.py populate_data")
        print("\n⚠️  Remember: .env file is in .gitignore and won't be committed to GitHub")
        
    except Exception as e:
        print(f"\n❌ Error creating .env file: {e}")

if __name__ == "__main__":
    setup_mongodb()

