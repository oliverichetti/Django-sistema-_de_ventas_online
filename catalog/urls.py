from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('categoria/<int:categoria_id>/', views.categoria_detalle, name='categoria_detalle'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    path('productos-destacados/', views.productos_destacados, name='productos_destacados'),
]