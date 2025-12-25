# 🚀 START HERE - Run Your Project

## Quick Start (Easiest Way)

### For macOS/Linux:
```bash
cd "/Users/dhina/Desktop/Vehicle Service Booking System"
./run_project.sh
```

### For Windows:
```bash
cd "C:\Users\dhina\Desktop\Vehicle Service Booking System"
run_project.bat
```

The script will automatically:
- ✅ Check dependencies
- ✅ Setup database
- ✅ Run migrations
- ✅ Start the server

---

## Manual Setup (Step by Step)

### Step 1: Install Dependencies
```bash
pip3 install -r requirements.txt
```

### Step 2: Setup Database

**Option A: Use SQLite (Default - Works Immediately)**
- No setup needed! Just run migrations:
```bash
python3 manage.py migrate
python3 manage.py populate_data
```

**Option B: Connect to MongoDB**

1. Get your MongoDB password from [MongoDB Atlas](https://cloud.mongodb.com/)

2. Create `.env` file:
```bash
nano .env
```

3. Add this (replace `YOUR_PASSWORD`):
```env
DJANGO_SECRET_KEY=django-insecure-vehicle-service-booking-system-2024
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
MONGODB_URI=mongodb+srv://dhinaharmurugesan:YOUR_PASSWORD@vehiclemanagement.8kw7dqf.mongodb.net/vehicle_management?retryWrites=true&w=majority
```

4. Configure MongoDB Network Access:
   - Go to MongoDB Atlas → Network Access
   - Add IP Address → Add Current IP Address

### Step 3: Run Migrations
```bash
python3 manage.py migrate
python3 manage.py populate_data
```

### Step 4: Create Admin User (Optional)
```bash
python3 manage.py createsuperuser
```

### Step 5: Start Server
```bash
python3 manage.py runserver
```

---

## Access Your Application

- **Home Page**: http://127.0.0.1:8000/
- **Login**: http://127.0.0.1:8000/login/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Register**: http://127.0.0.1:8000/register/

---

## Troubleshooting

### ❌ "Module not found"
```bash
pip3 install -r requirements.txt
```

### ❌ "Database connection failed" (MongoDB)
- Check `.env` file has correct password
- Verify MongoDB Atlas Network Access
- Or remove `MONGODB_URI` from `.env` to use SQLite

### ❌ "Port 8000 already in use"
```bash
python3 manage.py runserver 8001
```

### ❌ "No such file or directory"
Make sure you're in the project directory:
```bash
cd "/Users/dhina/Desktop/Vehicle Service Booking System"
```

---

## ✅ Verification Checklist

After running, verify:
- [ ] Server starts without errors
- [ ] Can access http://127.0.0.1:8000/
- [ ] Can register new users
- [ ] Can login
- [ ] Database operations work

---

## 🎯 Next Steps

1. **Create Test Users:**
   - Register as Vehicle Owner
   - Register as Service Center
   - Register as Mechanic

2. **Test Features:**
   - Add vehicles
   - Book services
   - Manage bookings
   - Generate invoices

3. **Deploy to Production:**
   - See `DEPLOYMENT.md` for Render deployment
   - See `MONGODB_SETUP.md` for MongoDB setup

---

**Your project is ready to run! 🚀**

