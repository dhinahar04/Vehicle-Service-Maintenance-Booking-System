from django.db import models
from accounts.models import ServiceCenter


class SparePart(models.Model):
    """Spare Parts Inventory Model"""
    service_center = models.ForeignKey(ServiceCenter, on_delete=models.CASCADE, related_name='spare_parts')
    name = models.CharField(max_length=200)
    part_number = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    min_stock_level = models.IntegerField(default=5)
    supplier = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ['service_center', 'part_number']
    
    def __str__(self):
        return f"{self.name} - {self.service_center.name}"
    
    @property
    def is_low_stock(self):
        return self.quantity <= self.min_stock_level


class InventoryTransaction(models.Model):
    """Inventory Transaction History"""
    TRANSACTION_TYPE_CHOICES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjustment', 'Adjustment'),
    ]
    
    spare_part = models.ForeignKey(SparePart, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transaction_type} - {self.spare_part.name} - Qty: {self.quantity}"

