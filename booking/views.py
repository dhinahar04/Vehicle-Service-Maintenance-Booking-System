from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from datetime import datetime, timedelta
import json
from django.db.models.functions import TruncMonth
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings

from .models import (
    User, Vehicle, ServiceCenter, Mechanic, Booking,
    ServiceCategory, Invoice, Inventory, Feedback
)
from .forms import (
    UserRegistrationForm, VehicleForm, BookingForm,
    FeedbackForm, InventoryForm, CustomPasswordChangeForm
)


@login_required
def pay_invoice(request, booking_id):
    """Simple simulated payment endpoint: allows the vehicle owner to mark
    the booking's invoice as paid (creates the invoice if it doesn't exist).
    This is a placeholder for a real payment gateway integration.
    """
    booking = get_object_or_404(Booking, id=booking_id)

    # Only the vehicle owner may pay
    if booking.vehicle.owner != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    try:
        invoice = booking.invoice
    except Invoice.DoesNotExist:
        # Create invoice if missing
        invoice_number = f"INV-{booking.id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        # Ensure Decimal arithmetic (booking fields are DecimalFields)
        subtotal = booking.actual_cost or booking.estimated_cost
        subtotal = Decimal(subtotal)
        tax = (subtotal * Decimal('0.18')).quantize(Decimal('0.01'))
        total = (subtotal + tax).quantize(Decimal('0.01'))
        invoice = Invoice.objects.create(
            booking=booking,
            invoice_number=invoice_number,
            subtotal=subtotal,
            tax=tax,
            total=total,
            payment_status='pending'
        )

    # Simulate payment success
    invoice.payment_status = 'paid'
    invoice.paid_at = timezone.now()
    invoice.save()

    messages.success(request, 'Payment received. Thank you!')
    return redirect('view_invoice', booking_id=booking.id)


@login_required
def request_mechanic_profile(request):
    """Allow a mechanic to request a Mechanic profile. The request is stored
    so service center admins can review it.
    """
    if request.method == 'POST':
        sc_id = request.POST.get('service_center')
        message = request.POST.get('message', '')
        sc = None
        if sc_id:
            try:
                sc = ServiceCenter.objects.get(id=int(sc_id))
            except (ValueError, ServiceCenter.DoesNotExist):
                sc = None

        # Create a MechanicRequest record
        from .models import MechanicRequest
        MechanicRequest.objects.create(user=request.user, service_center=sc, message=message)
        messages.success(request, 'Your request has been submitted. Please contact your service center admin for follow up.')
        return redirect('dashboard')

    # GET: show a small form listing available service centers
    service_centers = ServiceCenter.objects.all().order_by('name')
    return render(request, 'booking/mechanic/request_profile.html', {'service_centers': service_centers})


def home(request):
    """Home page"""
    service_centers = ServiceCenter.objects.filter(is_active=True)[:6]
    return render(request, 'booking/home.html', {'service_centers': service_centers})


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'booking/register.html', {'form': form})


def user_login(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'booking/login.html')


