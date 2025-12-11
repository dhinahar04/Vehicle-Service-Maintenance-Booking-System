from django.db import models
from accounts.models import User


class Notification(models.Model):
    """Notification Model"""
    NOTIFICATION_TYPE_CHOICES = [
        ('booking', 'Booking'),
        ('status_update', 'Status Update'),
        ('reminder', 'Reminder'),
        ('invoice', 'Invoice'),
        ('payment', 'Payment'),
        ('system', 'System'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"

