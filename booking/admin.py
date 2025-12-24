from django.contrib import admin
from .models import (
    User, ServiceCenter, Vehicle, Mechanic, ServiceCategory,
    Booking, Invoice, Inventory, Feedback, MechanicRequest
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'phone', 'is_active', 'created_at']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'email', 'phone']


@admin.register(ServiceCenter)
class ServiceCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'phone', 'email', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'phone', 'email']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'brand', 'model', 'vehicle_type', 'owner', 'year']
    list_filter = ['vehicle_type', 'year']
    search_fields = ['registration_number', 'brand', 'model']


@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    list_display = ['user', 'service_center', 'specialization', 'is_active']
    list_filter = ['is_active', 'service_center']
    search_fields = ['user__username', 'specialization']


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_price', 'is_active']
    list_filter = ['is_active']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicle', 'service_center', 'status', 'booking_date', 'estimated_cost']
    list_filter = ['status', 'booking_date', 'service_center']
    search_fields = ['vehicle__registration_number', 'service_center__name']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'booking', 'total', 'payment_status', 'created_at']
    list_filter = ['payment_status', 'created_at']
    search_fields = ['invoice_number']


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'service_center', 'quantity', 'unit_price', 'reorder_level']
    list_filter = ['service_center']
    search_fields = ['item_name']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['booking', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']


@admin.register(MechanicRequest)
class MechanicRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'service_center', 'handled', 'created_at']
    list_filter = ['handled', 'created_at', 'service_center']
    search_fields = ['user__username', 'message']
    readonly_fields = ['created_at']



