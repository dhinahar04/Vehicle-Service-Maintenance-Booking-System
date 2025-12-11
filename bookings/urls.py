from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.booking_list, name='list'),
    path('create/', views.booking_create, name='create'),
    path('<int:pk>/', views.booking_detail, name='detail'),
    path('<int:pk>/update-status/', views.booking_update_status, name='update_status'),
    path('<int:pk>/feedback/', views.feedback_create, name='feedback'),
    path('api/services/', views.get_services, name='get_services'),
]

