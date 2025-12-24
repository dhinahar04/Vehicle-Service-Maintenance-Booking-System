# Deployment Guide for Render

## Environment Variables for Render

Add these in **Render Dashboard → Your Web Service → Environment**:

### Required Variables:

1. **PYTHON_VERSION**
   ```
   3.10.13
   ```

2. **DJANGO_SECRET_KEY**
   ```
   (Generate a long random string - use Django secret key generator)
   ```

3. **DJANGO_DEBUG**
   ```
   False
   ```

4. **DJANGO_ALLOWED_HOSTS**
   ```
   your-service-name.onrender.com
   ```
   Replace `your-service-name` with your actual Render service name.

5. **MONGODB_URI**
   ```
   mongodb+srv://dhinaharmurugesan:YOUR_PASSWORD@vehiclemanagement.8kw7dqf.mongodb.net/vehicle_management?retryWrites=true&w=majority
   ```
   **Important**: Replace `YOUR_PASSWORD` with your actual MongoDB Atlas password.

### Optional Email Variables (if you need email functionality):

6. **EMAIL_HOST**
   ```
   smtp.gmail.com
   ```
   (or your SMTP provider)

7. **EMAIL_HOST_USER**
   ```
   your-email@gmail.com
   ```

8. **EMAIL_HOST_PASSWORD**
   ```
   your-app-password
   ```

9. **EMAIL_PORT**
   ```
   587
   ```

10. **EMAIL_USE_TLS**
    ```
    True
    ```

## Start Command

In Render → Your Web Service → Settings → Start Command:

```bash
bash -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn vehicle_service.wsgi:application"
```

## Build Command

```bash
pip install -r requirements.txt
```

## MongoDB Atlas Setup

1. Go to MongoDB Atlas: https://www.mongodb.com/cloud/atlas
2. Create a database user (if not already created)
3. Get your connection string
4. Replace `<db_password>` with your actual password
5. Add the full connection string to `MONGODB_URI` environment variable in Render

## Important Notes

- Make sure your MongoDB Atlas IP whitelist includes `0.0.0.0/0` (all IPs) for Render deployment
- The database name in the connection string should be `vehicle_management`
- If MongoDB connection fails, the app will fallback to SQLite (for local development only)

## After Deployment

1. Access your app at: `https://your-service-name.onrender.com`
2. Create a superuser:
   - Go to Render → Shell
   - Run: `python manage.py createsuperuser`
3. Populate initial data:
   - Run: `python manage.py populate_data`

