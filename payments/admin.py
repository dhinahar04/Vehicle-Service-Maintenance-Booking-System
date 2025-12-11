from django.contrib import admin
from .models import Invoice, InvoiceItem, Payment


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ['payment_date']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'customer', 'service_center', 'total_amount', 'payment_status', 'issued_date']
    list_filter = ['payment_status', 'issued_date', 'service_center']
    search_fields = ['invoice_number', 'customer__username']
    inlines = [InvoiceItemInline, PaymentInline]
    readonly_fields = ['issued_date', 'paid_date']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'amount', 'payment_method', 'payment_date']
    list_filter = ['payment_method', 'payment_date']
    readonly_fields = ['payment_date']

