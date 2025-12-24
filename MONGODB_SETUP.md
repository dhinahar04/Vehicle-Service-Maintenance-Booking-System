# MongoDB Atlas Connection Setup

## Your MongoDB Connection String

```
mongodb+srv://dhinaharmurugesan:<db_password>@vehiclemanagement.8kw7dqf.mongodb.net/?appName=vehicleManagement
```

## Steps to Connect

### 1. Get Your MongoDB Password

1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Login to your account
3. Go to **Database Access** → Find user `dhinaharmurugesan`
4. Click **Edit** → **Edit Password** → Copy your password

### 2. Update Connection String

Replace `<db_password>` in the connection string with your actual password:

**Format:**
```
mongodb+srv://dhinaharmurugesan:YOUR_ACTUAL_PASSWORD@vehiclemanagement.8kw7dqf.mongodb.net/vehicle_management?retryWrites=true&w=majority
```

**Example (if password is `mypass123`):**
```
mongodb+srv://dhinaharmurugesan:mypass123@vehiclemanagement.8kw7dqf.mongodb.net/vehicle_management?retryWrites=true&w=majority
```

### 3. For Local Development

Create a `.env` file in the project root:

```bash
cd "/Users/dhina/Desktop/Vehicle Service Booking System"
```

Create `.env` file:
```env
MONGODB_URI=mongodb+srv://dhinaharmurugesan:YOUR_PASSWORD@vehiclemanagement.8kw7dqf.mongodb.net/vehicle_management?retryWrites=true&w=majority
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
```

**Important:** Replace `YOUR_PASSWORD` with your actual MongoDB password.

### 4. For Render Deployment

In Render Dashboard → Your Web Service → Environment Variables:

Add:
- **Key:** `MONGODB_URI`
- **Value:** `mongodb+srv://dhinaharmurugesan:YOUR_PASSWORD@vehiclemanagement.8kw7dqf.mongodb.net/vehicle_management?retryWrites=true&w=majority`

(Replace `YOUR_PASSWORD` with your actual password)

### 5. MongoDB Atlas Network Access

Make sure your MongoDB Atlas allows connections:

1. Go to MongoDB Atlas → **Network Access**
2. Click **Add IP Address**
3. For local: Add your current IP
4. For Render: Add `0.0.0.0/0` (allow all IPs) or Render's IP ranges

### 6. Test Connection

After setting up, test the connection:

```bash
python manage.py migrate
```

If it works, you'll see migrations running. If you get connection errors, check:
- Password is correct
- Network Access is configured
- Connection string format is correct

## Database Name

The database will be created as: **`vehicle_management`**

All your Django models will be stored in this database.

