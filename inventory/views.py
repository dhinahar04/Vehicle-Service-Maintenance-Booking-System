from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import SparePart, InventoryTransaction
from accounts.models import ServiceCenter


@login_required
def inventory_list(request):
    """List all spare parts"""
    if not request.user.is_service_center:
        messages.error(request, 'Only service centers can access this page.')
        return redirect('accounts:dashboard')
    
    service_center = request.user.service_center_profile
    parts = SparePart.objects.filter(service_center=service_center).order_by('name')
    
    low_stock_filter = request.GET.get('low_stock')
    if low_stock_filter == 'true':
        parts = parts.filter(quantity__lte=models.F('min_stock_level'))
    
    return render(request, 'inventory/list.html', {'parts': parts})


@login_required
def inventory_add(request):
    """Add spare part"""
    if not request.user.is_service_center:
        messages.error(request, 'Only service centers can access this page.')
        return redirect('accounts:dashboard')
    
    service_center = request.user.service_center_profile
    
    if request.method == 'POST':
        try:
            part = SparePart.objects.create(
                service_center=service_center,
                name=request.POST.get('name'),
                part_number=request.POST.get('part_number', ''),
                description=request.POST.get('description', ''),
                category=request.POST.get('category', ''),
                unit_price=float(request.POST.get('unit_price')),
                quantity=int(request.POST.get('quantity', 0)),
                min_stock_level=int(request.POST.get('min_stock_level', 5)),
                supplier=request.POST.get('supplier', ''),
            )
            
            # Create transaction record
            if part.quantity > 0:
                InventoryTransaction.objects.create(
                    spare_part=part,
                    transaction_type='in',
                    quantity=part.quantity,
                    unit_price=part.unit_price,
                    notes='Initial stock',
                    created_by=request.user,
                )
            
            messages.success(request, 'Spare part added successfully!')
            return redirect('inventory:list')
        except Exception as e:
            messages.error(request, f'Error adding spare part: {str(e)}')
    
    return render(request, 'inventory/add.html')


@login_required
def inventory_edit(request, pk):
    """Edit spare part"""
    if not request.user.is_service_center:
        messages.error(request, 'Only service centers can access this page.')
        return redirect('accounts:dashboard')
    
    part = get_object_or_404(SparePart, pk=pk, service_center=request.user.service_center_profile)
    
    if request.method == 'POST':
        part.name = request.POST.get('name', part.name)
        part.part_number = request.POST.get('part_number', part.part_number)
        part.description = request.POST.get('description', part.description)
        part.category = request.POST.get('category', part.category)
        part.unit_price = float(request.POST.get('unit_price', part.unit_price))
        part.min_stock_level = int(request.POST.get('min_stock_level', part.min_stock_level))
        part.supplier = request.POST.get('supplier', part.supplier)
        part.save()
        
        messages.success(request, 'Spare part updated successfully!')
        return redirect('inventory:list')
    
    return render(request, 'inventory/edit.html', {'part': part})


@login_required
def inventory_transaction(request, pk):
    """Add inventory transaction"""
    if not request.user.is_service_center:
        messages.error(request, 'Only service centers can access this page.')
        return redirect('accounts:dashboard')
    
    part = get_object_or_404(SparePart, pk=pk, service_center=request.user.service_center_profile)
    
    if request.method == 'POST':
        transaction_type = request.POST.get('transaction_type')
        quantity = int(request.POST.get('quantity'))
        unit_price = float(request.POST.get('unit_price', part.unit_price))
        notes = request.POST.get('notes', '')
        
        # Update stock
        if transaction_type == 'in':
            part.quantity += quantity
        elif transaction_type == 'out':
            if part.quantity < quantity:
                messages.error(request, 'Insufficient stock!')
                return redirect('inventory:transaction', pk=part.pk)
            part.quantity -= quantity
        elif transaction_type == 'adjustment':
            part.quantity = quantity
        
        part.save()
        
        # Create transaction record
        InventoryTransaction.objects.create(
            spare_part=part,
            transaction_type=transaction_type,
            quantity=quantity,
            unit_price=unit_price,
            notes=notes,
            created_by=request.user,
        )
        
        messages.success(request, 'Transaction recorded successfully!')
        return redirect('inventory:list')
    
    return render(request, 'inventory/transaction.html', {'part': part})


@login_required
def inventory_history(request, pk):
    """View transaction history for a part"""
    if not request.user.is_service_center:
        messages.error(request, 'Only service centers can access this page.')
        return redirect('accounts:dashboard')
    
    part = get_object_or_404(SparePart, pk=pk, service_center=request.user.service_center_profile)
    transactions = InventoryTransaction.objects.filter(spare_part=part).order_by('-created_at')
    
    return render(request, 'inventory/history.html', {
        'part': part,
        'transactions': transactions,
    })

