from django.db import models
from accounts.models import User


class Vehicle(models.Model):
    """Vehicle Model"""
    VEHICLE_TYPE_CHOICES = [
        ('car', 'Car'),
        ('motorcycle', 'Motorcycle'),
        ('truck', 'Truck'),
        ('suv', 'SUV'),
        ('van', 'Van'),
        ('other', 'Other'),
    ]
    
    FUEL_TYPE_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
        ('cng', 'CNG'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)
    registration_number = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=50, blank=True)
    mileage = models.IntegerField(default=0)
    vin_number = models.CharField(max_length=50, blank=True)
    insurance_number = models.CharField(max_length=100, blank=True)
    insurance_expiry = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.make} {self.model} ({self.registration_number})"


class MaintenanceReminder(models.Model):
    """Maintenance Reminder Model"""
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=100)  # oil_change, service, insurance, etc.
    due_date = models.DateField()
    mileage_due = models.IntegerField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['due_date']
    
    def __str__(self):
        return f"{self.vehicle} - {self.reminder_type}"

