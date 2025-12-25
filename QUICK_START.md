# Quick Start Guide - Run Project Without Errors

## Step 1: Install Dependencies (if not already installed)

```bash
cd "/Users/dhina/Desktop/Vehicle Service Booking System"
pip3 install -r requirements.txt
```

## Step 2: Setup Database Connection

### Option A: Use SQLite (Quick Start - No MongoDB setup needed)

The project will automatically use SQLite if MongoDB is not configured. Just run:

```bash
python3 manage.py migrate
python3 manage.py populate_data
```

### Option B: Connect to MongoDB (Recommended for Production)

1. **Get your MongoDB password:**
   - Go to [MongoDB Atlas](https://cloud.mongodb.com/)
   - Database Access → Find user `dhinaharmurugesan`
   - Copy your password

2. **Create .env file:**
   ```bash
   cd "/Users/dhina/Desktop/Vehicle Service Booking System"
   ```

   Create `.env` file with this content (replace `YOUR_PASSWORD`):
   ```env
   DJANGO_SECRET_KEY=django-insecure-vehicle-service-booking-system-2024
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=*
   MONGODB_URI=mongodb+srv://dhinaharmurugesan:YOUR_PASSWORD@vehiclemanagement.8kw7dqf.mongodb.net/vehicle_management?retryWrites=true&w=majority
   ```

3. **Configure MongoDB Network Access:**
   - Go to MongoDB Atlas → Network Access
   - Add IP Address → Add Current IP Address (for local)
   - Or add `0.0.0.0/0` for all IPs (for production)

## Step 3: Run Migrations

```bash
python3 manage.py migrate
```

If using MongoDB and you get connection errors:
- Check password is correct in `.env`
- Verify Network Access is configured
- Try SQLite first (remove MONGODB_URI from .env)

## Step 4: Populate Initial Data

```bash
python3 manage.py populate_data
```

This creates 8 default service categories.

## Step 5: Create Admin User

```bash
python3 manage.py createsuperuser
```

Follow the prompts to create an admin account.

## Step 6: Run the Server

```bash
python3 manage.py runserver
```

Then open: **http://127.0.0.1:8000/**

## Troubleshooting

### Error: "Module not found"
```bash
pip3 install -r requirements.txt
```

### Error: "Database connection failed" (MongoDB)
- Check `.env` file exists and has correct password
- Verify MongoDB Atlas Network Access
- Or remove `MONGODB_URI` from `.env` to use SQLite

### Error: "No migrations to apply"
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### Error: "Port 8000 already in use"
```bash
python3 manage.py runserver 8001
```

## Verify Everything Works

1. ✅ Server starts without errors
2. ✅ Can access http://127.0.0.1:8000/
3. ✅ Can register/login
4. ✅ Can access admin panel
5. ✅ Database operations work

## Next Steps After Running

1. Login at: http://127.0.0.1:8000/login/
2. Register as different user types
3. Test all modules:
   - Vehicle Owner: Add vehicles, book services
   - Service Center: Manage bookings, assign mechanics
   - Mechanic: View and update tasks
   - Admin: Manage users and categories