@login_required
def dashboard(request):
    """Dashboard based on user role"""
    user = request.user
    
    if user.role == 'owner':
        vehicles = Vehicle.objects.filter(owner=user)
        bookings = Booking.objects.filter(vehicle__owner=user).order_by('-created_at')[:10]
        # Owner invoices: all invoices for bookings belonging to this owner's vehicles
        invoices = Invoice.objects.filter(booking__vehicle__owner=user).order_by('-created_at')
        context = {
            'vehicles': vehicles,
            'bookings': bookings,
            'invoices': invoices,
            'total_bookings': Booking.objects.filter(vehicle__owner=user).count(),
            'pending_bookings': Booking.objects.filter(vehicle__owner=user, status='pending').count(),
            'completed_bookings': Booking.objects.filter(vehicle__owner=user, status='completed').count(),
        }
        return render(request, 'booking/owner/dashboard.html', context)
    
    elif user.role == 'service_center':
        try:
            service_center = user.service_center
            today = timezone.now().date()
            bookings = Booking.objects.filter(service_center=service_center).order_by('-created_at')[:10]
            
            # Analytics
            total_bookings = Booking.objects.filter(service_center=service_center).count()
            today_bookings = Booking.objects.filter(service_center=service_center, booking_date=today).count()
            pending_bookings = Booking.objects.filter(service_center=service_center, status='pending').count()
            in_progress = Booking.objects.filter(service_center=service_center, status='in_progress').count()
            
            # Revenue
            total_revenue = Invoice.objects.filter(
                booking__service_center=service_center,
                payment_status='paid'
            ).aggregate(total=Sum('total'))['total'] or 0
            
            context = {
                'service_center': service_center,
                'bookings': bookings,
                'total_bookings': total_bookings,
                'today_bookings': today_bookings,
                'pending_bookings': pending_bookings,
                'in_progress': in_progress,
                'total_revenue': total_revenue,
            }
            return render(request, 'booking/service_center/dashboard.html', context)
        except ServiceCenter.DoesNotExist:
            messages.warning(request, 'Please complete your service center profile.')
            return redirect('service_center_profile')
    
    elif user.role == 'mechanic':
        try:
            mechanic = user.mechanic
            assigned_bookings = Booking.objects.filter(
                mechanic=mechanic,
                status__in=['accepted', 'in_progress']
            ).order_by('-created_at')
            
            completed_today = Booking.objects.filter(
                mechanic=mechanic,
                status='completed',
                completed_at__date=timezone.now().date()
            ).count()
            
            context = {
                'mechanic': mechanic,
                'assigned_bookings': assigned_bookings,
                'completed_today': completed_today,
            }
            return render(request, 'booking/mechanic/dashboard.html', context)
        except Mechanic.DoesNotExist:
            # Mechanic object not found for this user — show a helpful page
            # Render a dedicated page with instructions instead of a brief warning
            return render(request, 'booking/mechanic/profile_missing.html', {'user': request.user})
    
    elif user.role == 'admin':
        total_users = User.objects.count()
        total_centers = ServiceCenter.objects.count()
        total_bookings = Booking.objects.count()
        total_revenue = Invoice.objects.filter(payment_status='paid').aggregate(total=Sum('total'))['total'] or 0
        
        context = {
            'total_users': total_users,
            'total_centers': total_centers,
            'total_bookings': total_bookings,
            'total_revenue': total_revenue,
        }
        return render(request, 'booking/admin/dashboard.html', context)
    
    return redirect('home')


@login_required
def change_password(request):
    """Change password for logged in user"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('dashboard')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'booking/change_password.html', {'form': form})


# Vehicle Owner Views
@login_required
def add_vehicle(request):
    """Add a new vehicle"""
    if request.user.role != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            messages.success(request, 'Vehicle added successfully!')
            return redirect('my_vehicles')
    else:
        form = VehicleForm()
    return render(request, 'booking/owner/add_vehicle.html', {'form': form})


@login_required
def my_vehicles(request):
    """List all vehicles of the owner"""
    if request.user.role != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    vehicles = Vehicle.objects.filter(owner=request.user)
    return render(request, 'booking/owner/my_vehicles.html', {'vehicles': vehicles})


@login_required
def book_service(request):
    """Book a service"""
    if request.user.role != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.vehicle = form.cleaned_data['vehicle']
            if booking.vehicle.owner != request.user:
                messages.error(request, 'Invalid vehicle selection.')
                return redirect('book_service')
            
            # Set estimated cost
            booking.estimated_cost = booking.service_category.base_price
            booking.save()
            messages.success(request, 'Service booked successfully!')
            return redirect('my_bookings')
    else:
        form = BookingForm()
        form.fields['vehicle'].queryset = Vehicle.objects.filter(owner=request.user)
    
    service_centers = ServiceCenter.objects.filter(is_active=True)
    service_categories = ServiceCategory.objects.filter(is_active=True)
    
    return render(request, 'booking/owner/book_service.html', {
        'form': form,
        'service_centers': service_centers,
        'service_categories': service_categories,
    })


@login_required
def my_bookings(request):
    """List all bookings of the owner"""
    if request.user.role != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    bookings = Booking.objects.filter(vehicle__owner=request.user).order_by('-created_at')
    return render(request, 'booking/owner/my_bookings.html', {'bookings': bookings})


@login_required
def booking_detail(request, booking_id):
    """View booking details"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check access
    if request.user.role == 'owner' and booking.vehicle.owner != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    elif request.user.role == 'service_center' and booking.service_center.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    elif request.user.role == 'mechanic':
        if not booking.mechanic or booking.mechanic.user != request.user:
            messages.error(request, 'Access denied.')
            return redirect('dashboard')
    
    try:
        invoice = booking.invoice
    except Invoice.DoesNotExist:
        invoice = None
    
    try:
        feedback = booking.feedback
    except Feedback.DoesNotExist:
        feedback = None
    
    context = {
        'booking': booking,
        'invoice': invoice,
        'feedback': feedback,
    }
    
    if request.user.role == 'owner':
        return render(request, 'booking/owner/booking_detail.html', context)
    elif request.user.role == 'service_center':
        return render(request, 'booking/service_center/booking_detail.html', context)
    elif request.user.role == 'mechanic':
        return render(request, 'booking/mechanic/booking_detail.html', context)
    
    return redirect('dashboard')


