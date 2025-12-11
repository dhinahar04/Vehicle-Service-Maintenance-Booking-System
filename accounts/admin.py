from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ServiceCenter, Mechanic


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'phone', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'is_staff']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'address', 'profile_picture')}),
    )


@admin.register(ServiceCenter)
class ServiceCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'phone', 'is_active', 'rating', 'created_at']
    list_filter = ['is_active', 'city', 'state']
    search_fields = ['name', 'city', 'license_number']


@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_center', 'specialization', 'is_available']
    list_filter = ['is_available', 'service_center']
    search_fields = ['name', 'specialization']

