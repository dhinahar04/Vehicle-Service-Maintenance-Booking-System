from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Sum, Avg
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Booking, Service, ServiceCategory, Feedback
from vehicles.models import Vehicle
from accounts.models import ServiceCenter, Mechanic
from payments.models import Invoice
from notifications.models import Notification


@login_required
def booking_list(request):
    """List all bookings for the user"""
    if request.user.is_customer:
        bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    elif request.user.is_service_center:
        service_center = request.user.service_center_profile
        bookings = Booking.objects.filter(service_center=service_center).order_by('-created_at')
    else:
        bookings = Booking.objects.all().order_by('-created_at')
    
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    return render(request, 'bookings/list.html', {'bookings': bookings})


@login_required
def booking_create(request):
    """Create a new booking"""
    if not request.user.is_customer:
        messages.error(request, 'Only customers can create bookings.')
        return redirect('accounts:dashboard')
    
    vehicles = Vehicle.objects.filter(owner=request.user)
    service_centers = ServiceCenter.objects.filter(is_active=True)
    categories = ServiceCategory.objects.filter(is_active=True)
    
    if request.method == 'POST':
        try:
            vehicle = get_object_or_404(Vehicle, pk=request.POST.get('vehicle'), owner=request.user)
            service_center = get_object_or_404(ServiceCenter, pk=request.POST.get('service_center'))
            service = get_object_or_404(Service, pk=request.POST.get('service'))
            
            booking_date_str = request.POST.get('booking_date')
            booking_date = datetime.strptime(booking_date_str, '%Y-%m-%dT%H:%M')
            
            booking = Booking.objects.create(
                customer=request.user,
                service_center=service_center,
                vehicle=vehicle,
                service=service,
                booking_date=booking_date,
                preferred_time_slot=request.POST.get('preferred_time_slot', ''),
                problem_description=request.POST.get('problem_description'),
                estimated_cost=service.base_price,
            )
            
            # Create notification
            Notification.objects.create(
                user=request.user,
                notification_type='booking',
                title='Booking Confirmed',
                message=f'Your booking for {service.name} has been created successfully. Booking ID: #{booking.id}'
            )
            
            messages.success(request, 'Booking created successfully!')
            return redirect('bookings:detail', pk=booking.pk)
        except Exception as e:
            messages.error(request, f'Error creating booking: {str(e)}')
    
    return render(request, 'bookings/create.html', {
        'vehicles': vehicles,
        'service_centers': service_centers,
        'categories': categories,
    })


@login_required
def booking_detail(request, pk):
    """Booking detail view"""
    booking = get_object_or_404(Booking, pk=pk)
    
    # Check permissions
    if request.user.is_customer and booking.customer != request.user:
        messages.error(request, 'You do not have permission to view this booking.')
        return redirect('bookings:list')
    
    if request.user.is_service_center and booking.service_center != request.user.service_center_profile:
        messages.error(request, 'You do not have permission to view this booking.')
        return redirect('bookings:list')
    
    # Get invoice if exists
    invoice = None
    try:
        invoice = booking.invoice
    except Invoice.DoesNotExist:
        pass
    
    # Get feedback if exists
    feedback = None
    try:
        feedback = booking.feedback
    except Feedback.DoesNotExist:
        pass
    
    return render(request, 'bookings/detail.html', {
        'booking': booking,
        'invoice': invoice,
        'feedback': feedback,
    })


@login_required
def booking_update_status(request, pk):
    """Update booking status (Service Center only)"""
    if not request.user.is_service_center:
        messages.error(request, 'Only service centers can update booking status.')
        return redirect('accounts:dashboard')
    
    booking = get_object_or_404(Booking, pk=pk, service_center=request.user.service_center_profile)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        mechanic_id = request.POST.get('mechanic')
        
        if new_status in ['accepted', 'in_progress'] and mechanic_id:
            mechanic = get_object_or_404(Mechanic, pk=mechanic_id, service_center=request.user.service_center_profile)
            booking.mechanic = mechanic
        
        if new_status == 'in_progress' and not booking.service_started_at:
            booking.service_started_at = timezone.now()
        
        if new_status == 'completed' and not booking.service_completed_at:
            booking.service_completed_at = timezone.now()
        
        booking.status = new_status
        booking.notes = request.POST.get('notes', booking.notes)
        booking.actual_cost = request.POST.get('actual_cost') or booking.actual_cost
        booking.save()
        
        # Create notification
        Notification.objects.create(
            user=booking.customer,
            notification_type='status_update',
            title='Booking Status Updated',
            message=f'Your booking #{booking.id} status has been updated to {booking.get_status_display()}'
        )
        
        messages.success(request, 'Booking status updated successfully!')
        return redirect('bookings:detail', pk=booking.pk)
    
    mechanics = Mechanic.objects.filter(service_center=request.user.service_center_profile, is_available=True)
    return render(request, 'bookings/update_status.html', {
        'booking': booking,
        'mechanics': mechanics,
    })


@login_required
def get_services(request):
    """AJAX endpoint to get services for a service center"""
    from django.http import JsonResponse
    
    service_center_id = request.GET.get('service_center_id')
    category_id = request.GET.get('category_id')
    
    services = Service.objects.filter(service_center_id=service_center_id, is_active=True)
    
    if category_id:
        services = services.filter(category_id=category_id)
    
    services_data = [{
        'id': s.id,
        'name': s.name,
        'price': float(s.base_price),
        'duration': float(s.duration_hours)
    } for s in services]
    
    return JsonResponse({'services': services_data})


@login_required
def feedback_create(request, pk):
    """Create feedback for a completed booking"""
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    
    if booking.status != 'completed':
        messages.error(request, 'You can only provide feedback for completed bookings.')
        return redirect('bookings:detail', pk=booking.pk)
    
    if Feedback.objects.filter(booking=booking).exists():
        messages.error(request, 'You have already provided feedback for this booking.')
        return redirect('bookings:detail', pk=booking.pk)
    
    if request.method == 'POST':
        feedback = Feedback.objects.create(
            booking=booking,
            customer=request.user,
            service_center=booking.service_center,
            rating=int(request.POST.get('rating')),
            comment=request.POST.get('comment', ''),
        )
        
        # Update service center rating
        service_center = booking.service_center
        total_feedbacks = Feedback.objects.filter(service_center=service_center).count()
        avg_rating = Feedback.objects.filter(service_center=service_center).aggregate(
            avg=models.Avg('rating')
        )['avg'] or 0
        
        service_center.rating = round(avg_rating, 2)
        service_center.total_reviews = total_feedbacks
        service_center.save()
        
        messages.success(request, 'Thank you for your feedback!')
        return redirect('bookings:detail', pk=booking.pk)
    
    return render(request, 'bookings/feedback.html', {'booking': booking})

