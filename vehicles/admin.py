from django.contrib import admin
from .models import Vehicle, MaintenanceReminder


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'registration_number', 'owner', 'vehicle_type', 'year']
    list_filter = ['vehicle_type', 'fuel_type', 'year']
    search_fields = ['make', 'model', 'registration_number', 'vin_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MaintenanceReminder)
class MaintenanceReminderAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'reminder_type', 'due_date', 'is_completed']
    list_filter = ['reminder_type', 'is_completed']
    search_fields = ['vehicle__make', 'vehicle__model']

