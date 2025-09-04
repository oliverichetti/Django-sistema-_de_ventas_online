from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('confirmar/', views.confirmar_orden, name='confirmar_orden'),
    path('detalle/<int:orden_id>/', views.orden_detalle, name='orden_detalle'),
    path('historial/', views.historial_ordenes, name='historial_ordenes'),
]