from django.contrib import admin
from .models import MovimientoInventario, Despacho

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'variante', 'tipo', 'cantidad', 'fecha_creacion', 'motivo')
    list_filter = ('tipo', 'fecha_creacion')
    search_fields = ('producto__nombre', 'variante__nombre', 'motivo')

@admin.register(Despacho)
class DespachoAdmin(admin.ModelAdmin):
    list_display = ('orden', 'fecha_despacho')
    list_filter = ('fecha_despacho',)
    search_fields = ('orden__id',)
