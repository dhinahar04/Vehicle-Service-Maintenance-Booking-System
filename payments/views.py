from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Sum
from django.utils import timezone
from .models import Invoice, InvoiceItem, Payment
from bookings.models import Booking
from accounts.models import ServiceCenter
import uuid


@login_required
def invoice_list(request):
    """List all invoices"""
    if request.user.is_customer:
        invoices = Invoice.objects.filter(customer=request.user).order_by('-issued_date')
    elif request.user.is_service_center:
        service_center = request.user.service_center_profile
        invoices = Invoice.objects.filter(service_center=service_center).order_by('-issued_date')
    else:
        invoices = Invoice.objects.all().order_by('-issued_date')
    
    return render(request, 'payments/invoice_list.html', {'invoices': invoices})


@login_required
def invoice_detail(request, pk):
    """Invoice detail view"""
    invoice = get_object_or_404(Invoice, pk=pk)
    
    # Check permissions
    if request.user.is_customer and invoice.customer != request.user:
        messages.error(request, 'You do not have permission to view this invoice.')
        return redirect('payments:invoice_list')
    
    if request.user.is_service_center and invoice.service_center != request.user.service_center_profile:
        messages.error(request, 'You do not have permission to view this invoice.')
        return redirect('payments:invoice_list')
    
    return render(request, 'payments/invoice_detail.html', {'invoice': invoice})


@login_required
def generate_invoice(request, booking_id):
    """Generate invoice for a booking"""
    booking = get_object_or_404(Booking, pk=booking_id)
    
    if not request.user.is_service_center:
        messages.error(request, 'Only service centers can generate invoices.')
        return redirect('bookings:detail', pk=booking_id)
    
    if booking.service_center != request.user.service_center_profile:
        messages.error(request, 'You do not have permission to generate invoice for this booking.')
        return redirect('bookings:detail', pk=booking_id)
    
    if booking.status != 'completed':
        messages.error(request, 'Invoice can only be generated for completed bookings.')
        return redirect('bookings:detail', pk=booking_id)
    
    # Check if invoice already exists
    if hasattr(booking, 'invoice'):
        messages.info(request, 'Invoice already exists for this booking.')
        return redirect('payments:invoice_detail', pk=booking.invoice.pk)
    
    if request.method == 'POST':
        # Create invoice
        invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
        
        subtotal = float(request.POST.get('subtotal', booking.actual_cost or booking.service.base_price))
        tax_rate = float(request.POST.get('tax_rate', 0))
        discount = float(request.POST.get('discount', 0))
        
        tax_amount = (subtotal - discount) * (tax_rate / 100)
        total_amount = subtotal - discount + tax_amount
        
        invoice = Invoice.objects.create(
            booking=booking,
            invoice_number=invoice_number,
            customer=booking.customer,
            service_center=booking.service_center,
            subtotal=subtotal,
            tax_rate=tax_rate,
            tax_amount=tax_amount,
            discount=discount,
            total_amount=total_amount,
        )
        
        # Add invoice items
        items = request.POST.getlist('item_description')
        quantities = request.POST.getlist('item_quantity')
        prices = request.POST.getlist('item_price')
        
        for desc, qty, price in zip(items, quantities, prices):
            if desc and qty and price:
                InvoiceItem.objects.create(
                    invoice=invoice,
                    description=desc,
                    quantity=int(qty),
                    unit_price=float(price),
                )
        
        messages.success(request, 'Invoice generated successfully!')
        return redirect('payments:invoice_detail', pk=invoice.pk)
    
    # Pre-fill with service details
    context = {
        'booking': booking,
        'default_subtotal': booking.actual_cost or booking.service.base_price,
    }
    
    return render(request, 'payments/generate_invoice.html', context)


@login_required
def invoice_pdf(request, pk):
    """Generate PDF for invoice"""
    invoice = get_object_or_404(Invoice, pk=pk)
    
    # Check permissions
    if request.user.is_customer and invoice.customer != request.user:
        messages.error(request, 'You do not have permission to view this invoice.')
        return redirect('payments:invoice_list')
    
    # For now, return HTML version (can be converted to PDF using libraries like weasyprint)
    html = render_to_string('payments/invoice_pdf.html', {'invoice': invoice})
    response = HttpResponse(html)
    response['Content-Type'] = 'text/html'
    return response


@login_required
def add_payment(request, invoice_id):
    """Add payment for an invoice"""
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    
    if not request.user.is_service_center:
        messages.error(request, 'Only service centers can add payments.')
        return redirect('payments:invoice_detail', pk=invoice_id)
    
    if invoice.service_center != request.user.service_center_profile:
        messages.error(request, 'You do not have permission to add payment for this invoice.')
        return redirect('payments:invoice_detail', pk=invoice_id)
    
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        payment_method = request.POST.get('payment_method')
        transaction_id = request.POST.get('transaction_id', '')
        
        Payment.objects.create(
            invoice=invoice,
            amount=amount,
            payment_method=payment_method,
            transaction_id=transaction_id,
        )
        
        # Update invoice payment status
        total_paid = Payment.objects.filter(invoice=invoice).aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        if total_paid >= invoice.total_amount:
            invoice.payment_status = 'paid'
            invoice.paid_date = timezone.now()
        elif total_paid > 0:
            invoice.payment_status = 'partial'
        else:
            invoice.payment_status = 'pending'
        
        invoice.save()
        
        messages.success(request, 'Payment recorded successfully!')
        return redirect('payments:invoice_detail', pk=invoice_id)
    
    return render(request, 'payments/add_payment.html', {'invoice': invoice})

