from django.contrib import admin
from .models import Carrito, ItemCarrito


class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 1

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'clave_session', 'fecha_creacion', 'total')
    list_filter = ('fecha_creacion',)
    search_fields = ('clave_session',)
    inlines = [ItemCarritoInline]

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'variante', 'cantidad', 'precio_unitario', 'subtotal')
    list_filter = ('carrito',)
    search_fields = ('producto__nombre', 'variante__nombre')
