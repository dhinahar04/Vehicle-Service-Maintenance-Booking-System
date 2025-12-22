from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Common URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('change-password/', views.change_password, name='change_password'),
    
    # Vehicle Owner URLs
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path('vehicles/', views.my_vehicles, name='my_vehicles'),
    path('book-service/', views.book_service, name='book_service'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:booking_id>/feedback/', views.add_feedback, name='add_feedback'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('invoice/<int:booking_id>/', views.view_invoice, name='view_invoice'),
    
    # Service Center URLs
    path('service-center/profile/', views.service_center_profile, name='service_center_profile'),
    path('service-center/bookings/', views.manage_bookings, name='manage_bookings'),
    path('service-center/booking/<int:booking_id>/update/', views.update_booking_status, name='update_booking_status'),
    path('service-center/mechanics/', views.manage_mechanics, name='manage_mechanics'),
    path('service-center/mechanics/add/', views.add_mechanic, name='add_mechanic'),
    path('service-center/inventory/', views.manage_inventory, name='manage_inventory'),
    path('service-center/analytics/', views.analytics, name='analytics'),
    
    # Mechanic URLs
    path('mechanic/tasks/', views.mechanic_tasks, name='mechanic_tasks'),
    path('mechanic/task/<int:booking_id>/update/', views.update_task_status, name='update_task_status'),
    path('mechanic/request-profile/', views.request_mechanic_profile, name='request_mechanic_profile'),
    path('invoice/<int:booking_id>/pay/', views.pay_invoice, name='pay_invoice'),
    
    # Admin URLs
    path('admin/centers/', views.admin_manage_centers, name='admin_manage_centers'),
    path('admin/users/', views.admin_manage_users, name='admin_manage_users'),
    path('admin/categories/', views.admin_manage_categories, name='admin_manage_categories'),
]



