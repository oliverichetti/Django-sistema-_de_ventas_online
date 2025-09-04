from django.urls import path
from . import views

app_name = 'warehouse'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('inventario/', views.inventario, name='inventario'),
    path('movimientos/', views.movimientos, name='movimientos'),
    path('despachos/', views.despachos, name='despachos'),
    path('despachar/<int:orden_id>/', views.despachar_orden, name='despachar_orden'),
]