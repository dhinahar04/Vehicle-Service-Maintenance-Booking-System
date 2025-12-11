from django.urls import path
from . import views

app_name = 'service_centers'

urlpatterns = [
    path('create-profile/', views.create_profile, name='create_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bookings/', views.manage_bookings, name='manage_bookings'),
    path('mechanics/', views.manage_mechanics, name='manage_mechanics'),
    path('services/', views.manage_services, name='manage_services'),
    path('analytics/', views.analytics, name='analytics'),
]

