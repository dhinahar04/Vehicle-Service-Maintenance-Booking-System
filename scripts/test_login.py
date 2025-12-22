import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vehicle_service.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()

username = 'testuser'
password = 'testpass'

if not User.objects.filter(username=username).exists():
    print('Creating test user...')
    User.objects.create_user(username=username, password=password, email='test@example.com', role='owner')
else:
    print('Test user already exists')

c = Client()
print('Attempting login...')
r = c.post('/login/', {'username': username, 'password': password})
print('Status code:', r.status_code)
print('Redirect chain:', r.redirect_chain)
# Show final content snippet
content = r.content.decode('utf-8', errors='replace')
print('Response content (first 1000 chars):')
print(content[:1000])
