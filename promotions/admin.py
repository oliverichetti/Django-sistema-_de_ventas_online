from django.contrib import admin
from .models import Cupon

@admin.register(Cupon)
class CuponAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'tipo_descuento', 'monto', 'total_minimo', 'activo', 'valido_desde', 'valido_hasta')
    list_filter = ('activo', 'tipo_descuento')
    search_fields = ('codigo',)
