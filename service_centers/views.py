from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
from accounts.models import ServiceCenter, Mechanic, User
from bookings.models import Booking, Service, ServiceCategory
from vehicles.models import Vehicle
from payments.models import Invoice
from inventory.models import SparePart


@login_required
def create_profile(request):
    """Create Service Center Profile"""
    if not request.user.is_service_center:
        messages.error(request, 'Only service centers can access this page.')
        return redirect('accounts:dashboard')
    
    if ServiceCenter.objects.filter(user=request.user).exists():
        return redirect('service_centers:dashboard')
    
    if request.method == 'POST':
        try:
            service_center = ServiceCenter.objects.create(
                user=request.user,
                name=request.POST.get('name'),
                description=request.POST.get('description', ''),
                address=request.POST.get('address'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                zip_code=request.POST.get('zip_code'),
                phone=request.POST.get('phone'),
                email=request.POST.get('email'),
                license_number=request.POST.get('license_number'),
            )
            messages.success(request, 'Service center profile created successfully!')
            return redirect('service_centers:dashboard')
        except Exception as e:
            messages.error(request, f'Error creating profile: {str(e)}')
    
    return render(request, 'service_centers/create_profile.html')


@login_required
def dashboard(request):
    """Service Center Dashboard"""
    if not request.user.is_service_center:
        messages.error(request, 'Only service centers can access this page.')
        return redirect('accounts:dashboard')
    
    try:
        service_center = request.user.service_center_profile
    except ServiceCenter.DoesNotExist:
        return redirect('service_centers:create_profile')
    
    # Statistics
    today = timezone.now().date()
    today_bookings = Booking.objects.filter(
        service_center=service_center,
        booking_date__date=today
    ).count()
    
    total_bookings = Booking.objects.filter(service_center=service_center).count()
    pending_bookings = Booking.objects.filter(
        service_center=service_center,
        status='pending'
    ).count()
    
    in_progress_bookings = Booking.objects.filter(
        service_center=service_center,
        status='in_progress'
    ).count()
    
    # Revenue
    total_revenue = Invoice.objects.filter(
        service_center=service_center,
        payment_status='paid'
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    monthly_revenue = Invoice.objects.filter(
        service_center=service_center,
        payment_status='paid',
        issued_date__month=today.month,
        issued_date__year=today.year
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Recent bookings
    recent_bookings = Booking.objects.filter(
        service_center=service_center
    ).order_by('-created_at')[:10]
    
    # Most requested services
    popular_services = Booking.objects.filter(
        service_center=service_center
    ).values('service__name').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Most frequent customers
    frequent_customers = Booking.objects.filter(
        service_center=service_center
    ).values('customer__username', 'customer__email').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    context = {
        'service_center': service_center,
        'today_bookings': today_bookings,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'in_progress_bookings': in_progress_bookings,
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'recent_bookings': recent_bookings,
        'popular_services': popular_services,
        'frequent_customers': frequent_customers,
    }
    
    return render(request, 'service_centers/dashboard.html', context)


@login_required
def manage_bookings(request):
    """Manage all bookings"""
    if not request.user.is_service_center:
        messages.error(request, 'Only service centers can access this page.')
        return redirect('accounts:dashboard')
    
    service_center = request.user.service_center_profile
    bookings = Booking.objects.filter(service_center=service_center).order_by('-created_at')
    
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    return render(request, 'service_centers/manage_bookings.html', {'bookings': bookings})


@login_required
def manage_mechanics(request):
    """Manage mechanics"""
    if not request.user.is_service_center:
        messages.error(request, 'Only service centers can access this page.')
        return redirect('accounts:dashboard')
    
    service_center = request.user.service_center_profile
    
    if request.method == 'POST':
        Mechanic.objects.create(
            service_center=service_center,
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email', ''),
            specialization=request.POST.get('specialization', ''),
            experience_years=int(request.POST.get('experience_years', 0)),
        )
        messages.success(request, 'Mechanic added successfully!')
        return redirect('service_centers:manage_mechanics')
    
    mechanics = Mechanic.objects.filter(service_center=service_center)
    return render(request, 'service_centers/manage_mechanics.html', {'mechanics': mechanics})


@login_required
def manage_services(request):
    """Manage services"""
    if not request.user.is_service_center:
        messages.error(request, 'Only service centers can access this page.')
        return redirect('accounts:dashboard')
    
    service_center = request.user.service_center_profile
    categories = ServiceCategory.objects.filter(is_active=True)
    
    if request.method == 'POST':
        Service.objects.create(
            service_center=service_center,
            category_id=request.POST.get('category'),
            name=request.POST.get('name'),
            description=request.POST.get('description', ''),
            base_price=float(request.POST.get('base_price')),
            duration_hours=float(request.POST.get('duration_hours', 1.0)),
        )
        messages.success(request, 'Service added successfully!')
        return redirect('service_centers:manage_services')
    
    services = Service.objects.filter(service_center=service_center)
    return render(request, 'service_centers/manage_services.html', {
        'services': services,
        'categories': categories,
    })


@login_required
def analytics(request):
    """Analytics Dashboard"""
    if not request.user.is_service_center:
        messages.error(request, 'Only service centers can access this page.')
        return redirect('accounts:dashboard')
    
    service_center = request.user.service_center_profile
    
    # Daily bookings (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    daily_bookings = Booking.objects.filter(
        service_center=service_center,
        created_at__gte=thirty_days_ago
    ).extra(
        select={'day': 'date(created_at)'}
    ).values('day').annotate(
        count=Count('id')
    ).order_by('day')
    
    # Revenue by month (last 12 months)
    monthly_revenue = Invoice.objects.filter(
        service_center=service_center,
        payment_status='paid'
    ).extra(
        select={'month': "strftime('%%Y-%%m', issued_date)"}
    ).values('month').annotate(
        total=Sum('total_amount')
    ).order_by('month')
    
    # Most requested services
    popular_services = Booking.objects.filter(
        service_center=service_center
    ).values('service__name').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Most frequent customers
    frequent_customers = Booking.objects.filter(
        service_center=service_center
    ).values(
        'customer__username',
        'customer__email',
        'customer__phone'
    ).annotate(
        count=Count('id'),
        total_spent=Sum('invoice__total_amount')
    ).order_by('-count')[:10]
    
    context = {
        'service_center': service_center,
        'daily_bookings': list(daily_bookings),
        'monthly_revenue': list(monthly_revenue),
        'popular_services': list(popular_services),
        'frequent_customers': list(frequent_customers),
    }
    
    return render(request, 'service_centers/analytics.html', context)

