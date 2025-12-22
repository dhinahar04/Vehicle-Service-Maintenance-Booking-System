# Quick Setup Guide

## Step-by-Step Installation

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Admin User
```bash
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### 4. Populate Initial Data (Service Categories)
```bash
python manage.py populate_data
```
This will create default service categories like:
- General Service
- Oil Change
- Brake Service
- Tire Service
- Battery Replacement
- AC Service
- Engine Repair
- Car Wash

### 5. Start the Server
```bash
python manage.py runserver
```

### 6. Access the Application
- Open your browser and go to: `http://127.0.0.1:8000/`
- Login with your superuser credentials at: `http://127.0.0.1:8000/login/`

## Creating Test Users

### Option 1: Through Registration Page
1. Go to `http://127.0.0.1:8000/register/`
2. Register as:
   - **Vehicle Owner**: Select "Vehicle Owner" role
   - **Service Center**: Select "Service Center" role (then complete profile)
   - **Mechanic**: Select "Mechanic" role (needs to be assigned by Service Center)

### Option 2: Through Django Admin
1. Go to `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. Create users from the "Users" section

## Testing the System

### As Vehicle Owner:
1. Register/Login as Vehicle Owner
2. Add a vehicle (Dashboard → Add Vehicle)
3. Book a service (Dashboard → Book Service)
4. Track booking status
5. View invoice when service is completed
6. Submit feedback

### As Service Center:
1. Register/Login as Service Center
2. Complete service center profile
3. Add mechanics (Dashboard → Mechanics → Add Mechanic)
4. View bookings (Dashboard → Manage Bookings)
5. Accept/Update booking status
6. Assign mechanics to bookings
7. Generate invoices
8. View analytics

### As Mechanic:
1. Login (created by Service Center)
2. View assigned tasks
3. Update task status (In Progress → Completed)

### As Admin:
1. Login with superuser credentials
2. Manage all users
3. Manage service centers
4. Configure service categories
5. View system-wide analytics

## Making Server Accessible on Network

To access from other devices on your local network:

```bash
python manage.py runserver 0.0.0.0:8000
```

Then access using your PC's IP address:
- Find your IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
- Access: `http://YOUR_IP_ADDRESS:8000`

## Common Commands

```bash
# Create superuser
python manage.py createsuperuser

# Populate service categories
python manage.py populate_data

# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Start server
python manage.py runserver

# Start server on network
python manage.py runserver 0.0.0.0:8000
```

## Troubleshooting

### Database Issues
If you encounter database errors:
```bash
# Delete database and recreate
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_data
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Port Already in Use
Change the port:
```bash
python manage.py runserver 8001
```

## Next Steps

1. ✅ Complete setup
2. ✅ Create admin user
3. ✅ Populate service categories
4. ✅ Create test users (Owner, Service Center)
5. ✅ Test booking flow
6. ✅ Test all modules

Enjoy your Vehicle Service Booking System! 🚗



