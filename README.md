# Vehicle Service Booking System

A comprehensive full-stack web application for managing vehicle service bookings, connecting vehicle owners with service centers, and tracking maintenance history.

## Features

### Vehicle Owner Module
- User registration and login
- Add and manage multiple vehicles
- Book service appointments online
- Track service status in real-time
- View and download invoices
- Submit feedback and ratings
- Change password

### Service Center Module
- Dashboard with analytics
- Manage bookings (accept/reject/update status)
- Assign mechanics to bookings
- Generate digital invoices
- Manage inventory
- View analytics (daily bookings, revenue, popular services)
- Add and manage mechanics

### Mechanic Module
- View assigned tasks
- Update task completion status
- Track work progress

### Admin Module
- Manage all users
- Manage service centers
- Configure service categories
- System-wide analytics

## Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5.3
- **Database**: SQLite (default, can be changed to MySQL/PostgreSQL)
- **Authentication**: Django Authentication System

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Navigate to Project Directory
```bash
cd "Vehicle Service Booking System"
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### Step 6: Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Initial Setup

### 1. Create Admin User
After running migrations, create a superuser:
```bash
python manage.py createsuperuser
```

### 2. Create Service Categories (via Admin or App)
- Login as admin
- Go to Admin panel or use the "Manage Categories" page
- Add service categories (e.g., Oil Change, General Service, Brake Repair, etc.)

### 3. Create Test Users
You can create users through:
- Registration page (for owners, service centers, mechanics)
- Django Admin panel
- Service Center can add mechanics through their dashboard

## User Roles

1. **Vehicle Owner**: Register vehicles, book services, track status
2. **Service Center**: Manage bookings, assign mechanics, generate invoices
3. **Mechanic**: View and update assigned tasks
4. **Admin**: Manage system-wide settings and users

## Default Login

After creating a superuser, you can login at:
- URL: `http://127.0.0.1:8000/login/`
- Use the superuser credentials you created

## Project Structure

```
Vehicle Service Booking System/
├── booking/              # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── urls.py          # URL routing
│   ├── forms.py         # Form definitions
│   └── admin.py         # Admin configuration
├── vehicle_service/     # Django project settings
│   ├── settings.py     # Project settings
│   ├── urls.py         # Main URL configuration
│   └── wsgi.py         # WSGI configuration
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   └── booking/        # App-specific templates
├── static/             # Static files (CSS, JS, images)
├── media/              # User-uploaded files
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## Database Models

- **User**: Custom user model with roles
- **ServiceCenter**: Service center information
- **Vehicle**: Vehicle details
- **Mechanic**: Mechanic information
- **ServiceCategory**: Service types
- **Booking**: Service bookings
- **Invoice**: Generated invoices
- **Inventory**: Service center inventory
- **Feedback**: Customer feedback

## Deployment

### For Production Deployment:

1. **Update Settings**:
   - Set `DEBUG = False`
   - Update `ALLOWED_HOSTS`
   - Configure database (MySQL/PostgreSQL recommended)
   - Set up static files serving

2. **Collect Static Files**:
   ```bash
   python manage.py collectstatic
   ```

3. **Use Production Server**:
   - Use Gunicorn or uWSGI with Nginx
   - Configure SSL/HTTPS

### For Local Server Access:

To make the server accessible on your local network:

```bash
python manage.py runserver 0.0.0.0:8000
```

Then access from other devices on the same network using your PC's IP address:
`http://YOUR_IP_ADDRESS:8000`

## Common Issues & Solutions

### Issue: Migration errors
**Solution**: Delete `db.sqlite3` and migration files in `booking/migrations/` (except `__init__.py`), then run migrations again.

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic` and ensure `STATIC_URL` and `STATIC_ROOT` are configured correctly.

### Issue: Permission denied
**Solution**: Ensure you have write permissions in the project directory.

## Features Status

✅ User Registration & Login  
✅ Role-based Access Control  
✅ Vehicle Management  
✅ Service Booking  
✅ Status Tracking  
✅ Invoice Generation  
✅ Feedback System  
✅ Analytics Dashboard  
✅ Inventory Management  
✅ Password Change  
✅ Responsive Design  
✅ Mobile-Friendly UI  

## Support

For issues or questions, please check:
1. Django documentation: https://docs.djangoproject.com/
2. Project README and code comments
3. Django admin panel for data management

## License

This project is created for educational purposes.

---

**Note**: This is a development version. For production use, ensure proper security configurations, use a production database, and follow Django security best practices.



