from django.urls import path
from . import views, api

app_name = 'cart'

urlpatterns = [
    path('', views.carrito_detalle, name='carrito_detalle'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('api/mini/', api.mini_carrito_api, name='mini_carrito_api'),
    path('api/eliminar/<int:item_id>/', api.eliminar_item_api, name='eliminar_item_api'),
]