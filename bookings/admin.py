from django.contrib import admin
from .models import ServiceCategory, Service, Booking, BookingStatusUpdate, Feedback


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_center', 'category', 'base_price', 'is_active']
    list_filter = ['category', 'is_active', 'service_center']
    search_fields = ['name', 'description']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'service_center', 'vehicle', 'service', 'status', 'booking_date', 'created_at']
    list_filter = ['status', 'booking_date', 'service_center']
    search_fields = ['customer__username', 'vehicle__registration_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(BookingStatusUpdate)
class BookingStatusUpdateAdmin(admin.ModelAdmin):
    list_display = ['booking', 'status', 'updated_by', 'created_at']
    list_filter = ['status', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['booking', 'customer', 'service_center', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['customer__username', 'service_center__name']