@login_required
def add_feedback(request, booking_id):
    """Add feedback for a completed booking"""
    if request.user.role != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    booking = get_object_or_404(Booking, id=booking_id, vehicle__owner=request.user)
    
    if booking.status != 'completed':
        messages.error(request, 'Feedback can only be added for completed bookings.')
        return redirect('booking_detail', booking_id=booking_id)
    
    if Feedback.objects.filter(booking=booking).exists():
        messages.warning(request, 'Feedback already submitted.')
        return redirect('booking_detail', booking_id=booking_id)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.booking = booking
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('booking_detail', booking_id=booking_id)
    else:
        form = FeedbackForm()
    
    return render(request, 'booking/owner/add_feedback.html', {'form': form, 'booking': booking})


# Service Center Views
@login_required
def service_center_profile(request):
    """Create or update service center profile"""
    if request.user.role != 'service_center':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    try:
        service_center = request.user.service_center
        is_update = True
    except ServiceCenter.DoesNotExist:
        service_center = None
        is_update = False
    
    if request.method == 'POST':
        from .forms import ServiceCenterForm
        form = ServiceCenterForm(request.POST, instance=service_center)
        if form.is_valid():
            service_center = form.save(commit=False)
            service_center.user = request.user
            service_center.save()
            messages.success(request, 'Profile updated successfully!' if is_update else 'Profile created successfully!')
            return redirect('dashboard')
    else:
        from .forms import ServiceCenterForm
        form = ServiceCenterForm(instance=service_center)
    
    # Pass the service_center object so the template can show a summary when editing
    return render(request, 'booking/service_center/profile.html', {
        'form': form,
        'is_update': is_update,
        'service_center': service_center,
    })


@login_required
def manage_bookings(request):
    """Service center manage bookings"""
    if request.user.role != 'service_center':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    try:
        service_center = request.user.service_center
        bookings = Booking.objects.filter(service_center=service_center).order_by('-created_at')
        
        # Filter by status if provided
        status_filter = request.GET.get('status')
        if status_filter:
            bookings = bookings.filter(status=status_filter)
        
        return render(request, 'booking/service_center/manage_bookings.html', {
            'bookings': bookings,
            'status_filter': status_filter,
        })
    except ServiceCenter.DoesNotExist:
        messages.warning(request, 'Please complete your service center profile.')
        return redirect('service_center_profile')


