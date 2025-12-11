from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Vehicle, MaintenanceReminder
from accounts.models import User


@login_required
def vehicle_list(request):
    """List all vehicles for the logged-in user"""
    vehicles = Vehicle.objects.filter(owner=request.user)
    return render(request, 'vehicles/list.html', {'vehicles': vehicles})


@login_required
def vehicle_add(request):
    """Add a new vehicle"""
    if request.method == 'POST':
        try:
            vehicle = Vehicle.objects.create(
                owner=request.user,
                make=request.POST.get('make'),
                model=request.POST.get('model'),
                year=int(request.POST.get('year')),
                vehicle_type=request.POST.get('vehicle_type'),
                fuel_type=request.POST.get('fuel_type'),
                registration_number=request.POST.get('registration_number'),
                color=request.POST.get('color', ''),
                mileage=int(request.POST.get('mileage', 0)),
                vin_number=request.POST.get('vin_number', ''),
                insurance_number=request.POST.get('insurance_number', ''),
            )
            messages.success(request, f'Vehicle {vehicle.make} {vehicle.model} added successfully!')
            return redirect('vehicles:list')
        except Exception as e:
            messages.error(request, f'Error adding vehicle: {str(e)}')
    
    return render(request, 'vehicles/add.html')


@login_required
def vehicle_detail(request, pk):
    """Vehicle detail view"""
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)
    reminders = MaintenanceReminder.objects.filter(vehicle=vehicle, is_completed=False)
    return render(request, 'vehicles/detail.html', {
        'vehicle': vehicle,
        'reminders': reminders
    })


@login_required
def vehicle_edit(request, pk):
    """Edit vehicle"""
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        vehicle.make = request.POST.get('make', vehicle.make)
        vehicle.model = request.POST.get('model', vehicle.model)
        vehicle.year = int(request.POST.get('year', vehicle.year))
        vehicle.vehicle_type = request.POST.get('vehicle_type', vehicle.vehicle_type)
        vehicle.fuel_type = request.POST.get('fuel_type', vehicle.fuel_type)
        vehicle.color = request.POST.get('color', vehicle.color)
        vehicle.mileage = int(request.POST.get('mileage', vehicle.mileage))
        vehicle.vin_number = request.POST.get('vin_number', vehicle.vin_number)
        vehicle.insurance_number = request.POST.get('insurance_number', vehicle.insurance_number)
        vehicle.save()
        
        messages.success(request, 'Vehicle updated successfully!')
        return redirect('vehicles:detail', pk=vehicle.pk)
    
    return render(request, 'vehicles/edit.html', {'vehicle': vehicle})


@login_required
def vehicle_delete(request, pk):
    """Delete vehicle"""
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully!')
        return redirect('vehicles:list')
    return render(request, 'vehicles/delete.html', {'vehicle': vehicle})

