from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Sum
from .models import User, ServiceCenter
from vehicles.models import Vehicle
from bookings.models import Booking
from notifications.models import Notification


def register(request):
    """User Registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        role = request.POST.get('role', 'customer')
        
        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('accounts:register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('accounts:register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('accounts:register')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone,
            role=role
        )
        
        messages.success(request, 'Registration successful! Please login.')
        return redirect('accounts:login')
    
    return render(request, 'accounts/register.html')


def user_login(request):
    """User Login"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'accounts/login.html')


@login_required
def dashboard(request):
    """User Dashboard"""
    context = {}
    
    if request.user.is_customer:
        # Customer Dashboard
        vehicles = Vehicle.objects.filter(owner=request.user)
        bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')[:5]
        recent_bookings = Booking.objects.filter(customer=request.user).count()
        
        context = {
            'vehicles': vehicles,
            'bookings': bookings,
            'recent_bookings': recent_bookings,
            'total_vehicles': vehicles.count(),
        }
    
    elif request.user.is_service_center:
        # Service Center Dashboard
        try:
            service_center = request.user.service_center_profile
            today_bookings = Booking.objects.filter(
                service_center=service_center,
                booking_date__date=request.user.date_joined.date()
            ).count()
            
            total_bookings = Booking.objects.filter(service_center=service_center).count()
            pending_bookings = Booking.objects.filter(
                service_center=service_center,
                status='pending'
            ).count()
            
            from payments.models import Invoice
            total_revenue = Invoice.objects.filter(
                service_center=service_center,
                payment_status='paid'
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            
            recent_bookings = Booking.objects.filter(
                service_center=service_center
            ).order_by('-created_at')[:10]
            
            context = {
                'service_center': service_center,
                'today_bookings': today_bookings,
                'total_bookings': total_bookings,
                'pending_bookings': pending_bookings,
                'total_revenue': total_revenue,
                'recent_bookings': recent_bookings,
            }
        except ServiceCenter.DoesNotExist:
            messages.warning(request, 'Please complete your service center profile.')
            return redirect('service_centers:create_profile')
    
    elif request.user.is_admin_user:
        # Admin Dashboard
        total_users = User.objects.filter(role='customer').count()
        total_centers = ServiceCenter.objects.count()
        total_bookings = Booking.objects.count()
        active_centers = ServiceCenter.objects.filter(is_active=True).count()
        
        context = {
            'total_users': total_users,
            'total_centers': total_centers,
            'total_bookings': total_bookings,
            'active_centers': active_centers,
        }
    
    # Get unread notifications
    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')[:5]
    
    context['unread_notifications'] = unread_notifications
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    """User Profile"""
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.address = request.POST.get('address', user.address)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/profile.html')

