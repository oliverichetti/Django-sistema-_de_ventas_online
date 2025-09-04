from django.urls import path
from . import views

app_name = 'promotions'

urlpatterns = [
    path('aplicar-cupon/', views.aplicar_cupon, name='aplicar_cupon'),
    path('eliminar-cupon/', views.eliminar_cupon, name='eliminar_cupon'),
]