@login_required
def update_booking_status(request, booking_id):
    """Update booking status"""
    if request.user.role != 'service_center':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    booking = get_object_or_404(Booking, id=booking_id, service_center__user=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            
            # Create an invoice when booking is accepted so owners can pay early
            if new_status == 'accepted':
                # Create invoice if not exists (owner can pay while work hasn't started)
                try:
                    _ = booking.invoice
                except Invoice.DoesNotExist:
                    invoice_number = f"INV-{booking.id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    subtotal = booking.actual_cost or booking.estimated_cost
                    subtotal = Decimal(subtotal)
                    tax = (subtotal * Decimal('0.18')).quantize(Decimal('0.01'))
                    total = (subtotal + tax).quantize(Decimal('0.01'))
                    invoice = Invoice.objects.create(
                        booking=booking,
                        invoice_number=invoice_number,
                        subtotal=subtotal,
                        tax=tax,
                        total=total,
                        payment_status='pending'
                    )
                    # Send a simple notification email to the owner if email is configured
                    try:
                        if booking.vehicle.owner.email:
                            subject = f"Invoice {invoice.invoice_number} created for your booking"
                            message = f"Dear {booking.vehicle.owner.get_full_name() or booking.vehicle.owner.username},\n\nAn invoice (\#{invoice.invoice_number}) has been generated for your booking #{booking.id}. Total: ₹{invoice.total}. Please pay using your account.\n\nThank you."
                            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [booking.vehicle.owner.email], fail_silently=True)
                    except Exception:
                        # Silently ignore email failures in dev
                        pass

            if new_status == 'completed':
                booking.completed_at = timezone.now()
                # Create invoice if not exists
                try:
                    _ = booking.invoice
                except Invoice.DoesNotExist:
                    invoice_number = f"INV-{booking.id}-{datetime.now().strftime('%Y%m%d')}"
                    subtotal = booking.actual_cost or booking.estimated_cost
                    subtotal = Decimal(subtotal)
                    tax = (subtotal * Decimal('0.18')).quantize(Decimal('0.01'))
                    total = (subtotal + tax).quantize(Decimal('0.01'))
                    invoice = Invoice.objects.create(
                        booking=booking,
                        invoice_number=invoice_number,
                        subtotal=subtotal,
                        tax=tax,
                        total=total,
                    )
            
            booking.save()
            messages.success(request, f'Booking status updated to {booking.get_status_display()}.')
        
        # Handle mechanic assignment
        mechanic_id = request.POST.get('mechanic_id')
        if mechanic_id:
            try:
                mechanic = Mechanic.objects.get(id=mechanic_id, service_center=booking.service_center)
                booking.mechanic = mechanic
                booking.save()
                messages.success(request, 'Mechanic assigned successfully.')
            except Mechanic.DoesNotExist:
                messages.error(request, 'Invalid mechanic selection.')
        
        # Handle cost update
        actual_cost = request.POST.get('actual_cost')
        if actual_cost:
            try:
                booking.actual_cost = float(actual_cost)
                booking.save()
                messages.success(request, 'Cost updated successfully.')
            except ValueError:
                messages.error(request, 'Invalid cost value.')
    
    return redirect('booking_detail', booking_id=booking_id)


@login_required
def manage_mechanics(request):
    """Manage mechanics for service center"""
    if request.user.role != 'service_center':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    try:
        service_center = request.user.service_center
        mechanics = Mechanic.objects.filter(service_center=service_center)
        return render(request, 'booking/service_center/manage_mechanics.html', {'mechanics': mechanics})
    except ServiceCenter.DoesNotExist:
        messages.warning(request, 'Please complete your service center profile.')
        return redirect('service_center_profile')


@login_required
def add_mechanic(request):
    """Add a new mechanic"""
    if request.user.role != 'service_center':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    try:
        service_center = request.user.service_center
    except ServiceCenter.DoesNotExist:
        messages.warning(request, 'Please complete your service center profile.')
        return redirect('service_center_profile')
    
    from .forms import MechanicCreationForm

    if request.method == 'POST':
        form = MechanicCreationForm(request.POST)
        if form.is_valid():
            form.save(service_center=service_center)
            messages.success(request, 'Mechanic added successfully!')
            return redirect('manage_mechanics')
    else:
        form = MechanicCreationForm()

    return render(request, 'booking/service_center/add_mechanic.html', {'form': form})


@login_required
def manage_inventory(request):
    """Manage inventory"""
    if request.user.role != 'service_center':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    try:
        service_center = request.user.service_center
        inventory_items = Inventory.objects.filter(service_center=service_center).order_by('item_name')
        
        if request.method == 'POST':
            form = InventoryForm(request.POST)
            if form.is_valid():
                item = form.save(commit=False)
                item.service_center = service_center
                item.save()
                messages.success(request, 'Inventory item added successfully!')
                return redirect('manage_inventory')
        else:
            form = InventoryForm()
        
        return render(request, 'booking/service_center/manage_inventory.html', {
            'inventory_items': inventory_items,
            'form': form,
        })
    except ServiceCenter.DoesNotExist:
        messages.warning(request, 'Please complete your service center profile.')
        return redirect('service_center_profile')


@login_required
def analytics(request):
    """Service center analytics"""
    if request.user.role != 'service_center':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    try:
        service_center = request.user.service_center
        
        # Daily bookings (last 30 days)
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        daily_bookings = Booking.objects.filter(
            service_center=service_center,
            created_at__date__gte=thirty_days_ago
        ).values('created_at__date').annotate(count=Count('id')).order_by('created_at__date')
        
        # Most requested services
        popular_services = Booking.objects.filter(
            service_center=service_center
        ).values('service_category__name').annotate(count=Count('id')).order_by('-count')[:5]
        
        # Most frequent customers
        frequent_customers = Booking.objects.filter(
            service_center=service_center
        ).values('vehicle__owner__username').annotate(count=Count('id')).order_by('-count')[:5]
        
        # Revenue by month
        # Use TruncMonth to avoid ambiguous column names in SQL joins
        monthly_revenue = Invoice.objects.filter(
            booking__service_center=service_center,
            payment_status='paid'
        ).annotate(month=TruncMonth('created_at')).values('month').annotate(total=Sum('total')).order_by('month')
        
        context = {
            'daily_bookings': list(daily_bookings),
            'popular_services': list(popular_services),
            'frequent_customers': list(frequent_customers),
            'monthly_revenue': list(monthly_revenue),
        }
        
        return render(request, 'booking/service_center/analytics.html', context)
    except ServiceCenter.DoesNotExist:
        messages.warning(request, 'Please complete your service center profile.')
        return redirect('service_center_profile')


