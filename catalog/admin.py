from django.contrib import admin
from .models import Categoria, Producto, ImagenProducto, Variante, ItemStock

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1

class VarianteInline(admin.TabularInline):
    model = Variante
    extra = 1

class ItemStockInline(admin.TabularInline):
    model = ItemStock
    extra = 1

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'activo', 'destacado')
    list_filter = ('activo', 'destacado', 'categoria')
    search_fields = ('nombre', 'descripcion')
    prepopulated_fields = {'slug': ('nombre',)}
    inlines = [ImagenProductoInline, VarianteInline, ItemStockInline]

@admin.register(Variante)
class VarianteAdmin(admin.ModelAdmin):
    list_display = ('producto', 'nombre')
    search_fields = ('nombre', 'producto__nombre')

@admin.register(ItemStock)
class ItemStockAdmin(admin.ModelAdmin):
    list_display = ('producto', 'variante', 'cantidad')
    list_filter = ('producto',)
    search_fields = ('producto__nombre', 'variante__nombre')
