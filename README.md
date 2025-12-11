# Vehicle Service & Maintenance Booking System

A comprehensive web-based system for managing vehicle service bookings, maintenance reminders, and service center operations.

## Features

### User Module (Vehicle Owner)
- ✅ User registration and login
- ✅ Add and manage multiple vehicles
- ✅ Book service appointments
- ✅ Choose from various service types
- ✅ Track booking status (Pending, Accepted, In Progress, Completed, Ready for Delivery)
- ✅ View and download invoices
- ✅ Maintenance reminders via SMS/Email
- ✅ Service feedback and ratings

### Service Center Module
- ✅ Dashboard with overview statistics
- ✅ Manage bookings (Accept/Reject appointments)
- ✅ Assign mechanics automatically or manually
- ✅ Update service progress
- ✅ Estimate cost generator
- ✅ Generate digital invoices
- ✅ Maintain spare parts inventory
- ✅ Analytics:
  - Daily bookings
  - Revenue tracking
  - Most frequent customers
  - Most requested services

### Admin Module
- ✅ Manage service centers
- ✅ Manage users
- ✅ Configure service categories
- ✅ Monitor system reports

## Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (can be switched to MySQL/PostgreSQL)
- **Authentication**: Django Auth System
- **Notifications**: Email (SMTP) and SMS (Twilio)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd "Vehicle Service Booking System"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file and add your configuration:
   - Django SECRET_KEY
   - Email credentials (for notifications)
   - Twilio credentials (for SMS notifications - optional)

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Web application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
Vehicle Service Booking System/
├── accounts/              # User authentication and profiles
├── vehicles/              # Vehicle management
├── bookings/              # Booking management
├── service_centers/       # Service center operations
├── inventory/             # Spare parts inventory
├── payments/              # Invoice and payment management
├── notifications/         # Notification system
├── templates/             # HTML templates
├── static/                # CSS, JS, and images
│   ├── css/
│   └── js/
├── vehicle_service/       # Main project settings
├── manage.py
├── requirements.txt
└── README.md
```

## Usage Guide

### For Customers

1. **Register/Login**: Create an account or login
2. **Add Vehicles**: Add your vehicles with details (make, model, registration, etc.)
3. **Book Service**: Select vehicle, service center, service type, and preferred date/time
4. **Track Status**: Monitor your booking status in real-time
5. **View Invoices**: Access and download invoices after service completion
6. **Provide Feedback**: Rate and review completed services

### For Service Centers

1. **Create Profile**: Complete your service center profile after registration
2. **Manage Services**: Add and configure available services
3. **Manage Mechanics**: Add mechanics and assign them to bookings
4. **Process Bookings**: Accept/reject bookings and update status
5. **Generate Invoices**: Create invoices after service completion
6. **Manage Inventory**: Track spare parts and inventory
7. **View Analytics**: Monitor bookings, revenue, and customer insights

### For Administrators

1. **Access Admin Panel**: Login at `/admin/`
2. **Manage Users**: View and manage all users
3. **Manage Service Centers**: Approve/disable service centers
4. **Configure Categories**: Manage service categories
5. **View Reports**: Monitor system-wide statistics

## Database Models

- **User**: Custom user model with roles (customer, service_center, admin)
- **ServiceCenter**: Service center profiles
- **Mechanic**: Mechanic profiles linked to service centers
- **Vehicle**: Vehicle information
- **MaintenanceReminder**: Maintenance reminders for vehicles
- **ServiceCategory**: Service categories
- **Service**: Available services per service center
- **Booking**: Service bookings
- **Feedback**: Customer feedback and ratings
- **Invoice**: Generated invoices
- **Payment**: Payment records
- **SparePart**: Inventory items
- **Notification**: In-app notifications

## Color Scheme

The application uses a professional blue color scheme:
- **Primary**: #2563eb (Blue)
- **Secondary**: #10b981 (Green)
- **Success**: #10b981
- **Warning**: #f59e0b
- **Danger**: #ef4444
- **Info**: #06b6d4

## API Endpoints

- `/api/services/` - Get services for a service center (AJAX)

## Notifications

The system supports multiple notification channels:
- **In-app notifications**: Real-time notifications in the dashboard
- **Email notifications**: Sent via SMTP
- **SMS notifications**: Sent via Twilio (optional)

## Future Enhancements

- Mobile app (React Native/Flutter)
- Real-time chat support
- Payment gateway integration
- Advanced analytics dashboard
- Multi-language support
- API for third-party integrations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please create an issue in the repository or contact the development team.

---

**Developed with ❤️ using Django**

