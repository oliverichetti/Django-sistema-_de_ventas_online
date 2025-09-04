from django.contrib import admin
from .models import Orden, ItemOrden

class ItemOrdenInline(admin.TabularInline):
    model = ItemOrden
    extra = 1

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'clave_session', 'nombre_envio', 'fecha_creacion', 'estado', 'total')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('clave_session', 'nombre_envio')
    inlines = [ItemOrdenInline]

@admin.register(ItemOrden)
class ItemOrdenAdmin(admin.ModelAdmin):
    list_display = ('orden', 'producto', 'variante', 'cantidad', 'precio_unitario', 'total_linea')
    list_filter = ('orden',)
    search_fields = ('producto__nombre', 'variante__nombre')
