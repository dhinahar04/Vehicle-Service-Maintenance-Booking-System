from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoices/<int:pk>/pdf/', views.invoice_pdf, name='invoice_pdf'),
    path('generate/<int:booking_id>/', views.generate_invoice, name='generate_invoice'),
    path('add-payment/<int:invoice_id>/', views.add_payment, name='add_payment'),
]