# Mechanic Views
@login_required
def mechanic_tasks(request):
    """View assigned tasks"""
    if request.user.role != 'mechanic':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    try:
        mechanic = request.user.mechanic
        bookings = Booking.objects.filter(mechanic=mechanic).order_by('-created_at')
        return render(request, 'booking/mechanic/tasks.html', {'bookings': bookings})
    except Mechanic.DoesNotExist:
        # Render the missing-profile page with clear instructions
        return render(request, 'booking/mechanic/profile_missing.html', {'user': request.user})


@login_required
def update_task_status(request, booking_id):
    """Update task completion status"""
    if request.user.role != 'mechanic':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.mechanic and booking.mechanic.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['in_progress', 'completed']:
            booking.status = status
            if status == 'completed':
                booking.completed_at = timezone.now()
            booking.save()
            messages.success(request, 'Task status updated successfully!')
    
    return redirect('mechanic_tasks')


# Admin Views
@login_required
def admin_manage_centers(request):
    """Admin manage service centers"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    centers = ServiceCenter.objects.all().order_by('-created_at')
    return render(request, 'booking/admin/manage_centers.html', {'centers': centers})


@login_required
def admin_manage_users(request):
    """Admin manage users"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    users = User.objects.all().order_by('-date_joined')
    role_filter = request.GET.get('role')
    if role_filter:
        users = users.filter(role=role_filter)
    
    return render(request, 'booking/admin/manage_users.html', {
        'users': users,
        'role_filter': role_filter,
    })


@login_required
def admin_manage_categories(request):
    """Admin manage service categories"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        base_price = request.POST.get('base_price', 0)
        
        if name:
            ServiceCategory.objects.create(
                name=name,
                description=description,
                base_price=float(base_price) if base_price else 0.00
            )
            messages.success(request, 'Service category added successfully!')
            return redirect('admin_manage_categories')
    
    categories = ServiceCategory.objects.all().order_by('name')
    return render(request, 'booking/admin/manage_categories.html', {'categories': categories})


@login_required
def view_invoice(request, booking_id):
    """View invoice"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check access
    if request.user.role == 'owner' and booking.vehicle.owner != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    elif request.user.role == 'service_center' and booking.service_center.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    try:
        invoice = booking.invoice
    except Invoice.DoesNotExist:
        messages.warning(request, 'Invoice not generated yet.')
        return redirect('booking_detail', booking_id=booking_id)
    
    return render(request, 'booking/invoice.html', {'invoice': invoice, 'booking': booking})


@login_required
def cancel_booking(request, booking_id):
    """Allow a vehicle owner to cancel a booking (if allowed).

    Allowed only for the booking owner and only when the booking is in a
    cancellable state (pending or accepted). If an invoice exists and has
    been paid, the invoice status will be marked 'cancelled' here as a
    simple demo action — in production you'd integrate refunds with the
    payment provider and record refund transactions.
    """
    booking = get_object_or_404(Booking, id=booking_id, vehicle__owner=request.user)

    if request.method != 'POST':
        messages.error(request, 'Invalid request method.')
        return redirect('booking_detail', booking_id=booking_id)

    # Only allow cancellation for specific statuses
    if booking.status not in ['pending', 'accepted']:
        messages.error(request, 'This booking cannot be cancelled at its current stage.')
        return redirect('booking_detail', booking_id=booking_id)

    # Mark booking cancelled
    booking.status = 'cancelled'
    booking.save()

    # If invoice exists and was paid, mark it cancelled (demo behaviour)
    try:
        invoice = booking.invoice
        if invoice.payment_status == 'paid':
            invoice.payment_status = 'cancelled'
            invoice.save()
    except Invoice.DoesNotExist:
        pass

    messages.success(request, 'Your booking has been cancelled.')
    return redirect('my_bookings')

