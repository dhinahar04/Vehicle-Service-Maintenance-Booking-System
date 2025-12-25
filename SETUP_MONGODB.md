# MongoDB Database Setup Instructions

## Your MongoDB Connection String

```
mongodb+srv://dhinaharmurugesan:<db_password>@vehiclemanagement.8kw7dqf.mongodb.net/?appName=vehicleManagement
```

## Step-by-Step Setup

### Step 1: Get Your MongoDB Password

1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Log in to your account
3. Navigate to **Database Access** → Find user `dhinaharmurugesan`
4. Click **Edit** → **Edit Password** → Copy your password

### Step 2: Create .env File

Create a `.env` file in your project root directory:

```bash
cd "/Users/dhina/Desktop/Vehicle Service Booking System"
```

### Step 3: Add MongoDB Connection

Open the `.env` file and add your MongoDB connection string:

**IMPORTANT:** Replace `<db_password>` with your actual MongoDB password!

```env
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*

# MongoDB Atlas Connection
# Replace <db_password> with your actual password
MONGODB_URI=mongodb+srv://dhinaharmurugesan:YOUR_ACTUAL_PASSWORD@vehiclemanagement.8kw7dqf.mongodb.net/vehicle_management?retryWrites=true&w=majority
```

**Example** (if your password is `mypass123`):
```env
MONGODB_URI=mongodb+srv://dhinaharmurugesan:mypass123@vehiclemanagement.8kw7dqf.mongodb.net/vehicle_management?retryWrites=true&w=majority
```

### Step 4: Configure MongoDB Atlas Network Access

1. Go to MongoDB Atlas → **Network Access**
2. Click **Add IP Address**
3. For local development: Click **Add Current IP Address**
4. For production/Render: Add `0.0.0.0/0` (allow all IPs) or specific Render IP ranges

### Step 5: Test the Connection

Run migrations to test the connection:

```bash
python manage.py migrate
```

If successful, you'll see:
```
Operations to perform:
  Apply all migrations: ...
Running migrations:
  ...
```

If you get connection errors, check:
- ✅ Password is correct in `.env` file
- ✅ Network Access is configured in MongoDB Atlas
- ✅ Connection string format is correct

### Step 6: Populate Initial Data

After successful connection, populate service categories:

```bash
python manage.py populate_data
```

## Database Name

The database will be created as: **`vehicle_management`**

All your Django models will be stored in this database.

## Security Notes

- ⚠️ **Never commit `.env` file to GitHub** (it's already in `.gitignore`)
- ⚠️ **Never share your MongoDB password**
- ✅ Use environment variables in production (Render, etc.)

## Troubleshooting

### Error: "Server selection timed out"
- Check Network Access in MongoDB Atlas
- Verify your IP is whitelisted

### Error: "Authentication failed"
- Verify password is correct
- Check username is `dhinaharmurugesan`

### Error: "Connection refused"
- Check MongoDB Atlas cluster is running
- Verify connection string format

## For Production (Render)

In Render Dashboard → Environment Variables, add:

- **Key:** `MONGODB_URI`
- **Value:** `mongodb+srv://dhinaharmurugesan:YOUR_PASSWORD@vehiclemanagement.8kw7dqf.mongodb.net/vehicle_management?retryWrites=true&w=majority`

Replace `YOUR_PASSWORD` with your actual password.

