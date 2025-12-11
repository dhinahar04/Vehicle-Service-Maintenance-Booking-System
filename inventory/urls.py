from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_list, name='list'),
    path('add/', views.inventory_add, name='add'),
    path('<int:pk>/edit/', views.inventory_edit, name='edit'),
    path('<int:pk>/transaction/', views.inventory_transaction, name='transaction'),
    path('<int:pk>/history/', views.inventory_history, name='history'),
]

