from django.contrib import admin
from .models import SparePart, InventoryTransaction


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_center', 'part_number', 'quantity', 'unit_price', 'is_low_stock']
    list_filter = ['service_center', 'category']
    search_fields = ['name', 'part_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ['spare_part', 'transaction_type', 'quantity', 'unit_price', 'created_at', 'created_by']
    list_filter = ['transaction_type', 'created_at']
    readonly_fields = ['created_at']

