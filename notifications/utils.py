"""
Notification utility functions for sending SMS and Email notifications
"""
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Notification
from accounts.models import User


def send_notification(user, notification_type, title, message):
    """Create an in-app notification"""
    Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message
    )


def send_email_notification(user, subject, message, html_message=None):
    """Send email notification"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


def send_sms_notification(phone_number, message):
    """Send SMS notification using Twilio"""
    try:
        from twilio.rest import Client
        
        if not all([settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, settings.TWILIO_PHONE_NUMBER]):
            print("Twilio credentials not configured")
            return False
        
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return True
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return False


def notify_booking_created(booking):
    """Notify customer when booking is created"""
    user = booking.customer
    title = "Booking Confirmed"
    message = f"Your booking #{booking.id} for {booking.service.name} has been confirmed. Booking date: {booking.booking_date.strftime('%B %d, %Y at %I:%M %p')}"
    
    send_notification(user, 'booking', title, message)
    
    # Send email
    email_subject = f"Booking Confirmed - #{booking.id}"
    email_message = f"""
    Hello {user.username},
    
    Your service booking has been confirmed!
    
    Booking Details:
    - Booking ID: #{booking.id}
    - Service: {booking.service.name}
    - Vehicle: {booking.vehicle.make} {booking.vehicle.model}
    - Service Center: {booking.service_center.name}
    - Date: {booking.booking_date.strftime('%B %d, %Y at %I:%M %p')}
    
    Thank you for choosing our service!
    """
    send_email_notification(user, email_subject, email_message)
    
    # Send SMS if phone number is available
    if user.phone:
        sms_message = f"Booking #{booking.id} confirmed for {booking.service.name} on {booking.booking_date.strftime('%B %d, %Y')}"
        send_sms_notification(user.phone, sms_message)


def notify_booking_status_update(booking):
    """Notify customer when booking status is updated"""
    user = booking.customer
    title = "Booking Status Updated"
    message = f"Your booking #{booking.id} status has been updated to: {booking.get_status_display()}"
    
    send_notification(user, 'status_update', title, message)
    
    # Send email
    email_subject = f"Booking Status Updated - #{booking.id}"
    email_message = f"""
    Hello {user.username},
    
    Your booking status has been updated!
    
    Booking ID: #{booking.id}
    New Status: {booking.get_status_display()}
    Service: {booking.service.name}
    
    You can track your booking status in your dashboard.
    """
    send_email_notification(user, email_subject, email_message)
    
    # Send SMS if phone number is available
    if user.phone:
        sms_message = f"Booking #{booking.id} status: {booking.get_status_display()}"
        send_sms_notification(user.phone, sms_message)


def notify_invoice_generated(invoice):
    """Notify customer when invoice is generated"""
    user = invoice.customer
    title = "Invoice Generated"
    message = f"Invoice #{invoice.invoice_number} has been generated for your booking. Total amount: ${invoice.total_amount}"
    
    send_notification(user, 'invoice', title, message)
    
    # Send email
    email_subject = f"Invoice Generated - #{invoice.invoice_number}"
    email_message = f"""
    Hello {user.username},
    
    Your invoice has been generated!
    
    Invoice Number: {invoice.invoice_number}
    Total Amount: ${invoice.total_amount}
    Due Date: {invoice.due_date.strftime('%B %d, %Y') if invoice.due_date else 'N/A'}
    
    Please make payment at your earliest convenience.
    """
    send_email_notification(user, email_subject, email_message)


def notify_maintenance_reminder(reminder):
    """Notify customer about maintenance reminder"""
    user = reminder.vehicle.owner
    title = "Maintenance Reminder"
    message = f"Reminder: {reminder.reminder_type} is due for your {reminder.vehicle.make} {reminder.vehicle.model} on {reminder.due_date.strftime('%B %d, %Y')}"
    
    send_notification(user, 'reminder', title, message)
    
    # Send email
    email_subject = f"Maintenance Reminder - {reminder.reminder_type}"
    email_message = f"""
    Hello {user.username},
    
    This is a reminder for your vehicle maintenance!
    
    Vehicle: {reminder.vehicle.make} {reminder.vehicle.model} ({reminder.vehicle.registration_number})
    Maintenance Type: {reminder.reminder_type}
    Due Date: {reminder.due_date.strftime('%B %d, %Y')}
    
    Please schedule a service appointment soon.
    """
    send_email_notification(user, email_subject, email_message)
    
    # Send SMS if phone number is available
    if user.phone:
        sms_message = f"Reminder: {reminder.reminder_type} due on {reminder.due_date.strftime('%B %d, %Y')} for {reminder.vehicle.make} {reminder.vehicle.model}"
        send_sms_notification(user.phone, sms_message)

