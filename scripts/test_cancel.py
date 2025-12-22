from django.test import Client
from booking.models import *
from django.utils import timezone
from decimal import Decimal

u = User.objects.filter(role='owner').first()
print('owner:', u)
if not u:
    print('no owner found')
else:
    v = Vehicle.objects.filter(owner=u).first()
    sc = ServiceCenter.objects.first()
    if not sc:
        sc_user = User.objects.filter(role='service_center').first() or u
        sc = ServiceCenter.objects.create(name='Demo Center', user=sc_user, is_active=True)
    if not v:
        v = Vehicle.objects.create(owner=u, brand='TestBrand', model='T1', vehicle_type='car', year=2020, registration_number='TEST123', color='Grey', mileage=10000)
    cat = ServiceCategory.objects.first() or ServiceCategory.objects.create(name='TestService', base_price=Decimal('500.00'))
    b = Booking.objects.create(vehicle=v, service_center=sc, service_category=cat, booking_date=timezone.now().date(), booking_time=timezone.now().time(), service_description='Test booking', estimated_cost=Decimal('1000.00'), status='pending')
    print('created booking', b.id)
    client = Client()
    client.force_login(u)
    resp = client.post(f'/booking/{b.id}/cancel/')
    print('response status', resp.status_code)
    b.refresh_from_db()
    print('booking status after cancel:', b.status)
